#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Deterministic positive and one-defect fixtures for the NEXUS repository steward."""
import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/nexus_repository_steward.py"
spec = importlib.util.spec_from_file_location("steward", SCRIPT)
steward = importlib.util.module_from_spec(spec)
spec.loader.exec_module(steward)


class StewardTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / "research/r5/alpha").mkdir(parents=True)
        (self.root / "research/r5/alpha/README.md").write_text("# Lane\n", encoding="utf-8")
        self.structure = {"version": "1.7.15", "root_files": ["README.md"],
                          "root_directories": ["research"],
                          "active_research_lanes": {"alpha": {"path": "research/r5/alpha"}}}

    def entries(self):
        p = self.root / "research/r5/alpha/README.md"
        b = p.read_bytes()
        oid = hashlib.sha1(b"blob " + str(len(b)).encode() + b"\0" + b).hexdigest()
        return [("research/r5/alpha/README.md", "100644", "blob", oid, len(b))]

    def report(self, entries=None):
        return steward.audit(self.root, entries if entries is not None else self.entries(),
                             self.structure, "a" * 40)

    def test_positive_source_hash_and_lane_inventory(self):
        r = self.report()
        self.assertEqual(r["integrity_error_count"], 0)
        self.assertEqual(r["registered_lane_count"], 1)
        self.assertEqual(r["tracked_file_count"], 1)
        self.assertEqual(r["files"][0]["observed_sha256"],
                         hashlib.sha256(b"# Lane\n").hexdigest())

    def test_changed_original_detected(self):
        items = self.entries()
        (self.root / "research/r5/alpha/README.md").write_text("CHANGED\n")
        self.assertIn("WORKTREE_GIT_BLOB_MISMATCH",
                      [f["code"] for f in self.report(items)["findings"]])

    def test_missing_source_detected(self):
        items = self.entries()
        (self.root / "research/r5/alpha/README.md").unlink()
        codes = [f["code"] for f in self.report(items)["findings"]]
        self.assertIn("TRACKED_FILE_NOT_PRESENT", codes)

    def test_registered_readme_missing(self):
        self.assertIn("REGISTERED_LANE_README_MISSING",
                      [f["code"] for f in self.report([])["findings"]])

    def test_windows_reserved_rejected(self):
        self.assertIn("WINDOWS_RESERVED_NAME",
                      steward.policy("research/CON/notes.txt", {"research"})[2])

    def test_path_traversal_rejected(self):
        self.assertIn("INVALID_PATH_COMPONENT",
                      steward.policy("research/../secret.txt", {"research"})[2])

    def test_outside_root_rejected(self):
        self.assertIn("ROOT_NOT_ALLOWLISTED",
                      steward.policy("returns/raw.zip", {"research"})[2])

    def test_uppercase_legacy_is_review_only(self):
        owner, review, faults = steward.policy("research/r5/ALPHA/README.md", {"research"})
        self.assertIn("LEGACY_DIRECTORY_NAMING_REVIEW", review)
        self.assertEqual(faults, [])

    def test_unsafe_traversal_never_reads_files(self):
        entry = ("research/../private.txt", "100644", "blob", "a" * 40, 5)
        report = self.report([entry])
        self.assertIn("INVALID_PATH_COMPONENT", [f["code"] for f in report["findings"]])
        self.assertIsNone(report["files"][0]["observed_sha256"])

    def test_case_collision_is_integrity_fault(self):
        original = self.entries()[0]
        duplicate = ("research/r5/alpha/readme.md", *original[1:])
        self.assertIn("PORTABLE_CASE_COLLISION",
                      [f["code"] for f in self.report([original, duplicate])["findings"]])

    def test_no_mutation(self):
        before = (self.root / "research/r5/alpha/README.md").read_bytes()
        self.report()
        self.assertEqual(before, (self.root / "research/r5/alpha/README.md").read_bytes())

    def test_parse_git_tree_nul_safe(self):
        b = b"100644 blob " + b"a" * 40 + b" 5\tresearch/r5/alpha/README.md\0"
        self.assertEqual(steward.parse_ls_tree(b)[0][-1], 5)


if __name__ == "__main__":
    unittest.main()
