#!/usr/bin/env python3
"""Isolated C1 publication readback preflight; input is NOT an authenticated API receipt.

Checks caller-supplied original bytes against SHA-256 and Git blob identity, with
strict scoped PR/receipt/CI consistency. No network, writes, or runtime effects.
"""
import base64
import binascii
import hashlib
import json
import re
import sys

HEX40 = re.compile(r"[0-9a-f]{40}\Z")
HEX64 = re.compile(r"[0-9a-f]{64}\Z")
PATH = re.compile(r"research/[a-z0-9_./-]+\Z")
REPO = "nexusomegac27/NEXUS-OMEGA-EVIDENCE"


def unique_object(pairs):
    obj = {}
    for key, value in pairs:
        if key in obj:
            raise ValueError("duplicate_json_key")
        obj[key] = value
    return obj


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def hexstr(value, pattern):
    return isinstance(value, str) and bool(pattern.fullmatch(value))


def verify(payload):
    require(isinstance(payload, dict) and payload.get("schema_version") == "1", "envelope")
    main, parent = payload.get("main_commit"), payload.get("parent_commit")
    require(hexstr(main, HEX40) and hexstr(parent, HEX40) and main != parent, "commit_identity")
    pr = payload.get("pr")
    require(isinstance(pr, dict) and type(pr.get("number")) is int and pr["number"] > 0, "pr_number")
    require(pr.get("merged") is True and pr.get("merge_commit") == main
            and pr.get("base_commit") == parent and hexstr(pr.get("head_commit"), HEX40), "pr_commit_relation")
    files = payload.get("changed_files")
    declared = payload.get("declared_changed_files")
    require(isinstance(files, list) and type(declared) is int and declared > 0
            and len(files) == declared, "changed_file_census")
    seen = set()
    for item in files:
        require(isinstance(item, dict), "file_object")
        path = item.get("path")
        require(isinstance(path, str) and bool(PATH.fullmatch(path))
                and all(p not in ("", ".", "..") for p in path.split("/")), "file_path")
        require(path not in seen, "duplicate_path")
        seen.add(path)
        require(item.get("status") in ("added", "modified"), "file_status")
        require(type(item.get("bytes")) is int and item["bytes"] >= 0
                and hexstr(item.get("sha256"), HEX64)
                and hexstr(item.get("git_blob"), HEX40), "file_declared_identity")
        require(isinstance(item.get("content_b64"), str), "missing_original_bytes")
        try:
            raw = base64.b64decode(item["content_b64"], validate=True)
        except (binascii.Error, ValueError) as exc:
            raise ValueError("invalid_original_bytes_base64") from exc
        require(len(raw) == item["bytes"], "source_byte_mismatch")
        require(hashlib.sha256(raw).hexdigest() == item["sha256"], "source_sha256_mismatch")
        blob = hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()
        require(blob == item["git_blob"], "source_git_blob_mismatch")
    checks, count = payload.get("ci_checks"), payload.get("declared_checks")
    require(isinstance(checks, list) and type(count) is int and count > 0
            and len(checks) == count, "ci_census")
    require(all(isinstance(c, dict) and isinstance(c.get("name"), str)
                and c["name"].strip() and c.get("conclusion") == "success" for c in checks), "ci_failure_or_gap")
    receipt = payload.get("receipt")
    require(isinstance(receipt, dict) and type(receipt.get("id")) is int
            and receipt["id"] > 0 and receipt.get("actor") == "nexusomegac27"
            and isinstance(receipt.get("body"), str), "receipt_identity")
    lines = receipt["body"].splitlines()
    expected = ("ACTUAL_MAIN_READBACK=" + main,
                "ACTUAL_MAIN_PARENT=" + parent,
                "PR=https://github.com/" + REPO + "/pull/" + str(pr["number"]),
                "CLAIM_CEILING=C1_DESCRIPTIVE_ONLY")
    require(all(lines.count(line) == 1 for line in expected), "receipt_binding")
    require(not any(line.startswith("CLAIM_CEILING=") and line != expected[-1] for line in lines), "claim_promotion")
    return {"status": "LOCAL_BYTES_MATCH_UNAUTHENTICATED_INPUT",
            "local_file_matches": len(files), "declared_changed_files": declared,
            "declared_ci_successes": count, "receipt_actor_authenticated": False,
            "api_transport_authenticated": False,
            "complete_api_changed_file_census": "NOT_ESTABLISHED",
            "project_full_readback_rate": "NOT_COMPUTABLE",
            "claim_ceiling": "C1_DESCRIPTIVE_ONLY"}


def main():
    try:
        payload = json.loads(sys.stdin.read(), object_pairs_hook=unique_object,
                             parse_constant=lambda _: (_ for _ in ()).throw(ValueError("nonfinite_json")))
        result = verify(payload)
    except (ValueError, TypeError, KeyError, RecursionError, UnicodeError) as exc:
        result = {"status": "FAIL_CLOSED", "reason": str(exc)[:120]}
    print(json.dumps(result, sort_keys=True))
    return 2 if result["status"] == "FAIL_CLOSED" else 0


if __name__ == "__main__":
    sys.exit(main())
