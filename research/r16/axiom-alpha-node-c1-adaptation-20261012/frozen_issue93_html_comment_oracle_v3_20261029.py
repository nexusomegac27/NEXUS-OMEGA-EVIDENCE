#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Frozen subprocess evaluator: synthetic Issue #93 HTML-comment ambiguity.
Independent of candidate source; commit before candidate. No network/writes.
"""
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest

URL = 'https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/pull/'
TARGET = Path(os.environ.get('AXIOM_CANDIDATE', Path(__file__).with_name('alpha_issue93_html_comment_guard_v3_20261029.py')))


def receipt(n, sha):
    return f'PR={URL}{n}\nACTUAL_MAIN_READBACK={sha}\nCLAIM_CEILING=C1_DESCRIPTIVE_ONLY\n'


def fixture():
    return {'object': 'NEXUS_OMEGA_ALPHA_ISSUE93_EXACT_KEY_RECEIPT_CENSUS_V1',
            'repository': 'nexusomegac27/NEXUS-OMEGA-EVIDENCE', 'issue_number': 93,
            'expected_prs': [182, 183],
            'pulls': [{'number': 182, 'merged': True, 'merge_commit_sha': 'a'*40},
                      {'number': 183, 'merged': True, 'merge_commit_sha': 'b'*40}],
            'comments': [{'id': 100, 'user': {'login': 'nexusomegac27'}, 'body': receipt(182, 'a'*40)},
                         {'id': 101, 'user': {'login': 'nexusomegac27'}, 'body': receipt(183, 'b'*40)}]}


def invoke(obj):
    data = obj if isinstance(obj, bytes) else json.dumps(obj).encode()
    return subprocess.run([sys.executable, str(TARGET)], input=data, capture_output=True, timeout=8)


class FrozenOracle(unittest.TestCase):
    def good(self, obj):
        p = invoke(obj)
        self.assertEqual(p.returncode, 0, p.stderr.decode(errors='replace'))
        return json.loads(p.stdout)

    def bad(self, obj, reason):
        p = invoke(obj)
        self.assertEqual(p.returncode, 2, p.stderr.decode(errors='replace'))
        self.assertIn(reason.encode(), p.stderr)

    def test_01_valid(self):
        self.assertEqual(self.good(fixture())['matched_receipt_count'], 2)

    def test_02_forged_html_only(self):
        x = fixture(); x['comments'][1]['body'] = '<!--\n' + receipt(183, 'b'*40) + '-->\n'
        self.bad(x, 'MISSING_EXPECTED_PR_RECEIPT')

    def test_03_html_duplicate_ignored(self):
        x = fixture(); x['comments'][1]['body'] += '<!--\n' + receipt(183, 'b'*40) + '-->\n'
        self.good(x)

    def test_04_html_claim_ignored(self):
        x = fixture(); x['comments'][1]['body'] += '<!--\nCLAIM_CEILING=C2\n-->\n'
        self.good(x)

    def test_05_html_wrong_pr_ignored(self):
        x = fixture(); x['comments'][1]['body'] += '<!--\nPR=' + URL + '182\n-->\n'
        self.good(x)

    def test_06_unclosed_html_fail_closed(self):
        x = fixture(); x['comments'][1]['body'] += '<!--\nPR=' + URL + '182\n'
        self.bad(x, 'UNCLOSED_HTML_COMMENT')

    def test_07_real_receipt_after_html(self):
        x = fixture(); x['comments'][1]['body'] = '<!--\n' + receipt(183, 'b'*40) + '-->\n' + receipt(183, 'b'*40)
        self.good(x)

    def test_08_multiple_html_comments(self):
        x = fixture(); x['comments'][1]['body'] = '<!-- first -->\n<!-- second -->\n' + receipt(183, 'b'*40)
        self.good(x)

    def test_09_fence_regression(self):
        x = fixture(); x['comments'][1]['body'] = '~~~\n' + receipt(183, 'b'*40) + '~~~\n'
        self.bad(x, 'MISSING_EXPECTED_PR_RECEIPT')

    def test_10_wrong_merge(self):
        x = fixture(); x['pulls'][1]['merge_commit_sha'] = 'c'*40
        self.bad(x, 'PR_MAIN_READBACK_MISMATCH')

    def test_11_nonowner(self):
        x = fixture(); x['comments'][1]['user']['login'] = 'outsider'
        self.bad(x, 'RECEIPT_ACTOR_MISMATCH')

    def test_12_real_duplicate(self):
        x = fixture(); x['comments'][1]['body'] += 'PR=' + URL + '183\n'
        self.bad(x, 'DUPLICATE_RECEIPT_FIELD')

    def test_13_duplicate_json_key(self):
        self.bad(b'{"object":1,"object":2}', 'DUPLICATE_JSON_KEY')

    def test_14_nonfinite_json(self):
        self.bad(b'{"object":NaN}', 'NONFINITE_JSON')

    def test_15_claim_promotion(self):
        x = fixture(); x['comments'][1]['body'] = x['comments'][1]['body'].replace('C1_DESCRIPTIVE_ONLY', 'C2')
        self.bad(x, 'CLAIM_CEILING_MISMATCH')


if __name__ == '__main__':
    unittest.main()
