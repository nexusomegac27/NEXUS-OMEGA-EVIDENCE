#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Black-box, independent synthetic evaluator for actual unittest execution.
Frozen before candidate v2. Never imports candidate implementation.
"""
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

GUARD = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else None


def source(kind):
    if kind == 'fake_dead_1':
        return "import unittest\nif False:\n    unittest.main(exit=False)\nprint('Ran 1 test in 0.000s\\n\\nOK')\n"
    if kind == 'fake_dead_2':
        return "import unittest\nif 0:\n    unittest.main(exit=False)\nprint('Ran 2 tests in 0.001s\\n\\nOK')\n"
    if kind == 'fake_unguarded':
        return "print('Ran 1 test in 0.000s\\n\\nOK')\n"
    if kind == 'passing':
        return "import unittest\nclass C(unittest.TestCase):\n    def test_ok(self):\n        self.assertTrue(True)\nif __name__ == '__main__':\n    unittest.main(exit=False)\n"
    if kind == 'failing':
        return "import unittest\nclass C(unittest.TestCase):\n    def test_bad(self):\n        self.fail('NEGATIVE')\nif __name__ == '__main__':\n    unittest.main(exit=False)\n"
    if kind == 'error':
        return "import unittest\nclass C(unittest.TestCase):\n    def test_error(self):\n        raise RuntimeError('NEGATIVE')\nif __name__ == '__main__':\n    unittest.main(exit=False)\n"
    if kind == 'passing_2':
        return "import unittest\nclass C(unittest.TestCase):\n    def test_one(self):\n        self.assertTrue(True)\n    def test_two(self):\n        self.assertEqual(2,2)\nif __name__ == '__main__':\n    unittest.main(exit=False)\n"
    raise ValueError(kind)


def call(kind, expected=1):
    with tempfile.TemporaryDirectory() as td:
        p=Path(td)/'pinned.py'; p.write_text(source(kind),encoding='utf-8')
        digest=hashlib.sha256(p.read_bytes()).hexdigest()
        proc=subprocess.run([sys.executable,str(GUARD),'--script',str(p),'--sha256',digest,'--expected-tests',str(expected)],capture_output=True,text=True,timeout=12)
        try: o=json.loads(proc.stdout)
        except Exception: o={'status':'NO_JSON','reason':proc.stdout[:200]}
        return proc.returncode,o


class FrozenCases(unittest.TestCase):
    def test_01_dead_ast_one_must_fail(self):
        rc,o=call('fake_dead_1');self.assertNotEqual(rc,0);self.assertEqual(o['status'],'FAIL_CLOSED')
    def test_02_dead_ast_two_must_fail(self):
        rc,o=call('fake_dead_2',2);self.assertNotEqual(rc,0);self.assertEqual(o['status'],'FAIL_CLOSED')
    def test_03_no_unittest_call_must_fail(self):
        rc,o=call('fake_unguarded');self.assertNotEqual(rc,0)
    def test_04_true_one_pass(self):
        rc,o=call('passing');self.assertEqual(rc,0);self.assertEqual(o['status'],'PASS_ISOLATED')
    def test_05_true_two_pass(self):
        rc,o=call('passing_2',2);self.assertEqual(rc,0);self.assertEqual(o['status'],'PASS_ISOLATED')
    def test_06_failed_test_exit_false_must_fail(self):
        rc,o=call('failing');self.assertNotEqual(rc,0);self.assertEqual(o['status'],'FAIL_CLOSED')
    def test_07_errored_test_exit_false_must_fail(self):
        rc,o=call('error');self.assertNotEqual(rc,0);self.assertEqual(o['status'],'FAIL_CLOSED')
    def test_08_wrong_expected_count_must_fail(self):
        rc,o=call('passing',2);self.assertNotEqual(rc,0);self.assertEqual(o['status'],'FAIL_CLOSED')


if __name__=='__main__':
    if GUARD is None: raise SystemExit('usage: evaluator.py GUARD_PATH')
    unittest.main(argv=[sys.argv[0]],verbosity=2)
