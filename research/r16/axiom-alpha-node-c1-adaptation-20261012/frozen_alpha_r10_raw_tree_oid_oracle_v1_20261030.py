#!/usr/bin/env python3
"""Frozen black-box oracle for the R10 five-tree SHA-1 reconstruction candidate.

Run: python -S frozen_alpha_r10_raw_tree_oid_oracle_v1_20261030.py GATE.py PROJECTION.json
The oracle does not import or modify the candidate; tests use separate subprocesses.
"""
import copy
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

COMMIT = "dab7c59070d67e7e2a244bd6d05db9a4d37460e3"
ROOT = "d743c5d926d469470afa0d7331d5c56b8262d56c"
LEAF = "4e31f92be1f673f49a2c27e570b5849e754cca78"
SOURCE = "research/r10/biocomputing-independent-experts-20261016/returns_20261016/R10_EXTERNAL_RECEIVE_ACK_ASSERTION_20261016.txt"
EXPECTED_TREE_SHAS = [ROOT, "f1dd45775b781db06acad2e60377eb9780546caa", "3911eebd32855f25db0613401cd290e684b5ff44", "d7b2f423897ea086673bb1e9a6ffa09435f76c48", "e2a0b605f8d55090d52fde71e04744aaeda02dbe"]


def independent_sha(tree):
    # Independent oracle serialization, distinct from candidate bytearray algorithm.
    records = []
    for x in tree["entries"]:
        prefix = x["mode"].lstrip("0").encode("ascii") + b" " + x["path"].encode("utf-8") + b"\0"
        records.append(prefix + bytes.fromhex(x["sha"]))
    body = b"".join(records)
    return hashlib.sha1(b"tree %d\0" % len(body) + body).hexdigest()


def run(gate, obj, args=None, raw_override=None):
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "case.json"
        p.write_bytes(raw_override if raw_override is not None else (json.dumps(obj, ensure_ascii=False) + "\n").encode("utf-8"))
        cmd = [sys.executable, "-S", str(gate), str(p), "--commit", COMMIT,
               "--root-tree", ROOT, "--source-path", SOURCE, "--leaf-blob", LEAF]
        if args:
            cmd.extend(args)
        cp = subprocess.run(cmd, capture_output=True, text=True, timeout=8)
        try:
            result = json.loads(cp.stdout)
        except Exception:
            raise AssertionError("invalid subprocess JSON: " + cp.stdout + cp.stderr)
        return cp.returncode, result


def main():
    gate, fixture = Path(sys.argv[1]), Path(sys.argv[2])
    original = json.loads(fixture.read_text(encoding="utf-8"))
    assert original["commit_sha"] == COMMIT and original["root_tree_sha"] == ROOT
    assert len(original["trees"]) == 5
    for t, expected in zip(original["trees"], EXPECTED_TREE_SHAS):
        assert t["sha"] == expected and independent_sha(t) == expected, "independent real-tree hash mismatch"
    cases = [("real_5_tree_positive", original, True, None)]
    def neg(name, mutate):
        x = copy.deepcopy(original)
        mutate(x)
        cases.append((name, x, False, None))
    neg("mutated_leaf_blob", lambda x: x["trees"][-1]["entries"][4].update(sha="0" * 40))
    neg("mutated_same_length_path", lambda x: x["trees"][-1]["entries"][4].update(path="R10_EXTERNAL_RECEIVE_ACK_ASSERTION_20261016.txX"))
    neg("mutated_tree_mode", lambda x: x["trees"][0]["entries"][18].update(mode="100644"))
    neg("reordered_entries", lambda x: x["trees"][0]["entries"].reverse())
    neg("missing_entry", lambda x: x["trees"][0]["entries"].pop(0))
    neg("extra_entry", lambda x: x["trees"][0]["entries"].append(dict(x["trees"][0]["entries"][0])))
    neg("duplicate_path", lambda x: x["trees"][0]["entries"][1].update(path=x["trees"][0]["entries"][0]["path"]))
    neg("wrong_tree_sha", lambda x: x["trees"][3].update(sha="f" * 40))
    neg("wrong_child_link", lambda x: x["trees"][1]["entries"][7].update(sha="a" * 40))
    neg("wrong_root_pin", lambda x: x.update(root_tree_sha="f" * 40))
    neg("wrong_commit_pin", lambda x: x.update(commit_sha="f" * 40))
    neg("truncated_api_tree", lambda x: x["trees"][0].update(truncated=True))
    neg("removed_hop", lambda x: x["trees"].pop(2))
    neg("extra_hop", lambda x: x["trees"].append(copy.deepcopy(x["trees"][-1])))
    neg("forged_claim_field", lambda x: x.update(independent_receiver_ack=True))
    cases.append(("duplicate_json_keys", original, False, b'{"commit_sha":"x","commit_sha":"y"}'))
    cases.append(("nonfinite_json", original, False, b'{"commit_sha":NaN}'))
    cases.append(("malformed_json", original, False, b'{"bad":'))
    passed = 0
    for name, obj, positive, raw in cases:
        rc, result = run(gate, obj, raw_override=raw)
        good = (rc == 0 and result.get("status") == "API_TREE_OIDS_RECONSTRUCTED_NOT_AUTHENTICATED" and
                result.get("tree_count") == 5 and result.get("independent_receiver_ack") is False and
                result.get("actor_authenticated") is False) if positive else (rc != 0 and result.get("status") == "FAIL_CLOSED")
        print(("PASS" if good else "FAIL") + " " + name)
        if not good:
            raise AssertionError(name + " -> " + str((rc, result)))
        passed += 1
    print("FROZEN_ORACLE_PASS=%d/%d; NEGATIVE_FAIL_CLOSED=%d/%d" % (passed,len(cases),passed-1,len(cases)-1))


if __name__ == "__main__":
    main()
