#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Frozen, black-box, synthetic Issue #93 raw-HTML receipt attribution oracle.

Candidate is invoked only as a subprocess. No imports, network or writes.
The baseline must fail tests that put plausible receipts inside HTML raw blocks.
"""
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest

HERE = Path(__file__).parent
TARGET = Path(os.environ.get('AXIOM_CANDIDATE', HERE / 'alpha_issue93_raw_html_block_guard_v4_20261029.py'))
URL = 'https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/pull/'


def receipt(number, sha):
    return f'PR={URL}{number}\nACTUAL_MAIN_READBACK={sha}\nCLAIM_CEILING=C1_DESCRIPTIVE_ONLY\n'


def fixture():
    return {'object': 'NEXUS_OMEGA_ALPHA_ISSUE93_EXACT_KEY_RECEIPT_CENSUS_V1',
            'repository': 'nexusomegac27/NEXUS-OMEGA-EVIDENCE', 'issue_number': 93,
            'expected_prs': [182, 183],
            'pulls': [{'number': 182, 'merged': True, 'merge_commit_sha': 'a'*40},
                      {'number': 183, 'merged': True, 'merge_commit_sha': 'b'*40}],
            'comments': [{'id': 100, 'user': {'login': 'nexusomegac27'}, 'body': receipt(182, 'a'*40)},
                         {'id': 101, 'user': {'login': 'nexusomegac27'}, 'body': receipt(183, 'b'*40)}]}


def invoke(doc):
    return subprocess.run([sys.executable, str(TARGET)], input=json.dumps(doc),
                          capture_output=True, text=True, timeout=6)


class RawHTMLBlockOracle(unittest.TestCase):
    def valid(self, doc):
        p = invoke(doc)
        self.assertEqual(p.returncode, 0, p.stderr)
        return json.loads(p.stdout)

    def invalid(self, doc, reason):
        p = invoke(doc)
        self.assertEqual(p.returncode, 2, p.stdout + p.stderr)
        self.assertIn(reason, p.stderr)

    def test_01_plain_valid_receipts(self):
        self.assertEqual(self.valid(fixture())['matched_receipt_count'], 2)

    def test_02_pre_only_is_not_receipt(self):
        x = fixture(); x['comments'][1]['body'] = '<pre>\n' + receipt(183, 'b'*40) + '</pre>\n'
        self.invalid(x, 'MISSING_EXPECTED_PR_RECEIPT')

    def test_03_script_only_is_not_receipt(self):
        x = fixture(); x['comments'][1]['body'] = '<script>\n' + receipt(183, 'b'*40) + '</script>\n'
        self.invalid(x, 'MISSING_EXPECTED_PR_RECEIPT')

    def test_04_style_only_is_not_receipt(self):
        x = fixture(); x['comments'][1]['body'] = '<style>\n' + receipt(183, 'b'*40) + '</style>\n'
        self.invalid(x, 'MISSING_EXPECTED_PR_RECEIPT')

    def test_05_textarea_only_is_not_receipt(self):
        x = fixture(); x['comments'][1]['body'] = '<textarea>\n' + receipt(183, 'b'*40) + '</textarea>\n'
        self.invalid(x, 'MISSING_EXPECTED_PR_RECEIPT')

    def test_06_uppercase_with_attributes(self):
        x = fixture(); x['comments'][1]['body'] = '<PRE class="sample">\n' + receipt(183, 'b'*40) + '</PRE>\n'
        self.invalid(x, 'MISSING_EXPECTED_PR_RECEIPT')

    def test_07_raw_html_duplicate_ignored(self):
        x = fixture(); x['comments'][1]['body'] += '<pre>\n' + receipt(183, 'b'*40) + '</pre>\n'
        self.assertEqual(self.valid(x)['matched_receipt_count'], 2)

    def test_08_unclosed_raw_html_fails_closed(self):
        x = fixture(); x['comments'][1]['body'] += '<pre>\n' + receipt(183, 'b'*40)
        self.invalid(x, 'UNCLOSED_RAW_HTML_BLOCK')

    def test_09_valid_receipt_after_closed_html(self):
        x = fixture(); x['comments'][1]['body'] = '<pre>\n' + receipt(183, 'b'*40) + '</pre>\n' + receipt(183, 'b'*40)
        self.assertEqual(self.valid(x)['matched_receipt_count'], 2)

    def test_10_html_comment_regression(self):
        x = fixture(); x['comments'][1]['body'] = '<!--\n' + receipt(183, 'b'*40) + '-->\n'
        self.invalid(x, 'MISSING_EXPECTED_PR_RECEIPT')

    def test_11_fenced_markdown_regression(self):
        x = fixture(); x['comments'][1]['body'] = '~~~\n' + receipt(183, 'b'*40) + '~~~\n'
        self.invalid(x, 'MISSING_EXPECTED_PR_RECEIPT')

    def test_12_wrong_merge_regression(self):
        x = fixture(); x['pulls'][1]['merge_commit_sha'] = 'c'*40
        self.invalid(x, 'PR_MAIN_READBACK_MISMATCH')

    def test_13_nonowner_regression(self):
        x = fixture(); x['comments'][1]['user']['login'] = 'external'
        self.invalid(x, 'RECEIPT_ACTOR_MISMATCH')

    def test_14_real_duplicate_regression(self):
        x = fixture(); x['comments'][1]['body'] += 'PR=' + URL + '183\n'
        self.invalid(x, 'DUPLICATE_RECEIPT_FIELD')

    def test_15_never_project_rate(self):
        x = self.valid(fixture())
        self.assertEqual(x['project_automation_rate'], 'NOT_COMPUTABLE')
        self.assertEqual(x['project_readback_rate'], 'NOT_COMPUTABLE')
        self.assertFalse(x['api_origin_authenticated'])

    def test_16_pre_inline_close_followed_by_receipt(self):
        x = fixture(); x['comments'][1]['body'] = '<pre>example</pre>\n' + receipt(183, 'b'*40)
        self.assertEqual(self.valid(x)['matched_receipt_count'], 2)


    def test_17_pre_literal_inside_fence_is_not_unclosed_html(self):
        x = fixture(); x['comments'][1]['body'] += '~~~\n<pre>\n~~~\n'
        self.assertEqual(self.valid(x)['matched_receipt_count'], 2)

    def test_18_pre_literal_inside_html_comment_is_not_unclosed_html(self):
        x = fixture(); x['comments'][1]['body'] += '<!--\n<pre>\n-->\n'
        self.assertEqual(self.valid(x)['matched_receipt_count'], 2)

    def test_19_unclosed_markdown_fence_regression(self):
        x = fixture(); x['comments'][1]['body'] += '~~~\n' + receipt(183, 'b'*40)
        self.invalid(x, 'UNCLOSED_MARKDOWN_FENCE')

    def test_20_unclosed_html_comment_regression(self):
        x = fixture(); x['comments'][1]['body'] += '<!--\n' + receipt(183, 'b'*40)
        self.invalid(x, 'UNCLOSED_HTML_COMMENT')


if __name__ == '__main__':
    unittest.main()
