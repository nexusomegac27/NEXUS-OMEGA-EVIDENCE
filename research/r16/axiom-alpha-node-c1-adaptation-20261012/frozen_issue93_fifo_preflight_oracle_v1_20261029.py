#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Frozen, independent negative-control oracle for Issue #93 preflight FIFO safety.

Evaluates an isolated candidate against a separately pinned V1 predecessor.
Does not read network, execute parser modules, or mutate repository sources.
"""
import hashlib
import importlib.util
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
BASELINE = HERE / 'alpha_issue93_v7_dependency_fixity_preflight_v1_20261029.py'
CANDIDATE = HERE / 'alpha_issue93_v7_dependency_fixity_preflight_v2_20261029.py'
BASELINE_SHA256 = '0fb4f5408d4c61d3a2e4c9bd160cc63afe68b077febbdd288e757b0fb324af23'


def import_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def create_fixture(root):
    values = {'a.py': b'alpha\n', 'b.py': b'beta\n', 'c.py': b'gamma\n'}
    for name, raw in values.items():
        (root / name).write_bytes(raw)
    return {name: (len(raw), hashlib.sha256(raw).hexdigest()) for name, raw in values.items()}


class FrozenFifoOracle(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.assert_source = hashlib.sha256(BASELINE.read_bytes()).hexdigest()
        if cls.assert_source != BASELINE_SHA256:
            raise AssertionError('BASELINE_SOURCE_SHA256_MISMATCH')
        cls.old = import_module(BASELINE, 'baseline_v1')
        cls.new = import_module(CANDIDATE, 'candidate_v2')

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.expected = create_fixture(self.root)

    def test_01_positive_inventory(self):
        a = self.old.verify_inventory(self.root, self.expected)
        b = self.new.verify_inventory(self.root, self.expected)
        self.assertEqual((a['status'], b['status'], b['source_files'], b['source_bytes']), ('MATCH', 'MATCH', 3, 17))

    def test_02_same_size_mutation_rejected(self):
        (self.root / 'b.py').write_bytes(b'zeta\n')
        with self.assertRaisesRegex(self.new.FixityError, 'SHA256_MISMATCH'):
            self.new.verify_inventory(self.root, self.expected)

    def test_03_missing_file_rejected(self):
        (self.root / 'a.py').unlink()
        with self.assertRaisesRegex(self.new.FixityError, 'SOURCE_NOT_PRESENT'):
            self.new.verify_inventory(self.root, self.expected)

    def test_04_truncation_rejected(self):
        (self.root / 'c.py').write_bytes(b'X')
        with self.assertRaisesRegex(self.new.FixityError, 'BYTE_COUNT_MISMATCH'):
            self.new.verify_inventory(self.root, self.expected)

    def test_05_symlink_rejected(self):
        (self.root / 'a.py').unlink()
        try:
            (self.root / 'a.py').symlink_to(self.root / 'b.py')
        except (OSError, NotImplementedError):
            self.skipTest('symlink not available')
        with self.assertRaisesRegex(self.new.FixityError, 'SYMLINK_REJECTED'):
            self.new.verify_inventory(self.root, self.expected)

    def test_06_nonregular_directory_rejected(self):
        (self.root / 'a.py').unlink()
        (self.root / 'a.py').mkdir()
        with self.assertRaises((self.new.FixityError, OSError)):
            self.new.verify_inventory(self.root, self.expected)

    @unittest.skipUnless(hasattr(os, 'mkfifo') and hasattr(os, 'O_NONBLOCK'), 'POSIX FIFO required')
    def test_07_fifo_predecessor_hangs_but_candidate_fails_bounded(self):
        (self.root / 'a.py').unlink()
        os.mkfifo(self.root / 'a.py')
        code = '''import importlib.util, pathlib, sys
spec=importlib.util.spec_from_file_location("target",sys.argv[1]); m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
m.verify_inventory(sys.argv[2], {"a.py":(6,"%s")})
''' % self.expected['a.py'][1]
        baseline = [sys.executable, '-c', code, str(BASELINE), str(self.root)]
        with self.assertRaises(subprocess.TimeoutExpired):
            subprocess.run(baseline, capture_output=True, timeout=1.2)
        candidate = [sys.executable, '-c', code, str(CANDIDATE), str(self.root)]
        result = subprocess.run(candidate, capture_output=True, text=True, timeout=1.2)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('NONREGULAR_FILE', result.stderr)

    def test_08_unsafe_name_rejected(self):
        with self.assertRaisesRegex(self.new.FixityError, 'UNSAFE_NAME'):
            self.new.verify_inventory(self.root, {'../a.py': (6, '0' * 64)})

    def test_09_invalid_digest_rejected(self):
        with self.assertRaisesRegex(self.new.FixityError, 'INVALID_EXPECTATION'):
            self.new.verify_inventory(self.root, {'a.py': (6, 'G' * 64)})

    def test_10_empty_manifest_rejected(self):
        with self.assertRaisesRegex(self.new.FixityError, 'INVALID_ROOT_OR_MANIFEST'):
            self.new.verify_inventory(self.root, {})

    def test_11_extra_file_is_scoped(self):
        (self.root / 'extra.txt').write_bytes(b'outside scope')
        self.assertEqual(self.new.verify_inventory(self.root, self.expected)['source_files'], 3)

    def test_12_pinned_chain_unchanged(self):
        self.assertEqual(self.old.EXPECTED, self.new.EXPECTED)
        self.assertEqual(self.old.PINNED_MAIN, self.new.PINNED_MAIN)
        self.assertEqual(sum(v[0] for v in self.new.EXPECTED.values()), 24528)


if __name__ == '__main__':
    unittest.main()
