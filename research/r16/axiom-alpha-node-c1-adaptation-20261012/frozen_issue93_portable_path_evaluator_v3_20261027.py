#!/usr/bin/env python3
"""Frozen separate-process oracle: portable GitHub compare path identity C1.

Source fixture is synthetic and references the already published PR #142.
Freeze this evaluator on a dedicated GitHub branch BEFORE authoring V3.
It tests file-path portability only; it does not authenticate API origin,
prove GitHub main parity, or authorize runtime integration.
"""
import copy
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest

HERE = Path(__file__).resolve().parent
CANDIDATE = Path(os.environ.get('AXIOM_CANDIDATE', HERE / 'alpha_issue93_pr_compare_crosscheck_v3_20261027.py'))
REPO = 'nexusomegac27/NEXUS-OMEGA-EVIDENCE'
ROOT = 'research/r16/axiom-alpha-node-c1-adaptation-20261012/'
PARENT = '0fe6c909c57f905f63ca397ab4e84a32f10e1f54'
MAIN = '2ac039d555077f60c6949c24572878885e8a4d82'
HEAD = 'e14c8e356dcfab1296566e520c3b67c44933d3fe'


def fixture():
    body = ('OBJECT=NEXUS_OMEGA_AXIOM_ALPHA_HANDOFF_CENSUS_INPUT_BUDGET_V4_20261027_R0\n'
            'CLAIM_CEILING=C1_DESCRIPTIVE_ONLY\n'
            'PINNED_MAIN_BEFORE=' + PARENT + '\n'
            'PR142=https://github.com/' + REPO + '/pull/142\n'
            'PR142_HEAD_AT_MERGE=' + HEAD + '\n'
            'ACTUAL_MAIN_READBACK=' + MAIN + '\n'
            'ACTUAL_MAIN_PARENT=' + PARENT + '\n'
            'MAIN_CHANGED_FILES=2_ADDED_0_MODIFIED_0_DELETED\n')
    return {'repository': REPO, 'issue_number': 93,
            'receipt': {'id': 6432432648, 'actor_login': 'nexusomegac27', 'body': body},
            'pr': {'number': 142, 'state': 'closed', 'merged': True, 'base': 'main',
                   'base_sha': PARENT, 'head_sha': HEAD, 'merge_commit_sha': MAIN,
                   'head_repo_full_name': REPO},
            'compare': {'repository_full_name': REPO, 'status': 'ahead',
                        'base': PARENT, 'head': MAIN, 'ahead_by': 1, 'behind_by': 0,
                        'total_commits': 1, 'base_commit': {'sha': PARENT},
                        'merge_base_commit': {'sha': PARENT},
                        'files': [
                            {'filename': ROOT + 'alpha_handoff_coverage_census_input_budget_v4_20261027.py', 'status': 'added'},
                            {'filename': ROOT + 'frozen_handoff_coverage_input_budget_evaluator_v4_20261027.py', 'status': 'added'}]}}


def run(p):
    return subprocess.run([sys.executable, str(CANDIDATE)],
                          input=json.dumps(p, ensure_ascii=True, separators=(',', ':')).encode('ascii'),
                          capture_output=True, timeout=12)


class PortablePathOracle(unittest.TestCase):
    def good(self, p):
        r = run(p)
        self.assertEqual(r.returncode, 0, (r.returncode, r.stderr[:250]))
        d = json.loads(r.stdout)
        self.assertEqual(d['state'], 'PASS_PR_COMPARE_RECEIPT_CONSISTENCY_C1')
        self.assertEqual(d['checked_files'], 2)
        self.assertFalse(d['api_origin_authenticated'])
        self.assertFalse(d['live_main_verified'])
        self.assertEqual(d['project_automation_rate'], 'NOT_COMPUTABLE')

    def bad(self, p):
        r = run(p)
        self.assertEqual(r.returncode, 2, (r.returncode, r.stderr[:250]))
        self.assertIn(b'FAIL_CLOSED:', r.stderr)
        self.assertNotIn(b'"state"', r.stdout)

    def one(self, path):
        p = fixture()
        p['compare']['files'][0]['filename'] = ROOT + path
        return p

    def two(self, a, b):
        p = fixture()
        p['compare']['files'][0]['filename'] = ROOT + a
        p['compare']['files'][1]['filename'] = ROOT + b
        return p

    # Positive controls: preserve legitimate, portable names and old semantics.
    def test_01_positive_original(self): self.good(fixture())
    def test_02_positive_nested(self): self.good(self.one('sub/valid.py'))
    def test_03_positive_unicode_nfc(self): self.good(self.one('prüfung_ä.py'))
    def test_04_positive_emoji(self): self.good(self.one('sample_🧪.py'))
    def test_05_positive_nonreserved_prefix(self): self.good(self.one('consolidate.py'))
    def test_06_positive_lpt10(self): self.good(self.one('lpt10.py'))
    def test_07_positive_dot_inside(self): self.good(self.one('sample.v2.py'))
    def test_08_positive_distinct_names(self): self.good(self.two('alpha.py', 'beta.py'))
    def test_09_positive_compare_flag_false(self):
        p = fixture(); p['compare']['too_large'] = False; self.good(p)

    # Adversarial: V2 may pass these, although Windows or Unicode identity is ambiguous.
    def test_10_reject_bidi_override(self): self.bad(self.one('receipt_\u202eyp.txt'))
    def test_11_reject_zero_width_format(self): self.bad(self.one('receipt_\u200b.py'))
    def test_12_reject_unicode_c1_control(self): self.bad(self.one('receipt_\u0085.py'))
    def test_13_reject_unpaired_surrogate(self): self.bad(self.one('receipt_\ud800.py'))
    def test_14_reject_non_nfc_combining(self): self.bad(self.one('pru\u0308fung.py'))
    def test_15_reject_windows_con(self): self.bad(self.one('CON.py'))
    def test_16_reject_windows_nul_nested(self): self.bad(self.one('sub/NUL.txt'))
    def test_17_reject_windows_com1(self): self.bad(self.one('COM1.log'))
    def test_18_reject_windows_lpt9(self): self.bad(self.one('LPT9'))
    def test_19_reject_windows_ads_colon(self): self.bad(self.one('report.py:stream'))
    def test_20_reject_windows_wildcard(self): self.bad(self.one('file?.py'))
    def test_21_reject_windows_trailing_dot(self): self.bad(self.one('sub./file.py'))
    def test_22_reject_windows_trailing_space(self): self.bad(self.one('sub /file.py'))
    def test_23_reject_casefold_collision(self): self.bad(self.two('Report.py', 'report.py'))
    def test_24_reject_unicode_casefold_collision(self): self.bad(self.two('straße.py', 'strasse.py'))
    def test_25_reject_existing_parent_escape(self): self.bad(self.one('sub/../file.py'))
    def test_26_reject_existing_partial_compare(self):
        p = fixture(); p['compare']['too_large'] = True; self.bad(p)
    def test_27_reject_existing_duplicate_path(self): self.bad(self.two('same.py', 'same.py'))
    def test_28_reject_existing_modified(self):
        p = fixture(); p['compare']['files'][0]['status'] = 'modified'; self.bad(p)


if __name__ == '__main__':
    unittest.main()
