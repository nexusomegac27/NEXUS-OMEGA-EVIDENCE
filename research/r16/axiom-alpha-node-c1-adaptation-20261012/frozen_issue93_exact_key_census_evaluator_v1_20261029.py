#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Independent black-box subprocess evaluator for exact-key PR receipt census.

Run with AXIOM_CANDIDATE=<path> to evaluate an isolated candidate. Does not
import candidate code. Synthetic fixtures only, not API authentication.
"""
import copy
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest

TARGET = Path(os.environ.get('AXIOM_CANDIDATE', Path(__file__).with_name('alpha_issue93_exact_key_receipt_census_v1_20261029.py')))
ROOT = 'https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/pull/'


def sample():
    return {'object': 'NEXUS_OMEGA_ALPHA_ISSUE93_EXACT_KEY_RECEIPT_CENSUS_V1',
            'repository': 'nexusomegac27/NEXUS-OMEGA-EVIDENCE', 'issue_number': 93,
            'expected_prs': [182, 183],
            'pulls': [{'number': 182, 'merged': True, 'merge_commit_sha': 'a' * 40},
                      {'number': 183, 'merged': True, 'merge_commit_sha': 'b' * 40}],
            'comments': [
                {'id': 100, 'user': {'login': 'nexusomegac27'},
                 'body': 'PR=' + ROOT + '182\nACTUAL_MAIN_READBACK=' + 'a' * 40 + '\nCLAIM_CEILING=C1_DESCRIPTIVE_ONLY\n'},
                {'id': 101, 'user': {'login': 'nexusomegac27'},
                 'body': 'PREDECESSOR_PR=' + ROOT + '182\nPR=' + ROOT + '183\nACTUAL_MAIN_READBACK=' + 'b' * 40 + '\nCLAIM_CEILING=C1_DESCRIPTIVE_ONLY\n'}]}


def invoke(data):
    raw = data if isinstance(data, bytes) else json.dumps(data).encode('utf-8')
    return subprocess.run([sys.executable, str(TARGET)], input=raw,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=8)


class FrozenExactKeyOracle(unittest.TestCase):
    def good(self, data):
        p = invoke(data)
        self.assertEqual(p.returncode, 0, p.stderr.decode(errors='replace'))
        return json.loads(p.stdout)

    def bad(self, data, code):
        p = invoke(data)
        self.assertEqual(p.returncode, 2, p.stdout.decode(errors='replace'))
        self.assertIn(code.encode(), p.stderr)

    def test_01_exact_mapping(self):
        r = self.good(sample())
        self.assertEqual(r['receipt_ids'], {'182': 100, '183': 101})
        self.assertEqual((r['matched_receipt_count'], r['expected_pr_count']), (2, 2))
        self.assertEqual(r['project_automation_rate'], 'NOT_COMPUTABLE')

    def test_02_predecessor_only_is_ignored(self):
        x = sample()
        x['comments'].append({'id': 102, 'user': {'login': 'someone-else'},
                              'body': 'PREDECESSOR_PR=' + ROOT + '182\n'})
        r = self.good(x)
        self.assertEqual(r['receipt_ids']['182'], 100)
        self.assertEqual(r['predecessor_only_comments'], 1)

    def test_03_quoted_pr_is_not_current_receipt(self):
        x = sample()
        x['comments'].append({'id': 102, 'user': {'login': 'someone-else'},
                              'body': '> PR=' + ROOT + '182\n'})
        self.assertEqual(self.good(x)['matched_receipt_count'], 2)

    def test_04_duplicate_exact_pr_field(self):
        x = sample()
        x['comments'][0]['body'] += 'PR=' + ROOT + '183\n'
        self.bad(x, 'DUPLICATE_RECEIPT_FIELD')

    def test_05_duplicate_receipt_for_pr(self):
        x = sample()
        x['comments'].append(copy.deepcopy(x['comments'][0]))
        x['comments'][-1]['id'] = 102
        self.bad(x, 'DUPLICATE_PR_RECEIPT')

    def test_06_mismatched_merge(self):
        x = sample()
        x['pulls'][0]['merge_commit_sha'] = 'c' * 40
        self.bad(x, 'PR_MAIN_READBACK_MISMATCH')

    def test_07_missing_pr_receipt(self):
        x = sample()
        x['comments'][1]['body'] = 'PREDECESSOR_PR=' + ROOT + '182\n'
        self.bad(x, 'MISSING_EXPECTED_PR_RECEIPT')

    def test_08_actor_forgery(self):
        x = sample()
        x['comments'][0]['user']['login'] = 'unregistered'
        self.bad(x, 'RECEIPT_ACTOR_MISMATCH')

    def test_09_receipt_order(self):
        x = sample()
        x['comments'][0]['id'] = 200
        self.bad(x, 'NONMONOTONIC_RECEIPT_ORDER')

    def test_10_claim_promotion(self):
        x = sample()
        x['comments'][0]['body'] = x['comments'][0]['body'].replace('C1_DESCRIPTIVE_ONLY', 'C2')
        self.bad(x, 'CLAIM_CEILING_MISMATCH')

    def test_11_duplicate_json_key(self):
        self.bad(b'{"object":1,"object":2}', 'DUPLICATE_JSON_KEY')

    def test_12_nonfinite(self):
        self.bad(b'{"object":NaN}', 'NONFINITE_JSON')

    def test_13_duplicate_comment_id(self):
        x = sample()
        x['comments'][1]['id'] = 100
        self.bad(x, 'DUPLICATE_COMMENT_ID')

    def test_14_unknown_pr(self):
        x = sample()
        x['comments'][1]['body'] = x['comments'][1]['body'].replace('PR=' + ROOT + '183', 'PR=' + ROOT + '184')
        self.bad(x, 'UNEXPECTED_RECEIPT_PR')


if __name__ == '__main__':
    unittest.main()
