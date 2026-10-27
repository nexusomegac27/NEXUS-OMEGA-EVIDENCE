#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Frozen, separate C1 handoff-census evaluator; no candidate modifications.

A candidate cannot turn reported metadata into project-wide empirical proof.
"""
import copy
import importlib.util
from pathlib import Path
import sys
import unittest

CANDIDATE = Path(__file__).with_name("alpha_handoff_eligibility_reducer_v1_20261025.py")
spec = importlib.util.spec_from_file_location("alpha_handoff_eligibility_reducer", CANDIDATE)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
SHA = "a" * 64
COMMIT = "b" * 40


def good(id="h1"):
    return {"id": id, "public": True, "routine": True, "authorized": True,
            "source_access": "BYTE_VERIFIED", "source_readback": True,
            "source_sha256": SHA, "source_bytes": 18, "source_commit": COMMIT,
            "delivery": "RECEIVER_VERIFIED", "receiver_readback": True,
            "receiver_sha256": SHA, "receiver_bytes": 18, "receiver_commit": COMMIT,
            "manual_reprompt": False}


class FrozenEvaluator(unittest.TestCase):
    def test_good(self):
        r = module.reduce_sample([good()]); self.assertEqual((r["sample_eligible_denominator"], r["sample_automated_numerator"]), (1, 1))

    def test_project_never_promoted(self):
        self.assertEqual(module.reduce_sample([good()])["project_handoff_automation_rate"], "NOT_COMPUTABLE_NO_INDEPENDENT_COMPLETE_CENSUS")

    def test_empty(self):
        r = module.reduce_sample([]); self.assertEqual((r["sample_eligible_denominator"], r["sample_rate_percent"]), (0, None))

    def test_failed_delivery_in_denominator(self):
        r = good(); r["delivery"] = "FAILED"; self.assertEqual(module.reduce_sample([r])["sample_eligible_denominator"], 1)

    def test_pending_delivery_in_denominator(self):
        r = good(); r["delivery"] = "PENDING"; self.assertEqual(module.reduce_sample([r])["sample_automated_numerator"], 0)

    def test_branch_only_in_denominator(self):
        r = good(); r["delivery"] = "BRANCH_ONLY"; self.assertEqual(module.reduce_sample([r])["sample_eligible_denominator"], 1)

    def test_unknown_delivery_not_success(self):
        r = good(); r["delivery"] = "MAGIC_PASS"; self.assertEqual(module.reduce_sample([r])["sample_automated_numerator"], 0)

    def test_metadata_only_unknown(self):
        r = good(); r["source_access"] = "METADATA_ONLY"; self.assertEqual(module.reduce_sample([r])["unknown_or_unverified"], 1)

    def test_source_gap_unknown(self):
        r = good(); r["source_access"] = "SOURCE_GAP"; self.assertEqual(module.reduce_sample([r])["sample_eligible_denominator"], 0)

    def test_private_excluded(self):
        r = good(); r["public"] = False; self.assertEqual(module.reduce_sample([r])["excluded_out_of_scope"], 1)

    def test_unauthorized_excluded(self):
        r = good(); r["authorized"] = False; self.assertEqual(module.reduce_sample([r])["excluded_out_of_scope"], 1)

    def test_nonroutine_excluded(self):
        r = good(); r["routine"] = False; self.assertEqual(module.reduce_sample([r])["excluded_out_of_scope"], 1)

    def test_missing_scope_unknown(self):
        r = good(); del r["authorized"]; self.assertEqual(module.reduce_sample([r])["unknown_or_unverified"], 1)

    def test_boolean_integer_attack(self):
        r = good(); r["public"] = 1; self.assertEqual(module.reduce_sample([r])["unknown_or_unverified"], 1)

    def test_missing_source_hash_unknown(self):
        r = good(); r["source_sha256"] = ""; self.assertEqual(module.reduce_sample([r])["unknown_or_unverified"], 1)

    def test_source_bytes_boolean_unknown(self):
        r = good(); r["source_bytes"] = True; self.assertEqual(module.reduce_sample([r])["unknown_or_unverified"], 1)

    def test_missing_source_commit_unknown(self):
        r = good(); r["source_commit"] = ""; self.assertEqual(module.reduce_sample([r])["unknown_or_unverified"], 1)

    def test_receiver_mismatch_not_success(self):
        r = good(); r["receiver_sha256"] = "c" * 64; self.assertEqual(module.reduce_sample([r])["sample_automated_numerator"], 0)

    def test_receiver_bytes_mismatch_not_success(self):
        r = good(); r["receiver_bytes"] += 1; self.assertEqual(module.reduce_sample([r])["sample_automated_numerator"], 0)

    def test_receiver_readback_missing_not_success(self):
        r = good(); r["receiver_readback"] = False; self.assertEqual(module.reduce_sample([r])["sample_automated_numerator"], 0)

    def test_receiver_commit_missing_not_success(self):
        r = good(); r["receiver_commit"] = None; self.assertEqual(module.reduce_sample([r])["sample_automated_numerator"], 0)

    def test_manual_reprompt_not_success(self):
        r = good(); r["manual_reprompt"] = True; self.assertEqual(module.reduce_sample([r])["sample_automated_numerator"], 0)

    def test_manual_reprompt_missing_not_success(self):
        r = good(); del r["manual_reprompt"]; self.assertEqual(module.reduce_sample([r])["sample_automated_numerator"], 0)

    def test_duplicate_id_fail_closed(self):
        r = module.reduce_sample([good("dup"), good("dup")]); self.assertEqual((r["sample_eligible_denominator"], r["unknown_or_unverified"]), (0, 2))

    def test_mixed_sample(self):
        a = good("a"); b = good("b"); b["delivery"] = "FAILED"; c = good("c"); c["public"] = False
        d = good("d"); d["source_access"] = "METADATA_ONLY"
        r = module.reduce_sample([a,b,c,d]); self.assertEqual((r["sample_automated_numerator"], r["sample_eligible_denominator"], r["sample_rate_percent"], r["unknown_or_unverified"], r["excluded_out_of_scope"]), (1,2,50.0,1,1))

    def test_nonlist_fail_closed(self):
        with self.assertRaises(ValueError): module.reduce_sample({"h1":good()})

    def test_unsafe_id(self):
        r = good(" dup "); self.assertEqual(module.reduce_sample([r])["unknown_or_unverified"], 1)

    def test_malformed_row(self):
        self.assertEqual(module.reduce_sample([None])["unknown_or_unverified"], 1)

    def test_immutable_input(self):
        rows = [good()]; before = copy.deepcopy(rows); module.reduce_sample(rows); self.assertEqual(rows, before)


if __name__ == "__main__":
    unittest.main(verbosity=2)
