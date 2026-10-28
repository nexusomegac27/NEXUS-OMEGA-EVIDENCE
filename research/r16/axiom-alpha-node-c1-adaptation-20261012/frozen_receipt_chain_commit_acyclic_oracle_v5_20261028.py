#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Independent frozen black-box oracle: no repeated commit SHA in an additive main chain.

The oracle never imports the candidate and uses only subprocess exit codes,
error strings and scoped output fields. GitHub origin remains unauthenticated.
"""
import copy
import json
import os
import subprocess
import sys
import unittest

BASELINE = os.environ.get('AXIOM_BASELINE', 'alpha_receipt_chain_reconciler_v4_20261028.py')
TARGET = os.environ.get('AXIOM_CANDIDATE', 'alpha_receipt_chain_reconciler_v5_20261028.py')
ROOT = 'research/r16/axiom-alpha-node-c1-adaptation-20261012/'
A, B, C, D, E = ('a'*40, 'b'*40, 'c'*40, 'd'*40, 'e'*40)


def fixture(n=3):
    merges = [B, C, D, E][:n]
    records = []
    parent = A
    for k, commit in enumerate(merges):
        records.append({'pr': 174+k, 'merged': True, 'merge_sha': commit,
                        'receipt_id': 201+k, 'receipt_predecessor_id': 200+k,
                        'receipt_main_sha': commit, 'receipt_parent_sha': parent,
                        'compare': {'ahead': 1, 'behind': 0, 'files_added': 2,
                                    'files_modified': 0, 'files_deleted': 0},
                        'files': [{'path': ROOT + f'pr{k}_file{j}.py', 'status': 'added'}
                                  for j in range(2)]})
        parent = commit
    return {'object': 'NEXUS_OMEGA_ALPHA_RECEIPT_CHAIN_V2',
            'repository': 'nexusomegac27/NEXUS-OMEGA-EVIDENCE',
            'scope': {'first_pr': 174, 'last_pr': 173+n,
                      'base_sha': A, 'head_sha': merges[-1],
                      'predecessor_receipt_id': 200}, 'records': records}


def change_merges(obj, merges):
    assert len(merges) == len(obj['records'])
    parent = obj['scope']['base_sha']
    for record, sha in zip(obj['records'], merges):
        record['merge_sha'] = sha
        record['receipt_main_sha'] = sha
        record['receipt_parent_sha'] = parent
        parent = sha
    obj['scope']['head_sha'] = parent
    return obj


def raw(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':')).encode('utf-8')


def run(script, payload):
    return subprocess.run([sys.executable, script], input=payload,
                          capture_output=True, timeout=8)


class FrozenCommitAcyclicOracle(unittest.TestCase):
    def good(self, obj):
        payload = raw(obj)
        old = run(BASELINE, payload)
        self.assertEqual(old.returncode, 0, old.stderr.decode())
        new = run(TARGET, payload)
        self.assertEqual(new.returncode, 0, new.stderr.decode())
        data = json.loads(new.stdout)
        self.assertEqual(data['commit_acyclic_guard'], 'PASS_SYNTHETIC_METADATA_ONLY')
        self.assertEqual(data['records_checked'], len(obj['records']))
        self.assertIs(data['api_origin_authenticated'], False)
        self.assertIs(data['source_file_byte_readback_verified'], False)
        self.assertEqual(data['project_automation_rate'], 'NOT_COMPUTABLE')
        self.assertEqual(data['project_readback_rate'], 'NOT_COMPUTABLE')

    def gap(self, merges):
        obj = change_merges(fixture(len(merges)), merges)
        payload = raw(obj)
        old = run(BASELINE, payload)
        self.assertEqual(old.returncode, 0, 'V4 gap not reproduced: '+old.stderr.decode())
        new = run(TARGET, payload)
        self.assertEqual(new.returncode, 2, new.stdout.decode())
        self.assertEqual(new.stdout, b'')
        self.assertIn(b'REPEATED_MAIN_COMMIT_SHA', new.stderr)

    def retained_bad(self, edit, expected):
        obj = fixture()
        edit(obj)
        out = run(TARGET, raw(obj))
        self.assertEqual(out.returncode, 2)
        self.assertEqual(out.stdout, b'')
        self.assertIn(expected.encode(), out.stderr)

    def test_good_two(self): self.good(fixture(2))
    def test_good_three(self): self.good(fixture(3))
    def test_good_four(self): self.good(fixture(4))
    def test_gap_first_is_base(self): self.gap([A, C, D])
    def test_gap_second_self_parent(self): self.gap([B, B, D])
    def test_gap_return_to_base(self): self.gap([B, A, D])
    def test_gap_return_to_first(self): self.gap([B, C, B])
    def test_gap_return_to_base_last(self): self.gap([B, C, A])
    def test_gap_fourth_reuses_second(self): self.gap([B, C, D, C])
    def test_retained_prefix(self):
        self.retained_bad(lambda o: (o['records'][0]['files'][0].update(path=ROOT+'x'),
                                     o['records'][1]['files'][0].update(path=ROOT+'x/y.py')),
                          'FILE_DIRECTORY_PREFIX_CONFLICT')
    def test_retained_device(self):
        self.retained_bad(lambda o: o['records'][0]['files'][0].update(path=ROOT+'CON.py'),
                          'WINDOWS_DEVICE_NAME')
    def test_retained_duplicate(self):
        self.retained_bad(lambda o: o['records'][1]['files'][0].update(
            path=o['records'][0]['files'][0]['path']), 'DUPLICATE_ADDITIVE_PATH')
    def test_retained_parent(self):
        self.retained_bad(lambda o: o['records'][1].update(receipt_parent_sha=A),
                          'MAIN_PARENT_MISMATCH')
    def test_duplicate_json_key(self):
        self.assertEqual(run(TARGET, b'{"object":"x","object":"y"}').returncode, 2)
    def test_nonfinite_json(self):
        self.assertEqual(run(TARGET, raw(fixture()).replace(b'"ahead":1', b'"ahead":NaN')).returncode, 2)
    def test_oversize(self):
        self.assertEqual(run(TARGET, b'x'*1_048_577).returncode, 2)


if __name__ == '__main__':
    unittest.main()
