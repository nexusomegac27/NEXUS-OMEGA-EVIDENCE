#!/usr/bin/env python3
"""Frozen independent black-box R27-E slot integrity evaluator, C1 only.

Source is repository registry, independently pinned to original bytes/sha256.
No candidate imports. No real GitHub enforcement or actor authentication.
"""
import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
REGISTRY = ROOT / "docs/governance/EXTERNAL_AGENT_WRITE_SLOTS_V1.json"
TARGET = Path(os.environ.get("AXIOM_CANDIDATE", HERE / "alpha_r27e_slot_integrity_witness_v1_20261027.py"))
PINNED_SHA256 = "d257be3faef8336e30f688d440758b051d93dd2a29ece693882af4ed8e463e7c"
PINNED_BLOB = "1fabcab7f556e83621a3676ddfb3d11cdd964b55"
PASS = "PASS_PINNED_REGISTRY_SNAPSHOT_C1"
HOLD = "HOLD_SCOPED_REGISTRY_CONTRACT_DRIFT"


def source():
    raw = REGISTRY.read_bytes()
    assert len(raw) == 2178, "PINNED_SOURCE_LENGTH_MISMATCH"
    assert hashlib.sha256(raw).hexdigest() == PINNED_SHA256, "PINNED_SOURCE_HASH_MISMATCH"
    assert hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest() == PINNED_BLOB
    return json.loads(raw)


def run(obj):
    raw = obj if isinstance(obj, bytes) else json.dumps(obj).encode("utf-8")
    return subprocess.run([sys.executable, str(TARGET)], input=raw, capture_output=True,
                          cwd=HERE, timeout=8)


class FrozenSlotOracle(unittest.TestCase):
    def check(self, obj, state, field=None):
        p = run(obj)
        self.assertEqual(p.returncode, 0, p.stderr.decode(errors="replace"))
        result = json.loads(p.stdout)
        self.assertEqual(result["state"], state)
        self.assertIs(result["api_origin_authenticated"], False)
        self.assertIs(result["external_actor_authorized"], False)
        self.assertIs(result["github_ruleset_enforcement_verified"], False)
        self.assertEqual(result["claim_ceiling"], "C1_DESCRIPTIVE_ONLY")
        if field:
            self.assertIn(field, result["drift_fields"])

    def test_positive_pinned_original(self):
        self.check(source(), PASS)

    def test_positive_descriptive_metadata(self):
        x = source(); x["source_note"] = "descriptive only"; self.check(x, PASS)

    def test_negative_slot_path(self):
        x = source(); x["assignments"][0]["returns_path"] = "research/r27/custom/"
        self.check(x, HOLD, "assignments[0].returns_path")

    def test_negative_filename(self):
        x = source(); x["assignments"][0]["filenames"][0] = "FORGED.md"
        self.check(x, HOLD, "assignments[0].filenames")

    def test_negative_extra_filename(self):
        x = source(); x["assignments"][0]["filenames"].append("EIGHTH.md")
        self.check(x, HOLD, "assignments[0].filenames")

    def test_negative_parent_hash(self):
        x = source(); x["assignments"][0]["parent_order_sha256"] = "0" * 64
        self.check(x, HOLD, "assignments[0].parent_order_sha256")

    def test_negative_quota_boolean(self):
        x = source(); x["max_files_per_external_return"] = True
        self.check(x, HOLD, "max_files_per_external_return")

    def test_negative_quota_expansion(self):
        x = source(); x["max_total_bytes"] = 99999999
        self.check(x, HOLD, "max_total_bytes")

    def test_negative_actor_added(self):
        x = source(); x["external_actor_allowlist"] = ["unregistered"]
        self.check(x, HOLD, "external_actor_allowlist")

    def test_negative_authorized_assignment(self):
        x = source(); x["assignments"][0]["status"] = "AUTHORIZED"
        self.check(x, HOLD, "assignments[0].status")

    def test_negative_extra_assignment(self):
        x = source(); x["assignments"].append(copy.deepcopy(x["assignments"][0]))
        self.check(x, HOLD, "assignments")

    def test_negative_prohibition_missing(self):
        x = source(); x["prohibited"].remove("EXTERNAL_CREATE_SUBDIRECTORY")
        self.check(x, HOLD, "prohibited")

    def test_negative_duplicate_prohibition(self):
        x = source(); x["prohibited"].append("AUTO_MERGE")
        self.check(x, HOLD, "prohibited")

    def test_negative_manifest_policy(self):
        x = source(); x["manifest_self_hash"] = "SELF_HASH_REQUIRED"
        self.check(x, HOLD, "manifest_self_hash")

    def test_negative_duplicate_json_key(self):
        p = run(b'{"default":"DENY","default":"ALLOW"}')
        self.assertEqual(p.returncode, 2); self.assertIn(b"DUPLICATE_JSON_KEY", p.stderr)

    def test_negative_nonfinite_json(self):
        p = run(b'{"max_total_bytes":NaN}')
        self.assertEqual(p.returncode, 2); self.assertIn(b"NONFINITE_JSON", p.stderr)

    def test_negative_input_budget(self):
        p = run(b" " * 65537)
        self.assertEqual(p.returncode, 2); self.assertIn(b"INPUT_TOO_LARGE", p.stderr)


if __name__ == "__main__":
    unittest.main()
