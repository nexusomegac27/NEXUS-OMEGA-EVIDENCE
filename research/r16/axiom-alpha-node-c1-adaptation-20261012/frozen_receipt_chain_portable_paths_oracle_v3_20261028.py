#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Independent black-box V3 oracle; runs predecessor and candidate subprocesses.

Freeze this file on GitHub before publishing the V3 candidate. Synthetic
metadata tests only; it does not authenticate GitHub API responses or bytes.
"""
import copy
import json
import os
import subprocess
import sys
import unittest

BASELINE = os.environ.get('AXIOM_BASELINE', 'alpha_receipt_chain_reconciler_v2_20261028.py')
TARGET = os.environ.get('AXIOM_CANDIDATE', 'alpha_receipt_chain_reconciler_v3_20261028.py')
ROOT = 'research/r16/axiom-alpha-node-c1-adaptation-20261012/'
A, B, C = 'a'*40, 'b'*40, 'c'*40


def fixture():
    def record(pr, merge, parent, rid, prev, n):
        return {'pr': pr, 'merged': True, 'merge_sha': merge,
                'receipt_id': rid, 'receipt_predecessor_id': prev,
                'receipt_main_sha': merge, 'receipt_parent_sha': parent,
                'compare': {'ahead': 1, 'behind': 0, 'files_added': n,
                            'files_modified': 0, 'files_deleted': 0},
                'files': [{'path': ROOT + f'pr{pr}_item{i}.py', 'status': 'added'}
                          for i in range(n)]}
    return {'object': 'NEXUS_OMEGA_ALPHA_RECEIPT_CHAIN_V2',
            'repository': 'nexusomegac27/NEXUS-OMEGA-EVIDENCE',
            'scope': {'first_pr': 173, 'last_pr': 174, 'base_sha': A,
                      'head_sha': C, 'predecessor_receipt_id': 10},
            'records': [record(173, B, A, 11, 10, 4),
                        record(174, C, B, 12, 11, 4)]}


def encoded(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':')).encode('utf-8')


def run(script, raw):
    return subprocess.run([sys.executable, script], input=raw,
                          capture_output=True, timeout=8)


class PortablePathsOracle(unittest.TestCase):
    def good(self, obj=None):
        raw = encoded(fixture() if obj is None else obj)
        result = run(TARGET, raw)
        self.assertEqual(result.returncode, 0, result.stderr.decode())
        out = json.loads(result.stdout)
        self.assertEqual(out['project_automation_rate'], 'NOT_COMPUTABLE')
        self.assertEqual(out['project_readback_rate'], 'NOT_COMPUTABLE')
        self.assertIs(out['api_origin_authenticated'], False)
        self.assertIs(out['source_file_byte_readback_verified'], False)
        self.assertEqual(out['portable_path_guard'], 'PASS_SYNTHETIC_METADATA_ONLY')
        return out

    def gap(self, edit, expected):
        obj = fixture()
        edit(obj)
        raw = encoded(obj)
        old = run(BASELINE, raw)
        self.assertEqual(old.returncode, 0, 'baseline gap not reproduced: '+old.stderr.decode())
        new = run(TARGET, raw)
        self.assertEqual(new.returncode, 2, new.stdout.decode())
        self.assertEqual(new.stdout, b'')
        self.assertIn(expected.encode(), new.stderr)

    def bad(self, edit, expected):
        obj = fixture()
        edit(obj)
        new = run(TARGET, encoded(obj))
        self.assertEqual(new.returncode, 2)
        self.assertEqual(new.stdout, b'')
        self.assertIn(expected.encode(), new.stderr)

    def test_positive_4_plus_4(self):
        self.assertEqual(self.good()['files_checked'], 8)

    def test_positive_one_record(self):
        obj = fixture(); obj['records'] = obj['records'][1:]
        obj['scope'].update(first_pr=174, base_sha=B, predecessor_receipt_id=11)
        self.assertEqual(self.good(obj)['files_checked'], 4)

    def test_positive_case_distinct(self):
        obj = fixture()
        obj['records'][0]['files'][0]['path'] = ROOT+'Alpha.py'
        obj['records'][1]['files'][0]['path'] = ROOT+'Beta.py'
        self.good(obj)

    def test_case_alias_same_record(self):
        self.gap(lambda x: x['records'][0]['files'][1].update(path=ROOT+'PR173_ITEM0.py'), 'PORTABLE_PATH_COLLISION')

    def test_case_alias_across_records(self):
        def edit(x):
            x['records'][0]['files'][0]['path'] = ROOT+'Alpha.py'
            x['records'][1]['files'][0]['path'] = ROOT+'alpha.py'
        self.gap(edit, 'PORTABLE_PATH_COLLISION')

    def test_reserved_device_con(self):
        self.gap(lambda x: x['records'][0]['files'][0].update(path=ROOT+'CON.py'), 'WINDOWS_DEVICE_NAME')

    def test_reserved_device_lpt9(self):
        self.gap(lambda x: x['records'][0]['files'][0].update(path=ROOT+'lpt9.log'), 'WINDOWS_DEVICE_NAME')

    def test_reserved_device_nul(self):
        self.gap(lambda x: x['records'][0]['files'][0].update(path=ROOT+'NUL'), 'WINDOWS_DEVICE_NAME')

    def test_ntfs_alternate_stream(self):
        self.gap(lambda x: x['records'][0]['files'][0].update(path=ROOT+'file.py:stream'), 'WINDOWS_INVALID_CHARACTER')

    def test_windows_wildcard(self):
        self.gap(lambda x: x['records'][0]['files'][0].update(path=ROOT+'file?.py'), 'WINDOWS_INVALID_CHARACTER')

    def test_trailing_dot(self):
        self.gap(lambda x: x['records'][0]['files'][0].update(path=ROOT+'file.'), 'WINDOWS_TRAILING_DOT_SPACE')

    def test_trailing_space(self):
        self.gap(lambda x: x['records'][0]['files'][0].update(path=ROOT+'file '), 'WINDOWS_TRAILING_DOT_SPACE')

    def test_existing_exact_duplicate(self):
        self.bad(lambda x: x['records'][1]['files'][0].update(path=x['records'][0]['files'][0]['path']), 'DUPLICATE_ADDITIVE_PATH')

    def test_existing_parent_chain(self):
        self.bad(lambda x: x['records'][1].update(receipt_parent_sha=A), 'MAIN_PARENT_MISMATCH')

    def test_existing_compare_count(self):
        self.bad(lambda x: x['records'][1]['compare'].update(files_added=5), 'COMPARE_INVENTORY_MISMATCH')

    def test_duplicate_json_key(self):
        self.assertEqual(run(TARGET, b'{"object":"x","object":"y"}').returncode, 2)

    def test_nonfinite_json(self):
        self.assertEqual(run(TARGET, encoded(fixture()).replace(b'"ahead":1', b'"ahead":NaN')).returncode, 2)

    def test_oversize(self):
        self.assertEqual(run(TARGET, b'x'*1_048_577).returncode, 2)


if __name__ == '__main__':
    unittest.main()
