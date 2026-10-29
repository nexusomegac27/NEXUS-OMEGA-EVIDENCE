#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Frozen black-box negative evaluator; candidate is a separate subprocess.

Synthetic-only tests. Commit this oracle before candidate publication.
"""
import copy
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = 'https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/pull/'
TARGET = Path(os.environ.get('AXIOM_CANDIDATE', Path(__file__).with_name('alpha_issue93_fenced_receipt_guard_v2_20261029.py')))


def fixture():
    return {'object': 'NEXUS_OMEGA_ALPHA_ISSUE93_EXACT_KEY_RECEIPT_CENSUS_V1',
            'repository': 'nexusomegac27/NEXUS-OMEGA-EVIDENCE', 'issue_number': 93,
            'expected_prs': [182, 183],
            'pulls': [{'number': 182, 'merged': True, 'merge_commit_sha': 'a'*40},
                      {'number': 183, 'merged': True, 'merge_commit_sha': 'b'*40}],
            'comments': [
                {'id': 100, 'user': {'login': 'nexusomegac27'},
                 'body': 'PR='+ROOT+'182\nACTUAL_MAIN_READBACK='+'a'*40+'\nCLAIM_CEILING=C1_DESCRIPTIVE_ONLY\n'},
                {'id': 101, 'user': {'login': 'nexusomegac27'},
                 'body': 'PREDECESSOR_PR='+ROOT+'182\nPR='+ROOT+'183\nACTUAL_MAIN_READBACK='+'b'*40+'\nCLAIM_CEILING=C1_DESCRIPTIVE_ONLY\n'}]}


def invoke(x):
    raw = x if isinstance(x, bytes) else json.dumps(x).encode('utf-8')
    return subprocess.run([sys.executable, str(TARGET)], input=raw,
                          capture_output=True, timeout=8)


class FrozenFenceOracle(unittest.TestCase):
    def good(self, x):
        p = invoke(x)
        self.assertEqual(p.returncode, 0, p.stderr.decode(errors='replace'))
        return json.loads(p.stdout)

    def bad(self, x, error):
        p = invoke(x)
        self.assertEqual(p.returncode, 2, p.stdout.decode(errors='replace'))
        self.assertIn(error.encode(), p.stderr)

    def test_01_baseline_two_receipts(self):
        self.assertEqual(self.good(fixture())['matched_receipt_count'], 2)

    def test_02_predecessor_only_ignored(self):
        x = fixture(); x['comments'].append({'id': 102, 'user': {'login': 'outsider'}, 'body': 'PREDECESSOR_PR='+ROOT+'182'})
        self.assertEqual(self.good(x)['predecessor_only_comments'], 1)

    def test_03_backtick_forged_receipt_rejected(self):
        x = fixture(); x['comments'][1]['body'] = '```text\nPR='+ROOT+'183\nACTUAL_MAIN_READBACK='+'b'*40+'\nCLAIM_CEILING=C1_DESCRIPTIVE_ONLY\n```'
        self.bad(x, 'MISSING_EXPECTED_PR_RECEIPT')

    def test_04_tilde_forged_receipt_rejected(self):
        x = fixture(); x['comments'][1]['body'] = '~~~\nPR='+ROOT+'183\nACTUAL_MAIN_READBACK='+'b'*40+'\nCLAIM_CEILING=C1_DESCRIPTIVE_ONLY\n~~~'
        self.bad(x, 'MISSING_EXPECTED_PR_RECEIPT')

    def test_05_indented_fenced_example_rejected(self):
        x = fixture(); x['comments'][1]['body'] = '   ````md\nPR='+ROOT+'183\nACTUAL_MAIN_READBACK='+'b'*40+'\nCLAIM_CEILING=C1_DESCRIPTIVE_ONLY\n   ````'
        self.bad(x, 'MISSING_EXPECTED_PR_RECEIPT')

    def test_06_real_receipt_outside_fenced_example(self):
        x = fixture(); x['comments'][1]['body'] += '\n```text\nPR='+ROOT+'182\nACTUAL_MAIN_READBACK='+'a'*40+'\n```\n'
        self.assertEqual(self.good(x)['receipt_ids'], {'182':100, '183':101})

    def test_07_unclosed_fence_fail_closed(self):
        x = fixture(); x['comments'][1]['body'] += '\n```text\nPR='+ROOT+'182'
        self.bad(x, 'UNCLOSED_MARKDOWN_FENCE')

    def test_08_duplicate_outside_field(self):
        x = fixture(); x['comments'][1]['body'] += 'PR='+ROOT+'183\n'
        self.bad(x, 'DUPLICATE_RECEIPT_FIELD')

    def test_09_wrong_merge(self):
        x = fixture(); x['pulls'][1]['merge_commit_sha'] = 'c'*40
        self.bad(x, 'PR_MAIN_READBACK_MISMATCH')

    def test_10_nonowner_claimed_actor(self):
        x = fixture(); x['comments'][1]['user']['login'] = 'unknown'
        self.bad(x, 'RECEIPT_ACTOR_MISMATCH')

    def test_11_claim_promotion(self):
        x = fixture(); x['comments'][1]['body'] = x['comments'][1]['body'].replace('C1_DESCRIPTIVE_ONLY', 'C2')
        self.bad(x, 'CLAIM_CEILING_MISMATCH')

    def test_12_duplicate_json_key(self):
        self.bad(b'{"object":1,"object":2}', 'DUPLICATE_JSON_KEY')

    def test_13_nonfinite_json(self):
        self.bad(b'{"object":NaN}', 'NONFINITE_JSON')

    def test_14_fenced_example_ignored_from_nonowner(self):
        x = fixture(); x['comments'].append({'id':102,'user':{'login':'outsider'},'body':'```\nPR='+ROOT+'182\n```'})
        self.assertEqual(self.good(x)['matched_receipt_count'], 2)

    def test_15_fenced_duplicate_claim_ignored(self):
        x = fixture(); x['comments'][0]['body'] += '\n~~~\nCLAIM_CEILING=C2\n~~~\n'
        self.assertEqual(self.good(x)['matched_receipt_count'], 2)


if __name__ == '__main__':
    unittest.main()
