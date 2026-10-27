#!/usr/bin/env python3
"""Independent, separate-process C1 census input-budget oracle.

Freeze before publishing the candidate. This suite does not authenticate
GitHub events or establish the project-wide denominator. It only verifies
that a caller-supplied JSON sample cannot exceed the fixed input budget.
"""
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest

HERE = Path(__file__).resolve().parent
CANDIDATE = Path(os.environ.get('AXIOM_CANDIDATE', HERE / 'alpha_handoff_coverage_census_input_budget_v4_20261027.py'))
MAX_BYTES = 4 * 1024 * 1024


def record(ident='a', **kw):
    r = {'id': ident, 'scope': 'PUBLIC', 'accessible': True,
         'authorized': True, 'routine': True, 'automated': True,
         'outcome': 'SUCCESS', 'source_readback': 'MATCH',
         'publication_readback': 'MATCH'}
    r.update(kw)
    return r


def encoded(records):
    return json.dumps({'schema_version': 2, 'records': records},
                      separators=(',', ':'), ensure_ascii=True).encode('ascii')


def run(raw):
    return subprocess.run([sys.executable, str(CANDIDATE)], input=raw,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=15)


class FrozenBudgetOracle(unittest.TestCase):
    def good(self, raw, expected_num=None, expected_den=None):
        p = run(raw)
        self.assertEqual(p.returncode, 0, p.stderr.decode(errors='replace'))
        result = json.loads(p.stdout)
        self.assertEqual(result['project_rate'], 'NOT_COMPUTABLE')
        self.assertEqual(result['evidence_class'], 'UNVERIFIED_SAMPLE_ONLY')
        self.assertEqual(result['claim_ceiling'], 'C1_DESCRIPTIVE_ONLY')
        if expected_num is not None:
            self.assertEqual(result['automated_numerator'], expected_num)
        if expected_den is not None:
            self.assertEqual(result['eligible_denominator'], expected_den)
        return result

    def bad(self, raw):
        p = run(raw)
        self.assertEqual(p.returncode, 2, (p.returncode, p.stderr[:300]))
        self.assertIn(b'FAIL_CLOSED:', p.stderr)
        self.assertNotIn(b'"project_rate"', p.stdout)

    def test_01_one_success(self): self.good(encoded([record()]), 1, 1)
    def test_02_empty_sample(self): self.good(encoded([]), 0, 0)
    def test_03_private_excluded(self):
        result = self.good(encoded([record(scope='PRIVATE', accessible=False)]), 0, 0)
        self.assertEqual(result['excluded_count'], 1)
    def test_04_unknown_withheld(self):
        result = self.good(encoded([record(accessible=None)]), 0, 0)
        self.assertEqual(result['sample_rate'], 'WITHHELD_UNKNOWN_ELIGIBILITY')
    def test_05_mixed_counts(self):
        r = self.good(encoded([record('a'), record('b', automated=False),
                               record('c', scope='LOCAL', accessible=False)]), 1, 2)
        self.assertEqual(r['excluded_count'], 1)
    def test_06_exact_budget_positive(self):
        raw = encoded([record()])
        self.good(raw + b' ' * (MAX_BYTES - len(raw)), 1, 1)
    def test_07_budget_plus_one_valid_json_rejected(self):
        raw = encoded([record()])
        self.bad(raw + b' ' * (MAX_BYTES + 1 - len(raw)))
    def test_08_budget_plus_one_invalid_json_rejected(self):
        self.bad(b'{' + b' ' * MAX_BYTES)
    def test_09_duplicate_key_regression(self):
        self.bad(encoded([]).replace(b'"schema_version":', b'"schema_version":2,"schema_version":', 1))
    def test_10_nonfinite_regression(self):
        self.bad(encoded([]).replace(b'"schema_version":2', b'"schema_version":NaN', 1))
    def test_11_bad_utf8_regression(self): self.bad(b'\xff')
    def test_12_malformed_json_regression(self): self.bad(b'{')
    def test_13_duplicate_id_regression(self): self.bad(encoded([record('a'), record('a')]))
    def test_14_private_access_conflict(self):
        self.bad(encoded([record(scope='PRIVATE', accessible=True)]))
    def test_15_deep_json_fails_closed(self):
        self.bad(b'{"schema_version":2,"records":' + b'[' * 10000 + b'0' + b']' * 10000 + b'}')
    def test_16_eligible_pending_not_numerator(self):
        self.good(encoded([record(outcome='PENDING')]), 0, 1)


if __name__ == '__main__': unittest.main()
