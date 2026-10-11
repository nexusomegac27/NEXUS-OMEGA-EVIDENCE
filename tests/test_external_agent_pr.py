#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""R27-E firewall negative fixtures. Run with python -m unittest tests.test_external_agent_pr."""
import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("nexus_external_firewall", ROOT / "scripts/validate_external_agent_pr.py")
M = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(M)

SLOT = "research/r27/www-extern-wake-isolation-20261011/returns/"
FILES = ["R27-00_CAPABILITY_AND_TRUST_INVENTORY_R0.md", "R27-01_AUTHN_HARD_REMEDIATION_R0.md",
"R27-02_NEGATIVE_TEST_RESULTS_R0.md", "R27-03_E0_E1_E2_CONTRACTS_R0.json",
"R27-04_PROVIDER_FAILOVER_ASSESSMENT_R0.json", "R27-05_RETURN_MANIFEST_R0.json",
"R27-06_SEND_RECEIPT_R0.md"]
REG = {"owner_github_login":"nexusomegac27", "external_actor_allowlist":["verified-github-agent"],
"max_files_per_external_return":7, "assignments":[{"root":SLOT[:-9], "returns_path":SLOT,
"status":"ACTIVE_AUTHORIZED", "filenames":FILES, "parent_order_sha256":"a"*64}]}
FILES_META = [{"filename":SLOT+n, "status":"added"} for n in FILES]

class ExternalAgentFirewallTests(unittest.TestCase):
    def test_good_preassigned_complete_return(self):
        self.assertEqual(M.validate_paths(FILES_META, "verified-github-agent", REG), [])
    def test_unknown_actor_denied_even_if_labels_internal(self):
        self.assertIn("UNREGISTERED_EXTERNAL_GITHUB_ACTOR", M.validate_paths(FILES_META, "unverified-github", REG))
    def test_new_top_level_rejected(self):
        files = FILES_META + [{"filename":"governance/OWN_AGENTS.md", "status":"added"}]
        self.assertTrue(any("EXTERNAL_OUTSIDE_PREALLOCATED_SLOT" in s for s in M.validate_paths(files, "verified-github-agent", REG)))
    def test_new_agent_namespace_rejected(self):
        files = [{"filename":SLOT+"mistral/custom/return.md","status":"added"}]
        self.assertTrue(any("EXTERNAL_OUTSIDE_PREALLOCATED_SLOT" in x for x in M.validate_paths(files,"verified-github-agent",REG)))
    def test_existing_object_overwrite_rejected(self):
        files = [{"filename":SLOT+FILES[0], "status":"modified"}]
        self.assertTrue(any("EXTERNAL_NOT_CREATE_ONLY" in s for s in M.validate_paths(files,"verified-github-agent",REG)))
    def test_rename_delete_rejected(self):
        for status in ("removed", "renamed", "copied"):
            with self.subTest(status=status):
                v=M.validate_paths([{"filename":SLOT+FILES[0],"status":status}],"verified-github-agent",REG)
                self.assertTrue(any("FORBIDDEN_RETURN_PATH_OPERATION" in x for x in v))
    def test_unactivated_slot_denied(self):
        from copy import deepcopy
        reg=deepcopy(REG)
        reg["assignments"][0]["status"]="PREALLOCATED_NOT_YET_EXTERNAL_AUTHORIZED"
        self.assertIn("SLOT_NOT_ACTIVATED",M.validate_paths(FILES_META,"verified-github-agent",reg))
    def test_extra_file_rejected(self):
        files=FILES_META+[{"filename":SLOT+"my-notes.txt","status":"added"}]
        v=M.validate_paths(files,"verified-github-agent",REG)
        self.assertTrue(any("EXTERNAL_OUTSIDE_PREALLOCATED_SLOT" in x for x in v))
    def test_duplicate_json_keys_fail(self):
        with self.assertRaises(ValueError):
            M.strict_json(b'{"agent_id":"fake","agent_id":"internal"}')
    def test_git_blob_digest(self):
        self.assertEqual(M.git_blob_sha1(b"test"), "30d74d258442c7c65512eafab474568dd706c430")
    def test_owner_readme_preallocation_permitted(self):
        files=[{"filename":SLOT+"README.md","status":"added"}, {"filename":"docs/governance/EXTERNAL_AGENT_WRITE_SLOTS_V1.json","status":"added"}]
        self.assertEqual(M.validate_paths(files,"nexusomegac27",REG),[])
    def test_all_existing_paths_stay_unmodified(self):
        files=[{"filename":"AGENTS.md","status":"modified"}]
        self.assertTrue(M.validate_paths(files,"verified-github-agent",REG))
    def test_deepseek_parallel_governance_tree_forbidden(self):
        self.assertTrue(M.validate_paths([{"filename":"governance/STRUCTURE_CONTRACT.md","status":"added"}],"verified-github-agent",REG))
    def test_continuitiy_cannot_grant_authority(self):
        self.assertTrue(M.validate_paths([{"filename":SLOT+"internal-authorized.md","status":"added"}],"verified-github-agent",REG))

if __name__ == "__main__":
    unittest.main()
