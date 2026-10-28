#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Frozen independent subprocess oracle for C1 receipt inventory prefix conflicts.

The oracle is authored and committed before V4. It invokes two separate
programs, does not import the candidate, and does not authenticate GitHub.
"""
import copy
import json
import os
import subprocess
import sys
import unittest

BASELINE = os.environ.get('AXIOM_BASELINE', 'alpha_receipt_chain_reconciler_v3_20261028.py')
TARGET = os.environ.get('AXIOM_CANDIDATE', 'alpha_receipt_chain_reconciler_v4_20261028.py')
ROOT = 'research/r16/axiom-alpha-node-c1-adaptation-20261012/'
A, B, C = 'a'*40, 'b'*40, 'c'*40


def fixture():
    def record(pr, merge, parent, rid, prev, names):
        return {'pr': pr, 'merged': True, 'merge_sha': merge,
                'receipt_id': rid, 'receipt_predecessor_id': prev,
                'receipt_main_sha': merge, 'receipt_parent_sha': parent,
                'compare': {'ahead': 1, 'behind': 0, 'files_added': len(names),
                            'files_modified': 0, 'files_deleted': 0},
                'files': [{'path': ROOT + name, 'status': 'added'} for name in names]}
    return {'object': 'NEXUS_OMEGA_ALPHA_RECEIPT_CHAIN_V2',
            'repository': 'nexusomegac27/NEXUS-OMEGA-EVIDENCE',
            'scope': {'first_pr': 175, 'last_pr': 176, 'base_sha': A,
                      'head_sha': C, 'predecessor_receipt_id': 20},
            'records': [record(175, B, A, 21, 20, ['first.py', 'second.py']),
                        record(176, C, B, 22, 21, ['third.py', 'fourth.py'])]}


def encoded(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':')).encode('utf-8')


def run(script, raw):
    return subprocess.run([sys.executable, script], input=raw,
                          capture_output=True, timeout=8)


def setpath(obj, rec, file, name):
    obj['records'][rec]['files'][file]['path'] = ROOT + name


class FrozenPrefixOracle(unittest.TestCase):
    def good(self, obj):
        raw = encoded(obj)
        baseline = run(BASELINE, raw)
        self.assertEqual(baseline.returncode, 0, baseline.stderr.decode())
        target = run(TARGET, raw)
        self.assertEqual(target.returncode, 0, target.stderr.decode())
        result = json.loads(target.stdout)
        self.assertEqual(result['files_checked'], 4)
        self.assertEqual(result['prefix_guard'], 'PASS_SYNTHETIC_METADATA_ONLY')
        self.assertIs(result['api_origin_authenticated'], False)
        self.assertIs(result['source_file_byte_readback_verified'], False)
        self.assertEqual(result['project_automation_rate'], 'NOT_COMPUTABLE')
        self.assertEqual(result['project_readback_rate'], 'NOT_COMPUTABLE')

    def gap(self, edits):
        obj = fixture()
        for rec, file, name in edits:
            setpath(obj, rec, file, name)
        raw = encoded(obj)
        baseline = run(BASELINE, raw)
        self.assertEqual(baseline.returncode, 0,
                         'baseline gap not reproduced: ' + baseline.stderr.decode())
        target = run(TARGET, raw)
        self.assertEqual(target.returncode, 2, target.stdout.decode())
        self.assertEqual(target.stdout, b'')
        self.assertIn(b'FILE_DIRECTORY_PREFIX_CONFLICT', target.stderr)

    def retained_bad(self, edits, code):
        obj = fixture()
        for rec, file, name in edits:
            setpath(obj, rec, file, name)
        target = run(TARGET, encoded(obj))
        self.assertEqual(target.returncode, 2)
        self.assertEqual(target.stdout, b'')
        self.assertIn(code.encode(), target.stderr)

    def test_positive_baseline(self):
        self.good(fixture())

    def test_positive_common_directory(self):
        obj = fixture()
        setpath(obj, 0, 0, 'shared/a.py')
        setpath(obj, 1, 0, 'shared/b.py')
        self.good(obj)

    def test_positive_nested_siblings(self):
        obj = fixture()
        setpath(obj, 0, 0, 'pkg/deep/a.py')
        setpath(obj, 0, 1, 'pkg/deep/b.py')
        self.good(obj)

    def test_gap_same_record(self):
        self.gap([(0, 0, 'payload'), (0, 1, 'payload/child.py')])

    def test_gap_across_records_forward(self):
        self.gap([(0, 0, 'store'), (1, 0, 'store/part.py')])

    def test_gap_across_records_reverse(self):
        self.gap([(0, 0, 'archive/file.py'), (1, 0, 'archive')])

    def test_gap_casefold_directory(self):
        self.gap([(0, 0, 'DATA'), (1, 0, 'data/item.py')])

    def test_gap_nested_prefix(self):
        self.gap([(0, 0, 'x/y'), (1, 0, 'x/y/z.py')])

    def test_retained_case_alias(self):
        self.retained_bad([(0, 0, 'ALPHA.py'), (1, 0, 'alpha.py')],
                          'PORTABLE_PATH_COLLISION')

    def test_retained_device(self):
        self.retained_bad([(0, 0, 'CON.py')], 'WINDOWS_DEVICE_NAME')

    def test_retained_trailing_dot(self):
        self.retained_bad([(0, 0, 'bad.')], 'WINDOWS_TRAILING_DOT_SPACE')

    def test_retained_duplicate(self):
        self.retained_bad([(0, 0, 'same.py'), (1, 0, 'same.py')],
                          'DUPLICATE_ADDITIVE_PATH')

    def test_retained_chain(self):
        obj = fixture()
        obj['records'][1]['receipt_parent_sha'] = A
        target = run(TARGET, encoded(obj))
        self.assertEqual(target.returncode, 2)
        self.assertIn(b'MAIN_PARENT_MISMATCH', target.stderr)

    def test_duplicate_json_keys(self):
        self.assertEqual(run(TARGET, b'{"object":"x","object":"y"}').returncode, 2)

    def test_nonfinite_json(self):
        self.assertEqual(run(TARGET, encoded(fixture()).replace(b'"ahead":1', b'"ahead":NaN')).returncode, 2)

    def test_oversize(self):
        self.assertEqual(run(TARGET, b'x'*1_048_577).returncode, 2)


if __name__ == '__main__':
    unittest.main()
