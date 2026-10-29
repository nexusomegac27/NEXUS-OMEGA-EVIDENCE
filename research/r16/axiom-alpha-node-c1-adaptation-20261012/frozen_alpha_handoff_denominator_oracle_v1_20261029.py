#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Frozen synthetic oracle for an isolated handoff-denominator candidate.

The candidate is executed in a subprocess; it cannot modify these assertions.
This oracle establishes synthetic behavior, not the real project denominator.
"""
import json
import subprocess
import sys
import unittest
from pathlib import Path

CANDIDATE = Path(__file__).with_name('alpha_handoff_denominator_guard_v1_20261029.py')


def attempt(n, **overrides):
    row = dict(id=f'a{n}', accessible=True, routine=True, public=True,
               authorized=True, completed=True, manual_nudge=False,
               published=True, commit_readback=True, source_readback=True,
               test_readback=True, receipt_readback=True,
               unauthorized_write=False, concealed_source_gap=False,
               overwrite=False, claim_promotion=False)
    row.update(overrides)
    return row


def cohort(rows, ids=None, complete=True):
    return dict(cohort='SYNTHETIC_20261029', scope_complete=complete,
                declared_attempt_ids=ids if ids is not None else [r['id'] for r in rows],
                attempts=rows)


def run(data):
    p = subprocess.run([sys.executable, str(CANDIDATE)],
                       input=json.dumps(data), text=True, capture_output=True,
                       timeout=5)
    return p.returncode, json.loads(p.stdout) if p.stdout else None


class FrozenDenominatorOracle(unittest.TestCase):
    def test_01_positive_9_of_10(self):
        rows = [attempt(i) for i in range(10)]
        rows[-1]['manual_nudge'] = True
        code, out = run(cohort(rows))
        self.assertEqual(code, 0)
        self.assertEqual((out['eligible_n'], out['automated_n'], out['automation_pct']), (10, 9, 90.0))

    def test_02_missing_declared_attempt_fail_closed(self):
        code, out = run(cohort([attempt(1)], ['a1', 'a2']))
        self.assertEqual((code, out['status']), (2, 'FAIL_CLOSED'))

    def test_03_duplicate_attempt_fail_closed(self):
        code, out = run(cohort([attempt(1), attempt(1)]))
        self.assertEqual((code, out['status']), (2, 'FAIL_CLOSED'))

    def test_04_incomplete_scope_fail_closed(self):
        code, out = run(cohort([attempt(1)], complete=False))
        self.assertEqual((code, out['status']), (2, 'FAIL_CLOSED'))

    def test_05_ineligible_private_not_denominator(self):
        code, out = run(cohort([attempt(1, public=False), attempt(2)]))
        self.assertEqual((code, out['eligible_n'], out['automated_n']), (0, 1, 1))

    def test_06_inaccessible_not_denominator(self):
        code, out = run(cohort([attempt(1, accessible=False), attempt(2)]))
        self.assertEqual((code, out['eligible_n']), (0, 1))

    def test_07_unauthorized_not_denominator(self):
        code, out = run(cohort([attempt(1, authorized=False), attempt(2)]))
        self.assertEqual((code, out['eligible_n']), (0, 1))

    def test_08_nonroutine_not_denominator(self):
        code, out = run(cohort([attempt(1, routine=False), attempt(2)]))
        self.assertEqual((code, out['eligible_n']), (0, 1))

    def test_09_failed_handoff_not_numerator(self):
        code, out = run(cohort([attempt(1, completed=False), attempt(2)]))
        self.assertEqual((code, out['automated_n'], out['eligible_n']), (0, 1, 2))

    def test_10_published_missing_test_readback(self):
        code, out = run(cohort([attempt(1, test_readback=False)]))
        self.assertEqual((code, out['published_n'], out['full_readback_n']), (0, 1, 0))

    def test_11_unpublished_excluded_readback_denominator(self):
        code, out = run(cohort([attempt(1, published=False), attempt(2)]))
        self.assertEqual((code, out['published_n'], out['full_readback_n']), (0, 1, 1))

    def test_12_violation_flag_blocks_clean_status(self):
        code, out = run(cohort([attempt(1, unauthorized_write=True)]))
        self.assertEqual((code, out['violations_n'], out['safety_status']), (0, 1, 'VIOLATION_REPORTED'))

    def test_13_concealed_source_gap_blocks_clean_status(self):
        code, out = run(cohort([attempt(1, concealed_source_gap=True)]))
        self.assertEqual((code, out['violations_n']), (0, 1))

    def test_14_invalid_boolean_fail_closed(self):
        code, out = run(cohort([attempt(1, authorized='yes')]))
        self.assertEqual((code, out['status']), (2, 'FAIL_CLOSED'))

    def test_15_zero_eligible_no_rate(self):
        code, out = run(cohort([attempt(1, accessible=False)]))
        self.assertEqual((code, out['automation_pct'], out['eligible_n']), (0, None, 0))

    def test_16_unknown_id_fail_closed(self):
        code, out = run(cohort([attempt(1)], ['a2']))
        self.assertEqual((code, out['status']), (2, 'FAIL_CLOSED'))

    def test_17_missing_field_fail_closed(self):
        row = attempt(1)
        del row['receipt_readback']
        code, out = run(cohort([row]))
        self.assertEqual((code, out['status']), (2, 'FAIL_CLOSED'))

    def test_18_no_project_wide_promotion(self):
        code, out = run(cohort([attempt(1)]))
        self.assertEqual((code, out['project_wide_claim']), (0, 'NOT_ESTABLISHED'))


if __name__ == '__main__':
    unittest.main(verbosity=2)
