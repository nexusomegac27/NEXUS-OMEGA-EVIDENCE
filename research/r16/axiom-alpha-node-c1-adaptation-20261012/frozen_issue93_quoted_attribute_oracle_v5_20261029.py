#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Frozen independent subprocess oracle for Issue93 quoted-attribute raw-HTML bypass.

Synthetic input only; no GitHub API, no filesystem mutation. The target is a
subprocess, not imported. Freeze this file before implementing V5.
"""
import copy
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest

HERE = Path(__file__).parent
TARGET = Path(os.environ.get('AXIOM_CANDIDATE', HERE / 'alpha_issue93_quoted_attribute_guard_v5_20261029.py'))
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


def run(doc):
    return subprocess.run([sys.executable, str(TARGET)], input=json.dumps(doc),
                          capture_output=True, text=True, timeout=6)


class QuotedAttributeOracle(unittest.TestCase):
    def ok(self, doc):
        p = run(doc)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual(json.loads(p.stdout)['matched_receipt_count'], 2)

    def bad(self, doc, code):
        p = run(doc)
        self.assertEqual(p.returncode, 2, p.stdout + p.stderr)
        self.assertIn(code, p.stderr)

    def fake(self, prefix, suffix=''):
        d = fixture()
        d['comments'][1]['body'] = prefix + receipt(183, 'b'*40) + suffix
        return d

    def test_01_plain_valid(self):
        self.ok(fixture())

    def test_02_double_quote_nested_pre_close(self):
        self.bad(self.fake('<pre>\n<div data-x="</pre>">\n', '</pre>\n'), 'MISSING_EXPECTED_PR_RECEIPT')

    def test_03_single_quote_nested_pre_close(self):
        self.bad(self.fake("<pre>\n<div data-x='</pre>'>\n", '</pre>\n'), 'MISSING_EXPECTED_PR_RECEIPT')

    def test_04_script_attribute_close(self):
        self.bad(self.fake('<script data-x="</script>">\n', '</script>\n'), 'MISSING_EXPECTED_PR_RECEIPT')

    def test_05_style_attribute_close(self):
        self.bad(self.fake('<style data-x="</style>">\n', '</style>\n'), 'MISSING_EXPECTED_PR_RECEIPT')

    def test_06_textarea_attribute_close(self):
        self.bad(self.fake('<textarea data-x="</textarea>">\n', '</textarea>\n'), 'MISSING_EXPECTED_PR_RECEIPT')

    def test_07_double_quote_with_gt_and_close(self):
        self.bad(self.fake('<pre>\n<div title="x > </pre> y">\n', '</pre>\n'), 'MISSING_EXPECTED_PR_RECEIPT')

    def test_08_single_quote_with_gt_and_close(self):
        self.bad(self.fake("<pre>\n<div title='x > </pre> y'>\n", '</pre>\n'), 'MISSING_EXPECTED_PR_RECEIPT')

    def test_09_uppercase_quoted_close(self):
        self.bad(self.fake('<PRE CLASS="x">\n<div title="</PRE>">\n', '</PRE>\n'), 'MISSING_EXPECTED_PR_RECEIPT')

    def test_10_nested_quote_in_other_tag(self):
        self.bad(self.fake('<pre>\n<a href="</pre>">text</a>\n', '</pre>\n'), 'MISSING_EXPECTED_PR_RECEIPT')

    def test_11_simple_pre_only(self):
        self.bad(self.fake('<pre>\n', '</pre>\n'), 'MISSING_EXPECTED_PR_RECEIPT')

    def test_12_raw_duplicate_ignored(self):
        d = fixture()
        d['comments'][1]['body'] += '<pre>\n<div title="</pre>">\n' + receipt(183, 'b'*40) + '</pre>\n'
        self.ok(d)

    def test_13_valid_after_actual_close(self):
        d = self.fake('<pre>\n<div title="</pre>">\n', '</pre>\n' + receipt(183, 'b'*40))
        self.ok(d)

    def test_14_inline_raw_close_then_valid(self):
        d = self.fake('<pre>example</pre>\n')
        self.ok(d)

    def test_15_fenced_html_literal_then_valid(self):
        d = self.fake('~~~\n<pre>\n~~~\n')
        self.ok(d)

    def test_16_comment_html_literal_then_valid(self):
        d = self.fake('<!--\n<pre>\n-->\n')
        self.ok(d)

    def test_17_html_comment_only(self):
        self.bad(self.fake('<!--\n', '-->\n'), 'MISSING_EXPECTED_PR_RECEIPT')

    def test_18_markdown_fence_only(self):
        self.bad(self.fake('~~~\n', '~~~\n'), 'MISSING_EXPECTED_PR_RECEIPT')

    def test_19_unclosed_raw(self):
        self.bad(self.fake('<pre>\n'), 'UNCLOSED_RAW_HTML_BLOCK')

    def test_20_wrong_merge(self):
        d = fixture()
        d['pulls'][1]['merge_commit_sha'] = 'c'*40
        self.bad(d, 'PR_MAIN_READBACK_MISMATCH')

    def test_21_non_owner(self):
        d = fixture()
        d['comments'][1]['user']['login'] = 'other'
        self.bad(d, 'RECEIPT_ACTOR_MISMATCH')

    def test_22_duplicate_binding(self):
        d = fixture()
        d['comments'][1]['body'] += 'PR=' + URL + '183\n'
        self.bad(d, 'DUPLICATE_RECEIPT_FIELD')

    def test_23_mixed_case_attribute_after_closed_tag(self):
        d = self.fake('<PRE DATA-x="a > b">example</PRE>\n')
        self.ok(d)

    def test_24_nested_tag_with_comment_open_in_quote(self):
        d = self.fake('<pre>\n<div data-x="<!-- </pre> -->">\n', '</pre>\n')
        self.bad(d, 'MISSING_EXPECTED_PR_RECEIPT')


if __name__ == '__main__':
    unittest.main()
