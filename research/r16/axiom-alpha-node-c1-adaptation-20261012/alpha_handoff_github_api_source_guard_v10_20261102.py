"""Isolated C1 GitHub Contents API readback guard, not a production/actor oracle.

LIVE mode: GET an immutable commit/path directly from api.github.com over HTTPS.
OFFLINE mode: accepts a caller-controlled fixture only with an explicit test flag,
and never reports a live API result. The commit/path must be independently pinned.
No token, GitHub write, runtime change, or event-census claim.
"""
import argparse
import base64
import binascii
import hashlib
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

REPO = "nexusomegac27/NEXUS-OMEGA-EVIDENCE"
HEX40 = re.compile(r"[0-9a-f]{40}\Z")
HEX64 = re.compile(r"[0-9a-f]{64}\Z")
MAX_BYTES = 1048576
MAX_JSON = 2 * 1048576
SCOPE = "PINNED_COMMIT_PATH_BYTE_MATCH_NO_ACTOR_OR_EVENT_CENSUS_AUTHENTICATION"


def unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("DUPLICATE_KEY")
        result[key] = value
    return result


def parse_json(raw):
    return json.loads(raw.decode("utf-8"), object_pairs_hook=unique_pairs,
                      parse_constant=lambda _: (_ for _ in ()).throw(ValueError("NONFINITE")))


def valid_path(value):
    return (type(value) is str and 0 < len(value) <= 512 and
            not value.startswith("/") and "\\" not in value and "\x00" not in value and
            all(part not in ("", ".", "..") for part in value.split("/")))


def git_blob(raw):
    return hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()


def read_limited(fp):
    raw = fp.read(MAX_JSON + 1)
    if len(raw) > MAX_JSON:
        raise ValueError("OVERSIZED_RESPONSE")
    return raw


def api_contents(commit, path):
    # No user-provided host or repo; path segments are individually quoted.
    encoded = "/".join(urllib.parse.quote(s, safe="") for s in path.split("/"))
    url = ("https://api.github.com/repos/" + REPO + "/contents/" + encoded +
           "?ref=" + commit)
    req = urllib.request.Request(url, headers={
        "Accept": "application/vnd.github+json",
        "User-Agent": "NEXUS-OMEGA-Alpha-C1-ReadOnly",
        "X-GitHub-Api-Version": "2022-11-28"})
    with urllib.request.urlopen(req, timeout=8) as fp:
        if fp.status != 200 or fp.geturl() != url:
            raise ValueError("UNEXPECTED_HTTP_OR_REDIRECT")
        return parse_json(read_limited(fp))


def check(envelope, api, commit, path, fixture_mode):
    failure = {"status": "NOT_COMPUTABLE", "byte_match": False,
               "authenticated_actor": False, "scope": SCOPE}
    if (type(envelope) is not dict or type(api) is not dict or
            type(commit) is not str or not HEX40.fullmatch(commit) or not valid_path(path)):
        return failure
    if set(envelope) != {"source_b64", "source_sha256", "source_commit", "source_path", "source_git_blob_sha1"}:
        return failure
    if (type(envelope["source_commit"]) is not str or envelope["source_commit"] != commit or
            type(envelope["source_path"]) is not str or envelope["source_path"] != path or
            type(envelope["source_sha256"]) is not str or not HEX64.fullmatch(envelope["source_sha256"]) or
            type(envelope["source_git_blob_sha1"]) is not str or
            not HEX40.fullmatch(envelope["source_git_blob_sha1"]) or
            type(envelope["source_b64"]) is not str or
            len(envelope["source_b64"]) > 4 * MAX_BYTES // 3 + 8):
        return failure
    if (api.get("type") != "file" or type(api.get("path")) is not str or
            api["path"] != path or type(api.get("sha")) is not str or
            not HEX40.fullmatch(api["sha"]) or type(api.get("size")) is not int or
            not 0 < api["size"] <= MAX_BYTES or api.get("encoding") != "base64" or
            type(api.get("content")) is not str or
            len(api["content"]) > 4 * MAX_BYTES // 3 + 100000):
        return failure
    try:
        producer = base64.b64decode(envelope["source_b64"], validate=True)
        # GitHub Contents REST base64 field may contain CR/LF line wraps.
        remote = base64.b64decode(api["content"].replace("\n", "").replace("\r", ""), validate=True)
    except (ValueError, binascii.Error, OverflowError):
        return failure
    if not producer or len(producer) > MAX_BYTES or len(remote) != api["size"]:
        return failure
    if producer != remote:
        return failure
    blob = git_blob(remote)
    sha256 = hashlib.sha256(remote).hexdigest()
    if (blob != api["sha"] or blob != envelope["source_git_blob_sha1"] or
            sha256 != envelope["source_sha256"]):
        return failure
    return {"status": "FIXTURE_BOUND_C1_BYTES_ONLY" if fixture_mode else "LIVE_API_BOUND_C1_BYTES_ONLY",
            "byte_match": True, "authenticated_actor": False,
            "bytes": len(remote), "sha256": sha256, "git_blob_sha1": blob,
            "scope": SCOPE, "source": "OFFLINE_FIXTURE_UNTRUSTED" if fixture_mode else "GITHUB_HTTPS_CONTENTS_API"}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--trusted-commit", required=True)
    p.add_argument("--trusted-path", required=True)
    p.add_argument("--offline-fixture-test", action="store_true")
    p.add_argument("--fixture-response")
    args = p.parse_args()
    failure = {"status": "NOT_COMPUTABLE", "byte_match": False,
               "authenticated_actor": False, "scope": SCOPE}
    try:
        if (type(args.trusted_commit) is not str or not HEX40.fullmatch(args.trusted_commit) or
                not valid_path(args.trusted_path) or
                args.offline_fixture_test != (args.fixture_response is not None)):
            raise ValueError("INVALID_TRUST_ANCHOR_OR_MODE")
        envelope = parse_json(read_limited(sys.stdin.buffer))
        if args.offline_fixture_test:
            with open(args.fixture_response, "rb") as fp:
                api = parse_json(read_limited(fp))
        else:
            api = api_contents(args.trusted_commit, args.trusted_path)
        result = check(envelope, api, args.trusted_commit, args.trusted_path, args.offline_fixture_test)
    except (ValueError, TypeError, UnicodeError, RecursionError, OSError,
            urllib.error.URLError, TimeoutError):
        result = failure
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
