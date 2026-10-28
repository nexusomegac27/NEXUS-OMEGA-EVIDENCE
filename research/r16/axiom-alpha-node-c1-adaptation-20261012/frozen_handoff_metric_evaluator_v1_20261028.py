#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Frozen subprocess oracle for bounded C1 public-handoff metric arithmetic.

Synthetic cases only. No GitHub authentication; no import of candidate internals.
"""
import copy
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest

TARGET = Path(os.environ.get('AXIOM_CANDIDATE', Path(__file__).with_name('alpha_handoff_metric_witness_v1_20261028.py')))


def event(i, **updates):
    x = dict(id=f'event-{i:02d}', channel='PUBLIC_GITHUB', routine=True,
             authorized=True, accessible=True, published=True, automatic=True,
             commit_readback=True, source_readback=True, test_readback=True,
             receipt_readback=True, unauthorized_write=False,
             hidden_source_gap=False, source_overwrite=False, claim_promotion=False)
    x.update(updates)
    return x


def fixture():
    e = [event(i) for i in range(10)]
    e[-1]['automatic'] = False
    e += [event(10, channel='PRIVATE_LOCAL'), event(11, accessible=False)]
    return dict(object='NEXUS_OMEGA_ALPHA_HANDOFF_METRIC_WITNESS_V1',
                repository='nexusomegac27/NEXUS-OMEGA-EVIDENCE',
                scope=dict(scope_id='synthetic-20261028', coverage='DECLARED_COMPLETE',
                           source_commit_sha='a' * 40, source_manifest_sha256='b' * 64),
                events=e)


def run(obj):
    raw = obj if isinstance(obj, bytes) else json.dumps(obj, ensure_ascii=False).encode()
    return subprocess.run([sys.executable, str(TARGET)], input=raw, capture_output=True, timeout=8)


class FrozenOracle(unittest.TestCase):
    def good(self, obj):
        p = run(obj)
        self.assertEqual(p.returncode, 0, p.stderr.decode(errors='replace'))
        return json.loads(p.stdout)

    def bad(self, obj, code):
        p = run(obj)
        self.assertEqual(p.returncode, 2, p.stdout.decode(errors='replace'))
        self.assertIn(code.encode(), p.stderr)

    def test_eligible_numerator_denominator(self):
        r = self.good(fixture())
        self.assertEqual((r['eligible'], r['automated'], r['excluded'], r['unknown_eligibility']), (10, 9, 2, 0))
        self.assertEqual(r['scope_automation_rate'], '9/10')
        self.assertEqual(r['scope_automation_percent'], 90.0)
        self.assertEqual(r['project_automation_rate'], 'NOT_COMPUTABLE')

    def test_readback_complete(self):
        r = self.good(fixture())
        self.assertEqual((r['publications'], r['complete_readbacks'], r['readback_rate']), (11, 11, '11/11'))
        self.assertFalse(r['api_origin_authenticated'])
        self.assertFalse(r['source_completeness_authenticated'])
        self.assertEqual(r['claim_ceiling'], 'C1_DESCRIPTIVE_ONLY')

    def test_private_auto_never_in_denominator(self):
        x = fixture(); x['events'][10]['automatic'] = True
        r = self.good(x)
        self.assertEqual((r['eligible'], r['automated']), (10, 9))

    def test_inaccessible_public_never_in_denominator(self):
        x = fixture(); x['events'][11]['automatic'] = True
        r = self.good(x)
        self.assertEqual((r['eligible'], r['automated']), (10, 9))

    def test_missing_one_readback_not_success(self):
        x = fixture(); x['events'][0]['source_readback'] = False
        r = self.good(x)
        self.assertEqual((r['publications'], r['complete_readbacks'], r['readback_rate']), (11, 10, '10/11'))

    def test_public_unknown_eligibility_not_computable(self):
        x = fixture(); x['events'][0]['authorized'] = None
        r = self.good(x)
        self.assertEqual(r['scope_automation_rate'], 'NOT_COMPUTABLE')
        self.assertEqual(r['unknown_eligibility'], 1)

    def test_partial_coverage_not_scope_rate(self):
        x = fixture(); x['scope']['coverage'] = 'PARTIAL'
        r = self.good(x)
        self.assertEqual(r['scope_automation_rate'], 'NOT_COMPUTABLE')
        self.assertEqual(r['observed_sample_rate'], '9/10')

    def test_unauthorized_publication_flag(self):
        x = fixture(); x['events'][0]['authorized'] = False
        r = self.good(x)
        self.assertEqual(r['unauthorized_publications'], 1)
        self.assertEqual(r['eligible'], 9)

    def test_explicit_safety_flags(self):
        x = fixture(); x['events'][0]['hidden_source_gap'] = True; x['events'][1]['claim_promotion'] = True
        r = self.good(x)
        self.assertEqual(r['safety_event_count'], 2)
        self.assertFalse(r['global_zero_violations_established'])

    def test_duplicate_event_id(self):
        x = fixture(); x['events'][1]['id'] = x['events'][0]['id']
        self.bad(x, 'DUPLICATE_EVENT_ID')

    def test_boolean_string_rejected(self):
        x = fixture(); x['events'][0]['published'] = 'false'
        self.bad(x, 'INVALID_EVENT_FIELD')

    def test_duplicate_json_key(self):
        self.bad(b'{"object":1,"object":2}', 'DUPLICATE_JSON_KEY')

    def test_nonfinite_json(self):
        self.bad(b'{"object":NaN}', 'NONFINITE_JSON')

    def test_oversized_input(self):
        self.bad(b' ' * 1_048_577, 'INPUT_TOO_LARGE')

    def test_unknown_channel_rejected(self):
        x = fixture(); x['events'][0]['channel'] = 'MAGIC'
        self.bad(x, 'INVALID_EVENT_FIELD')


if __name__ == '__main__':
    unittest.main()
