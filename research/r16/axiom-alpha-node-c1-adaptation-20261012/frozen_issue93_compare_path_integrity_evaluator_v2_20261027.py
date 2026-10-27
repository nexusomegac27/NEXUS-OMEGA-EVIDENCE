#!/usr/bin/env python3
"""Independent frozen black-box oracle for Issue #93 compare path-integrity C1.

Fixtures are synthetic and use pinned public PR #142 IDs. This oracle is not
GitHub actor authentication, CI, a scientific claim, or live-main verification.
Commit this file before creating the candidate; do not alter it thereafter.
"""
import copy
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest

HERE = Path(__file__).resolve().parent
CANDIDATE = Path(os.environ.get('AXIOM_CANDIDATE', HERE / 'alpha_issue93_pr_compare_crosscheck_v2_20261027.py'))
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


def execute(data):
    return subprocess.run([sys.executable, str(CANDIDATE)],
                          input=json.dumps(data, separators=(',', ':')).encode('utf-8'),
                          capture_output=True, timeout=15)


class PathIntegrityOracle(unittest.TestCase):
    def good(self, payload):
        r = execute(payload)
        self.assertEqual(r.returncode, 0, (r.returncode, r.stderr[:200]))
        out = json.loads(r.stdout)
        self.assertEqual(out['state'], 'PASS_PR_COMPARE_RECEIPT_CONSISTENCY_C1')
        self.assertFalse(out['api_origin_authenticated'])
        self.assertFalse(out['live_main_verified'])
        self.assertEqual(out['checked_files'], 2)

    def bad(self, payload):
        r = execute(payload)
        self.assertEqual(r.returncode, 2, (r.returncode, r.stderr[:200]))
        self.assertIn(b'FAIL_CLOSED:', r.stderr)
        self.assertNotIn(b'"state"', r.stdout)

    def changed(self, path):
        p = fixture()
        p['compare']['files'][0]['filename'] = path
        return p

    def test_01_positive_exact(self): self.good(fixture())
    def test_02_positive_subdirectory(self): self.good(self.changed(ROOT + 'sub/valid.py'))
    def test_03_positive_unicode(self): self.good(self.changed(ROOT + 'pruefung_ä.py'))
    def test_04_reject_parent_escape(self): self.bad(self.changed(ROOT + '../docs/rogue.py'))
    def test_05_reject_internal_parent(self): self.bad(self.changed(ROOT + 'sub/../rogue.py'))
    def test_06_reject_dot_segment(self): self.bad(self.changed(ROOT + './rogue.py'))
    def test_07_reject_empty_segment(self): self.bad(self.changed(ROOT + 'sub//rogue.py'))
    def test_08_reject_trailing_slash(self): self.bad(self.changed(ROOT + 'rogue.py/'))
    def test_09_reject_backslash(self): self.bad(self.changed(ROOT + 'sub\\rogue.py'))
    def test_10_reject_nul(self): self.bad(self.changed(ROOT + 'rogue\x00.py'))
    def test_11_reject_control(self): self.bad(self.changed(ROOT + 'rogue\x1f.py'))
    def test_12_reject_partial_compare(self):
        p = fixture(); p['compare']['too_large'] = True; self.bad(p)
    def test_13_positive_complete_flag(self):
        p = fixture(); p['compare']['too_large'] = False; self.good(p)
    def test_14_reject_modified_file(self):
        p = fixture(); p['compare']['files'][0]['status'] = 'modified'; self.bad(p)
    def test_15_reject_wrong_main(self):
        p = fixture(); p['compare']['head'] = 'f' * 40; self.bad(p)


if __name__ == '__main__':
    unittest.main()
