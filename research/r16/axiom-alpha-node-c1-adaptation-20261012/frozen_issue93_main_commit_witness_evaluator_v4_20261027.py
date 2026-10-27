#!/usr/bin/env python3
"""Frozen independent subprocess oracle for Issue #93 main-commit witness V4.

The evaluator must be GitHub-committed BEFORE the V4 candidate. It uses a
synthetic fixture keyed to PR #145's immutable identifiers, not a live API
response. It is not API authentication, scientific approval, or a production
GitHub-to-WWW proof. AXIOM_CANDIDATE can point to a deliberately weakened mutant.
"""
import copy
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest

HERE = Path(__file__).resolve().parent
CANDIDATE = Path(os.environ.get('AXIOM_CANDIDATE', HERE / 'alpha_issue93_main_commit_witness_v4_20261027.py'))
REPO = 'nexusomegac27/NEXUS-OMEGA-EVIDENCE'
ROOT = 'research/r16/axiom-alpha-node-c1-adaptation-20261012/'
PARENT = '3ebcae92ac943c823da2b94e6e8226631b2d24e0'
MAIN = '4e06b90c79f9dd4eeb841b6fe0c7097dcad80225'
HEAD = 'f02e417cc110641c18b52a79c7b89d060aa28342'
FILE_A = ROOT + 'alpha_issue93_pr_compare_crosscheck_v3_20261027.py'
FILE_B = ROOT + 'frozen_issue93_portable_path_evaluator_v3_20261027.py'
BLOB_A = 'b3e31eb9d8094a493065c1f66f73a605b3aaa145'
BLOB_B = 'aa1670a79977ecd5ae287e0353acd33e6e8d4f70'


def fixture():
    body = ('OBJECT=NEXUS_OMEGA_AXIOM_ALPHA_ISSUE93_PORTABLE_PATH_INTEGRITY_V3_20261027_R0\n'
            'CLAIM_CEILING=C1_DESCRIPTIVE_ONLY\n'
            'PINNED_MAIN_BEFORE=' + PARENT + '\n'
            'PR145=https://github.com/' + REPO + '/pull/145\n'
            'PR145_HEAD_AT_MERGE=' + HEAD + '\n'
            'ACTUAL_MAIN_READBACK=' + MAIN + '\n'
            'ACTUAL_MAIN_PARENT=' + PARENT + '\n'
            'MAIN_CHANGED_FILES=2_ADDED_0_MODIFIED_0_DELETED\n')
    return {'repository': REPO, 'issue_number': 93,
            'receipt': {'id': 6434552312, 'actor_login': 'nexusomegac27', 'body': body},
            'pr': {'number': 145, 'state': 'closed', 'merged': True, 'base': 'main',
                   'base_sha': PARENT, 'head_sha': HEAD, 'merge_commit_sha': MAIN,
                   'head_repo_full_name': REPO},
            'compare': {'repository_full_name': REPO, 'status': 'ahead',
                        'base': PARENT, 'head': MAIN, 'ahead_by': 1, 'behind_by': 0,
                        'total_commits': 1, 'base_commit': {'sha': PARENT},
                        'merge_base_commit': {'sha': PARENT},
                        'files': [{'filename': FILE_A, 'status': 'added'},
                                  {'filename': FILE_B, 'status': 'added'}]},
            'branch': {'name': 'main', 'commit': {'sha': MAIN}},
            'commit': {'sha': MAIN, 'parents': [{'sha': PARENT}],
                       'files': [{'filename': FILE_A, 'status': 'added', 'sha': BLOB_A},
                                 {'filename': FILE_B, 'status': 'added', 'sha': BLOB_B}]}}


def run(payload):
    return subprocess.run([sys.executable, str(CANDIDATE)],
                          input=json.dumps(payload, ensure_ascii=True, separators=(',', ':')).encode('ascii'),
                          capture_output=True, timeout=12)


class MainCommitWitnessOracle(unittest.TestCase):
    def good(self, payload):
        r = run(payload)
        self.assertEqual(r.returncode, 0, (r.returncode, r.stderr[:200]))
        d = json.loads(r.stdout)
        self.assertEqual(d['state'], 'PASS_MAIN_COMMIT_WITNESS_CONSISTENCY_C1')
        self.assertEqual(d['checked_commit_blobs'], 2)
        self.assertFalse(d['api_origin_authenticated'])
        self.assertFalse(d['live_main_verified'])
        self.assertEqual(d['project_automation_rate'], 'NOT_COMPUTABLE')

    def bad(self, payload):
        r = run(payload)
        self.assertEqual(r.returncode, 2, (r.returncode, r.stderr[:200]))
        self.assertIn(b'FAIL_CLOSED:', r.stderr)
        self.assertNotIn(b'"state"', r.stdout)

    # Positive controls. Order of file arrays is not semantic identity.
    def test_01_valid_two_file_witness(self): self.good(fixture())
    def test_02_reordered_commit_files(self):
        p = fixture(); p['commit']['files'].reverse(); self.good(p)
    def test_03_explicit_complete_flags(self):
        p = fixture(); p['commit']['too_large'] = False; p['compare']['too_large'] = False; self.good(p)
    def test_04_additional_api_metadata(self):
        p = fixture(); p['commit']['html_url'] = 'https://github.com/' + REPO + '/commit/' + MAIN; self.good(p)

    # V3 checks only receipt+PR+compare; these mutations leave that triple intact.
    def test_05_reject_wrong_branch_tip(self):
        p = fixture(); p['branch']['commit']['sha'] = '0' * 40; self.bad(p)
    def test_06_reject_wrong_branch_name(self):
        p = fixture(); p['branch']['name'] = 'codex/fake'; self.bad(p)
    def test_07_reject_wrong_commit_sha(self):
        p = fixture(); p['commit']['sha'] = '0' * 40; self.bad(p)
    def test_08_reject_wrong_commit_parent(self):
        p = fixture(); p['commit']['parents'][0]['sha'] = '0' * 40; self.bad(p)
    def test_09_reject_multiple_commit_parents(self):
        p = fixture(); p['commit']['parents'].append({'sha': '1' * 40}); self.bad(p)
    def test_10_reject_missing_commit_file(self):
        p = fixture(); p['commit']['files'].pop(); self.bad(p)
    def test_11_reject_extra_commit_file(self):
        p = fixture(); p['commit']['files'].append({'filename': ROOT + 'extra.py', 'status': 'added', 'sha': '1'*40}); self.bad(p)
    def test_12_reject_mismatched_commit_filename(self):
        p = fixture(); p['commit']['files'][0]['filename'] = ROOT + 'different.py'; self.bad(p)
    def test_13_reject_modified_commit_file(self):
        p = fixture(); p['commit']['files'][0]['status'] = 'modified'; self.bad(p)
    def test_14_reject_missing_blob_sha(self):
        p = fixture(); p['commit']['files'][0].pop('sha'); self.bad(p)
    def test_15_reject_malformed_blob_sha(self):
        p = fixture(); p['commit']['files'][0]['sha'] = 'xyz'; self.bad(p)
    def test_16_reject_duplicate_commit_filename(self):
        p = fixture(); p['commit']['files'][1]['filename'] = FILE_A; self.bad(p)
    def test_17_reject_explicit_truncated_commit_files(self):
        p = fixture(); p['commit']['too_large'] = True; self.bad(p)
    def test_18_reject_null_branch_pointer(self):
        p = fixture(); p['branch']['commit'] = None; self.bad(p)


if __name__ == '__main__':
    unittest.main()
