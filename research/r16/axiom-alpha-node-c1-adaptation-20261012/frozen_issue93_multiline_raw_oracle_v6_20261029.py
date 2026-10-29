#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Frozen subprocess evaluator for multiline raw-HTML Issue #93 receipt ambiguity.

No network, no GitHub authentication, no writes. Candidate runs in a separate
Python process. The test fixture is synthetic, and no live Issue #93 attack is
asserted. This oracle must be committed before the candidate implementation.
"""
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest

HERE = Path(__file__).parent
TARGET = Path(os.environ.get('AXIOM_CANDIDATE', HERE / 'alpha_issue93_multiline_raw_guard_v6_20261029.py'))
URL = 'https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/pull/'


def receipt(n, sha):
    return f'PR={URL}{n}\nACTUAL_MAIN_READBACK={sha}\nCLAIM_CEILING=C1_DESCRIPTIVE_ONLY\n'


def fixture(body=None):
    return {'object': 'NEXUS_OMEGA_ALPHA_ISSUE93_EXACT_KEY_RECEIPT_CENSUS_V1',
            'repository': 'nexusomegac27/NEXUS-OMEGA-EVIDENCE', 'issue_number': 93,
            'expected_prs': [182, 183],
            'pulls': [{'number': 182, 'merged': True, 'merge_commit_sha': 'a'*40},
                      {'number': 183, 'merged': True, 'merge_commit_sha': 'b'*40}],
            'comments': [{'id': 100, 'user': {'login': 'nexusomegac27'}, 'body': receipt(182, 'a'*40)},
                         {'id': 101, 'user': {'login': 'nexusomegac27'},
                          'body': receipt(183, 'b'*40) if body is None else body}]}


def run(doc):
    return subprocess.run([sys.executable, str(TARGET)], input=json.dumps(doc),
                          capture_output=True, text=True, timeout=8)


class MultilineRawOracle(unittest.TestCase):
    def ok(self, body=None, doc=None):
        p = run(doc if doc is not None else fixture(body))
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual(json.loads(p.stdout)['matched_receipt_count'], 2)

    def bad(self, body=None, code='MISSING_EXPECTED_PR_RECEIPT', doc=None):
        p = run(doc if doc is not None else fixture(body))
        self.assertEqual(p.returncode, 2, p.stdout + p.stderr)
        self.assertIn(code, p.stderr)

    def hidden(self, opening, closing):
        return opening + receipt(183, 'b'*40) + closing

    def test_01_plain_valid(self):
        self.ok()

    def test_02_multiline_pre(self):
        self.bad(self.hidden('<pre\n class="x">\n', '</pre>\n'))

    def test_03_multiline_script(self):
        self.bad(self.hidden('<script\n type="text/plain">\n', '</script>\n'))

    def test_04_multiline_style(self):
        self.bad(self.hidden('<style\n media="all">\n', '</style>\n'))

    def test_05_multiline_textarea(self):
        self.bad(self.hidden('<textarea\n rows="3">\n', '</textarea>\n'))

    def test_06_quoted_gt_inside_multiline_open(self):
        self.bad(self.hidden('<pre\n title="a > b">\n', '</pre>\n'))

    def test_07_quoted_fake_close_inside_multiline_open(self):
        self.bad(self.hidden('<pre\n title="</pre>">\n', '</pre>\n'))

    def test_08_three_line_open(self):
        self.bad(self.hidden('<pre\n data-a="x"\n data-b="y">\n', '</pre>\n'))

    def test_09_uppercase_multiline_open(self):
        self.bad(self.hidden('<PRE\n DATA-X="x">\n', '</PRE>\n'))

    def test_10_comment_marker_in_quoted_attribute(self):
        self.bad(self.hidden('<pre\n title="<!-- -->">\n', '</pre>\n'))

    def test_11_open_tag_line_contains_quoted_gt(self):
        self.bad(self.hidden('<pre title="a > b"\n class="z">\n', '</pre>\n'))

    def test_12_valid_after_multiline_raw_close(self):
        self.ok('<pre\n class="x">\nexample\n</pre>\n' + receipt(183, 'b'*40))

    def test_13_valid_after_multiline_nonraw_tag(self):
        self.ok('<div\n title="x">\n</div>\n' + receipt(183, 'b'*40))

    def test_14_fenced_literal_multiline_open(self):
        self.ok('~~~\n<pre\n title="x">\n~~~\n' + receipt(183, 'b'*40))

    def test_15_commented_literal_multiline_open(self):
        self.ok('<!--\n<pre\n title="x">\n-->\n' + receipt(183, 'b'*40))

    def test_16_inline_raw_close_then_valid(self):
        self.ok('<pre>example</pre>\n' + receipt(183, 'b'*40))

    def test_17_unclosed_multiline_open(self):
        self.bad('<pre\n class="x"\n' + receipt(183, 'b'*40), 'UNCLOSED_HTML_TAG')

    def test_18_unclosed_multiline_quote(self):
        self.bad('<pre\n title="x > y\n' + receipt(183, 'b'*40), 'UNCLOSED_HTML_TAG')

    def test_19_wrong_merge(self):
        d = fixture()
        d['pulls'][1]['merge_commit_sha'] = 'c'*40
        self.bad(doc=d, code='PR_MAIN_READBACK_MISMATCH')

    def test_20_nonowner(self):
        d = fixture()
        d['comments'][1]['user']['login'] = 'other'
        self.bad(doc=d, code='RECEIPT_ACTOR_MISMATCH')

    def test_21_duplicate_receipt_field(self):
        self.bad(receipt(183, 'b'*40) + 'PR=' + URL + '183\n', 'DUPLICATE_RECEIPT_FIELD')

    def test_22_hidden_duplicate_ignored(self):
        self.ok(receipt(183, 'b'*40) + '<pre\n class="x">\n' + receipt(183, 'b'*40) + '</pre>\n')

    def test_23_plain_singleline_raw_hidden(self):
        self.bad(self.hidden('<pre>\n', '</pre>\n'))

    def test_24_excessive_pending_tag(self):
        self.bad('<pre\n title="' + ('x' * 12000) + '\n' + receipt(183, 'b'*40), 'HTML_TAG_TOO_LONG')


if __name__ == '__main__':
    unittest.main()
