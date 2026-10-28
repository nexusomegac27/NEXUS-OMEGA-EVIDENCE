#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Independent frozen subprocess oracle for the offline API-shaped crosscheck."""
import copy
import json
import os
import subprocess
import sys
import unittest

TARGET = os.environ.get('AXIOM_API_CROSSCHECK_CANDIDATE', 'alpha_issue93_api_crosscheck_v1_20261028.py')
REPO = 'nexusomegac27/NEXUS-OMEGA-EVIDENCE'
BASE = '1c434c820c30d662ea8d557c7a5b06bb90f75823'
HEAD = '6e700be6fd408c3d78d3d7e08619b635de92966f'
PATH = 'research/r16/axiom-alpha-node-c1-adaptation-20261012/alpha_receipt_order_guard_v1_20261028.py'


def fixture():
    issue = f'https://api.github.com/repos/{REPO}/issues/93'
    return {'object': 'NEXUS_OMEGA_ALPHA_ISSUE93_API_CROSSCHECK_V1',
            'repository': REPO,
            'comment': {'id': 6478246029, 'issue_url': issue, 'user': {'login': 'nexusomegac27'},
                        'created_at': '2026-10-28T19:14:07Z', 'updated_at': '2026-10-28T19:14:07Z',
                        'body': f'PR=https://github.com/{REPO}/pull/178\n'
                                f'ACTUAL_MAIN_READBACK={HEAD}\nPINNED_MAIN_BEFORE={BASE}\n'
                                'PREDECESSOR_ISSUE93_RECEIPT=6477928081\n'
                                'CLAIM_CEILING=C1_DESCRIPTIVE_ONLY'},
            'predecessor_comment': {'id': 6477928081, 'issue_url': issue,
                                    'user': {'login': 'nexusomegac27'},
                                    'created_at': '2026-10-28T18:59:30Z',
                                    'updated_at': '2026-10-28T18:59:30Z'},
            'pull': {'number': 178, 'user': {'login': 'nexusomegac27'},
                     'merged_at': '2026-10-28T19:13:22Z', 'merge_commit_sha': HEAD},
            'commit': {'sha': HEAD, 'parents': [{'sha': BASE}],
                       'commit': {'verification': {'verified': True, 'reason': 'valid'}},
                       'files': [{'filename': PATH, 'status': 'added'}]},
            'branch': {'commit': {'sha': HEAD}},
            'pr_files': [{'filename': PATH, 'status': 'added'}]}


def run(x):
    raw = x if type(x) is bytes else json.dumps(x, sort_keys=True).encode('utf-8')
    return subprocess.run([sys.executable, TARGET], input=raw, stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, timeout=8)


class FrozenOracle(unittest.TestCase):
    def accept(self, x):
        p = run(x)
        self.assertEqual(p.returncode, 0, p.stderr.decode())
        y = json.loads(p.stdout)
        self.assertEqual(y['state'], 'C1_SCOPED_API_SHAPED_METADATA_CROSSCHECK_PASS')
        self.assertIs(y['api_origin_authenticated'], False)
        self.assertIs(y['original_file_bytes_verified'], False)
        self.assertIs(y['independent_expert_ack'], False)
        self.assertEqual(y['project_automation_rate'], 'NOT_COMPUTABLE')
        self.assertEqual(y['project_readback_rate'], 'NOT_COMPUTABLE')
    def reject(self, x, code):
        p = run(x)
        self.assertEqual(p.returncode, 2, p.stdout.decode())
        self.assertEqual(p.stdout, b'')
        self.assertIn(code.encode(), p.stderr)
    def test_valid_observed_shaped(self): self.accept(fixture())
    def test_valid_extra_api_fields(self):
        x = fixture(); x['commit']['extra_rest_field'] = 'safe'; self.accept(x)
    def test_forged_main(self):
        x = fixture(); x['comment']['body'] = x['comment']['body'].replace(HEAD, BASE)
        self.reject(x, 'MAIN_PR_COMMIT_MISMATCH')
    def test_forged_pr_merge(self):
        x = fixture(); x['pull']['merge_commit_sha'] = BASE
        self.reject(x, 'MAIN_PR_COMMIT_MISMATCH')
    def test_wrong_main_ref(self):
        x = fixture(); x['branch']['commit']['sha'] = BASE
        self.reject(x, 'MAIN_PR_COMMIT_MISMATCH')
    def test_wrong_parent(self):
        x = fixture(); x['commit']['parents'][0]['sha'] = HEAD
        self.reject(x, 'MAIN_PARENT_MISMATCH')
    def test_forged_actor(self):
        x = fixture(); x['comment']['user']['login'] = 'unregistered'
        self.reject(x, 'ISSUE_ACTOR_OR_SCOPE_MISMATCH')
    def test_missing_predecessor(self):
        x = fixture(); x['predecessor_comment']['id'] = 6476336042
        self.reject(x, 'RECEIPT_PARENT_MISMATCH')
    def test_edited_comment(self):
        x = fixture(); x['comment']['updated_at'] = '2026-10-28T19:15:00Z'
        self.reject(x, 'RECEIPT_TIME_OR_EDIT_MISMATCH')
    def test_bad_signature(self):
        x = fixture(); x['commit']['commit']['verification']['verified'] = False
        self.reject(x, 'COMMIT_SIGNATURE_UNVERIFIED')
    def test_changed_files(self):
        x = fixture(); x['pr_files'][0]['filename'] += '.tampered'
        self.reject(x, 'PR_COMMIT_FILE_MISMATCH')
    def test_duplicate_receipt_field(self):
        x = fixture(); x['comment']['body'] += '\nCLAIM_CEILING=C1_DESCRIPTIVE_ONLY'
        self.reject(x, 'DUPLICATE_RECEIPT_FIELD')
    def test_claim_promotion(self):
        x = fixture(); x['comment']['body'] = x['comment']['body'].replace('C1_DESCRIPTIVE_ONLY', 'C2')
        self.reject(x, 'CLAIM_PROMOTION')
    def test_duplicate_json_key(self):
        self.reject(b'{"object":"x","object":"y"}', 'DUPLICATE_JSON_KEY')
    def test_nonfinite(self):
        self.reject(json.dumps(fixture()).replace('"number": 178', '"number": NaN').encode(), 'NONFINITE_JSON')
    def test_wrong_issue(self):
        x = fixture(); x['comment']['issue_url'] = x['comment']['issue_url'].replace('/93','/92')
        self.reject(x, 'ISSUE_ACTOR_OR_SCOPE_MISMATCH')


if __name__ == '__main__':
    unittest.main()
