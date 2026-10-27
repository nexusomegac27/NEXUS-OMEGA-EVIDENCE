#!/usr/bin/env python3
"""Independent black-box oracle for bounded strict JSON receipt intake (C1 only).

Freeze this evaluator before writing the V3 candidate. It invokes the selected
candidate via a separate process and never imports its implementation. It
checks only JSON intake and the existing structural result, not GitHub identity,
source completeness, scientific truth, or productive integration.
"""
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest

HERE = Path(__file__).resolve().parent
CANDIDATE = Path(os.environ.get('AXIOM_CANDIDATE', HERE / 'alpha_issue93_receipt_chain_json_rfc8259_v3_20261027.py'))


def comment(cid, predecessor):
    return {'id': cid, 'actor_login': 'nexusomegac27',
            'body': ('OBJECT=NEXUS_TEST_%d\nCLAIM_CEILING=C1_DESCRIPTIVE_ONLY\n'
                     'PREDECESSOR_ISSUE93_RECEIPT=%d\nACTUAL_MAIN_READBACK=%s\n') %
                    (cid, predecessor, 'a' * 40)}


def sample():
    return {'repository': 'nexusomegac27/NEXUS-OMEGA-EVIDENCE',
            'issue_number': 93, 'anchor_predecessor_id': 100,
            'expected_tail_id': 102, 'comments': [comment(101, 100), comment(102, 101)]}


def serialized(metadata=None):
    payload = sample()
    if metadata is not None:
        payload['metadata'] = metadata
    return json.dumps(payload, allow_nan=False, separators=(',', ':')).encode('utf-8')


def run(raw):
    return subprocess.run([sys.executable, str(CANDIDATE)], input=raw,
                          capture_output=True, timeout=10)


class FrozenRFC8259Oracle(unittest.TestCase):
    def good(self, raw):
        proc = run(raw)
        self.assertEqual(proc.returncode, 0, proc.stderr.decode(errors='replace'))
        self.assertEqual(json.loads(proc.stdout)['state'], 'PASS_RECEIPT_CHAIN_STRUCTURE_C1')

    def bad(self, raw):
        proc = run(raw)
        self.assertEqual(proc.returncode, 2, proc.stderr.decode(errors='replace'))
        self.assertIn(b'FAIL_CLOSED:', proc.stderr)
        self.assertNotIn(b'PASS_RECEIPT_CHAIN_STRUCTURE_C1', proc.stdout)

    def with_literal(self, literal, nested=False):
        # Raw insertion avoids json.dumps sanitizing the deliberately invalid JSON constants.
        raw = serialized({'slot': 'PLACEHOLDER'} if not nested else {'inner': {'slot': 'PLACEHOLDER'}})
        return raw.replace(b'"PLACEHOLDER"', literal.encode('ascii'), 1)

    def test_01_clean_two_comments(self): self.good(serialized())
    def test_02_clean_one_comment(self):
        p = sample(); p['comments'] = p['comments'][:1]; p['expected_tail_id'] = 101
        self.good(json.dumps(p).encode())
    def test_03_clean_pretty(self): self.good(json.dumps(sample(), indent=2).encode())
    def test_04_clean_finite_float(self): self.good(serialized({'v': 1.25}))
    def test_05_clean_finite_negative_float_nested(self): self.good(serialized({'inner': {'v': -0.125}}))
    def test_06_reject_nan_top(self): self.bad(self.with_literal('NaN'))
    def test_07_reject_positive_infinity_top(self): self.bad(self.with_literal('Infinity'))
    def test_08_reject_negative_infinity_top(self): self.bad(self.with_literal('-Infinity'))
    def test_09_reject_nan_nested(self): self.bad(self.with_literal('NaN', nested=True))
    def test_10_reject_positive_infinity_nested(self): self.bad(self.with_literal('Infinity', nested=True))
    def test_11_reject_negative_infinity_nested(self): self.bad(self.with_literal('-Infinity', nested=True))
    def test_12_reject_overflow_exponent_top(self): self.bad(self.with_literal('1e999'))
    def test_13_reject_negative_overflow_nested(self): self.bad(self.with_literal('-1e999', nested=True))
    def test_14_reject_duplicate_key_regression(self):
        raw = serialized().replace(b'"repository":', b'"repository":"forged/repo","repository":', 1)
        self.bad(raw)
    def test_15_reject_broken_predecessor_regression(self):
        p = sample(); p['comments'][1] = comment(102, 100)
        self.bad(json.dumps(p).encode())
    def test_16_reject_malformed_json(self): self.bad(b'{"repository":')
    def test_17_reject_oversized_input(self): self.bad(b' ' * 1048577)
    def test_18_reject_excessive_nesting_fail_closed(self):
        raw = serialized({'slot': 'PLACEHOLDER'})
        raw = raw.replace(b'"PLACEHOLDER"', b'[' * 10000 + b'0' + b']' * 10000, 1)
        self.bad(raw)
    def test_19_clean_surrounding_whitespace(self): self.good(b' \n' + serialized() + b'\t')
    def test_20_clean_finite_small_exponent(self): self.good(self.with_literal('1e-300'))


if __name__ == '__main__': unittest.main()
