#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Frozen independent black-box oracle for chronological receipt IDs.

Only evaluates the proposed isolated receipt-order guard, not GitHub actor identity.
The fixture and expected result are implemented separately from the candidate.
"""
import copy
import json
import os
import subprocess
import sys
import unittest

TARGET = os.environ.get('AXIOM_RECEIPT_ORDER_CANDIDATE', 'alpha_receipt_order_guard_v1_20261028.py')


def fixture(n=3):
    previous = 100
    records = []
    for i in range(n):
        current = 110 + i * 10
        records.append({'receipt_id': current, 'receipt_predecessor_id': previous})
        previous = current
    return {'object': 'NEXUS_OMEGA_ALPHA_RECEIPT_ORDER_GUARD_V1',
            'scope': {'predecessor_receipt_id': 100}, 'records': records}


def run(payload):
    return subprocess.run([sys.executable, TARGET], input=payload,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          timeout=8)


def encode(obj):
    return json.dumps(obj, separators=(',', ':'), sort_keys=True).encode('utf-8')


class FrozenReceiptOrderOracle(unittest.TestCase):
    def accepted(self, obj):
        proc = run(encode(obj))
        self.assertEqual(proc.returncode, 0, proc.stderr.decode())
        out = json.loads(proc.stdout)
        self.assertEqual(out['records_checked'], len(obj['records']))
        self.assertEqual(out['receipt_order_guard'], 'PASS_CALLER_SUPPLIED_METADATA_ONLY')
        self.assertIs(out['api_origin_authenticated'], False)
        self.assertEqual(out['project_automation_rate'], 'NOT_COMPUTABLE')
        self.assertEqual(out['project_readback_rate'], 'NOT_COMPUTABLE')

    def rejected(self, obj, marker):
        proc = run(encode(obj))
        self.assertEqual(proc.returncode, 2, proc.stdout.decode())
        self.assertEqual(proc.stdout, b'')
        self.assertIn(marker.encode(), proc.stderr)

    def test_valid_single(self): self.accepted(fixture(1))
    def test_valid_three(self): self.accepted(fixture(3))
    def test_valid_hundred(self): self.accepted(fixture(100))
    def test_self_reference_initial(self):
        obj = fixture(); obj['records'][0]['receipt_id'] = 100
        obj['records'][1]['receipt_predecessor_id'] = 100
        self.rejected(obj, 'RECEIPT_NOT_CHRONOLOGICAL')
    def test_backward_initial(self):
        obj = fixture(); obj['records'][0]['receipt_id'] = 99
        obj['records'][1]['receipt_predecessor_id'] = 99
        self.rejected(obj, 'RECEIPT_NOT_CHRONOLOGICAL')
    def test_self_reference_later(self):
        obj = fixture(); obj['records'][1]['receipt_id'] = 110
        obj['records'][2]['receipt_predecessor_id'] = 110
        self.rejected(obj, 'RECEIPT_NOT_CHRONOLOGICAL')
    def test_backward_later(self):
        obj = fixture(); obj['records'][1]['receipt_id'] = 109
        obj['records'][2]['receipt_predecessor_id'] = 109
        self.rejected(obj, 'RECEIPT_NOT_CHRONOLOGICAL')
    def test_broken_link(self):
        obj = fixture(); obj['records'][1]['receipt_predecessor_id'] = 100
        self.rejected(obj, 'RECEIPT_PREDECESSOR_MISMATCH')
    def test_zero(self):
        obj = fixture(); obj['records'][0]['receipt_id'] = 0
        self.rejected(obj, 'INVALID_RECEIPT_ID')
    def test_bool(self):
        obj = fixture(); obj['records'][0]['receipt_id'] = True
        self.rejected(obj, 'INVALID_RECEIPT_ID')
    def test_duplicate_json_key(self):
        proc = run(b'{"object":"x","object":"y"}')
        self.assertEqual(proc.returncode, 2)
        self.assertIn(b'DUPLICATE_JSON_KEY', proc.stderr)
    def test_nonfinite(self):
        proc = run(encode(fixture()).replace(b'"receipt_id":110', b'"receipt_id":NaN'))
        self.assertEqual(proc.returncode, 2)
    def test_too_many_records(self):
        self.rejected(fixture(101), 'INVALID_RECORD_COUNT')
    def test_extra_fields(self):
        obj = fixture(); obj['unexpected'] = 'x'
        self.rejected(obj, 'INVALID_ENVELOPE')
    def test_empty(self):
        self.rejected({'object': 'NEXUS_OMEGA_ALPHA_RECEIPT_ORDER_GUARD_V1',
                       'scope': {'predecessor_receipt_id': 100}, 'records': []}, 'INVALID_RECORD_COUNT')


if __name__ == '__main__':
    unittest.main()
