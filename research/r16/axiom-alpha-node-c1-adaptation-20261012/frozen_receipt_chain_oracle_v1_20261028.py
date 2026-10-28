#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Independent subprocess oracle for C1 PR/receipt chain reconciler.

Synthetic only; no candidate imports or GitHub network use.
"""
import copy
import json
import os
import subprocess
import sys
import unittest

TARGET = os.environ.get('AXIOM_CANDIDATE', 'alpha_receipt_chain_reconciler_v1_20261028.py')
A, B, C = 'a'*40, 'b'*40, 'c'*40


def fixture():
    return {'object': 'NEXUS_OMEGA_ALPHA_RECEIPT_CHAIN_V1',
            'repository': 'nexusomegac27/NEXUS-OMEGA-EVIDENCE',
            'scope': {'first_pr': 1, 'last_pr': 2, 'base_sha': A,
                      'head_sha': C, 'predecessor_receipt_id': 9},
            'records': [
                {'pr': 1, 'merged': True, 'merge_sha': B,
                 'receipt_id': 10, 'receipt_predecessor_id': 9,
                 'receipt_main_sha': B, 'receipt_parent_sha': A,
                 'compare': {'ahead': 1, 'behind': 0, 'files_added': 3,
                             'files_modified': 0, 'files_deleted': 0}},
                {'pr': 2, 'merged': True, 'merge_sha': C,
                 'receipt_id': 11, 'receipt_predecessor_id': 10,
                 'receipt_main_sha': C, 'receipt_parent_sha': B,
                 'compare': {'ahead': 1, 'behind': 0, 'files_added': 3,
                             'files_modified': 0, 'files_deleted': 0}}]}


def raw(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':')).encode()


def run(payload):
    return subprocess.run([sys.executable, TARGET], input=payload,
                          capture_output=True, timeout=8)


class ReceiptChainOracle(unittest.TestCase):
    def good(self):
        p = run(raw(fixture()))
        self.assertEqual(p.returncode, 0, p.stderr.decode())
        return json.loads(p.stdout)

    def bad(self, edit):
        x = copy.deepcopy(fixture()); edit(x)
        p = run(raw(x))
        self.assertEqual(p.returncode, 2, p.stdout.decode())
        self.assertEqual(p.stdout, b'')

    def test_positive(self):
        d = self.good()
        self.assertEqual(d['metadata_chain_match'], '2/2')
        self.assertEqual(d['project_readback_rate'], 'NOT_COMPUTABLE')
        self.assertFalse(d['api_origin_authenticated'])

    def test_wrong_merge(self):
        self.bad(lambda x: x['records'][0].update(merge_sha='d'*40))

    def test_wrong_parent(self):
        self.bad(lambda x: x['records'][1].update(receipt_parent_sha=A))

    def test_wrong_predecessor(self):
        self.bad(lambda x: x['records'][1].update(receipt_predecessor_id=9))

    def test_duplicate_receipt(self):
        self.bad(lambda x: x['records'][1].update(receipt_id=10))

    def test_missing_record(self):
        self.bad(lambda x: x['records'].pop())

    def test_wrong_pr_order(self):
        self.bad(lambda x: x['records'][1].update(pr=3))

    def test_wrong_head(self):
        self.bad(lambda x: x['scope'].update(head_sha='d'*40))

    def test_wrong_base(self):
        self.bad(lambda x: x['scope'].update(base_sha='d'*40))

    def test_compare_mismatch(self):
        self.bad(lambda x: x['records'][1]['compare'].update(files_added=2))

    def test_wrong_repo(self):
        self.bad(lambda x: x.update(repository='other/repo'))

    def test_extra_field(self):
        self.bad(lambda x: x['records'][0].update(unauthorized_override=True))

    def test_duplicate_json_key(self):
        self.assertEqual(run(b'{"object":"a","object":"b"}').returncode, 2)

    def test_nonfinite(self):
        self.assertEqual(run(raw(fixture()).replace(b'"ahead":1', b'"ahead":NaN')).returncode, 2)

    def test_invalid_utf8(self):
        self.assertEqual(run(b'\xff').returncode, 2)

    def test_oversized(self):
        self.assertEqual(run(b'x'*1_048_577).returncode, 2)


if __name__ == '__main__':
    unittest.main()
