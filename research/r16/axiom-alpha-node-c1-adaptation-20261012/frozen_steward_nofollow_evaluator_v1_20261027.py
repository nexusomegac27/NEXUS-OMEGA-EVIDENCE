#!/usr/bin/env python3
"""Frozen independent synthetic oracle for no-follow steward research candidate.

Tests a precise predicate from pinned steward source (not the full steward).
No network, GitHub write, production mutation, or claim promotion.
"""
import hashlib
import importlib.util
import os
from pathlib import Path
import tempfile
import unittest

TARGET = Path(os.environ.get("AXIOM_CANDIDATE", Path(__file__).with_name(
    "alpha_steward_nofollow_read_candidate_v1_20261027.py")))
spec = importlib.util.spec_from_file_location("candidate", TARGET)
candidate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(candidate)
DATA = b"# identical tracked bytes\n"
REL = "research/r5/alpha/README.md"


class FrozenNoFollowOracle(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / "checkout"
        self.outside = Path(self.tmp.name) / "outside"
        (self.root / "research/r5/alpha").mkdir(parents=True)
        (self.outside / "alpha").mkdir(parents=True)
        (self.root / REL).write_bytes(DATA)
        (self.outside / "alpha/README.md").write_bytes(DATA)

    def parent_symlink(self):
        (self.root / REL).unlink()
        (self.root / "research/r5/alpha").rmdir()
        (self.root / "research/r5").rmdir()
        (self.root / "research/r5").symlink_to(self.outside, target_is_directory=True)

    def test_regular_positive(self):
        self.assertEqual(candidate.read_tracked(self.root, REL), DATA)

    def test_parent_symlink_negative_and_baseline_false_accept(self):
        self.parent_symlink()
        leaf = self.root / REL
        self.assertTrue(leaf.is_file() and not leaf.is_symlink())
        self.assertFalse(leaf.resolve().is_relative_to(self.root.resolve()))
        self.assertEqual(hashlib.sha1(b"blob " + str(len(leaf.read_bytes())).encode() +
                         b"\0" + leaf.read_bytes()).hexdigest(),
                         hashlib.sha1(b"blob " + str(len(DATA)).encode() + b"\0" + DATA).hexdigest())
        with self.assertRaises(OSError):
            candidate.read_tracked(self.root, REL)

    def test_leaf_symlink_negative(self):
        (self.root / REL).unlink()
        (self.root / REL).symlink_to(self.outside / "alpha/README.md")
        with self.assertRaises(OSError):
            candidate.read_tracked(self.root, REL)

    def test_traversal_negative(self):
        with self.assertRaisesRegex(ValueError, "INVALID_RELATIVE_PATH"):
            candidate.read_tracked(self.root, "research/../outside/alpha/README.md")

    def test_directory_negative(self):
        with self.assertRaises((OSError, ValueError)):
            candidate.read_tracked(self.root, "research/r5/alpha")

    def test_size_budget_negative(self):
        with self.assertRaisesRegex(ValueError, "FILE_TOO_LARGE"):
            candidate.read_tracked(self.root, REL, max_bytes=3)

    def test_empty_path_negative(self):
        with self.assertRaisesRegex(ValueError, "INVALID_RELATIVE_PATH"):
            candidate.read_tracked(self.root, "")


if __name__ == "__main__":
    unittest.main()
