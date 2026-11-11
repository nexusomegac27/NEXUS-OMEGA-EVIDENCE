#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Frozen independent black-box tests for C1 unittest exit-status guard.

Uses synthetic unittest scripts only; no import of guard implementation.
The oracle checks subprocess status and JSON reason, not candidate assertions.
"""
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
GUARD = HERE / "alpha_unittest_process_result_guard_v1_20261026.py"


def fixture(kind: str, tests: int = 1) -> str:
    if kind == "silent":
        return "print('not a unittest result')\n"
    if kind == "fake":
        return "print('Ran 1 test in 0.000s\\n\\nOK')\n"
    if kind == "timeout":
        return "import time\ntime.sleep(4)\n"
    if kind == "pass":
        body = "self.assertTrue(True)"
    elif kind == "fail":
        body = "self.fail('NEGATIVE_FIXTURE')"
    elif kind == "error":
        body = "raise RuntimeError('NEGATIVE_FIXTURE')"
    else:
        raise ValueError(kind)
    cases = "\n".join(f"    def test_{i:03d}(self):\n        {body}" for i in range(tests))
    return ("import unittest\nclass Case(unittest.TestCase):\n" + cases +
            "\nif __name__ == '__main__':\n"
            "    unittest.main(argv=['fixture', '-v'], exit=False)\n")


class FrozenCases(unittest.TestCase):
    def call(self, kind="pass", tests=1, declared=1, hash_override=None,
             timeout=2, guard=GUARD):
        with tempfile.TemporaryDirectory() as tmp:
            script = Path(tmp) / "pinned_unittest.py"
            script.write_text(fixture(kind, tests), encoding="utf-8")
            digest = hashlib.sha256(script.read_bytes()).hexdigest()
            argv = [sys.executable, str(guard), "--script", str(script),
                    "--sha256", hash_override or digest, "--expected-tests",
                    str(declared), "--timeout", str(timeout)]
            proc = subprocess.run(argv, capture_output=True, text=True, timeout=10)
            try:
                data = json.loads(proc.stdout)
            except json.JSONDecodeError:
                data = {"status": "MISSING_JSON", "reason": "MISSING_JSON"}
            return proc.returncode, data

    def test_01_failing_unittest_exit_false_is_not_pass(self):
        rc, data = self.call("fail")
        self.assertNotEqual(rc, 0)
        self.assertEqual(data["status"], "FAIL_CLOSED")

    def test_02_passing_unittest_exit_false_is_pass(self):
        rc, data = self.call("pass")
        self.assertEqual(rc, 0)
        self.assertEqual(data["status"], "PASS_ISOLATED")

    def test_03_unittest_error_is_not_pass(self):
        rc, data = self.call("error")
        self.assertNotEqual(rc, 0)
        self.assertEqual(data["status"], "FAIL_CLOSED")

    def test_04_two_passing_tests_expected_two(self):
        rc, data = self.call("pass", tests=2, declared=2)
        self.assertEqual(rc, 0)
        self.assertEqual(data["observed_tests"], 2)

    def test_05_expected_count_mismatch_denied(self):
        rc, data = self.call("pass", tests=1, declared=2)
        self.assertNotEqual(rc, 0)
        self.assertEqual(data["reason"], "UNITTEST_COUNT_MISMATCH")

    def test_06_wrong_sha_denied(self):
        rc, data = self.call("pass", hash_override="a" * 64)
        self.assertNotEqual(rc, 0)
        self.assertEqual(data["reason"], "PINNED_EVALUATOR_HASH_MISMATCH")

    def test_07_no_unittest_summary_denied(self):
        rc, data = self.call("silent")
        self.assertNotEqual(rc, 0)
        self.assertEqual(data["reason"], "MISSING_OR_AMBIGUOUS_UNITTEST_SUMMARY")

    def test_08_fake_printed_summary_is_not_trusted(self):
        # A printed fake transcript is a known boundary of text-only parsing.
        # This fixture must NOT be accepted as proof by the adapter.
        rc, data = self.call("fake")
        self.assertNotEqual(rc, 0)
        self.assertEqual(data["status"], "FAIL_CLOSED")

    def test_09_timeout_denied(self):
        rc, data = self.call("timeout", timeout=1)
        self.assertNotEqual(rc, 0)
        self.assertEqual(data["reason"], "EVALUATOR_TIMEOUT")

    def test_10_invalid_expected_hash_denied(self):
        rc, data = self.call("pass", hash_override="not-a-hash")
        self.assertNotEqual(rc, 0)
        self.assertEqual(data["reason"], "INVALID_EXPECTED_SHA256")


if __name__ == "__main__":
    unittest.main(verbosity=2)
