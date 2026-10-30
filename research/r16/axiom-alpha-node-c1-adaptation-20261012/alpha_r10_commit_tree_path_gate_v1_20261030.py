#!/usr/bin/env python3
"""C1-only offline GitHub API path-projection consistency gate, not authentication."""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

HEX40 = re.compile(r"[0-9a-f]{40}\Z")
HEX64 = re.compile(r"[0-9a-f]{64}\Z")


def unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("DUPLICATE_JSON_KEY")
        result[key] = value
    return result


def load_proof(path):
    raw = Path(path).read_bytes()
    if len(raw) > 65536:
        raise ValueError("PROOF_TOO_LARGE")
    proof = json.loads(raw.decode("utf-8"), object_pairs_hook=unique_pairs,
                       parse_constant=lambda _: (_ for _ in ()).throw(ValueError("NONFINITE_JSON")))
    if type(proof) is not dict or set(proof) != {"commit_sha", "root_tree_sha", "hops"}:
        raise ValueError("INVALID_PROOF_FIELDS")
    return proof


def hex_pin(value, pattern):
    if type(value) is not str or not pattern.fullmatch(value):
        raise ValueError("INVALID_HEX_PIN")


def check(source, proof, args):
    for v, pattern in ((args.expected_commit, HEX40), (args.expected_root_tree, HEX40),
                       (args.expected_source_sha256, HEX64), (args.expected_blob, HEX40)):
        hex_pin(v, pattern)
    if type(args.expected_bytes) is not int or args.expected_bytes <= 0:
        raise ValueError("INVALID_EXPECTED_BYTES")
    path = args.expected_path
    if not path.startswith("research/r10/") or len(path) > 512 or "\\" in path:
        raise ValueError("INVALID_EXPECTED_PATH")
    parts = path.split("/")
    if any(p in ("", ".", "..") or "\x00" in p for p in parts) or len(parts) != 5:
        raise ValueError("INVALID_PATH_COMPONENTS")
    if proof["commit_sha"] != args.expected_commit or proof["root_tree_sha"] != args.expected_root_tree:
        raise ValueError("COMMIT_ROOT_PIN_MISMATCH")
    hops = proof["hops"]
    if type(hops) is not list or len(hops) != len(parts):
        raise ValueError("INVALID_HOP_COUNT")
    parent = args.expected_root_tree
    for i, (part, hop) in enumerate(zip(parts, hops)):
        if type(hop) is not dict or set(hop) != {"parent_tree_sha", "truncated", "entry"}:
            raise ValueError("INVALID_HOP_FIELDS")
        if hop["parent_tree_sha"] != parent or hop["truncated"] is not False:
            raise ValueError("BROKEN_TREE_CHAIN_OR_TRUNCATION")
        entry = hop["entry"]
        if type(entry) is not dict or set(entry) != {"path", "mode", "type", "sha", "size"}:
            raise ValueError("INVALID_ENTRY_FIELDS")
        if entry["path"] != part:
            raise ValueError("PATH_COMPONENT_MISMATCH")
        hex_pin(entry["sha"], HEX40)
        if i < len(parts) - 1:
            if entry["mode"] != "040000" or entry["type"] != "tree" or entry["size"] is not None:
                raise ValueError("INVALID_DIRECTORY_ENTRY")
        else:
            if (entry["mode"], entry["type"], entry["sha"], entry["size"]) != (
                    "100644", "blob", args.expected_blob, args.expected_bytes):
                raise ValueError("SOURCE_TREE_ENTRY_MISMATCH")
        parent = entry["sha"]
    if not source or len(source) > 1048576:
        raise ValueError("INVALID_SOURCE_SIZE")
    blob = hashlib.sha1(b"blob " + str(len(source)).encode("ascii") + b"\0" + source).hexdigest()
    if (len(source), hashlib.sha256(source).hexdigest(), blob) != (
            args.expected_bytes, args.expected_source_sha256, args.expected_blob):
        raise ValueError("SOURCE_BYTE_INTEGRITY_MISMATCH")
    return {"commit_tree_path": "API_METADATA_CONSISTENT_NOT_AUTHENTICATED",
            "source_bytes_sha256_git_blob": "MATCH", "independent_receiver_ack": "NOT_ESTABLISHED",
            "authenticated_github_actor": "NOT_ESTABLISHED", "expert_execution": "NOT_ESTABLISHED",
            "claim_ceiling": "C1_DESCRIPTIVE_ONLY"}


def main():
    ap = argparse.ArgumentParser()
    for name in ("source", "proof", "expected-commit", "expected-root-tree",
                 "expected-source-sha256", "expected-blob", "expected-path"):
        ap.add_argument("--" + name, required=True)
    ap.add_argument("--expected-bytes", type=int, required=True)
    args = ap.parse_args()
    try:
        source = Path(args.source).read_bytes()
        result = check(source, load_proof(args.proof), args)
    except (ValueError, UnicodeError, OSError, TypeError, KeyError) as exc:
        print(json.dumps({"status": "FAIL_CLOSED", "reason": str(exc)}, sort_keys=True))
        return 2
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
