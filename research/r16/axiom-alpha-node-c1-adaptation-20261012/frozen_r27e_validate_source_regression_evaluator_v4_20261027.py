#!/usr/bin/env python3
"""Frozen black-box falsifier: V3 ref-exclusion auditor lost V2 validate-app pin.

Synthetic JSON only. Expected integration_id=15368 is pinned to the 2026-10-27
GitHub ruleset #21252293 read, not an independent API authentication claim.
This evaluator is frozen before the successor candidate is authored.
"""
import copy
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest

HERE = Path(__file__).resolve().parent
TARGET = Path(os.environ.get("AXIOM_CANDIDATE", HERE / "alpha_r27e_ruleset_validate_source_and_ref_v4_20261027.py"))
PASS = "PASS_REQUIRED_CONFIG_WITNESSES_C1"
HOLD = "HOLD_SCOPED_ENFORCEMENT_GAP"


def fixture():
    return {
        "ruleset": {
            "id": 21252293, "target": "branch",
            "source": "nexusomegac27/NEXUS-OMEGA-EVIDENCE",
            "enforcement": "active", "bypass_actors": [],
            "conditions": {"ref_name": {"include": ["refs/heads/main"], "exclude": []}},
            "rules": [
                {"type": "required_status_checks", "parameters": {
                    "required_status_checks": [
                        {"context": "validate", "integration_id": 15368},
                        {"context": "r27e-external-structural-firewall"},
                        {"context": "nexus-preentry-lab"}]}},
                {"type": "pull_request", "parameters": {
                    "required_approving_review_count": 1,
                    "require_code_owner_review": True}}
            ]},
        "registry": {
            "object": "NEXUS_OMEGA_EXTERNAL_AGENT_WRITE_SLOTS_V1",
            "anchor_repo": "nexusomegac27/NEXUS-OMEGA-EVIDENCE",
            "claim_ceiling": "C1_DESCRIPTIVE_ONLY",
            "default": "DENY", "external_actor_allowlist": []}}


def run(payload):
    raw = payload if isinstance(payload, bytes) else json.dumps(payload).encode("utf-8")
    return subprocess.run([sys.executable, str(TARGET)], input=raw,
                          capture_output=True, timeout=8)


class ValidateAppRegressionOracle(unittest.TestCase):
    def check(self, payload, state, source_pinned):
        p = run(payload)
        self.assertEqual(p.returncode, 0, p.stderr.decode(errors="replace"))
        obj = json.loads(p.stdout)
        self.assertEqual(obj["state"], state)
        self.assertIs(obj["validate_expected_app_source_pinned"], source_pinned)
        self.assertIs(obj["api_origin_authenticated"], False)
        self.assertIs(obj["github_ruleset_precedence_verified"], False)
        self.assertIs(obj["external_actor_authorized"], False)
        self.assertEqual(obj["claim_ceiling"], "C1_DESCRIPTIVE_ONLY")

    def test_01_positive_exact_source(self):
        self.check(fixture(), PASS, True)

    def test_02_positive_nonmain_literal_exclusion(self):
        x = fixture(); x["ruleset"]["conditions"]["ref_name"]["exclude"] = ["refs/heads/dev"]
        self.check(x, PASS, True)

    def test_03_positive_additional_unpinned_context(self):
        x = fixture(); x["ruleset"]["rules"][0]["parameters"]["required_status_checks"].append({"context":"other"})
        self.check(x, PASS, True)

    def test_04_negative_wrong_integration_id(self):
        x = fixture(); x["ruleset"]["rules"][0]["parameters"]["required_status_checks"][0]["integration_id"] = 15369
        self.check(x, HOLD, False)

    def test_05_negative_missing_integration_id(self):
        x = fixture(); del x["ruleset"]["rules"][0]["parameters"]["required_status_checks"][0]["integration_id"]
        self.check(x, HOLD, False)

    def test_06_negative_boolean_integration_id(self):
        x = fixture(); x["ruleset"]["rules"][0]["parameters"]["required_status_checks"][0]["integration_id"] = True
        self.check(x, HOLD, False)

    def test_07_negative_string_integration_id(self):
        x = fixture(); x["ruleset"]["rules"][0]["parameters"]["required_status_checks"][0]["integration_id"] = "15368"
        self.check(x, HOLD, False)

    def test_08_negative_null_integration_id(self):
        x = fixture(); x["ruleset"]["rules"][0]["parameters"]["required_status_checks"][0]["integration_id"] = None
        self.check(x, HOLD, False)

    def test_09_existing_wildcard_exclusion_hold(self):
        x = fixture(); x["ruleset"]["conditions"]["ref_name"]["exclude"] = ["refs/heads/*"]
        self.check(x, HOLD, True)

    def test_10_existing_registry_allow_hold(self):
        x = fixture(); x["registry"]["default"] = "ALLOW"
        self.check(x, HOLD, True)

    def test_11_existing_missing_required_check_hold(self):
        x = fixture(); x["ruleset"]["rules"][0]["parameters"]["required_status_checks"].pop()
        self.check(x, HOLD, True)

    def test_12_existing_bypass_hold(self):
        x = fixture(); x["ruleset"]["bypass_actors"] = [{"actor_id": 2}]
        self.check(x, HOLD, True)

    def test_13_duplicate_json_fail_closed(self):
        p = run(b'{"ruleset":{},"ruleset":{},"registry":{}}')
        self.assertEqual(p.returncode, 2)
        self.assertIn(b"FAIL_CLOSED", p.stderr)

    def test_14_nonfinite_json_fail_closed(self):
        p = run(b'{"ruleset":NaN,"registry":{}}')
        self.assertEqual(p.returncode, 2)
        self.assertIn(b"FAIL_CLOSED", p.stderr)


if __name__ == "__main__":
    unittest.main()
