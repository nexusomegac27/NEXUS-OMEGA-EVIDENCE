#!/usr/bin/env python3
"""Pre-candidate, black-box R27-E registry contract falsifier (C1 only).

Oracle uses an independently declared fixed registry contract from the pinned
public registry at main 91f79dbb89190d38f5576321e67e18e7be82db6a.
Never imports or modifies candidate code. No live writes.
"""
import copy
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest

HERE = Path(__file__).resolve().parent
TARGET = Path(os.environ.get("AXIOM_CANDIDATE", HERE / "alpha_r27e_ruleset_registry_contract_v5_20261027.py"))
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
            "default": "DENY", "external_actor_allowlist": [],
            "status": "C1_OPERATOR_PREALLOCATED_SLOTS_EXTERNAL_ACTORS_NOT_AUTHORIZED",
            "authority": "NEXUS_OPERATOR_GOVERNED_ONLY",
            "owner_github_login": "nexusomegac27",
            "assignments": [{
                "assignment_id": "R27-E-20261011",
                "returns_path": "research/r27/www-extern-wake-isolation-20261011/returns/",
                "status": "PREALLOCATED_NOT_YET_EXTERNAL_AUTHORIZED"}],
            "prohibited": ["AUTO_MERGE", "AUTO_RUNTIME", "NEW_WORKER",
                           "EXTERNAL_PATCH_GOVERNANCE_CODE_CI",
                           "EXTERNAL_EDIT_EXISTING_FILES"]}}


def run(payload):
    raw = payload if isinstance(payload, bytes) else json.dumps(payload).encode("utf-8")
    return subprocess.run([sys.executable, str(TARGET)], input=raw,
                          capture_output=True, timeout=8)


class RegistryContractOracle(unittest.TestCase):
    def check(self, payload, state):
        p = run(payload)
        self.assertEqual(p.returncode, 0, p.stderr.decode(errors="replace"))
        obj = json.loads(p.stdout)
        self.assertEqual(obj["state"], state)
        self.assertIs(obj["api_origin_authenticated"], False)
        self.assertIs(obj["external_actor_authorized"], False)
        self.assertEqual(obj["claim_ceiling"], "C1_DESCRIPTIVE_ONLY")

    def test_01_positive_pinned_contract(self):
        self.check(fixture(), PASS)

    def test_02_positive_unrelated_registry_metadata(self):
        x = fixture(); x["registry"]["schema_version"] = "1.0.0"
        self.check(x, PASS)

    def test_03_negative_registry_status_authorized(self):
        x = fixture(); x["registry"]["status"] = "EXTERNAL_ACTORS_AUTHORIZED"
        self.check(x, HOLD)

    def test_04_negative_registry_status_missing(self):
        x = fixture(); del x["registry"]["status"]
        self.check(x, HOLD)

    def test_05_negative_registry_authority_forged(self):
        x = fixture(); x["registry"]["authority"] = "AGENT_SELF_GOVERNED"
        self.check(x, HOLD)

    def test_06_negative_owner_mismatch(self):
        x = fixture(); x["registry"]["owner_github_login"] = "external-bot"
        self.check(x, HOLD)

    def test_07_negative_assignments_missing(self):
        x = fixture(); del x["registry"]["assignments"]
        self.check(x, HOLD)

    def test_08_negative_assignment_authorized(self):
        x = fixture(); x["registry"]["assignments"][0]["status"] = "AUTHORIZED"
        self.check(x, HOLD)

    def test_09_negative_assignment_wrong_id(self):
        x = fixture(); x["registry"]["assignments"][0]["assignment_id"] = "R27-E-FORGED"
        self.check(x, HOLD)

    def test_10_negative_return_path_redirected(self):
        x = fixture(); x["registry"]["assignments"][0]["returns_path"] = "research/r27/custom/"
        self.check(x, HOLD)

    def test_11_negative_second_assignment(self):
        x = fixture(); x["registry"]["assignments"].append(copy.deepcopy(x["registry"]["assignments"][0]))
        self.check(x, HOLD)

    def test_12_negative_prohibition_missing(self):
        x = fixture(); x["registry"]["prohibited"].remove("AUTO_MERGE")
        self.check(x, HOLD)

    def test_13_negative_prohibition_invalid_type(self):
        x = fixture(); x["registry"]["prohibited"] = "AUTO_MERGE"
        self.check(x, HOLD)

    def test_14_negative_validate_app_id(self):
        x = fixture(); x["ruleset"]["rules"][0]["parameters"]["required_status_checks"][0]["integration_id"] = 15369
        self.check(x, HOLD)

    def test_15_negative_wildcard_ref_exclusion(self):
        x = fixture(); x["ruleset"]["conditions"]["ref_name"]["exclude"] = ["refs/heads/*"]
        self.check(x, HOLD)

    def test_16_negative_default_allow(self):
        x = fixture(); x["registry"]["default"] = "ALLOW"
        self.check(x, HOLD)

    def test_17_duplicate_json_fail_closed(self):
        p = run(b'{"ruleset":{},"ruleset":{},"registry":{}}')
        self.assertEqual(p.returncode, 2)
        self.assertIn(b"FAIL_CLOSED", p.stderr)


if __name__ == "__main__":
    unittest.main()
