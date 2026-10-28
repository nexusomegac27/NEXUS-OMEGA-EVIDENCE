#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Frozen independent subprocess oracle for bounded paginated handoff census.

Synthetic API-page fixtures only. Does not import candidate or authenticate GitHub.
"""
import copy
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest

TARGET = Path(os.environ.get('AXIOM_CANDIDATE', Path(__file__).with_name('alpha_handoff_page_census_witness_v2_20261028.py')))


def event(i, **changes):
    e = dict(id=f'handoff-{i:02d}', channel='PUBLIC_GITHUB', routine=True,
             authorized=True, accessible=True, published=True, automatic=True,
             commit_readback=True, source_readback=True, test_readback=True,
             receipt_readback=True, unauthorized_write=False,
             hidden_source_gap=False, source_overwrite=False, claim_promotion=False)
    e.update(changes)
    return e


def fixture():
    events = [event(i) for i in range(10)]
    events[9]['automatic'] = False
    events += [event(10, channel='PRIVATE_LOCAL'), event(11, accessible=False)]
    sha = 'a' * 40
    return dict(object='NEXUS_OMEGA_ALPHA_HANDOFF_PAGE_CENSUS_V2',
                repository='nexusomegac27/NEXUS-OMEGA-EVIDENCE',
                scope=dict(scope_id='synthetic-page-20261028', coverage='DECLARED_COMPLETE',
                           source_commit_sha=sha, source_manifest_sha256='b' * 64),
                pages=[dict(page=1, source_commit_sha=sha, reported_total=12,
                            next_page=2, events=events[:7]),
                       dict(page=2, source_commit_sha=sha, reported_total=12,
                            next_page=None, events=events[7:])])


def invoke(payload):
    raw = payload if isinstance(payload, bytes) else json.dumps(payload).encode('utf-8')
    return subprocess.run([sys.executable, str(TARGET)], input=raw,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=8)


class FrozenPageOracle(unittest.TestCase):
    def good(self, payload):
        p = invoke(payload)
        self.assertEqual(p.returncode, 0, p.stderr.decode(errors='replace'))
        return json.loads(p.stdout)

    def bad(self, payload, code):
        p = invoke(payload)
        self.assertEqual(p.returncode, 2, p.stdout.decode(errors='replace'))
        self.assertIn(code.encode(), p.stderr)

    def test_two_page_complete_scope(self):
        r = self.good(fixture())
        self.assertEqual((r['pages_observed'], r['events_observed'], r['reported_total']), (2, 12, 12))
        self.assertEqual((r['eligible'], r['automated'], r['excluded']), (10, 9, 2))
        self.assertEqual(r['scope_automation_rate'], '9/10')
        self.assertEqual(r['scope_automation_percent'], 90.0)
        self.assertEqual(r['project_automation_rate'], 'NOT_COMPUTABLE')

    def test_public_readback(self):
        r = self.good(fixture())
        self.assertEqual((r['publications'], r['complete_readbacks'], r['readback_rate']), (11, 11, '11/11'))
        self.assertFalse(r['api_origin_authenticated'])
        self.assertFalse(r['source_completeness_authenticated'])

    def test_missing_terminal_page(self):
        x = fixture(); x['pages'].pop()
        self.bad(x, 'MISSING_PAGE')

    def test_missing_event_with_forged_complete(self):
        x = fixture(); x['pages'][1]['events'].pop()
        self.bad(x, 'PAGE_TOTAL_MISMATCH')

    def test_conflicting_reported_totals(self):
        x = fixture(); x['pages'][1]['reported_total'] = 11
        self.bad(x, 'PAGE_TOTAL_MISMATCH')

    def test_all_pages_consistent_but_wrong_total(self):
        x = fixture()
        for page in x['pages']: page['reported_total'] = 11
        self.bad(x, 'PAGE_TOTAL_MISMATCH')

    def test_duplicate_event_across_pages(self):
        x = fixture(); x['pages'][1]['events'][0]['id'] = x['pages'][0]['events'][0]['id']
        self.bad(x, 'DUPLICATE_EVENT_ID')

    def test_page_order_reversed(self):
        x = fixture(); x['pages'].reverse()
        self.bad(x, 'PAGE_ORDER_INVALID')

    def test_page_index_gap(self):
        x = fixture(); x['pages'][1]['page'] = 3
        self.bad(x, 'PAGE_ORDER_INVALID')

    def test_foreign_page_commit(self):
        x = fixture(); x['pages'][1]['source_commit_sha'] = 'c' * 40
        self.bad(x, 'PAGE_SOURCE_MISMATCH')

    def test_wrong_next_link(self):
        x = fixture(); x['pages'][0]['next_page'] = 3
        self.bad(x, 'PAGE_CHAIN_INVALID')

    def test_terminal_has_successor(self):
        x = fixture(); x['pages'][1]['next_page'] = 3
        self.bad(x, 'MISSING_PAGE')

    def test_partial_page_census_not_scoped_rate(self):
        x = fixture(); x['scope']['coverage'] = 'PARTIAL'; x['pages'].pop()
        r = self.good(x)
        self.assertEqual(r['scope_automation_rate'], 'NOT_COMPUTABLE')
        self.assertEqual(r['observed_sample_rate'], '7/7')
        self.assertEqual(r['pagination_state'], 'INCOMPLETE')

    def test_unknown_public_eligibility_not_computable(self):
        x = fixture(); x['pages'][0]['events'][0]['authorized'] = None
        r = self.good(x)
        self.assertEqual(r['scope_automation_rate'], 'NOT_COMPUTABLE')
        self.assertEqual(r['unknown_eligibility'], 1)

    def test_missing_readback(self):
        x = fixture(); x['pages'][0]['events'][0]['receipt_readback'] = False
        r = self.good(x)
        self.assertEqual(r['readback_rate'], '10/11')

    def test_private_and_inaccessible_excluded(self):
        x = fixture(); x['pages'][1]['events'][-1]['automatic'] = True
        r = self.good(x)
        self.assertEqual((r['eligible'], r['automated']), (10, 9))

    def test_boolean_string_rejected(self):
        x = fixture(); x['pages'][0]['events'][0]['published'] = 'false'
        self.bad(x, 'INVALID_EVENT_FIELD')

    def test_duplicate_json_key(self):
        self.bad(b'{"object":1,"object":2}', 'DUPLICATE_JSON_KEY')

    def test_nonfinite_json(self):
        self.bad(b'{"object":NaN}', 'NONFINITE_JSON')

    def test_input_limit(self):
        self.bad(b' ' * 1_048_577, 'INPUT_TOO_LARGE')

    def test_empty_page_events(self):
        x = fixture(); x['pages'][0]['events'] = []
        self.bad(x, 'INVALID_EVENT_COUNT')


if __name__ == '__main__':
    unittest.main()
