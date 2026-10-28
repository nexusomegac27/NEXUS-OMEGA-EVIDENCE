#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Frozen black-box oracle: variable additive-file counts, fail-closed inventory.

No import of candidate; synthetic fixtures only. Set AXIOM_CANDIDATE to target.
"""
import copy
import json
import os
import subprocess
import sys
import unittest

TARGET = os.environ.get('AXIOM_CANDIDATE', 'alpha_receipt_chain_reconciler_v2_20261028.py')
A, B, C = 'a'*40, 'b'*40, 'c'*40
ROOT = 'research/r16/axiom-alpha-node-c1-adaptation-20261012/'


def fixture():
    def record(pr, merge, parent, rid, prior, n):
        return {'pr': pr, 'merged': True, 'merge_sha': merge,
                'receipt_id': rid, 'receipt_predecessor_id': prior,
                'receipt_main_sha': merge, 'receipt_parent_sha': parent,
                'compare': {'ahead': 1, 'behind': 0, 'files_added': n,
                            'files_modified': 0, 'files_deleted': 0},
                'files': [{'path': ROOT + f'pr{pr}_artifact{i}.py', 'status': 'added'}
                          for i in range(n)]}
    return {'object': 'NEXUS_OMEGA_ALPHA_RECEIPT_CHAIN_V2',
            'repository': 'nexusomegac27/NEXUS-OMEGA-EVIDENCE',
            'scope': {'first_pr': 172, 'last_pr': 173, 'base_sha': A,
                      'head_sha': C, 'predecessor_receipt_id': 9},
            'records': [record(172, B, A, 10, 9, 3),
                        record(173, C, B, 11, 10, 4)]}


def raw(x):
    return json.dumps(x, sort_keys=True, separators=(',', ':')).encode()


def run(payload):
    return subprocess.run([sys.executable, TARGET], input=payload,
                          capture_output=True, timeout=8)


class InventoryOracle(unittest.TestCase):
    def good(self, x=None):
        p = run(raw(x if x is not None else fixture()))
        self.assertEqual(p.returncode, 0, p.stderr.decode())
        return json.loads(p.stdout)

    def bad(self, edit):
        x = fixture(); edit(x)
        p = run(raw(x))
        self.assertEqual(p.returncode, 2, p.stdout.decode())
        self.assertEqual(p.stdout, b'')

    def test_positive_variable_3_and_4(self):
        d = self.good()
        self.assertEqual(d['metadata_chain_match'], '2/2')
        self.assertEqual(d['files_checked'], 7)
        self.assertFalse(d['api_origin_authenticated'])
        self.assertEqual(d['project_readback_rate'], 'NOT_COMPUTABLE')

    def test_positive_one_four(self):
        x = fixture(); x['records'] = x['records'][1:]
        x['scope'].update(first_pr=173, base_sha=B, predecessor_receipt_id=10)
        self.assertEqual(self.good(x)['files_checked'], 4)

    def test_missing_file_in_inventory(self):
        self.bad(lambda x: x['records'][1]['files'].pop())

    def test_inflated_compare(self):
        self.bad(lambda x: x['records'][1]['compare'].update(files_added=5))

    def test_duplicate_file_path(self):
        self.bad(lambda x: x['records'][1]['files'][1].update(path=x['records'][1]['files'][0]['path']))

    def test_modified_file_status(self):
        self.bad(lambda x: x['records'][1]['files'][0].update(status='modified'))

    def test_path_escape(self):
        self.bad(lambda x: x['records'][1]['files'][0].update(path=ROOT+'../GOVERNANCE.md'))

    def test_path_other_root(self):
        self.bad(lambda x: x['records'][1]['files'][0].update(path='scripts/evil.py'))

    def test_broken_receipt_predecessor(self):
        self.bad(lambda x: x['records'][1].update(receipt_predecessor_id=9))

    def test_broken_main_parent(self):
        self.bad(lambda x: x['records'][1].update(receipt_parent_sha=A))

    def test_missing_pr(self):
        self.bad(lambda x: x['records'].pop())

    def test_duplicate_json_key(self):
        self.assertEqual(run(b'{"object":"x","object":"y"}').returncode, 2)

    def test_nonfinite_json(self):
        self.assertEqual(run(raw(fixture()).replace(b'"ahead":1', b'"ahead":NaN')).returncode, 2)

    def test_invalid_utf8(self):
        self.assertEqual(run(b'\xff').returncode, 2)

    def test_oversize(self):
        self.assertEqual(run(b'x'*1_048_577).returncode, 2)

    def test_boolean_count(self):
        self.bad(lambda x: x['records'][1]['compare'].update(files_added=True))


if __name__ == '__main__':
    unittest.main()
