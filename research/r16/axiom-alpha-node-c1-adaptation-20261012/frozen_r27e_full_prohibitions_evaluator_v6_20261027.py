#!/usr/bin/env python3
"""Independent, pre-candidate C1 black-box oracle for R27-E prohibition completeness.

Source contract: docs/governance/EXTERNAL_AGENT_WRITE_SLOTS_V1.json,
main 36d712268072d0252a94ebd699113ee151c80f1f, Git blob
1fabcab7f556e83621a3676ddfb3d11cdd964b55. No imports from target.
Synthetic ruleset is a positive control, NOT evidence of actual GitHub enforcement.
"""
import copy
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest

HERE = Path(__file__).resolve().parent
TARGET = Path(os.environ.get("AXIOM_CANDIDATE", HERE / "alpha_r27e_ruleset_full_prohibitions_v6_20261027.py"))
PASS = "PASS_REQUIRED_CONFIG_WITNESSES_C1"
HOLD = "HOLD_SCOPED_ENFORCEMENT_GAP"
# Fixed independently from the original public registry, not imported from target.
FULL_PROHIBITIONS = (
    "EXTERNAL_ROOT_OR_NAMESPACE_CREATION",
    "EXTERNAL_EDIT_EXISTING_FILES",
    "EXTERNAL_RENAME_DELETE_MOVE",
    "EXTERNAL_CREATE_SUBDIRECTORY",
    "EXTERNAL_PATCH_GOVERNANCE_CODE_CI",
    "EXTERNAL_CREATE_OWN_TEMPLATE",
    "AUTO_MERGE",
    "AUTO_RUNTIME",
    "NEW_WORKER",
)


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
            "default": "DENY", "external_actor_allowlist": [],
            "status": "C1_OPERATOR_PREALLOCATED_SLOTS_EXTERNAL_ACTORS_NOT_AUTHORIZED",
            "authority": "NEXUS_OPERATOR_GOVERNED_ONLY",
            "owner_github_login": "nexusomegac27",
            "assignments": [{
                "assignment_id": "R27-E-20261011",
                "returns_path": "research/r27/www-extern-wake-isolation-20261011/returns/",
                "status": "PREALLOCATED_NOT_YET_EXTERNAL_AUTHORIZED"}],
            "prohibited": list(FULL_PROHIBITIONS)}}


def run(payload):
    raw = payload if isinstance(payload, bytes) else json.dumps(payload).encode("utf-8")
    return subprocess.run([sys.executable, str(TARGET)], input=raw,
                          capture_output=True, timeout=8, cwd=HERE)


class FullProhibitionsOracle(unittest.TestCase):
    def check(self, payload, expected):
        p = run(payload)
        self.assertEqual(p.returncode, 0, p.stderr.decode(errors="replace"))
        obj = json.loads(p.stdout)
        self.assertEqual(obj["state"], expected)
        self.assertIs(obj["api_origin_authenticated"], False)
        self.assertIs(obj["external_actor_authorized"], False)
        self.assertEqual(obj["claim_ceiling"], "C1_DESCRIPTIVE_ONLY")

    def test_10_positive_full_registry(self):
        self.check(fixture(), PASS)

    def test_11_positive_extra_metadata(self):
        x = fixture(); x["registry"]["schema_version"] = "1.0.0"
        self.check(x, PASS)

    def test_12_negative_duplicate_prohibition(self):
        x = fixture(); x["registry"]["prohibited"].append("AUTO_MERGE")
        self.check(x, HOLD)

    def test_13_negative_default_allow(self):
        x = fixture(); x["registry"]["default"] = "ALLOW"
        self.check(x, HOLD)

    def test_14_negative_validate_app_source(self):
        x = fixture()
        x["ruleset"]["rules"][0]["parameters"]["required_status_checks"][0]["integration_id"] = 15369
        self.check(x, HOLD)

    def test_15_duplicate_json_key_fail_closed(self):
        p = run(b'{"ruleset":{},"ruleset":{},"registry":{}}')
        self.assertEqual(p.returncode, 2)
        self.assertIn(b"FAIL_CLOSED", p.stderr)


def make_missing_prohibition_test(prohibition):
    def test(self):
        x = fixture()
        x["registry"]["prohibited"].remove(prohibition)
        self.check(x, HOLD)
    return test


for i, item in enumerate(FULL_PROHIBITIONS, 1):
    setattr(FullProhibitionsOracle, f"test_{i:02d}_negative_missing_{item.lower()}",
            make_missing_prohibition_test(item))


if __name__ == "__main__":
    unittest.main()
