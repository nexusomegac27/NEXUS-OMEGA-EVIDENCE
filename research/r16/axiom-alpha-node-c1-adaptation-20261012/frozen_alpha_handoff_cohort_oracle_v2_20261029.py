#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Frozen separate subprocess evaluator for C1 cohort-denominator V2.

Synthetic fixtures are not authenticated GitHub attempts or real-world rates.
"""
import json
from pathlib import Path
import subprocess
import sys
import unittest

CANDIDATE = Path(__file__).with_name('alpha_handoff_denominator_guard_v2_20261029.py')


def row(n, **changes):
    item = dict(id=f'a{n}', accessible=True, routine=True, public=True,
                authorized=True, automated=True, delivered=True, manual_nudge=False,
                published=True, commit_readback=True, source_readback=True,
                test_readback=True, receipt_readback=True, unauthorized_write=False,
                concealed_source_gap=False, overwrite=False, claim_promotion=False)
    item.update(changes)
    return item


def cohort(rows, ids=None, complete=True):
    return dict(cohort='SYNTHETIC_20261029', scope_complete=complete,
                declared_attempt_ids=ids if ids is not None else [r['id'] for r in rows],
                handoffs=rows)


def run(doc):
    p = subprocess.run([sys.executable, str(CANDIDATE)], input=json.dumps(doc),
                       text=True, capture_output=True, timeout=5)
    return p.returncode, json.loads(p.stdout) if p.stdout else p.stderr


class FrozenCohortOracle(unittest.TestCase):
    def test_01_positive_nine_of_ten(self):
        rows = [row(i) for i in range(10)]
        rows[-1]['manual_nudge'] = True
        code, out = run(cohort(rows))
        self.assertEqual((code, out['eligible'], out['automated_success'],
                          out['sample_automation_ratio']), (0, 10, 9, '9/10'))

    def test_02_missing_declared_attempt(self):
        code, _ = run(cohort([row(1)], ['a1', 'a2']))
        self.assertEqual(code, 2)

    def test_03_duplicate_observed_attempt(self):
        code, _ = run(cohort([row(1), row(1)]))
        self.assertEqual(code, 2)

    def test_04_incomplete_scope(self):
        code, _ = run(cohort([row(1)], complete=False))
        self.assertEqual(code, 2)

    def test_05_private_excluded(self):
        code, out = run(cohort([row(1, public=False), row(2)]))
        self.assertEqual((code, out['eligible'], out['excluded']), (0, 1, 1))

    def test_06_inaccessible_excluded(self):
        code, out = run(cohort([row(1, accessible=False), row(2)]))
        self.assertEqual((code, out['eligible']), (0, 1))

    def test_07_unauthorized_excluded(self):
        code, out = run(cohort([row(1, authorized=False), row(2)]))
        self.assertEqual((code, out['eligible']), (0, 1))

    def test_08_nonroutine_excluded(self):
        code, out = run(cohort([row(1, routine=False), row(2)]))
        self.assertEqual((code, out['eligible']), (0, 1))

    def test_09_failed_delivery_not_numerator(self):
        code, out = run(cohort([row(1, delivered=False), row(2)]))
        self.assertEqual((code, out['automated_success']), (0, 1))

    def test_10_missing_test_readback(self):
        code, out = run(cohort([row(1, test_readback=False)]))
        self.assertEqual((code, out['published'], out['full_readback']), (0, 1, 0))

    def test_11_unpublished_excluded_from_readback_denominator(self):
        code, out = run(cohort([row(1, published=False), row(2)]))
        self.assertEqual((code, out['published'], out['full_readback']), (0, 1, 1))

    def test_12_unauthorized_write_reported(self):
        code, out = run(cohort([row(1, unauthorized_write=True)]))
        self.assertEqual((code, out['reported_violations'], out['safety_status']),
                         (0, 1, 'VIOLATION_REPORTED'))

    def test_13_concealed_gap_reported(self):
        code, out = run(cohort([row(1, concealed_source_gap=True)]))
        self.assertEqual((code, out['reported_violations']), (0, 1))

    def test_14_invalid_boolean(self):
        code, _ = run(cohort([row(1, authorized='yes')]))
        self.assertEqual(code, 2)

    def test_15_zero_eligible(self):
        code, out = run(cohort([row(1, accessible=False)]))
        self.assertEqual((code, out['sample_automation_ratio']), (0, 'NOT_COMPUTABLE'))

    def test_16_unknown_declared_id(self):
        code, _ = run(cohort([row(1)], ['a2']))
        self.assertEqual(code, 2)

    def test_17_missing_field(self):
        item = row(1)
        del item['receipt_readback']
        code, _ = run(cohort([item]))
        self.assertEqual(code, 2)

    def test_18_project_wide_not_promoted(self):
        code, out = run(cohort([row(1)]))
        self.assertEqual((code, out['project_automation_rate'],
                          out['independent_github_authentication']),
                         (0, 'NOT_COMPUTABLE', False))

    def test_19_duplicate_json_key(self):
        p = subprocess.run([sys.executable, str(CANDIDATE)],
                           input='{"cohort":"a","cohort":"b"}', text=True,
                           capture_output=True, timeout=5)
        self.assertEqual(p.returncode, 2)

    def test_20_unregistered_publication(self):
        code, out = run(cohort([row(1, authorized=False)]))
        self.assertEqual((code, out['reported_violations']), (0, 1))


if __name__ == '__main__':
    unittest.main(verbosity=2)
