#!/usr/bin/env python3
"""Frozen black-box adversarial evaluator for isolated handoff coverage census V1.
This evaluator has no write or GitHub capabilities and is not a scientific oracle.
"""
import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

CANDIDATE = os.environ.get("AXIOM_CANDIDATE", str(Path(__file__).with_name("alpha_handoff_coverage_census_v1_20261026.py")))

def record(id, **kwargs):
    r = {"id": id, "scope": "PUBLIC", "accessible": True,
         "authorized": True, "routine": True, "automated": True,
         "outcome": "SUCCESS", "source_readback": "MATCH", "publication_readback": "MATCH"}
    r.update(kwargs)
    return r

def run(payload):
    if isinstance(payload, (dict, list)):
        payload = json.dumps(payload, separators=(",", ":"), allow_nan=False)
    return subprocess.run([sys.executable, CANDIDATE], input=payload, capture_output=True,
                          text=True, timeout=5)

def output(payload):
    p = run(payload)
    if p.returncode != 0:
        raise AssertionError((p.returncode, p.stdout, p.stderr))
    return json.loads(p.stdout)

class FrozenHandoffCoverage(unittest.TestCase):
    def test_partial_automation_does_not_inflate_rate(self):
        r = output({"schema_version": 1, "records": [record("a"), record("b", automated=False)]})
        self.assertEqual((r["eligible_denominator"], r["claimed_automated_numerator"]), (2, 1))
        self.assertEqual(r["observed_sample_rate"], "1/2")
        self.assertEqual(r["project_rate"], "NOT_COMPUTABLE")
    def test_inaccessible_local_private_excluded(self):
        r = output({"schema_version": 1, "records": [record("a"),record("b", scope="LOCAL", accessible=False),record("c", scope="PRIVATE", accessible=False)]})
        self.assertEqual((r["eligible_denominator"], r["excluded_count"]), (1, 2))
    def test_public_inaccessible_not_success(self):
        r = output({"schema_version": 1, "records": [record("a", accessible=False), record("b")]})
        self.assertEqual((r["eligible_denominator"],r["claimed_automated_numerator"]), (1,1))
    def test_source_gap_is_denominator_failure(self):
        r = output({"schema_version": 1, "records": [record("a",source_readback="GAP"), record("b")]})
        self.assertEqual((r["eligible_denominator"],r["claimed_automated_numerator"]), (2,1))
    def test_publication_gap_is_denominator_failure(self):
        r = output({"schema_version": 1, "records": [record("a",publication_readback="GAP"), record("b")]})
        self.assertEqual(r["claimed_automated_numerator"], 1)
    def test_pending_is_denominator_failure(self):
        r = output({"schema_version": 1, "records": [record("a",outcome="PENDING"), record("b")]})
        self.assertEqual(r["observed_sample_rate"], "1/2")
    def test_unknown_eligibility_withholds_rate(self):
        r = output({"schema_version": 1, "records": [record("a"), record("b", authorized=None)]})
        self.assertEqual(r["unknown_eligibility_count"], 1)
        self.assertEqual(r["observed_sample_rate"], "WITHHELD_UNKNOWN_ELIGIBILITY")
    def test_empty_denominator_withheld(self):
        r = output({"schema_version": 1, "records": [record("a",scope="PRIVATE")]})
        self.assertEqual(r["observed_sample_rate"], "NOT_COMPUTABLE_ZERO_DENOMINATOR")
    def test_all_success_is_still_not_project_wide(self):
        r = output({"schema_version": 1, "records": [record("a")]})
        self.assertEqual(r["observed_sample_rate"], "1/1")
        self.assertEqual(r["project_rate"], "NOT_COMPUTABLE")
        self.assertEqual(r["evidence_class"], "UNVERIFIED_SAMPLE_ONLY")
    def test_duplicate_ids_fail_closed(self):
        self.assertNotEqual(run({"schema_version":1,"records":[record("a"),record("a")]}).returncode,0)
    def test_duplicate_json_keys_fail_closed(self):
        self.assertNotEqual(run('{"schema_version":1,"records":[],"records":[]}').returncode,0)
    def test_nonfinite_json_fail_closed(self):
        self.assertNotEqual(run('{"schema_version":1,"records":[],"other":NaN}').returncode,0)
    def test_missing_required_field_fail_closed(self):
        bad=record("a");del bad["authorized"]
        self.assertNotEqual(run({"schema_version":1,"records":[bad]}).returncode,0)
    def test_boolean_schema_version_rejected(self):
        self.assertNotEqual(run({"schema_version":True,"records":[]}).returncode,0)
    def test_unsupported_scope_rejected(self):
        self.assertNotEqual(run({"schema_version":1,"records":[record("a",scope="INTERNAL_SECRET")]}).returncode,0)
    def test_bad_record_type_rejected(self):
        self.assertNotEqual(run({"schema_version":1,"records":["a"]}).returncode,0)
    def test_conflicting_scope_fields_rejected(self):
        self.assertNotEqual(run({"schema_version":1,"records":[record("a",scope="PRIVATE",accessible=True)]}).returncode,0)
    def test_no_extra_fields(self):
        self.assertNotEqual(run({"schema_version":1,"records":[record("a",admin_override=True)]}).returncode,0)
    def test_untrusted_inventory_completeness_cannot_claim_project(self):
        self.assertNotEqual(run({"schema_version":1,"records":[record("a")],"inventory_complete":True}).returncode,0)

if __name__ == "__main__":
    unittest.main()
