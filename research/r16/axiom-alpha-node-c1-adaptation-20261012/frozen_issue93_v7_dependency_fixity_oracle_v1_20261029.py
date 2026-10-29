#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Frozen, separately authored test of a read-only dependency-fixity preflight.

No external network, no production source mutation, no acceptance of GitHub actor.
"""
import hashlib
import importlib.util
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

CANDIDATE = Path(__file__).with_name('alpha_issue93_v7_dependency_fixity_preflight_v1_20261029.py')
spec = importlib.util.spec_from_file_location('candidate_under_test', CANDIDATE)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def setup(root):
    files = {'v1.py': b'alpha\n', 'v2.py': b'beta\n', 'v3.py': b'gamma\n'}
    for name, data in files.items():
        (root / name).write_bytes(data)
    return {name: (len(data), hashlib.sha256(data).hexdigest()) for name, data in files.items()}


class FrozenFixityOracle(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.expected = setup(self.root)

    def test_positive_exact_three_files(self):
        r = module.verify_inventory(self.root, self.expected)
        self.assertEqual((r['status'], r['source_files'], r['source_bytes']), ('MATCH', 3, 17))
        self.assertFalse(r['parser_executed'])

    def test_same_size_mutant_fails(self):
        (self.root / 'v2.py').write_bytes(b'zeta\n')
        with self.assertRaisesRegex(module.FixityError, 'SHA256_MISMATCH'):
            module.verify_inventory(self.root, self.expected)

    def test_naive_exists_baseline_misses_mutant(self):
        (self.root / 'v2.py').write_bytes(b'zeta\n')
        self.assertTrue(all((self.root / x).exists() for x in self.expected))
        with self.assertRaises(module.FixityError):
            module.verify_inventory(self.root, self.expected)

    def test_missing_file_fails(self):
        (self.root / 'v1.py').unlink()
        with self.assertRaisesRegex(module.FixityError, 'SOURCE_NOT_PRESENT'):
            module.verify_inventory(self.root, self.expected)

    def test_truncated_file_fails(self):
        (self.root / 'v3.py').write_bytes(b'x')
        with self.assertRaisesRegex(module.FixityError, 'BYTE_COUNT_MISMATCH'):
            module.verify_inventory(self.root, self.expected)

    def test_symlink_fails(self):
        (self.root / 'v1.py').unlink()
        try:
            (self.root / 'v1.py').symlink_to(self.root / 'v2.py')
        except (OSError, NotImplementedError):
            self.skipTest('symlinks unsupported')
        with self.assertRaisesRegex(module.FixityError, 'SYMLINK_REJECTED'):
            module.verify_inventory(self.root, self.expected)

    def test_wrong_expected_digest_fails(self):
        self.expected['v2.py'] = (5, '0' * 64)
        with self.assertRaisesRegex(module.FixityError, 'SHA256_MISMATCH'):
            module.verify_inventory(self.root, self.expected)

    def test_path_traversal_rejected(self):
        self.expected['../other.py'] = (1, '0' * 64)
        with self.assertRaisesRegex(module.FixityError, 'UNSAFE_NAME'):
            module.verify_inventory(self.root, self.expected)

    def test_backslash_traversal_rejected(self):
        self.expected['..\\other.py'] = (1, '0' * 64)
        with self.assertRaisesRegex(module.FixityError, 'UNSAFE_NAME'):
            module.verify_inventory(self.root, self.expected)

    def test_invalid_digest_rejected(self):
        self.expected['v2.py'] = (5, 'G' * 64)
        with self.assertRaisesRegex(module.FixityError, 'INVALID_EXPECTATION'):
            module.verify_inventory(self.root, self.expected)

    def test_noninteger_byte_count_rejected(self):
        self.expected['v2.py'] = (True, '0' * 64)
        with self.assertRaisesRegex(module.FixityError, 'INVALID_EXPECTATION'):
            module.verify_inventory(self.root, self.expected)

    def test_extra_unscoped_file_does_not_break_scoped_audit(self):
        (self.root / 'other.txt').write_bytes(b'extra')
        self.assertEqual(module.verify_inventory(self.root, self.expected)['source_files'], 3)

    def test_empty_manifest_rejected(self):
        with self.assertRaisesRegex(module.FixityError, 'INVALID_ROOT_OR_MANIFEST'):
            module.verify_inventory(self.root, {})

    def test_missing_real_chain_cli_fails_closed(self):
        p = subprocess.run([sys.executable, str(CANDIDATE), '--root', str(self.root)],
                           capture_output=True, text=True, timeout=5)
        self.assertEqual(p.returncode, 2)
        self.assertIn('FAIL_CLOSED', p.stderr)

    def test_pinned_real_chain_manifest_is_seven(self):
        self.assertEqual(len(module.EXPECTED), 7)
        self.assertEqual(sum(x[0] for x in module.EXPECTED.values()), 24528)
        self.assertEqual(len(module.PINNED_MAIN), 40)


if __name__ == '__main__':
    unittest.main()
