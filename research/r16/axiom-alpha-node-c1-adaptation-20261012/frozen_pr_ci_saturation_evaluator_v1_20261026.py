#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Independent, frozen C1 evaluator for PR CI saturation triage.

The evaluator is committed before the candidate and never authorizes merge.
"""
import importlib.util
import sys
import unittest
from copy import deepcopy
from pathlib import Path

if len(sys.argv) != 2:
    raise SystemExit('usage: evaluator.py CANDIDATE_PATH')
spec = importlib.util.spec_from_file_location('candidate_under_test', Path(sys.argv[1]))
candidate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(candidate)
SHA = 'd355400dabed3c280e1fce5030cab69ea099428b'
HEAD = 'e81030061ff5349064d7c400d3ba2d35b70ab8a7'
NAMES = ('validate-anchor', 'validate-scientific-communication',
         'validate-scientific-ledger', 'validate-a83-framework-hardening',
         'Validate repository structure', 'R27-E External Agent Structural Firewall')

def snapshot():
    return {'repository': 'nexusomegac27/NEXUS-OMEGA-EVIDENCE',
            'pr_number': 124, 'owner_login': 'nexusomegac27',
            'main_sha': SHA, 'base_sha': SHA, 'head_sha': HEAD,
            'changed_files': 138,
            'runs': [{'name': name, 'head_sha': HEAD,
                      'status': 'completed',
                      'conclusion': 'failure' if name.startswith('R27-E') else 'success'}
                     for name in NAMES],
            'r27e_failure_reason': 'TOO_MANY_PR_CHANGES'}

class FrozenOracle(unittest.TestCase):
    def test_01_observed_138_and_failure_blocks_accumulation(self):
        self.assertEqual(candidate.triage(snapshot())['status'], 'HOLD_ACCUMULATION_C1')
    def test_02_139_still_blocks(self):
        s=snapshot();s['changed_files']=139
        self.assertEqual(candidate.triage(s)['status'], 'HOLD_ACCUMULATION_C1')
    def test_03_no_failure_not_size_only(self):
        s=snapshot();s['runs'][-1]['conclusion']='success';s['r27e_failure_reason']=None
        self.assertEqual(candidate.triage(s)['status'], 'CI_CLEAR_NOT_MERGE_AUTHORITY')
    def test_04_missing_required_check_fails_closed(self):
        s=snapshot();s['runs'].pop()
        self.assertEqual(candidate.triage(s)['status'], 'HOLD_INCOMPLETE_CI')
    def test_05_wrong_commit_fails_closed(self):
        s=snapshot();s['runs'][0]['head_sha']='a'*40
        self.assertEqual(candidate.triage(s)['status'], 'HOLD_SOURCE_DRIFT')
    def test_06_duplicate_check_fails_closed(self):
        s=snapshot();s['runs'].append(deepcopy(s['runs'][0]))
        self.assertEqual(candidate.triage(s)['status'], 'HOLD_INCOMPLETE_CI')
    def test_07_pending_check_not_success(self):
        s=snapshot();s['runs'][0]['status']='in_progress';s['runs'][0]['conclusion']=None
        self.assertEqual(candidate.triage(s)['status'], 'HOLD_PENDING_CI')
    def test_08_unknown_failure_cannot_claim_cap(self):
        s=snapshot();s['r27e_failure_reason']='UNKNOWN'
        self.assertEqual(candidate.triage(s)['status'], 'HOLD_FAILED_CI')
    def test_09_bool_count_rejected(self):
        s=snapshot();s['changed_files']=True
        self.assertEqual(candidate.triage(s)['status'], 'HOLD_INVALID_METADATA')
    def test_10_nonowner_scope_denied(self):
        s=snapshot();s['owner_login']='external-bot'
        self.assertEqual(candidate.triage(s)['status'], 'HOLD_ACTOR_SCOPE')
    def test_11_no_implicit_merge_authority(self):
        s=snapshot();s['runs'][-1]['conclusion']='success';s['r27e_failure_reason']=None
        self.assertFalse(candidate.triage(s)['merge_authorized'])
    def test_12_wrong_base_denied(self):
        s=snapshot();s['base_sha']='b'*40
        self.assertEqual(candidate.triage(s)['status'], 'HOLD_SOURCE_DRIFT')
    def test_13_extra_unknown_ci_check_denied(self):
        s=snapshot();s['runs'].append({'name':'new-required-check','head_sha':HEAD,'status':'completed','conclusion':'failure'})
        self.assertEqual(candidate.triage(s)['status'], 'HOLD_FAILED_CI')
    def test_14_small_failure_not_saturation(self):
        s=snapshot();s['changed_files']=17
        self.assertEqual(candidate.triage(s)['status'], 'HOLD_FAILED_CI')

if __name__=='__main__':
    unittest.main(argv=[sys.argv[0]], verbosity=2)
