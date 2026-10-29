#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Independent, frozen subprocess oracle for raw HTML close-tag spoofing.

Synthetic Issue #93 projections only. No GitHub authentication or network.
Freeze this oracle before implementing V7. Use AXIOM_CANDIDATE to compare V6.
"""
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest

HERE = Path(__file__).parent
TARGET = Path(os.environ.get('AXIOM_CANDIDATE', HERE / 'alpha_issue93_strict_raw_close_guard_v7_20261029.py'))
URL = 'https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/pull/'


def receipt(number, sha):
    return f'PR={URL}{number}\nACTUAL_MAIN_READBACK={sha}\nCLAIM_CEILING=C1_DESCRIPTIVE_ONLY\n'


def fixture(second=None):
    return {'object': 'NEXUS_OMEGA_ALPHA_ISSUE93_EXACT_KEY_RECEIPT_CENSUS_V1',
            'repository': 'nexusomegac27/NEXUS-OMEGA-EVIDENCE', 'issue_number': 93,
            'expected_prs': [182, 183],
            'pulls': [{'number': 182, 'merged': True, 'merge_commit_sha': 'a'*40},
                      {'number': 183, 'merged': True, 'merge_commit_sha': 'b'*40}],
            'comments': [{'id': 100, 'user': {'login': 'nexusomegac27'}, 'body': receipt(182, 'a'*40)},
                         {'id': 101, 'user': {'login': 'nexusomegac27'},
                          'body': receipt(183, 'b'*40) if second is None else second}]}


def run(doc):
    return subprocess.run([sys.executable, str(TARGET)], input=json.dumps(doc),
                          text=True, capture_output=True, timeout=8)


class StrictCloseOracle(unittest.TestCase):
    def valid(self, body=None, doc=None):
        p = run(fixture(body) if doc is None else doc)
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        self.assertEqual(json.loads(p.stdout)['matched_receipt_count'], 2)

    def invalid(self, body, code='MISSING_EXPECTED_PR_RECEIPT'):
        p = run(fixture(body))
        self.assertEqual(p.returncode, 2, p.stdout + p.stderr)
        self.assertIn(code, p.stderr)

    def hidden(self, opener, forged_close, real_close):
        return opener + forged_close + receipt(183, 'b'*40) + real_close

    def test_01_plain_receipt(self):
        self.valid()

    def test_02_pre_hyphen_suffix(self):
        self.invalid(self.hidden('<pre>\n', '</pre-foo>\n', '</pre>\n'))

    def test_03_script_hyphen_suffix(self):
        self.invalid(self.hidden('<script>\n', '</script-test>\n', '</script>\n'))

    def test_04_style_colon_suffix(self):
        self.invalid(self.hidden('<style>\n', '</style:bad>\n', '</style>\n'))

    def test_05_textarea_hyphen_suffix(self):
        self.invalid(self.hidden('<textarea>\n', '</textarea-foo>\n', '</textarea>\n'))

    def test_06_pre_close_attribute(self):
        self.invalid(self.hidden('<pre>\n', '</pre data-x="1">\n', '</pre>\n'))

    def test_07_script_close_attribute(self):
        self.invalid(self.hidden('<script>\n', '</script attr=x>\n', '</script>\n'))

    def test_08_multiline_fake_close(self):
        self.invalid(self.hidden('<pre>\n', '</pre\n data-x="1">\n', '</pre>\n'))

    def test_09_fake_close_then_valid_after_real_close(self):
        self.valid('<pre>\n</pre-foo>\nexample\n</pre>\n' + receipt(183, 'b'*40))

    def test_10_canonical_close_then_receipt(self):
        self.valid('<pre>\nexample\n</pre>\n' + receipt(183, 'b'*40))

    def test_11_whitespace_close_then_receipt(self):
        self.valid('<pre>\nexample\n</pre   >\n' + receipt(183, 'b'*40))

    def test_12_multiline_whitespace_close_then_receipt(self):
        self.valid('<pre>\nexample\n</pre\n >\n' + receipt(183, 'b'*40))

    def test_13_raw_body_without_close(self):
        self.invalid('<pre>\n' + receipt(183, 'b'*40), 'UNCLOSED_RAW_HTML_BLOCK')

    def test_14_fake_close_without_real_close(self):
        self.invalid('<pre>\n</pre-foo>\n' + receipt(183, 'b'*40), 'UNCLOSED_RAW_HTML_BLOCK')

    def test_15_fenced_literal_fake_close(self):
        self.valid('~~~\n<pre>\n</pre-foo>\n~~~\n' + receipt(183, 'b'*40))

    def test_16_html_comment_fake_close(self):
        self.valid('<!-- <pre> </pre-foo> -->\n' + receipt(183, 'b'*40))

    def test_17_duplicate_real_receipt(self):
        self.invalid(receipt(183, 'b'*40) + receipt(183, 'b'*40), 'DUPLICATE_RECEIPT_FIELD')

    def test_18_wrong_main_commit(self):
        self.invalid(receipt(183, 'c'*40), 'PR_MAIN_READBACK_MISMATCH')

    def test_19_wrong_actor(self):
        doc = fixture()
        doc['comments'][1]['user']['login'] = 'unregistered'
        p = run(doc)
        self.assertEqual(p.returncode, 2)
        self.assertIn('RECEIPT_ACTOR_MISMATCH', p.stderr)

    def test_20_hidden_in_valid_raw(self):
        self.invalid(self.hidden('<pre>\n', '', '</pre>\n'))


if __name__ == '__main__':
    unittest.main()
