# SPDX-License-Identifier: Apache-2.0
"""R28 synthetic pre-entry adversarial fixtures.

These exercise the actual R27-E path/manifest policy, not the vulnerable
local Node.js broker. Passing them does NOT repair AUTH001/002/003.
"""
import copy
import hashlib
import unittest
from pathlib import Path

from scripts import nexus_preentry_lab as LAB
from tests.test_external_agent_pr import M, REG, FILES, FILES_META, SLOT

ROOT = Path(__file__).resolve().parents[1]


class PreentryLabTests(unittest.TestCase):
    def test_01_owner_preallocated_exact_slots_only(self):
        self.assertEqual(M.validate_paths(FILES_META, "verified-github-agent", REG), [])

    def test_02_forged_actor_label_cannot_impersonate_authenticated_github_login(self):
        hostile = copy.deepcopy(FILES_META)
        hostile[0]["claimed_actor"] = "verified-github-agent"
        self.assertIn("UNREGISTERED_EXTERNAL_GITHUB_ACTOR",
                      M.validate_paths(hostile, "unknown-user", REG))

    def test_03_default_unactivated_assignment_denies(self):
        r = copy.deepcopy(REG)
        r["assignments"][0]["status"] = "PREALLOCATED_NOT_YET_EXTERNAL_AUTHORIZED"
        self.assertIn("SLOT_NOT_ACTIVATED",
                      M.validate_paths(FILES_META, "verified-github-agent", r))

    def test_04_extra_namespace_cannot_enter(self):
        hostile = copy.deepcopy(FILES_META)
        hostile.append({"filename": "governance/STRUCTURE_CONTRACT.md", "status": "added"})
        errors = M.validate_paths(hostile, "verified-github-agent", REG)
        self.assertTrue(any("EXTERNAL_OUTSIDE_PREALLOCATED_SLOT" in e for e in errors))

    def test_05_sibling_r28_return_is_not_owner_preallocated(self):
        x = [{"filename": "research/r28/github-validation-computer/returns/"
                           "R28-00_FAKE_RECEIPT_R0.md", "status": "added"}]
        self.assertTrue(M.validate_paths(x, "verified-github-agent", REG))

    def test_06_path_traversal_rejected(self):
        x = [{"filename": SLOT + "../governance/FAKE.json", "status": "added"}]
        self.assertTrue(any("INVALID_PATH" in e for e in
                            M.validate_paths(x, "verified-github-agent", REG)))

    def test_07_double_slash_and_backslash_rejected(self):
        for path in (SLOT + "//" + FILES[0], SLOT + "\\\\" + FILES[0]):
            x = [{"filename": path, "status": "added"}]
            self.assertTrue(any("INVALID_PATH" in e for e in
                                M.validate_paths(x, "verified-github-agent", REG)))

    def test_08_external_modify_delete_cannot_pass(self):
        for action in ("modified", "removed", "renamed", "copied"):
            x = [{"filename": SLOT + FILES[0], "status": action}]
            self.assertTrue(M.validate_paths(x, "verified-github-agent", REG))

    def test_09_incomplete_seven_file_set_rejected(self):
        errors = M.validate_paths(FILES_META[:-1], "verified-github-agent", REG)
        self.assertIn("INCOMPLETE_OR_EXTRA_RETURN_FILE_SET", errors)

    def test_10_duplicate_json_keys_rejected(self):
        with self.assertRaisesRegex(ValueError, "DUPLICATE_JSON_KEY"):
            M.strict_json(b'{"status":"PASS","status":"FAIL"}')

    def test_11_forged_manifest_is_not_owner_registry(self):
        r = copy.deepcopy(REG)
        r["assignments"][0]["filenames"].append("R28-05_RETURN_MANIFEST_R0.json")
        with self.assertRaisesRegex(ValueError, "ASSIGNMENT_MUST_HAVE_ONE_MANIFEST"):
            M.manifest_path_for_assignment(r["assignments"][0])

    def test_12_r27f_names_remain_unregistered(self):
        x = [{"filename": SLOT + "R27F-05_RETURN_MANIFEST_R0.json",
              "status": "added"}]
        errors = M.validate_paths(x, "verified-github-agent", REG)
        self.assertTrue(any("EXTERNAL_OUTSIDE_PREALLOCATED_SLOT" in e for e in errors))

    def test_13_receipt_cannot_claim_runtime_live_or_egress_block(self):
        d = LAB.receipt({"status": "PASS_OFFLINE_FIXTURES_C1",
                         "results": [], "all_passed": True}, [])
        self.assertFalse(d["untrusted_pr_code_executed"])
        self.assertEqual(d["egress_default_deny"], "NOT_ENFORCED")
        self.assertEqual(d["runtime_auth001_002_003"], "HOLD_SECURITY_NOT_TESTED_HERE")
        self.assertEqual(d["www_or_internal_entry_guard"], "NOT_INSTALLED")

    def test_14_fixed_commands_have_no_shell_and_no_network_install(self):
        self.assertTrue(all(isinstance(c, tuple) and len(c) >= 2
                            for c in LAB.COMMANDS))
        flat = " ".join(" ".join(c) for c in LAB.COMMANDS)
        for suspect in ("npm install", "npm ci", "curl ", "wget ", "bash -c",
                        "pip install", "git push"):
            self.assertNotIn(suspect, flat)
        self.assertNotIn("shell=True", Path(LAB.__file__).read_text())

    def test_15_missing_trusted_source_fails_closed(self):
        import tempfile
        with tempfile.TemporaryDirectory() as t:
            with self.assertRaisesRegex(ValueError, "MISSING_OR_UNSAFE_TRUSTED_SOURCE"):
                LAB.compute_bindings(Path(t))

    def test_16_input_bindings_are_byte_derived_not_hardcoded(self):
        bindings = LAB.compute_bindings(ROOT)
        self.assertEqual(len(bindings), len(LAB.SOURCE_FILES))
        for b in bindings:
            raw = (ROOT / b["path"]).read_bytes()
            self.assertEqual(b["sha256"], hashlib.sha256(raw).hexdigest())
            self.assertEqual(b["bytes"], len(raw))

    def test_17_no_status_claim_without_all_tests(self):
        x = [{"command": ["test"], "passed": False, "exit_code": 1}]
        d = LAB.receipt({"status": "FAIL_CLOSED", "all_passed": False,
                         "results": x}, [])
        self.assertEqual(d["status"], "FAIL_CLOSED")
        self.assertFalse(d["tests"][0]["passed"])

    def test_18_no_provider_identity_is_assumed_from_receipt(self):
        d = LAB.receipt({"status": "PASS_OFFLINE_FIXTURES_C1",
                         "all_passed": True, "results": []}, [])
        self.assertEqual(d["independent_provider_signature"], "NOT_ESTABLISHED")
        self.assertEqual(d["production_release"], "NOT_AUTHORIZED")
        self.assertEqual(d["artifact_attestation"], "NOT_GENERATED")

    def test_19_registry_source_is_single_existing_implementation(self):
        self.assertEqual(M.CONTRACT, "docs/governance/EXTERNAL_AGENT_WRITE_SLOTS_V1.json")
        self.assertEqual(LAB.SOURCE_FILES.count(M.CONTRACT), 1)


if __name__ == "__main__":
    unittest.main()
