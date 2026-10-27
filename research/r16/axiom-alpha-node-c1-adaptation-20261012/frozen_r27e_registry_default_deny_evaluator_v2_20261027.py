#!/usr/bin/env python3
"""Frozen black-box evaluator for the R27-E registry-default-deny C1 witness.

Synthetic input only. This is a separate test oracle, not an authenticated
GitHub source, external peer review, or authorization to change rulesets.
"""
import copy
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest

HERE = Path(__file__).resolve().parent
CANDIDATE = Path(os.environ.get(
    "AXIOM_CANDIDATE", HERE / "alpha_r27e_ruleset_registry_default_deny_audit_v2_20261027.py"))
PASS = "PASS_REQUIRED_CONFIG_WITNESSES_C1"
HOLD = "HOLD_SCOPED_ENFORCEMENT_GAP"


def fixture():
    return {
        "ruleset": {
            "id": 21252293, "target": "branch",
            "source": "nexusomegac27/NEXUS-OMEGA-EVIDENCE",
            "enforcement": "active",
            "conditions": {"ref_name": {"include": ["refs/heads/main"], "exclude": []}},
            "bypass_actors": [],
            "rules": [
                {"type": "required_status_checks", "parameters": {
                    "required_status_checks": [
                        {"context": "validate"},
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
            "default": "DENY", "external_actor_allowlist": []}
    }


def run(payload):
    raw = payload if isinstance(payload, bytes) else json.dumps(payload).encode("utf-8")
    return subprocess.run([sys.executable, str(CANDIDATE)], input=raw,
                          capture_output=True, timeout=8)


class RegistryDenyOracle(unittest.TestCase):
    def check(self, payload, expected, registry_deny):
        p = run(payload)
        self.assertEqual(p.returncode, 0, p.stderr.decode(errors="replace"))
        d = json.loads(p.stdout)
        self.assertEqual(d["state"], expected)
        self.assertIs(d["external_registry_default_deny_empty"], registry_deny)
        self.assertIs(d["api_origin_authenticated"], False)
        self.assertIs(d["external_actor_authorized"], False)
        self.assertEqual(d["claim_ceiling"], "C1_DESCRIPTIVE_ONLY")

    def test_01_complete_positive_control(self):
        self.check(fixture(), PASS, True)

    def test_02_live_ruleset_missing_checks_remains_hold(self):
        x = fixture()
        x["ruleset"]["rules"][0]["parameters"]["required_status_checks"] = [{"context": "validate"}]
        self.check(x, HOLD, True)

    def test_03_bypass_remains_hold(self):
        x = fixture(); x["ruleset"]["bypass_actors"] = [{"actor_id": 1}]
        self.check(x, HOLD, True)

    def test_04_inactive_remains_hold(self):
        x = fixture(); x["ruleset"]["enforcement"] = "disabled"
        self.check(x, HOLD, True)

    def test_05_default_allow_falsifier(self):
        x = fixture(); x["registry"]["default"] = "ALLOW"
        self.check(x, HOLD, False)

    def test_06_default_missing_falsifier(self):
        x = fixture(); del x["registry"]["default"]
        self.check(x, HOLD, False)

    def test_07_allowlist_nonempty_falsifier(self):
        x = fixture(); x["registry"]["external_actor_allowlist"] = ["unregistered"]
        self.check(x, HOLD, False)

    def test_08_both_unsafe_falsifier(self):
        x = fixture(); x["registry"].update(default="ALLOW", external_actor_allowlist=["unknown"])
        self.check(x, HOLD, False)

    def test_09_duplicate_json_rejected(self):
        p = run(b'{"ruleset":{},"ruleset":{},"registry":{}}')
        self.assertEqual(p.returncode, 2)
        self.assertIn(b"FAIL_CLOSED", p.stderr)

    def test_10_nonfinite_json_rejected(self):
        p = run(b'{"ruleset":NaN,"registry":{}}')
        self.assertEqual(p.returncode, 2)
        self.assertIn(b"FAIL_CLOSED", p.stderr)


if __name__ == "__main__":
    unittest.main()
