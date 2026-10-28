#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Offline C1 byte/size/SHA256/Git-blob cross-check of caller-supplied GitHub evidence.

This cannot authenticate a GitHub actor, API origin, completeness of a remote
file listing, actual main tip, CI, or scientific validity. No network/writes.
"""
import base64
import binascii
import hashlib
import json
from pathlib import PurePosixPath
import re
import sys

OBJECT = "NEXUS_OMEGA_ALPHA_RECEIPT_FILE_DIGEST_WITNESS_V1"
REPO = "nexusomegac27/NEXUS-OMEGA-EVIDENCE"
MAX_INPUT = 2_097_152
MAX_FILES = 32
MAX_FILE_BYTES = 262_144
HEX40 = re.compile(r"[0-9a-f]{40}\Z")
HEX64 = re.compile(r"[0-9a-f]{64}\Z")


def fail(code):
    raise ValueError(code)


def unique_pairs(pairs):
    out = {}
    for key, value in pairs:
        if key in out:
            fail("DUPLICATE_JSON_KEY")
        out[key] = value
    return out


def finite_constant(_):
    fail("NONFINITE_JSON")


def sha(value, size):
    if type(value) is not str or not (HEX40 if size == 40 else HEX64).fullmatch(value):
        fail("INVALID_SHA")
    return value


def canonical_path(path):
    if type(path) is not str or not 1 <= len(path) <= 512:
        fail("INVALID_PATH")
    if (path.startswith("/") or "\\" in path or "\x00" in path or
            any(part in ("", ".", "..") for part in path.split("/")) or
            str(PurePosixPath(path)) != path):
        fail("INVALID_PATH")
    return path


def rows(value, keys, label):
    if type(value) is not list or not 1 <= len(value) <= MAX_FILES:
        fail("INVALID_" + label + "_COUNT")
    result = {}
    for row in value:
        if type(row) is not dict or set(row) != keys:
            fail("INVALID_" + label + "_FIELDS")
        path = canonical_path(row["path"] if "path" in row else row["filename"])
        if path in result:
            fail("DUPLICATE_" + label + "_PATH")
        result[path] = row
    return result


def audit(obj):
    if type(obj) is not dict or set(obj) != {
            "object", "repository", "commit_sha", "commit_files", "receipt_files", "original_bytes_b64"}:
        fail("INVALID_ENVELOPE")
    if obj["object"] != OBJECT or obj["repository"] != REPO:
        fail("INVALID_SCOPE")
    commit = sha(obj["commit_sha"], 40)
    remote = rows(obj["commit_files"], {"filename", "status", "sha"}, "COMMIT")
    receipt = rows(obj["receipt_files"], {"path", "bytes", "sha256", "git_blob_sha1"}, "RECEIPT")
    originals = rows(obj["original_bytes_b64"], {"path", "content_base64"}, "ORIGINAL")
    if set(remote) != set(receipt) or set(remote) != set(originals):
        fail("FILE_SET_MISMATCH")
    verified = []
    for path in sorted(remote):
        cr, rr, br = remote[path], receipt[path], originals[path]
        if cr["status"] != "added":
            fail("UNEXPECTED_COMMIT_STATUS")
        blob = sha(cr["sha"], 40)
        declared_blob = sha(rr["git_blob_sha1"], 40)
        declared_sha = sha(rr["sha256"], 64)
        n = rr["bytes"]
        if type(n) is not int or not 0 <= n <= MAX_FILE_BYTES:
            fail("INVALID_DECLARED_BYTE_COUNT")
        encoded = br["content_base64"]
        if type(encoded) is not str or len(encoded) > 4 * ((MAX_FILE_BYTES + 2) // 3):
            fail("INVALID_BASE64_SIZE")
        try:
            raw = base64.b64decode(encoded, validate=True)
        except (ValueError, binascii.Error):
            fail("INVALID_BASE64")
        if base64.b64encode(raw).decode("ascii") != encoded:
            fail("NONCANONICAL_BASE64")
        if len(raw) != n:
            fail("BYTE_COUNT_MISMATCH")
        actual_sha = hashlib.sha256(raw).hexdigest()
        if actual_sha != declared_sha:
            fail("SHA256_MISMATCH")
        actual_blob = hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\x00" + raw).hexdigest()
        if actual_blob != declared_blob or actual_blob != blob:
            fail("GIT_BLOB_MISMATCH")
        verified.append({"path": path, "bytes": n, "sha256": actual_sha, "git_blob_sha1": actual_blob})
    return {"state": "PASS_CALLER_SUPPLIED_FILE_BYTES_C1", "commit_sha": commit,
            "verified_files": len(verified), "files": verified,
            "api_origin_authenticated": False, "live_main_verified": False,
            "receipt_authenticity_verified": False, "claim_ceiling": "C1_DESCRIPTIVE_ONLY"}


def main():
    try:
        raw = sys.stdin.buffer.read(MAX_INPUT + 1)
        if len(raw) > MAX_INPUT:
            fail("INPUT_TOO_LARGE")
        obj = json.loads(raw.decode("utf-8"), object_pairs_hook=unique_pairs,
                         parse_constant=finite_constant)
        print(json.dumps(audit(obj), sort_keys=True, separators=(",", ":")))
        return 0
    except (ValueError, TypeError, UnicodeError, RecursionError) as exc:
        print("FAIL_CLOSED: " + str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
