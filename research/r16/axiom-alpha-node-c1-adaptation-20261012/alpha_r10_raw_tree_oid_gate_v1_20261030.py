#!/usr/bin/env python3
"""Offline C1 research gate: reconstruct SHA-1 of Git tree objects from API entries.

Not an actor-authentication, commit-signature, scientific, or runtime validator.
"""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

HEX40 = re.compile(r"[0-9a-f]{40}\Z")
MODES = {"040000": "tree", "100644": "blob", "100755": "blob", "120000": "blob", "160000": "commit"}


def pairs_no_duplicates(pairs):
    out = {}
    for k, v in pairs:
        if k in out:
            raise ValueError("duplicate JSON key")
        out[k] = v
    return out


def fail_constant(x):
    raise ValueError("nonfinite JSON")


def exact_keys(o, keys):
    if not isinstance(o, dict) or set(o) != set(keys):
        raise ValueError("unexpected or missing fields")


def sha40(x):
    if not isinstance(x, str) or not HEX40.fullmatch(x):
        raise ValueError("invalid sha")
    return x


def name_bytes(x):
    if not isinstance(x, str) or not x or x in (".", "..") or "/" in x or "\x00" in x:
        raise ValueError("invalid Git path component")
    return x.encode("utf-8", "strict")


def reconstruct_tree(tree):
    exact_keys(tree, ("sha", "truncated", "entries"))
    expected = sha40(tree["sha"])
    if tree["truncated"] is not False:
        raise ValueError("truncated or nonboolean tree")
    entries = tree["entries"]
    if not isinstance(entries, list) or not entries or len(entries) > 100000:
        raise ValueError("invalid tree entries")
    prev = None
    raw = bytearray()
    lookup = {}
    for entry in entries:
        exact_keys(entry, ("mode", "path", "sha"))
        mode = entry["mode"]
        if not isinstance(mode, str) or mode not in MODES:
            raise ValueError("invalid tree mode")
        path = entry["path"]
        path_bytes = name_bytes(path)
        child_sha = sha40(entry["sha"])
        sort_key = path_bytes + (b"/" if mode == "040000" else b"")
        if prev is not None and sort_key <= prev:
            raise ValueError("noncanonical order or duplicate path")
        prev = sort_key
        if path in lookup:
            raise ValueError("duplicate path")
        lookup[path] = (mode, child_sha)
        raw.extend(("40000" if mode == "040000" else mode).encode("ascii"))
        raw.extend(b" ")
        raw.extend(path_bytes)
        raw.extend(b"\0")
        raw.extend(bytes.fromhex(child_sha))
    header = b"tree " + str(len(raw)).encode("ascii") + b"\0"
    computed = hashlib.sha1(header + raw).hexdigest()
    if computed != expected:
        raise ValueError("Git tree object ID mismatch")
    return lookup, len(raw), computed


def verify(payload, commit, root, source_path, leaf_blob):
    exact_keys(payload, ("commit_sha", "root_tree_sha", "trees"))
    if sha40(payload["commit_sha"]) != sha40(commit):
        raise ValueError("commit pin mismatch")
    if sha40(payload["root_tree_sha"]) != sha40(root):
        raise ValueError("root pin mismatch")
    sha40(leaf_blob)
    if not isinstance(source_path, str) or not source_path.startswith("research/r10/"):
        raise ValueError("source path out of scope")
    parts = source_path.split("/")
    if len(parts) != 5:
        raise ValueError("unexpected source depth")
    for part in parts:
        name_bytes(part)
    trees = payload["trees"]
    if not isinstance(trees, list) or len(trees) != len(parts):
        raise ValueError("incomplete or excess tree chain")
    expected = root
    witness = []
    for i, (part, tree) in enumerate(zip(parts, trees)):
        lookup, size, calculated = reconstruct_tree(tree)
        if calculated != expected:
            raise ValueError("broken parent-child Git tree link")
        if part not in lookup:
            raise ValueError("source path absent")
        mode, child_sha = lookup[part]
        if i < len(parts) - 1 and mode != "040000":
            raise ValueError("intermediate path is not a tree")
        if i == len(parts) - 1 and (mode != "100644" or child_sha != leaf_blob):
            raise ValueError("source blob pin mismatch")
        witness.append({"tree_sha1": calculated, "entry_count": len(tree["entries"]), "raw_tree_bytes": size})
        expected = child_sha
    return {"status": "API_TREE_OIDS_RECONSTRUCTED_NOT_AUTHENTICATED", "commit_api_pin": commit,
            "tree_count": len(witness), "leaf_blob": leaf_blob, "trees": witness,
            "actor_authenticated": False, "independent_receiver_ack": False,
            "raw_commit_object_authenticated": False}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("projection")
    parser.add_argument("--commit", required=True)
    parser.add_argument("--root-tree", required=True)
    parser.add_argument("--source-path", required=True)
    parser.add_argument("--leaf-blob", required=True)
    a = parser.parse_args()
    try:
        raw = Path(a.projection).read_bytes()
        if len(raw) > 262144:
            raise ValueError("oversize projection")
        obj = json.loads(raw.decode("utf-8", "strict"), object_pairs_hook=pairs_no_duplicates,
                         parse_constant=fail_constant)
        result = verify(obj, a.commit, a.root_tree, a.source_path, a.leaf_blob)
        print(json.dumps(result, sort_keys=True))
    except (ValueError, TypeError, UnicodeError, OSError) as e:
        print(json.dumps({"status": "FAIL_CLOSED", "reason": str(e)}))
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
