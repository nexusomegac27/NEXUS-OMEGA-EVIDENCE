#!/usr/bin/env python3
"""Frozen, separate-process Unicode-scalar intake oracle for Issue #93 C1 snapshots.

The evaluator does not import candidate code, trust source metadata, or authenticate
GitHub actors. Freeze before writing V4; positive controls preserve valid JSON.
"""
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest

HERE = Path(__file__).resolve().parent
CANDIDATE = Path(os.environ.get('AXIOM_CANDIDATE', HERE / 'alpha_issue93_receipt_chain_unicode_scalar_v4_20261027.py'))


def snapshot():
    return {'repository': 'nexusomegac27/NEXUS-OMEGA-EVIDENCE',
            'issue_number': 93, 'anchor_predecessor_id': 100,
            'expected_tail_id': 101,
            'comments': [{'id': 101, 'actor_login': 'nexusomegac27',
                          'body': 'OBJECT=NEXUS_TEST\\nCLAIM_CEILING=C1_DESCRIPTIVE_ONLY\\n'
                                  'PREDECESSOR_ISSUE93_RECEIPT=100\\nACTUAL_MAIN_READBACK=' + 'a' * 40 + '\\n'}]}


def encoded(payload):
    return json.dumps(payload, ensure_ascii=True, separators=(',', ':')).encode('ascii')


def run(raw):
    return subprocess.run([sys.executable, str(CANDIDATE)], input=raw,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10)


class FrozenUnicodeScalarOracle(unittest.TestCase):
    def good(self, raw):
        proc = run(raw)
        self.assertEqual(proc.returncode, 0, proc.stderr.decode(errors='replace'))
        self.assertEqual(json.loads(proc.stdout)['state'], 'PASS_RECEIPT_CHAIN_STRUCTURE_C1')

    def bad(self, raw):
        proc = run(raw)
        self.assertEqual(proc.returncode, 2, proc.stderr.decode(errors='replace'))
        self.assertIn(b'FAIL_CLOSED:', proc.stderr)
        self.assertNotIn(b'PASS_RECEIPT_CHAIN_STRUCTURE_C1', proc.stdout)

    def test_01_plain_positive(self): self.good(encoded(snapshot()))
    def test_02_valid_bmp_unicode(self):
        p = snapshot(); p['metadata'] = {'label': 'Grüße'}; self.good(encoded(p))
    def test_03_valid_nonbmp_surrogate_pair_escape(self):
        p = snapshot(); p['metadata'] = {'label': '\\U0001f680'}; self.good(encoded(p))
    def test_04_valid_nonbmp_key(self):
        p = snapshot(); p['metadata'] = {'\\U0001f680': 'ok'}; self.good(encoded(p))
    def test_05_valid_nested_unicode(self):
        p = snapshot(); p['metadata'] = [{'inner': ['\\U0001f642', 'A']}]; self.good(encoded(p))
    def test_06_valid_comment_body_unicode(self):
        p = snapshot(); p['comments'][0]['body'] += 'NOTE=\\U0001f642\\n'; self.good(encoded(p))
    def test_07_reject_lone_high_value(self):
        p = snapshot(); p['metadata'] = {'label': '\\ud800'}; self.bad(encoded(p))
    def test_08_reject_lone_low_value(self):
        p = snapshot(); p['metadata'] = {'label': '\\udfff'}; self.bad(encoded(p))
    def test_09_reject_lone_high_key(self):
        p = snapshot(); p['metadata'] = {'\\ud800': 'ok'}; self.bad(encoded(p))
    def test_10_reject_lone_low_nested_key(self):
        p = snapshot(); p['metadata'] = [{'\\udc00': 1}]; self.bad(encoded(p))
    def test_11_reject_nested_array_surrogate(self):
        p = snapshot(); p['metadata'] = {'nested': [[0, '\\ud801']]}; self.bad(encoded(p))
    def test_12_reject_actor_login_surrogate(self):
        p = snapshot(); p['comments'][0]['actor_login'] += '\\ud800'; self.bad(encoded(p))
    def test_13_reject_body_surrogate(self):
        p = snapshot(); p['comments'][0]['body'] += 'NOTE=\\udfff\\n'; self.bad(encoded(p))
    def test_14_reject_mixed_valid_pair_and_lone(self):
        p = snapshot(); p['metadata'] = '\\U0001f600\\ud800'; self.bad(encoded(p))
    def test_15_duplicate_json_key_regression(self):
        raw = encoded(snapshot()).replace(b'"repository":', b'"repository":"forged/repo","repository":', 1)
        self.bad(raw)
    def test_16_nonfinite_regression(self):
        raw = encoded({'metadata': 'PLACEHOLDER', **snapshot()}).replace(b'"PLACEHOLDER"', b'NaN', 1)
        self.bad(raw)
    def test_17_broken_predecessor_regression(self):
        p = snapshot(); p['comments'][0]['body'] = p['comments'][0]['body'].replace('RECEIPT=100', 'RECEIPT=99')
        self.bad(encoded(p))
    def test_18_oversize_regression(self): self.bad(b' ' * 1048577)


if __name__ == '__main__': unittest.main()
