#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Frozen, independent evaluator for duplicate-key handoff JSON intake (C1).

This evaluator defines behavior without importing any candidate implementation.
It uses synthetic records only; it does not authenticate GitHub actors or handoffs.
"""
from __future__ import annotations
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
TARGET = Path(os.environ.get("HANDOFF_CANDIDATE", str(HERE / "alpha_handoff_strict_json_intake_v1_20261025.py")))
spec = importlib.util.spec_from_file_location("candidate_under_test", TARGET)
if spec is None or spec.loader is None:
    raise RuntimeError("CANDIDATE_IMPORT_UNAVAILABLE")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def record(identity="h1"):
    return {"id": identity, "public": True, "routine": True, "authorized": True,
            "source_access": "BYTE_VERIFIED", "source_readback": True,
            "source_sha256": "a" * 64, "source_bytes": 18, "source_commit": "b" * 40,
            "delivery": "RECEIVER_VERIFIED", "receiver_readback": True,
            "receiver_sha256": "a" * 64, "receiver_bytes": 18,
            "receiver_commit": "b" * 40, "manual_reprompt": False}


def with_duplicate(field, before, after):
    # Raw JSON syntax is intentional: json.dumps(dict) cannot represent duplicate keys.
    base = json.dumps(record(), separators=(",", ":"))
    needle = json.dumps(field) + ":" + json.dumps(after)
    replacement = json.dumps(field) + ":" + json.dumps(before) + "," + needle
    assert needle in base
    return "[" + base.replace(needle, replacement, 1) + "]"


class FrozenHandoffDuplicateKeyEvaluator(unittest.TestCase):
    def assertRejected(self, text):
        with self.assertRaisesRegex(ValueError, "DUPLICATE_JSON_KEY"):
            module.reduce_json_text(text)

    def test_conflicting_manual_reprompt(self):
        self.assertRejected(with_duplicate("manual_reprompt", True, False))

    def test_conflicting_authorized(self):
        self.assertRejected(with_duplicate("authorized", False, True))

    def test_conflicting_public(self):
        self.assertRejected(with_duplicate("public", False, True))

    def test_conflicting_routine(self):
        self.assertRejected(with_duplicate("routine", False, True))

    def test_conflicting_delivery(self):
        self.assertRejected(with_duplicate("delivery", "FAILED", "RECEIVER_VERIFIED"))

    def test_conflicting_source_access(self):
        self.assertRejected(with_duplicate("source_access", "METADATA_ONLY", "BYTE_VERIFIED"))

    def test_duplicate_id_even_same_value(self):
        self.assertRejected(with_duplicate("id", "h1", "h1"))

    def test_duplicate_irrelevant_field(self):
        self.assertRejected('[{"id":"h1","extra":1,"extra":2}]')

    def test_duplicate_nested_field(self):
        self.assertRejected('[{"id":"h1","meta":{"x":1,"x":2}}]')

    def test_duplicate_unicode_escaped_equivalent(self):
        self.assertRejected('[{"public":true,"\\u0070ublic":false}]')

    def test_duplicate_non_ascii_equivalent(self):
        self.assertRejected('[{"é":1,"\\u00e9":2}]')

    def test_valid_single_automated(self):
        r = module.reduce_json_text(json.dumps([record()]))
        self.assertEqual((r["sample_eligible_denominator"], r["sample_automated_numerator"]), (1, 1))
        self.assertEqual(r["project_handoff_automation_rate"], "NOT_COMPUTABLE_NO_INDEPENDENT_COMPLETE_CENSUS")

    def test_valid_failed_stays_denominator(self):
        row = record(); row["delivery"] = "FAILED"
        r = module.reduce_json_text(json.dumps([row]))
        self.assertEqual((r["sample_eligible_denominator"], r["sample_automated_numerator"]), (1, 0))

    def test_valid_malformed_delivery_preserves_v2(self):
        row = record(); row["delivery"] = []
        r = module.reduce_json_text(json.dumps([row]))
        self.assertEqual(r["outcomes"][0]["reason"], "DELIVERY_STATE_INVALID_TYPE")
        self.assertEqual((r["sample_eligible_denominator"], r["sample_automated_numerator"]), (1, 0))

    def test_valid_two_records_mixed(self):
        good = record("ok"); failed = record("bad"); failed["delivery"] = "FAILED"
        r = module.reduce_json_text(json.dumps([good, failed]))
        self.assertEqual((r["sample_eligible_denominator"], r["sample_automated_numerator"], r["sample_rate_percent"]), (2, 1, 50.0))

    def test_valid_nested_distinct_keys(self):
        row = record(); row["meta"] = {"x": 1, "y": 2}
        r = module.reduce_json_text(json.dumps([row]))
        self.assertEqual(r["sample_automated_numerator"], 1)

    def test_valid_unicode_distinct_keys(self):
        row = record(); row["é"] = 1; row["e"] = 2
        r = module.reduce_json_text(json.dumps([row], ensure_ascii=False))
        self.assertEqual(r["sample_automated_numerator"], 1)

    def test_empty_array(self):
        r = module.reduce_json_text("[]")
        self.assertEqual((r["sample_eligible_denominator"], r["sample_rate_percent"]), (0, None))

    def test_non_array_rejected(self):
        with self.assertRaises(ValueError):
            module.reduce_json_text("{}")

    def test_non_text_rejected(self):
        with self.assertRaises(ValueError):
            module.reduce_json_text([record()])

    def test_deterministic_output(self):
        data = json.dumps([record()])
        self.assertEqual(module.reduce_json_text(data), module.reduce_json_text(data))

    def test_cli_duplicate_fail_closed(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "records.json"
            p.write_text(with_duplicate("manual_reprompt", True, False), encoding="utf-8")
            cp = subprocess.run([sys.executable, str(TARGET), str(p)], capture_output=True, text=True)
            self.assertNotEqual(cp.returncode, 0)
            self.assertNotIn('"sample_automated_numerator":1', cp.stdout)
            self.assertIn("DUPLICATE_JSON_KEY", cp.stderr)

    def test_cli_valid_preserves_success(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "records.json"
            p.write_text(json.dumps([record()]), encoding="utf-8")
            cp = subprocess.run([sys.executable, str(TARGET), str(p)], capture_output=True, text=True)
            self.assertEqual(cp.returncode, 0, cp.stderr)
            self.assertEqual(json.loads(cp.stdout)["sample_automated_numerator"], 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
