#!/usr/bin/env python3
"""Pre-candidate frozen black-box oracle for read-only R27-E ruleset audit.

All fixtures synthetic, modeled on pinned 2026-10-27 GitHub ruleset #21252293.
No network access, no mutation, no automatic approval or scientific validation.
"""
import copy
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest

HERE = Path(__file__).resolve().parent
CANDIDATE = Path(os.environ.get("AXIOM_CANDIDATE", HERE / "alpha_r27e_ruleset_enforcement_audit_v1_20261027.py"))


def fixture():
    return {
        "ruleset": {
            "id": 21252293, "target": "branch", "source": "nexusomegac27/NEXUS-OMEGA-EVIDENCE",
            "enforcement": "active", "conditions": {"ref_name": {
                "include": ["refs/heads/main"], "exclude": []}}, "bypass_actors": [],
            "rules": [
                {"type": "required_status_checks", "parameters": {
                    "strict_required_status_checks_policy": True,
                    "required_status_checks": [{"context": "validate"},
                                               {"context": "r27e-external-structural-firewall"},
                                               {"context": "nexus-preentry-lab"}]}},
                {"type": "pull_request", "parameters": {
                    "required_approving_review_count": 1, "require_code_owner_review": True}},
            ]},
        "registry": {"object": "NEXUS_OMEGA_EXTERNAL_AGENT_WRITE_SLOTS_V1",
                     "anchor_repo": "nexusomegac27/NEXUS-OMEGA-EVIDENCE",
                     "claim_ceiling": "C1_DESCRIPTIVE_ONLY", "default": "DENY",
                     "external_actor_allowlist": []},
    }


def run(data):
    raw = data if isinstance(data, bytes) else json.dumps(data, separators=(",", ":")).encode()
    return subprocess.run([sys.executable, str(CANDIDATE)], input=raw,
                          capture_output=True, timeout=10)


class RulesetOracle(unittest.TestCase):
    def good(self, data, state="PASS_REQUIRED_CONFIG_WITNESSES_C1", missing=None):
        p = run(data)
        self.assertEqual(p.returncode, 0, p.stderr.decode(errors="replace"))
        d = json.loads(p.stdout)
        self.assertEqual(d["state"], state)
        if missing is not None:
            self.assertEqual(d["missing_required_status_contexts"], missing)
        self.assertFalse(d["api_origin_authenticated"])
        self.assertFalse(d["external_actor_authorized"])
        self.assertEqual(d["claim_ceiling"], "C1_DESCRIPTIVE_ONLY")
        return d

    def bad(self, data):
        p = run(data)
        self.assertEqual(p.returncode, 2, (p.returncode, p.stderr[:200]))
        self.assertIn(b"FAIL_CLOSED:", p.stderr)

    def test_01_complete_controls(self): self.good(fixture())
    def test_02_reordered_rules(self):
        x = fixture(); x["ruleset"]["rules"].reverse(); self.good(x)
    def test_03_live_baseline_missing_two_checks(self):
        x = fixture(); x["ruleset"]["rules"][0]["parameters"]["required_status_checks"] = [{"context": "validate"}]
        x["ruleset"]["rules"][1]["parameters"].update(required_approving_review_count=0, require_code_owner_review=False)
        d = self.good(x, "HOLD_SCOPED_ENFORCEMENT_GAP", ["nexus-preentry-lab", "r27e-external-structural-firewall"])
        self.assertFalse(d["one_approval_required"])
        self.assertFalse(d["codeowner_review_required"])
        self.assertTrue(d["external_registry_default_deny_empty"])
    def test_04_missing_firewall_check(self):
        x = fixture(); x["ruleset"]["rules"][0]["parameters"]["required_status_checks"].pop(1)
        self.good(x, "HOLD_SCOPED_ENFORCEMENT_GAP", ["r27e-external-structural-firewall"])
    def test_05_missing_preentry_check(self):
        x = fixture(); x["ruleset"]["rules"][0]["parameters"]["required_status_checks"].pop()
        self.good(x, "HOLD_SCOPED_ENFORCEMENT_GAP", ["nexus-preentry-lab"])
    def test_06_wrong_case(self):
        x = fixture(); x["ruleset"]["rules"][0]["parameters"]["required_status_checks"][1]["context"] = "R27E-external-structural-firewall"
        self.good(x, "HOLD_SCOPED_ENFORCEMENT_GAP")
    def test_07_inactive_ruleset(self):
        x = fixture(); x["ruleset"]["enforcement"] = "disabled"
        d = self.good(x, "HOLD_SCOPED_ENFORCEMENT_GAP"); self.assertFalse(d["main_exact_ref_active"])
    def test_08_main_excluded(self):
        x = fixture(); x["ruleset"]["conditions"]["ref_name"]["exclude"] = ["refs/heads/main"]
        self.good(x, "HOLD_SCOPED_ENFORCEMENT_GAP")
    def test_09_no_codeowner_review(self):
        x = fixture(); x["ruleset"]["rules"][1]["parameters"]["require_code_owner_review"] = False
        d = self.good(x, "HOLD_SCOPED_ENFORCEMENT_GAP"); self.assertFalse(d["codeowner_review_required"])
    def test_10_zero_approvals(self):
        x = fixture(); x["ruleset"]["rules"][1]["parameters"]["required_approving_review_count"] = 0
        self.good(x, "HOLD_SCOPED_ENFORCEMENT_GAP")
    def test_11_bypass_actor(self):
        x = fixture(); x["ruleset"]["bypass_actors"] = [{"actor_id": 1}]
        d = self.good(x, "HOLD_SCOPED_ENFORCEMENT_GAP"); self.assertEqual(d["bypass_actor_count"], 1)
    def test_12_registry_allowlist_not_empty(self):
        x = fixture(); x["registry"]["external_actor_allowlist"] = ["unregistered"]
        d = self.good(x); self.assertFalse(d["external_registry_default_deny_empty"])
    def test_13_wrong_ruleset_id(self):
        x = fixture(); x["ruleset"]["id"] = 0; self.bad(x)
    def test_14_duplicate_json_key(self): self.bad(b'{"ruleset":{},"ruleset":{},"registry":{}}')
    def test_15_nonfinite_json(self): self.bad(b'{"ruleset":NaN,"registry":{}}')
    def test_16_duplicate_status_context(self):
        x = fixture(); x["ruleset"]["rules"][0]["parameters"]["required_status_checks"].append({"context": "validate"}); self.bad(x)
    def test_17_invalid_registry(self):
        x = fixture(); x["registry"]["anchor_repo"] = "other/repo"; self.bad(x)
    def test_18_over_budget(self): self.bad(b" " * (1024 * 1024 + 1))
    def test_19_no_rules(self):
        x = fixture(); x["ruleset"]["rules"] = []
        self.good(x, "HOLD_SCOPED_ENFORCEMENT_GAP")
    def test_20_no_main_include(self):
        x = fixture(); x["ruleset"]["conditions"]["ref_name"]["include"] = ["refs/heads/other"]
        self.good(x, "HOLD_SCOPED_ENFORCEMENT_GAP")


if __name__ == "__main__":
    unittest.main()
