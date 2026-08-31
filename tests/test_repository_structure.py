#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0

import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "validate_repository_structure", ROOT / "scripts" / "validate_repository_structure.py"
)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class RepositoryStructureTests(unittest.TestCase):
    def test_current_repository_passes(self):
        self.assertEqual(MODULE.validate(ROOT), [])

    def test_unexpected_root_entry_fails(self):
        names = set(MODULE.ROOT_FILES | MODULE.ROOT_DIRS)
        names.add("agent-return-random.zip")
        self.assertIn(
            "UNEXPECTED_ROOT_ENTRY:agent-return-random.zip",
            MODULE.validate_root_entries(names),
        )

    def test_missing_required_root_entry_fails(self):
        names = set(MODULE.ROOT_FILES | MODULE.ROOT_DIRS)
        names.remove("research")
        self.assertIn(
            "REQUIRED_ROOT_ENTRY_MISSING:research",
            MODULE.validate_root_entries(names),
        )

    def test_r5_lane_without_readme_fails(self):
        with tempfile.TemporaryDirectory() as td:
            r5_root = Path(td) / "research" / "r5"
            (r5_root / "anonymous-agent").mkdir(parents=True)
            self.assertEqual(
                MODULE.validate_r5_lane_readmes(r5_root),
                ["R5_LANE_README_MISSING:anonymous-agent"],
            )

    def test_r5_lane_with_readme_passes(self):
        with tempfile.TemporaryDirectory() as td:
            r5_root = Path(td) / "research" / "r5"
            lane = r5_root / "declared-agent"
            lane.mkdir(parents=True)
            (lane / "README.md").write_text("# declared\n", encoding="utf-8")
            self.assertEqual(MODULE.validate_r5_lane_readmes(r5_root), [])


if __name__ == "__main__":
    unittest.main()
