"""C1 research-only, offline source-byte comparator; no network or writes.

Caller MUST independently acquire GitHub Contents bytes at the manifest's immutable
merge commits. Caller-controlled manifest and expected SHA together are NOT trusted.
"""
import base64
import binascii
import hashlib
import json
import re

PINNED_COHORT_MANIFEST_SHA256 = "8f835b1dd27472702ee0aad0e2c5c5fc3e9d467d4d7423518ba3cb4c41e3191c"
HEX40 = re.compile(r"[0-9a-f]{40}\Z")
HEX64 = re.compile(r"[0-9a-f]{64}\Z")


def _no_duplicate_keys(pairs):
    d = {}
    for key, value in pairs:
        if key in d:
            raise ValueError("duplicate JSON key")
        d[key] = value
    return d


def _git_blob(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def evaluate(manifest_bytes, records, trusted_manifest_sha256=PINNED_COHORT_MANIFEST_SHA256):
    """Return fail-closed descriptive outcome; records are independent API reads.

    Each record: {path, commit, content_b64, github_blob_sha1}.
    A PASS is byte identity, never actor authenticity or scientific validation.
    """
    errors = []
    if not isinstance(manifest_bytes, bytes) or len(manifest_bytes) > 1048576:
        return {"status": "FAIL_CLOSED", "checked": 0, "expected": 0, "errors": ["MANIFEST_TYPE_OR_SIZE"]}
    if not isinstance(trusted_manifest_sha256, str) or not HEX64.fullmatch(trusted_manifest_sha256):
        return {"status": "FAIL_CLOSED", "checked": 0, "expected": 0, "errors": ["ANCHOR_INVALID"]}
    if hashlib.sha256(manifest_bytes).hexdigest() != trusted_manifest_sha256:
        return {"status": "FAIL_CLOSED", "checked": 0, "expected": 0, "errors": ["MANIFEST_HASH_MISMATCH"]}
    try:
        manifest = json.loads(manifest_bytes.decode("utf-8"), object_pairs_hook=_no_duplicate_keys)
        if not isinstance(manifest, dict) or manifest.get("claim_ceiling") != "C1_DESCRIPTIVE_ONLY":
            raise ValueError("invalid manifest scope")
        prs = manifest["prs"]
        if not isinstance(prs, list) or not prs or len(prs) > 100:
            raise ValueError("invalid PR list")
        expected = {}
        for pr in prs:
            commit = pr["merge_commit"]
            if not isinstance(commit, str) or not HEX40.fullmatch(commit):
                raise ValueError("invalid commit")
            for f in pr["files"]:
                path = f["path"]
                key = (commit, path)
                if not isinstance(path, str) or not path.startswith("research/") or key in expected:
                    raise ValueError("invalid or duplicate source path")
                if type(f["bytes"]) is not int or f["bytes"] < 0 or f["bytes"] > 1048576:
                    raise ValueError("invalid expected bytes")
                if not HEX64.fullmatch(f["sha256"]) or not HEX40.fullmatch(f["git_blob_sha1"]):
                    raise ValueError("invalid expected digest")
                expected[key] = f
        if not expected or len(expected) > 128:
            raise ValueError("invalid expected file count")
    except (KeyError, TypeError, ValueError, UnicodeError, json.JSONDecodeError):
        return {"status": "FAIL_CLOSED", "checked": 0, "expected": 0, "errors": ["MANIFEST_SCHEMA_INVALID"]}
    if not isinstance(records, list) or len(records) != len(expected):
        return {"status": "FAIL_CLOSED", "checked": 0, "expected": len(expected), "errors": ["INCOMPLETE_OR_EXTRA_READBACK"]}
    seen = set()
    checked = 0
    for index, record in enumerate(records):
        try:
            key = (record["commit"], record["path"])
            if key in seen or key not in expected:
                raise ValueError("duplicate or unknown source")
            seen.add(key)
            f = expected[key]
            data = base64.b64decode(record["content_b64"], validate=True)
            if base64.b64encode(data).decode("ascii") != record["content_b64"]:
                raise ValueError("noncanonical base64")
            if len(data) != f["bytes"]:
                raise ValueError("byte count mismatch")
            if hashlib.sha256(data).hexdigest() != f["sha256"]:
                raise ValueError("sha256 mismatch")
            blob = _git_blob(data)
            if blob != f["git_blob_sha1"] or blob != record["github_blob_sha1"]:
                raise ValueError("git blob mismatch")
            checked += 1
        except (KeyError, TypeError, ValueError, binascii.Error, UnicodeError):
            errors.append("SOURCE_MISMATCH_AT_INDEX_" + str(index))
    if len(seen) != len(expected):
        errors.append("SOURCE_SET_INCOMPLETE")
    return {"status": "PASS" if not errors else "FAIL_CLOSED", "checked": checked,
            "expected": len(expected), "errors": errors}
