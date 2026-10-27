#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Independent frozen evaluator: malformed JSON delivery must not abort whole handoff sample.

Source of truth: exact v1 SHA-256 118098276a26a12ca8a7c90c1692ce72eeafbe3702eb5e5ec89c5d81064115f9.
The evaluator is intentionally separate from the v2 candidate and uses synthetic data only.
"""
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
TARGET = HERE / "alpha_handoff_eligibility_reducer_v2_20261025.py"
spec = importlib.util.spec_from_file_location("handoff_v2", TARGET)
candidate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(candidate)


def good(identity="h1"):
    return {"id": identity, "public": True, "routine": True, "authorized": True,
            "source_access": "BYTE_VERIFIED", "source_readback": True,
            "source_sha256": "a" * 64, "source_bytes": 18, "source_commit": "b" * 40,
            "delivery": "RECEIVER_VERIFIED", "receiver_readback": True,
            "receiver_sha256": "a" * 64, "receiver_bytes": 18,
            "receiver_commit": "b" * 40, "manual_reprompt": False}


class FrozenMalformedDelivery(unittest.TestCase):
    def assertFailedOne(self, value):
        row = good()
        row["delivery"] = value
        result = candidate.reduce_sample([row])
        self.assertEqual(result["sample_eligible_denominator"], 1)
        self.assertEqual(result["sample_automated_numerator"], 0)
        self.assertEqual(result["outcomes"][0]["reason"], "DELIVERY_STATE_INVALID_TYPE")
        self.assertEqual(result["project_handoff_automation_rate"], "NOT_COMPUTABLE_NO_INDEPENDENT_COMPLETE_CENSUS")

    def test_list_empty(self): self.assertFailedOne([])
    def test_list_nested(self): self.assertFailedOne([{"state": ["RECEIVER_VERIFIED"]}])
    def test_dict_empty(self): self.assertFailedOne({})
    def test_dict_nested(self): self.assertFailedOne({"delivery": {"value": "RECEIVER_VERIFIED"}})
    def test_null(self): self.assertFailedOne(None)
    def test_integer(self): self.assertFailedOne(1)
    def test_boolean(self): self.assertFailedOne(True)
    def test_float(self): self.assertFailedOne(1.5)

    def test_mixed_batch_survives(self):
        rows = [good("ok"), good("bad"), good("failed"), good("private")]
        rows[1]["delivery"] = []
        rows[2]["delivery"] = "FAILED"
        rows[3]["public"] = False
        rows[3]["delivery"] = {}
        result = candidate.reduce_sample(rows)
        self.assertEqual((result["sample_automated_numerator"], result["sample_eligible_denominator"], result["excluded_out_of_scope"]), (1, 3, 1))
        self.assertEqual(result["sample_rate_percent"], 33.33)
        self.assertEqual([x["status"] for x in result["outcomes"]], ["ELIGIBLE_AUTOMATED", "ELIGIBLE_FAILED", "ELIGIBLE_FAILED", "EXCLUDED"])

    def test_unverified_source_not_eligible(self):
        row = good(); row["source_access"] = "METADATA_ONLY"; row["delivery"] = []
        result = candidate.reduce_sample([row]); self.assertEqual((result["sample_eligible_denominator"], result["unknown_or_unverified"]), (0, 1))

    def test_out_of_scope_not_eligible(self):
        row = good(); row["authorized"] = False; row["delivery"] = {}
        result = candidate.reduce_sample([row]); self.assertEqual((result["sample_eligible_denominator"], result["excluded_out_of_scope"]), (0, 1))

    def test_duplicate_ids_fail_closed(self):
        a = good("dup"); b = good("dup"); b["delivery"] = []
        result = candidate.reduce_sample([a, b]); self.assertEqual((result["sample_eligible_denominator"], result["unknown_or_unverified"]), (0, 2))

    def test_valid_success_preserved(self):
        result = candidate.reduce_sample([good()]); self.assertEqual((result["sample_eligible_denominator"], result["sample_automated_numerator"]), (1, 1))

    def test_valid_failure_preserved(self):
        row = good(); row["delivery"] = "FAILED"
        result = candidate.reduce_sample([row]); self.assertEqual((result["sample_eligible_denominator"], result["sample_automated_numerator"]), (1, 0))

    def test_immutable_input(self):
        rows = [good("x"), good("y")]; rows[0]["delivery"] = ["RECEIVER_VERIFIED"]
        old = copy.deepcopy(rows); candidate.reduce_sample(rows); self.assertEqual(rows, old)

    def test_json_roundtrip(self):
        rows = [good("ok"), good("bad")]; rows[1]["delivery"] = {"nested": [1, 2]}
        output = candidate.reduce_sample(json.loads(json.dumps(rows)))
        self.assertEqual(json.loads(json.dumps(output))["sample_eligible_denominator"], 2)

    def test_nonlist_rejected(self):
        with self.assertRaises(ValueError): candidate.reduce_sample({"not": "list"})

    def test_cli_batch(self):
        rows = [good("ok"), good("bad")]; rows[1]["delivery"] = []
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "rows.json"; p.write_text(json.dumps(rows), encoding="utf-8")
            cp = subprocess.run([sys.executable, str(TARGET), str(p)], capture_output=True, text=True)
            self.assertEqual(cp.returncode, 0, cp.stderr)
            output = json.loads(cp.stdout)
            self.assertEqual((output["sample_eligible_denominator"], output["sample_automated_numerator"]), (2, 1))

    def test_falsifier_no_fake_success(self):
        rows = [good("good"), good("evil")]; rows[1]["delivery"] = {"state": "RECEIVER_VERIFIED"}
        result = candidate.reduce_sample(rows)
        self.assertNotEqual(result["sample_automated_numerator"], 2)
        self.assertEqual(result["sample_automated_numerator"], 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
