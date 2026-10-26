#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Frozen, separate C1 negative oracle for pinned-byte execution.

The evaluator never changes its expectations based on the candidate. A controlled
subprocess launch-hook mutates and restores the source file between the guard's
pre-execution and post-execution hash checks. Only a byte-frozen execution
snapshot can prevent a false PASS on the original failing source.
"""
import hashlib
import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

if len(sys.argv) != 2:
    raise SystemExit('usage: frozen_evaluator.py GUARD_PATH')
GUARD = Path(sys.argv[1]).resolve()
spec = importlib.util.spec_from_file_location('pinned_guard_under_test', GUARD)
guard = importlib.util.module_from_spec(spec)
spec.loader.exec_module(guard)

FAIL_1 = ("import unittest\nclass T(unittest.TestCase):\n"
          "    def test_a(self): self.fail('PINNED_FAIL')\n"
          "if __name__ == '__main__': unittest.main(exit=False)\n")
PASS_1 = ("import unittest\nclass T(unittest.TestCase):\n"
          "    def test_a(self): self.assertTrue(True)\n"
          "if __name__ == '__main__': unittest.main(exit=False)\n")
FAIL_2 = ("import unittest\nclass T(unittest.TestCase):\n"
          "    def test_a(self): self.fail('PINNED_FAIL')\n"
          "    def test_b(self): self.assertTrue(True)\n"
          "if __name__ == '__main__': unittest.main(exit=False)\n")
PASS_2 = ("import unittest\nclass T(unittest.TestCase):\n"
          "    def test_a(self): self.assertTrue(True)\n"
          "    def test_b(self): self.assertTrue(True)\n"
          "if __name__ == '__main__': unittest.main(exit=False)\n")


def invoke(original, replacement=None, expected=1, check_snapshot=False):
    with tempfile.TemporaryDirectory(prefix='alpha162_eval_') as td:
        source = Path(td) / 'pinned_source.py'
        source.write_bytes(original.encode('utf-8'))
        digest = hashlib.sha256(source.read_bytes()).hexdigest()
        original_run = guard.subprocess.run
        captured = {}

        def launch_hook(argv, **kwargs):
            child_script = Path(argv[4])  # python -I -c BOOTSTRAP script nonce
            captured['launch_path'] = child_script
            captured['launch_bytes'] = child_script.read_bytes()
            if replacement is not None:
                source.write_bytes(replacement.encode('utf-8'))
            try:
                return original_run(argv, **kwargs)
            finally:
                if replacement is not None:
                    source.write_bytes(original.encode('utf-8'))

        with patch.object(guard.subprocess, 'run', side_effect=launch_hook):
            result = guard.assess(source, digest, expected, [], timeout=10)
        return result, captured, source == captured.get('launch_path'), digest


class FrozenOracle(unittest.TestCase):
    def test_01_mutate_restore_one_test_fails_closed(self):
        out, _, _, _ = invoke(FAIL_1, PASS_1)
        self.assertEqual(out['status'], 'FAIL_CLOSED')
        self.assertEqual(out['reason'], 'UNITTEST_ACTUAL_RESULT_FAILED')

    def test_02_mutate_restore_two_tests_fails_closed(self):
        out, _, _, _ = invoke(FAIL_2, PASS_2, expected=2)
        self.assertEqual(out['status'], 'FAIL_CLOSED')
        self.assertEqual(out['reason'], 'UNITTEST_ACTUAL_RESULT_FAILED')

    def test_03_execution_path_not_mutable_source(self):
        out, captured, same_path, _ = invoke(FAIL_1)
        self.assertFalse(same_path)
        self.assertEqual(captured['launch_bytes'], FAIL_1.encode('utf-8'))

    def test_04_original_failing_source_fails(self):
        out, _, _, _ = invoke(FAIL_1)
        self.assertEqual(out['status'], 'FAIL_CLOSED')

    def test_05_original_passing_source_passes(self):
        out, _, _, _ = invoke(PASS_1)
        self.assertEqual(out['status'], 'PASS_ISOLATED')

    def test_06_original_two_passing_tests_pass(self):
        out, _, _, _ = invoke(PASS_2, expected=2)
        self.assertEqual(out['status'], 'PASS_ISOLATED')

    def test_07_count_mismatch_rejected(self):
        out, _, _, _ = invoke(PASS_1, expected=2)
        self.assertEqual(out['status'], 'FAIL_CLOSED')
        self.assertEqual(out['reason'], 'UNITTEST_COUNT_MISMATCH')

    def test_08_expected_hash_mismatch_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            source = Path(td) / 'source.py'
            source.write_text(PASS_1, encoding='utf-8')
            out = guard.assess(source, '0'*64, 1, [], timeout=10)
            self.assertEqual(out['status'], 'FAIL_CLOSED')
            self.assertEqual(out['reason'], 'PINNED_EVALUATOR_HASH_MISMATCH')

    def test_09_invalid_count_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            source = Path(td) / 'source.py'
            source.write_text(PASS_1, encoding='utf-8')
            out = guard.assess(source, hashlib.sha256(source.read_bytes()).hexdigest(), 0, [], timeout=10)
            self.assertEqual(out['status'], 'FAIL_CLOSED')


if __name__ == '__main__':
    unittest.main(argv=[sys.argv[0]], verbosity=2)
