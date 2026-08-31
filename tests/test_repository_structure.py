#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0

import importlib.util
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


if __name__ == "__main__":
    unittest.main()
