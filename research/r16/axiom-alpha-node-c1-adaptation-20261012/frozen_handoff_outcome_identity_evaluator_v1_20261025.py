#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Independent frozen C1 evaluator for post-reducer outcome-ID consistency.

Synthetic outputs only. Tests do not establish a real handoff census, source
attestation, authenticated actor, or productive integration. Freeze before candidate.
"""
import copy
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
TARGET = Path(os.environ.get('HANDOFF_CANDIDATE', str(HERE / 'alpha_handoff_outcome_identity_guard_v2_20261025.py')))
spec = importlib.util.spec_from_file_location('candidate_under_test', TARGET)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def fixture(statuses, ids=None):
    if ids is None:
        ids = ['h' + str(i) for i in range(len(statuses))]
    denominator = sum(s in ('ELIGIBLE_AUTOMATED', 'ELIGIBLE_FAILED') for s in statuses)
    numerator = statuses.count('ELIGIBLE_AUTOMATED')
    return dict(
        claim_ceiling='C1_DESCRIPTIVE_ONLY',
        measurement_scope='CALLER_ASSERTED_SAMPLE_ONLY_NOT_INDEPENDENTLY_AUDITED',
        project_handoff_automation_rate='NOT_COMPUTABLE_NO_INDEPENDENT_COMPLETE_CENSUS',
        sample_eligible_denominator=denominator,
        sample_automated_numerator=numerator,
        sample_rate_percent=round(100 * numerator / denominator, 2) if denominator else None,
        unknown_or_unverified=statuses.count('UNKNOWN'),
        excluded_out_of_scope=statuses.count('EXCLUDED'),
        outcomes=[dict(index=i, id=ids[i], status=status, reason='SYNTHETIC')
                  for i, status in enumerate(statuses)],
    )


class FrozenOracle(unittest.TestCase):
    def test_01_single_eligible_valid(self):
        for status, expected in [('ELIGIBLE_AUTOMATED', 100.0), ('ELIGIBLE_FAILED', 0.0)]:
            self.assertEqual(module.guard_reducer_result(fixture([status]))['sample_rate_percent'], expected)

    def test_02_mixed_valid(self):
        sample = fixture(['ELIGIBLE_AUTOMATED', 'ELIGIBLE_FAILED', 'EXCLUDED'])
        self.assertEqual(module.guard_reducer_result(sample)['sample_rate_percent'], 50.0)

    def test_03_unknown_withholds(self):
        sample = fixture(['ELIGIBLE_AUTOMATED', 'UNKNOWN'])
        result = module.guard_reducer_result(sample)
        self.assertIsNone(result['sample_rate_percent'])
        self.assertEqual(result['sample_rate_status'], 'WITHHELD_UNRESOLVED_ROWS')

    def test_04_no_denominator(self):
        for statuses in [[], ['EXCLUDED'], ['UNKNOWN']]:
            self.assertIsNone(module.guard_reducer_result(fixture(statuses))['sample_rate_percent'])

    def test_05_duplicate_eligible_identity_rejected(self):
        for statuses in [
            ['ELIGIBLE_AUTOMATED', 'ELIGIBLE_AUTOMATED'],
            ['ELIGIBLE_AUTOMATED', 'ELIGIBLE_FAILED'],
            ['ELIGIBLE_FAILED', 'ELIGIBLE_FAILED'],
        ]:
            with self.assertRaisesRegex(ValueError, 'DUPLICATE_ID_NON_UNKNOWN_OUTCOME'):
                module.guard_reducer_result(fixture(statuses, ['same', 'same']))

    def test_06_duplicate_across_exclusion_rejected(self):
        for statuses in [
            ['ELIGIBLE_AUTOMATED', 'EXCLUDED'],
            ['EXCLUDED', 'ELIGIBLE_FAILED'],
            ['EXCLUDED', 'EXCLUDED'],
            ['UNKNOWN', 'ELIGIBLE_AUTOMATED'],
        ]:
            with self.assertRaisesRegex(ValueError, 'DUPLICATE_ID_NON_UNKNOWN_OUTCOME'):
                module.guard_reducer_result(fixture(statuses, ['same', 'same']))

    def test_07_invalid_eligible_identity_rejected(self):
        for identifier in [None, 4, True, '', 'white space', 'bad/segment', 'é', 'x'*129]:
            with self.subTest(identifier=repr(identifier)):
                with self.assertRaisesRegex(ValueError, 'NON_UNKNOWN_OUTCOME_ID_INVALID'):
                    module.guard_reducer_result(fixture(['ELIGIBLE_AUTOMATED'], [identifier]))

    def test_08_invalid_excluded_identity_rejected(self):
        for identifier in [None, [], {}, 'a\nb']:
            with self.subTest(identifier=repr(identifier)):
                with self.assertRaisesRegex(ValueError, 'NON_UNKNOWN_OUTCOME_ID_INVALID'):
                    module.guard_reducer_result(fixture(['EXCLUDED'], [identifier]))

    def test_09_duplicate_unknown_allowed_but_withheld(self):
        sample = fixture(['UNKNOWN', 'UNKNOWN'], ['same', 'same'])
        result = module.guard_reducer_result(sample)
        self.assertIsNone(result['sample_rate_percent'])
        self.assertEqual(result['sample_rate_status'], 'WITHHELD_UNRESOLVED_ROWS')

    def test_10_unknown_invalid_id_allowed_but_withheld(self):
        sample = fixture(['UNKNOWN', 'ELIGIBLE_FAILED'], [None, 'valid'])
        self.assertIsNone(module.guard_reducer_result(sample)['sample_rate_percent'])

    def test_11_forged_count_rejected(self):
        sample = fixture(['ELIGIBLE_AUTOMATED'])
        sample['sample_eligible_denominator'] = 0
        with self.assertRaisesRegex(ValueError, 'REDUCER_COUNT_MISMATCH'):
            module.guard_reducer_result(sample)

    def test_12_forged_claim_rejected(self):
        sample = fixture(['ELIGIBLE_AUTOMATED'])
        sample['project_handoff_automation_rate'] = 100
        with self.assertRaisesRegex(ValueError, 'UNAUTHORIZED_PROJECT_RATE'):
            module.guard_reducer_result(sample)

    def test_13_nonmutation_and_determinism(self):
        sample = fixture(['ELIGIBLE_AUTOMATED', 'ELIGIBLE_FAILED'])
        original = copy.deepcopy(sample)
        self.assertEqual(module.guard_reducer_result(sample), module.guard_reducer_result(sample))
        self.assertEqual(sample, original)

    def test_14_cli_forged_duplicate_fails_closed(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / 'input.json'
            p.write_text(json.dumps(fixture(['ELIGIBLE_AUTOMATED', 'ELIGIBLE_AUTOMATED'], ['same', 'same'])), encoding='utf-8')
            cp = subprocess.run([sys.executable, str(TARGET), str(p)], text=True, capture_output=True)
            self.assertNotEqual(cp.returncode, 0)
            self.assertEqual(cp.stdout, '')

    def test_15_cli_valid(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / 'input.json'
            p.write_text(json.dumps(fixture(['ELIGIBLE_AUTOMATED'])), encoding='utf-8')
            cp = subprocess.run([sys.executable, str(TARGET), str(p)], text=True, capture_output=True)
            self.assertEqual(cp.returncode, 0, cp.stderr)
            self.assertEqual(json.loads(cp.stdout)['sample_rate_percent'], 100.0)

    def test_16_fuzz_duplicate_eligible_fail_closed(self):
        for n in range(2, 502):
            statuses = ['ELIGIBLE_AUTOMATED'] * n
            ids = ['h' + str(i) for i in range(n)]
            ids[-1] = ids[0]
            with self.assertRaisesRegex(ValueError, 'DUPLICATE_ID_NON_UNKNOWN_OUTCOME'):
                module.guard_reducer_result(fixture(statuses, ids))


if __name__ == '__main__':
    unittest.main(verbosity=2)
