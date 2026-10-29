#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Frozen black-box oracle for C1 handoff-accounting research candidate.
Only synthetic fixtures. Candidate imported nowhere; subprocess-only evaluation.
"""
import json
import os
import subprocess
import sys
import unittest

CANDIDATE = os.environ.get('AXIOM_CANDIDATE', 'alpha_handoff_denominator_guard_v1_20261029.py')


def row(i, **changes):
    item = dict(id=i, accessible=True, routine=True, public=True,
                authorized=True, automated=True, delivered=True,
                published=True, commit_readback=True, source_readback=True,
                test_readback=True, receipt_readback=True)
    item.update(changes)
    return item


def execute(rows):
    return subprocess.run([sys.executable, CANDIDATE], input=json.dumps({'handoffs': rows}),
                          text=True, capture_output=True, timeout=4)


class FrozenAccountingOracle(unittest.TestCase):
    def test_success_and_failure_in_denominator(self):
        p = execute([row('A'), row('B', automated=False), row('C', delivered=False)])
        self.assertEqual(p.returncode, 0, p.stderr)
        x = json.loads(p.stdout)
        self.assertEqual((x['eligible'], x['automated_success']), (3, 1))
        self.assertEqual(x['sample_automation_ratio'], '1/3')
        self.assertEqual((x['published'], x['full_readback']), (3, 3))
        self.assertEqual(x['project_automation_rate'], 'NOT_COMPUTABLE')
        self.assertEqual(x['project_readback_rate'], 'NOT_COMPUTABLE')

    def test_unavailable_excluded(self):
        p = execute([row('A'), row('PRIVATE', accessible=False, automated=True)])
        self.assertEqual(p.returncode, 0, p.stderr)
        x = json.loads(p.stdout)
        self.assertEqual((x['eligible'], x['excluded'], x['automated_success']), (1, 1, 1))

    def test_nonroutine_excluded(self):
        p = execute([row('A'), row('ONEOFF', routine=False)])
        self.assertEqual(json.loads(p.stdout)['eligible'], 1)

    def test_unauthorized_excluded(self):
        p = execute([row('A'), row('UNAUTH', authorized=False)])
        self.assertEqual(json.loads(p.stdout)['eligible'], 1)

    def test_nonpublic_excluded(self):
        p = execute([row('A'), row('PRIVATE', public=False)])
        self.assertEqual(json.loads(p.stdout)['eligible'], 1)

    def test_partial_readback_not_full(self):
        p = execute([row('A'), row('B', receipt_readback=False)])
        x = json.loads(p.stdout)
        self.assertEqual((x['published'], x['full_readback']), (2, 1))
        self.assertEqual(x['sample_readback_ratio'], '1/2')

    def test_no_eligible_is_not_computable(self):
        p = execute([row('PRIVATE', accessible=False)])
        self.assertEqual(json.loads(p.stdout)['sample_automation_ratio'], 'NOT_COMPUTABLE')

    def test_duplicate_ids_fail_closed(self):
        self.assertNotEqual(execute([row('A'), row('A')]).returncode, 0)

    def test_boolean_strings_fail_closed(self):
        self.assertNotEqual(execute([row('A', automated='true')]).returncode, 0)

    def test_missing_required_field_fail_closed(self):
        r = row('A'); del r['authorized']
        self.assertNotEqual(execute([r]).returncode, 0)

    def test_unknown_field_fail_closed(self):
        self.assertNotEqual(execute([row('A', imaginary=True)]).returncode, 0)

    def test_missing_document_key_fail_closed(self):
        p = subprocess.run([sys.executable, CANDIDATE], input='{}', text=True, capture_output=True)
        self.assertNotEqual(p.returncode, 0)

    def test_duplicate_json_keys_fail_closed(self):
        p = subprocess.run([sys.executable, CANDIDATE], input='{"handoffs":[],"handoffs":[]}', text=True, capture_output=True)
        self.assertNotEqual(p.returncode, 0)

    def test_invalid_json_fail_closed(self):
        p = subprocess.run([sys.executable, CANDIDATE], input='not-json', text=True, capture_output=True)
        self.assertNotEqual(p.returncode, 0)

    def test_empty_inventory_not_project_computable(self):
        p = execute([])
        x = json.loads(p.stdout)
        self.assertEqual(x['sample_automation_ratio'], 'NOT_COMPUTABLE')
        self.assertEqual(x['project_automation_rate'], 'NOT_COMPUTABLE')

    def test_reported_100_percent_is_not_project_100_percent(self):
        p = execute([row('A')])
        x = json.loads(p.stdout)
        self.assertEqual(x['sample_automation_ratio'], '1/1')
        self.assertEqual(x['sample_readback_ratio'], '1/1')
        self.assertEqual(x['project_automation_rate'], 'NOT_COMPUTABLE')

    def test_ineligible_publication_still_requires_readback(self):
        p = execute([row('A'), row('X', authorized=False, receipt_readback=False)])
        x = json.loads(p.stdout)
        self.assertEqual((x['published'], x['full_readback']), (2, 1))
        self.assertEqual(x['declared_unauthorized_publications'], 1)


if __name__ == '__main__':
    unittest.main()
