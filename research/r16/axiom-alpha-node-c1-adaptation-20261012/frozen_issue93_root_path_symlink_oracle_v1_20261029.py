#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Frozen, separate evaluator for symlinked-root provenance in the C1 V2 preflight.

Synthetic filesystem tests only. Does not authenticate a checkout or a GitHub actor.
The V2 source hash is fixed independently of the candidate. No parser is executed.
"""
import hashlib
import importlib.util
import os
from pathlib import Path
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
BASE = HERE / 'alpha_issue93_v7_dependency_fixity_preflight_v2_20261029.py'
CAND = HERE / 'alpha_issue93_v7_dependency_fixity_preflight_v3_20261029.py'
BASE_SHA256 = 'e224c42beced1c23748f241532b467b4a8ef9ef097e69c95d74e67a667748312'


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class RootPathSymlinkOracle(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if hashlib.sha256(BASE.read_bytes()).hexdigest() != BASE_SHA256:
            raise AssertionError('BASELINE_SHA256_MISMATCH')
        cls.old = load(BASE, 'frozen_v2')
        cls.new = load(CAND, 'candidate_v3')

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.top = Path(self.tmp.name)
        self.root = self.top / 'real'
        self.root.mkdir()
        self.raw = b'alpha\nbeta\n'
        (self.root / 'a.py').write_bytes(self.raw)
        self.expected = {'a.py': (len(self.raw), hashlib.sha256(self.raw).hexdigest())}

    def test_01_real_directory_positive(self):
        self.assertEqual(self.old.verify_inventory(self.root, self.expected)['status'], 'MATCH')
        self.assertEqual(self.new.verify_inventory(self.root, self.expected)['status'], 'MATCH')

    @unittest.skipUnless(hasattr(os, 'symlink'), 'symlinks unavailable')
    def test_02_root_symlink_baseline_accepts_candidate_rejects(self):
        link = self.top / 'linked-root'
        link.symlink_to(self.root, target_is_directory=True)
        self.assertEqual(self.old.verify_inventory(link, self.expected)['status'], 'MATCH')
        with self.assertRaisesRegex(self.new.FixityError, 'SYMLINK_ROOT_REJECTED'):
            self.new.verify_inventory(link, self.expected)

    @unittest.skipUnless(hasattr(os, 'symlink'), 'symlinks unavailable')
    def test_03_ancestor_symlink_baseline_accepts_candidate_rejects(self):
        parent = self.top / 'parent'
        parent.mkdir()
        nested = parent / 'inner'
        nested.mkdir()
        (nested / 'a.py').write_bytes(self.raw)
        (self.top / 'alias-parent').symlink_to(parent, target_is_directory=True)
        alias = self.top / 'alias-parent' / 'inner'
        self.assertEqual(self.old.verify_inventory(alias, self.expected)['status'], 'MATCH')
        with self.assertRaisesRegex(self.new.FixityError, 'SYMLINK_ROOT_REJECTED'):
            self.new.verify_inventory(alias, self.expected)

    def test_04_same_size_mutation_rejected(self):
        (self.root / 'a.py').write_bytes(b'omega\nbeta\n')
        with self.assertRaisesRegex(self.new.FixityError, 'SHA256_MISMATCH'):
            self.new.verify_inventory(self.root, self.expected)

    def test_05_missing_file_rejected(self):
        (self.root / 'a.py').unlink()
        with self.assertRaisesRegex(self.new.FixityError, 'SOURCE_NOT_PRESENT'):
            self.new.verify_inventory(self.root, self.expected)

    @unittest.skipUnless(hasattr(os, 'symlink'), 'symlinks unavailable')
    def test_06_leaf_symlink_rejected(self):
        (self.root / 'a.py').unlink()
        (self.root / 'real.py').write_bytes(self.raw)
        (self.root / 'a.py').symlink_to(self.root / 'real.py')
        with self.assertRaisesRegex(self.new.FixityError, 'SYMLINK_REJECTED'):
            self.new.verify_inventory(self.root, self.expected)

    def test_07_unsafe_filename_rejected(self):
        with self.assertRaisesRegex(self.new.FixityError, 'UNSAFE_NAME'):
            self.new.verify_inventory(self.root, {'../a.py': self.expected['a.py']})

    def test_08_empty_manifest_rejected(self):
        with self.assertRaisesRegex(self.new.FixityError, 'INVALID_ROOT_OR_MANIFEST'):
            self.new.verify_inventory(self.root, {})

    def test_09_manifest_and_ceiling_preserved(self):
        self.assertEqual(self.old.EXPECTED, self.new.EXPECTED)
        self.assertEqual(self.old.PINNED_MAIN, self.new.PINNED_MAIN)
        self.assertEqual(self.new.verify_inventory(self.root, self.expected)['claim_ceiling'], 'C1_DESCRIPTIVE_ONLY')

    @unittest.skipUnless(hasattr(os, 'mkfifo') and hasattr(os, 'O_NONBLOCK'), 'POSIX FIFO required')
    def test_10_fifo_still_rejected_nonblocking(self):
        (self.root / 'a.py').unlink()
        os.mkfifo(self.root / 'a.py')
        with self.assertRaisesRegex(self.new.FixityError, 'NONREGULAR_FILE'):
            self.new.verify_inventory(self.root, self.expected)


if __name__ == '__main__':
    unittest.main(verbosity=2)
