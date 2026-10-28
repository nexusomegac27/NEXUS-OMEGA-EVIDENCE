#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Frozen, independent regression oracle for an isolated directory-prefix witness."""
import importlib.util
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent


def candidate():
    spec = importlib.util.spec_from_file_location(
        "steward_directory_alias_witness_v1", HERE / "steward_directory_alias_witness_v1.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def original_full_path_case_collision(paths):
    """Exact relevant predicate shape in pinned steward audit(), not a full audit."""
    seen = {}
    collisions = []
    for path in sorted(paths):
        identity = path.casefold()
        if identity in seen and seen[identity] != path:
            collisions.append(path)
        seen[identity] = path
    return collisions


class DirectoryAliasWitnessTests(unittest.TestCase):
    def test_baseline_misses_distinct_leaf_files_under_case_alias(self):
        paths = ["research/r16/Case/a.txt", "research/r16/case/b.txt"]
        self.assertEqual(original_full_path_case_collision(paths), [])

    def test_case_alias_detected(self):
        paths = ["research/r16/Case/a.txt", "research/r16/case/b.txt"]
        self.assertIn(("research/r16/Case", "research/r16/case"),
                      candidate().directory_alias_collisions(paths))

    def test_unicode_nfc_nfd_directory_alias_detected(self):
        paths = ["research/r16/caf\u00e9/a.txt", "research/r16/cafe\u0301/b.txt"]
        self.assertEqual(len(candidate().directory_alias_collisions(paths)), 1)

    def test_nested_case_alias_detected(self):
        paths = ["research/r16/topic/Inner/a.txt", "research/r16/topic/inner/b.txt"]
        self.assertIn(("research/r16/topic/Inner", "research/r16/topic/inner"),
                      candidate().directory_alias_collisions(paths))

    def test_distinct_directories_not_flagged(self):
        paths = ["research/r16/red/a.txt", "research/r16/blue/b.txt"]
        self.assertEqual(candidate().directory_alias_collisions(paths), [])

    def test_same_directory_multiple_files_not_flagged(self):
        paths = ["research/r16/topic/a.txt", "research/r16/topic/b.txt"]
        self.assertEqual(candidate().directory_alias_collisions(paths), [])

    def test_leaf_only_case_alias_not_misclassified_as_directory(self):
        paths = ["research/r16/topic/A.txt", "research/r16/topic/a.txt"]
        self.assertEqual(candidate().directory_alias_collisions(paths), [])

    def test_duplicate_paths_not_flagged(self):
        paths = ["research/r16/topic/a.txt"] * 2
        self.assertEqual(candidate().directory_alias_collisions(paths), [])

    def test_malformed_paths_fail_closed(self):
        for path in ["", "/absolute/file", "research//file", "research/../file", "research/./file"]:
            with self.subTest(path=path), self.assertRaises(ValueError):
                candidate().directory_alias_collisions([path])


if __name__ == "__main__":
    unittest.main(verbosity=2)
