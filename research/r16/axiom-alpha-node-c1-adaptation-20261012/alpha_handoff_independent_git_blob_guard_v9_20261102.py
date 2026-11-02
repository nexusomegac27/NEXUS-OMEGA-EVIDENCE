"""Research-only C1 byte identity cross-check against independently pinned Git blob.

The trusted commit/path/blob arguments MUST be obtained independently from the
producer envelope. This code does not fetch GitHub, authenticate actors, or
establish event completeness. It never changes a repository or runtime.
"""
import argparse
import base64
import binascii
import hashlib
import json
import re
import sys

HEX40 = re.compile(r"[0-9a-f]{40}\Z")
HEX64 = re.compile(r"[0-9a-f]{64}\Z")
MAX_BYTES = 1048576


def unique_pairs(pairs):
    out = {}
    for key, value in pairs:
        if key in out:
            raise ValueError("DUPLICATE_KEY")
        out[key] = value
    return out


def valid_path(path):
    return (type(path) is str and 0 < len(path) <= 512 and
            not path.startswith("/") and "\\" not in path and "\x00" not in path and
            all(x not in ("", ".", "..") for x in path.split("/"))


def check(data, trusted_commit, trusted_path, trusted_blob):
    fail = {"status": "NOT_COMPUTABLE", "identity_verified": False,
            "scope": "INDEPENDENT_GIT_BLOB_ID_REQUIRED_NO_ACTOR_AUTHENTICATION"}
    if (type(data) is not dict or not HEX40.fullmatch(trusted_commit) or
            not HEX40.fullmatch(trusted_blob) or not valid_path(trusted_path)):
        return fail
    if set(data) != {"source_b64", "source_sha256", "source_commit", "source_path", "source_git_blob_sha1"}:
        return fail
    if (type(data["source_commit"]) is not str or data["source_commit"] != trusted_commit or
            type(data["source_path"]) is not str or data["source_path"] != trusted_path or
            type(data["source_git_blob_sha1"]) is not str or data["source_git_blob_sha1"] != trusted_blob or
            type(data["source_sha256"]) is not str or not HEX64.fullmatch(data["source_sha256"]) or
            type(data["source_b64"]) is not str or len(data["source_b64"]) > 4 * MAX_BYTES // 3 + 8):
        return fail
    try:
        raw = base64.b64decode(data["source_b64"], validate=True)
        if not raw or len(raw) > MAX_BYTES:
            return fail
        sha256 = hashlib.sha256(raw).hexdigest()
        blob = hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()
        if sha256 != data["source_sha256"] or blob != trusted_blob:
            return fail
        return {"status": "BOUND_C1_BYTES_ONLY", "identity_verified": True,
                "bytes": len(raw), "sha256": sha256, "git_blob_sha1": blob,
                "scope": "INDEPENDENT_GIT_BLOB_ID_REQUIRED_NO_ACTOR_AUTHENTICATION"}
    except (ValueError, binascii.Error, OverflowError, TypeError):
        return fail


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--trusted-commit", required=True)
    p.add_argument("--trusted-path", required=True)
    p.add_argument("--trusted-blob", required=True)
    args = p.parse_args()
    try:
        data = json.loads(sys.stdin.buffer.read(4 * MAX_BYTES + 1).decode("utf-8"),
                          object_pairs_hook=unique_pairs,
                          parse_constant=lambda _: (_ for _ in ()).throw(ValueError("NONFINITE")))
        result = check(data, args.trusted_commit, args.trusted_path, args.trusted_blob)
    except (ValueError, UnicodeError, TypeError, RecursionError):
        result = check({}, args.trusted_commit, args.trusted_path, args.trusted_blob)
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
