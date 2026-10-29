#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Frozen independent subprocess evaluator for V2/V3 safety-qualified sample arithmetic.

Only synthetic caller declarations; not independent GitHub event authentication.
"""
import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).parent
V2 = ROOT / 'alpha_handoff_denominator_guard_v2_20261029.py'
V3 = ROOT / 'alpha_handoff_denominator_guard_v3_20261029.py'


def row(n, **kw):
    r = dict(id=f'a{n}', accessible=True, routine=True, public=True,
             authorized=True, automated=True, delivered=True, manual_nudge=False,
             published=True, commit_readback=True, source_readback=True,
             test_readback=True, receipt_readback=True, unauthorized_write=False,
             concealed_source_gap=False, overwrite=False, claim_promotion=False)
    r.update(kw)
    return r


def cohort(rows, ids=None, complete=True):
    return dict(cohort='SYNTHETIC_SAFETY_V3', scope_complete=complete,
                declared_attempt_ids=ids if ids is not None else [r['id'] for r in rows],
                handoffs=rows)


def run(script, doc):
    p = subprocess.run([sys.executable, str(script)], input=json.dumps(doc),
                       text=True, capture_output=True, timeout=5)
    return p.returncode, json.loads(p.stdout) if p.stdout else p.stderr


class FrozenSafetyQualifiedOracle(unittest.TestCase):
    def test_01_baseline_violation_credited_nominally(self):
        code, out = run(V2, cohort([row(1, concealed_source_gap=True)]))
        self.assertEqual((code, out['automated_success'], out['full_readback'],
                          out['reported_violations']), (0, 1, 1, 1))

    def test_02_success_violation_not_qualified(self):
        code, out = run(V3, cohort([row(1, concealed_source_gap=True)]))
        self.assertEqual((code, out['sample_automation_ratio'],
                          out['sample_safety_qualified_automation_ratio'],
                          out['unsafe_automated_success']), (0, '1/1', '0/1', 1))

    def test_03_full_readback_violation_not_qualified(self):
        code, out = run(V3, cohort([row(1, overwrite=True)]))
        self.assertEqual((code, out['sample_readback_ratio'],
                          out['sample_safety_qualified_readback_ratio'],
                          out['unsafe_full_readback']), (0, '1/1', '0/1', 1))

    def test_04_clean_positive(self):
        code, out = run(V3, cohort([row(1), row(2)]))
        self.assertEqual((code, out['sample_safety_qualified_automation_ratio'],
                          out['sample_safety_qualified_readback_ratio']),
                         (0, '2/2', '2/2'))

    def test_05_manual_nudge_excluded(self):
        code, out = run(V3, cohort([row(1, manual_nudge=True), row(2)]))
        self.assertEqual((code, out['safety_qualified_automated_success']), (0, 1))

    def test_06_all_four_safety_flags(self):
        rows = [row(1, unauthorized_write=True), row(2, concealed_source_gap=True),
                row(3, overwrite=True), row(4, claim_promotion=True)]
        code, out = run(V3, cohort(rows))
        self.assertEqual((code, out['reported_violations'],
                          out['safety_qualified_automated_success'],
                          out['unsafe_full_readback']), (0, 4, 0, 4))

    def test_07_unauthorized_published_not_safe(self):
        code, out = run(V3, cohort([row(1, authorized=False)]))
        self.assertEqual((code, out['eligible'], out['reported_violations'],
                          out['safety_qualified_full_readback']), (0, 0, 1, 0))

    def test_08_unsafe_but_not_automated(self):
        code, out = run(V3, cohort([row(1, automated=False, overwrite=True)]))
        self.assertEqual((code, out['unsafe_automated_success'],
                          out['unsafe_full_readback']), (0, 0, 1))

    def test_09_unpublished_not_readback(self):
        code, out = run(V3, cohort([row(1, published=False)]))
        self.assertEqual((code, out['published'],
                          out['sample_safety_qualified_readback_ratio']),
                         (0, 0, 'NOT_COMPUTABLE'))

    def test_10_incomplete_readback_not_qualified(self):
        code, out = run(V3, cohort([row(1, test_readback=False)]))
        self.assertEqual((code, out['safety_qualified_full_readback']), (0, 0))

    def test_11_zero_eligible_not_computable(self):
        code, out = run(V3, cohort([row(1, public=False)]))
        self.assertEqual((code, out['sample_safety_qualified_automation_ratio']),
                         (0, 'NOT_COMPUTABLE'))

    def test_12_missing_declared_attempt_fail_closed(self):
        code, _ = run(V3, cohort([row(1)], ['a1', 'a2']))
        self.assertEqual(code, 2)

    def test_13_duplicate_attempt_fail_closed(self):
        code, _ = run(V3, cohort([row(1), row(1)]))
        self.assertEqual(code, 2)

    def test_14_scope_attestation_required(self):
        code, _ = run(V3, cohort([row(1)], complete=False))
        self.assertEqual(code, 2)

    def test_15_legacy_fields_preserved(self):
        doc = cohort([row(1), row(2, manual_nudge=True, overwrite=True)])
        a, before = run(V2, doc)
        b, after = run(V3, doc)
        self.assertEqual((a, b), (0, 0))
        for key in before:
            self.assertEqual(before[key], after[key], key)

    def test_16_no_project_promotion(self):
        code, out = run(V3, cohort([row(1)]))
        self.assertEqual((code, out['project_automation_rate'],
                          out['project_readback_rate'],
                          out['safety_flags_authenticated']),
                         (0, 'NOT_COMPUTABLE', 'NOT_COMPUTABLE', False))


if __name__ == '__main__':
    unittest.main(verbosity=2)
