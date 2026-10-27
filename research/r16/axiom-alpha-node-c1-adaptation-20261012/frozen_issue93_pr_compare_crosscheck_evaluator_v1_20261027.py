#!/usr/bin/env python3
"""Frozen separate-process oracle for a caller-supplied PR/compare/receipt C1 witness.

Fixtures are synthetic, anchored to public PR #142 identifiers. The oracle does
not authenticate API origin or prove main currently points to the compared SHA.
"""
import copy
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest

HERE = Path(__file__).resolve().parent
CANDIDATE = Path(os.environ.get('AXIOM_CANDIDATE', HERE / 'alpha_issue93_pr_compare_crosscheck_v1_20261027.py'))
MAIN = '2ac039d555077f60c6949c24572878885e8a4d82'
PARENT = '0fe6c909c57f905f63ca397ab4e84a32f10e1f54'
HEAD = 'e14c8e356dcfab1296566e520c3b67c44933d3fe'
REPO = 'nexusomegac27/NEXUS-OMEGA-EVIDENCE'
ROOT = 'research/r16/axiom-alpha-node-c1-adaptation-20261012/'


def sample():
    body = ('OBJECT=NEXUS_OMEGA_AXIOM_ALPHA_HANDOFF_CENSUS_INPUT_BUDGET_V4_20261027_R0\n'
            'CLAIM_CEILING=C1_DESCRIPTIVE_ONLY\n'
            'PREDECESSOR_ISSUE93_RECEIPT=6431537398\n'
            'PINNED_MAIN_BEFORE=' + PARENT + '\n'
            'PR142=https://github.com/' + REPO + '/pull/142\n'
            'PR142_HEAD_AT_MERGE=' + HEAD + '\n'
            'ACTUAL_MAIN_READBACK=' + MAIN + '\n'
            'ACTUAL_MAIN_PARENT=' + PARENT + '\n'
            'MAIN_CHANGED_FILES=2_ADDED_0_MODIFIED_0_DELETED\n')
    return {
        'repository': REPO, 'issue_number': 93,
        'receipt': {'id': 6432432648, 'actor_login': 'nexusomegac27', 'body': body},
        'pr': {'number': 142, 'state': 'closed', 'merged': True, 'base': 'main',
               'base_sha': PARENT, 'head_sha': HEAD, 'merge_commit_sha': MAIN,
               'head_repo_full_name': REPO},
        'compare': {'repository_full_name': REPO, 'base': PARENT, 'head': MAIN,
                    'status': 'ahead', 'ahead_by': 1, 'behind_by': 0,
                    'total_commits': 1, 'base_commit': {'sha': PARENT},
                    'merge_base_commit': {'sha': PARENT},
                    'files': [{'filename': ROOT + 'alpha_handoff_coverage_census_input_budget_v4_20261027.py', 'status': 'added'},
                              {'filename': ROOT + 'frozen_handoff_coverage_input_budget_evaluator_v4_20261027.py', 'status': 'added'}]}}


def run(payload):
    raw = payload if isinstance(payload, bytes) else json.dumps(payload, separators=(',', ':')).encode()
    return subprocess.run([sys.executable, str(CANDIDATE)], input=raw,
                          capture_output=True, timeout=15)


class FrozenCrossSourceOracle(unittest.TestCase):
    def good(self, data):
        p = run(data)
        self.assertEqual(p.returncode, 0, p.stderr.decode(errors='replace'))
        out = json.loads(p.stdout)
        self.assertEqual(out['state'], 'PASS_PR_COMPARE_RECEIPT_CONSISTENCY_C1')
        self.assertEqual(out['claim_ceiling'], 'C1_DESCRIPTIVE_ONLY')
        self.assertEqual(out['api_origin_authenticated'], False)
        self.assertEqual(out['live_main_verified'], False)
        self.assertEqual(out['checked_files'], 2)

    def bad(self, data):
        p = run(data)
        self.assertEqual(p.returncode, 2, (p.returncode, p.stderr.decode(errors='replace')[:300]))
        self.assertIn(b'FAIL_CLOSED:', p.stderr)
        self.assertNotIn(b'"state"', p.stdout)

    def mutate(self, fn):
        p = sample()
        fn(p)
        self.bad(p)

    def test_01_positive_exact_cross_source(self): self.good(sample())
    def test_02_forged_receipt_main(self):
        self.mutate(lambda p: p['receipt'].update(body=p['receipt']['body'].replace(MAIN, 'a'*40)))
    def test_03_forged_receipt_parent(self):
        self.mutate(lambda p: p['receipt'].update(body=p['receipt']['body'].replace(PARENT, 'b'*40)))
    def test_04_wrong_pr_url(self):
        self.mutate(lambda p: p['receipt'].update(body=p['receipt']['body'].replace('/pull/142', '/pull/141')))
    def test_05_wrong_head(self):
        self.mutate(lambda p: p['pr'].update(head_sha='c'*40))
    def test_06_wrong_merge_sha(self):
        self.mutate(lambda p: p['pr'].update(merge_commit_sha='d'*40))
    def test_07_wrong_compare_ahead(self):
        self.mutate(lambda p: p['compare'].update(ahead_by=2))
    def test_08_wrong_compare_base(self):
        self.mutate(lambda p: p['compare'].update(base='e'*40))
    def test_09_modified_file_not_additive(self):
        self.mutate(lambda p: p['compare']['files'][0].update(status='modified'))
    def test_10_duplicate_receipt_field(self):
        self.mutate(lambda p: p['receipt'].update(body=p['receipt']['body']+'ACTUAL_MAIN_READBACK='+MAIN+'\n'))
    def test_11_duplicate_json_key(self):
        raw = json.dumps(sample(), separators=(',', ':')).encode()
        self.bad(raw.replace(b'"issue_number":93', b'"issue_number":93,"issue_number":93', 1))
    def test_12_claim_promotion(self):
        self.mutate(lambda p: p['receipt'].update(body=p['receipt']['body'].replace('C1_DESCRIPTIVE_ONLY','C2')))
    def test_13_wrong_owner_claim(self):
        self.mutate(lambda p: p['receipt'].update(actor_login='external-bot'))
    def test_14_unmerged_pr(self):
        self.mutate(lambda p: p['pr'].update(merged=False))
    def test_15_oversized_json(self):
        self.bad(json.dumps(sample()).encode()+b' '*(1048577))
    def test_16_missing_file(self):
        self.mutate(lambda p: p['compare'].update(files=p['compare']['files'][:1]))


if __name__ == '__main__':
    unittest.main()
