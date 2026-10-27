#!/usr/bin/env python3
"""Frozen independent black-box oracle for R27-E exclusion-pattern false-green.

Synthetic inputs only. No GitHub API authentication, ruleset mutation, or claim promotion.
An ambiguous exclusion must HOLD rather than assert main is protected.
"""
import copy
import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
CANDIDATE = Path(os.environ.get("AXIOM_CANDIDATE", HERE / "alpha_r27e_ruleset_ref_exclusion_audit_v3_20261027.py"))
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
                    "required_status_checks": [{"context": s} for s in (
                        "validate", "r27e-external-structural-firewall", "nexus-preentry-lab")]}},
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


class RefExclusionOracle(unittest.TestCase):
    def check(self, payload, expected, main_applies):
        p = run(payload)
        self.assertEqual(p.returncode, 0, p.stderr.decode(errors="replace"))
        d = json.loads(p.stdout)
        self.assertEqual(d["state"], expected)
        self.assertIs(d["main_exact_ref_active"], main_applies)
        self.assertIs(d["api_origin_authenticated"], False)
        self.assertIs(d["github_ruleset_precedence_verified"], False)
        self.assertIs(d["external_actor_authorized"], False)
        self.assertEqual(d["claim_ceiling"], "C1_DESCRIPTIVE_ONLY")

    def with_excludes(self, excludes):
        x = fixture()
        x["ruleset"]["conditions"]["ref_name"]["exclude"] = excludes
        return x

    def test_01_positive_exact_main(self):
        self.check(fixture(), PASS, True)

    def test_02_positive_literal_other_branch(self):
        self.check(self.with_excludes(["refs/heads/dev"]), PASS, True)

    def test_03_positive_multiple_literal_other_branches(self):
        self.check(self.with_excludes(["refs/heads/dev", "refs/heads/release"]), PASS, True)

    def test_04_existing_missing_check_hold(self):
        x = fixture()
        x["ruleset"]["rules"][0]["parameters"]["required_status_checks"] = [{"context": "validate"}]
        self.check(x, HOLD, True)

    def test_05_existing_bypass_hold(self):
        x = fixture(); x["ruleset"]["bypass_actors"] = [{"actor_id": 1}]
        self.check(x, HOLD, True)

    def test_06_existing_registry_default_allow_hold(self):
        x = fixture(); x["registry"]["default"] = "ALLOW"
        self.check(x, HOLD, True)

    def test_07_wildcard_all_branches(self):
        self.check(self.with_excludes(["refs/heads/*"]), HOLD, False)

    def test_08_wildcard_main_prefix(self):
        self.check(self.with_excludes(["refs/heads/main*"]), HOLD, False)

    def test_09_question_mark_pattern(self):
        self.check(self.with_excludes(["refs/heads/ma?n"]), HOLD, False)

    def test_10_character_class_pattern(self):
        self.check(self.with_excludes(["refs/heads/[m]ain"]), HOLD, False)

    def test_11_default_branch_token(self):
        self.check(self.with_excludes(["~DEFAULT_BRANCH"]), HOLD, False)

    def test_12_all_branches_token(self):
        self.check(self.with_excludes(["~ALL"]), HOLD, False)

    def test_13_unresolved_nonmatching_pattern_conservative_hold(self):
        self.check(self.with_excludes(["refs/heads/dev*"]), HOLD, False)

    def test_14_duplicate_json_fail_closed(self):
        p = run(b'{"ruleset":{},"ruleset":{},"registry":{}}')
        self.assertEqual(p.returncode, 2)
        self.assertIn(b"FAIL_CLOSED", p.stderr)

    def test_15_invalid_exclusion_type_fail_closed(self):
        p = run(self.with_excludes([None]))
        self.assertEqual(p.returncode, 2)
        self.assertIn(b"FAIL_CLOSED", p.stderr)


if __name__ == "__main__":
    unittest.main()
