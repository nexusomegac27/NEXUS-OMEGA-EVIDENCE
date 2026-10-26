#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Frozen independent oracle for PR #124 raw GitHub check-run triage V2.

One pinned 2026-10-26 snapshot. No network, write, merge or runtime actions.
Tests deliberately distinguish duplicate check *names* from duplicate check IDs.
"""
import copy
import importlib.util
import sys
import unittest

if len(sys.argv) != 2:
    raise SystemExit('usage: python frozen_pr_ci_raw_check_evaluator_v2_20261026.py CANDIDATE_PATH')
spec = importlib.util.spec_from_file_location('candidate_under_test', sys.argv[1])
candidate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(candidate)

MAIN = 'c657146b64f28401f1dac11d16fafdd63b649629'
BASE = 'd355400dabed3c280e1fce5030cab69ea099428b'
HEAD = 'e81030061ff5349064d7c400d3ba2d35b70ab8a7'
CHECKS = (
    (121432429315, 'nexus-preentry-lab', 'github-actions', 'failure'),
    (121432403923, 'validate-repository-structure', 'github-actions', 'success'),
    (121432403660, 'validate', 'github-actions', 'success'),
    (121432403624, 'validate', 'github-actions', 'success'),
    (121432403500, 'validate', 'github-actions', 'success'),
    (121432403150, 'validate', 'github-actions', 'success'),
    (121432393510, 'r27e-external-structural-firewall', 'github-actions', 'failure'),
    (121432391765, 'semgrep-cloud-platform/scan', 'semgrep-code-nexusomegac27', 'success'),
)

def fixture():
    checks = [{'id': i, 'name': n, 'app_slug': a, 'status': 'completed',
               'conclusion': c, 'head_sha': HEAD} for i, n, a, c in CHECKS]
    snapshot = {'repository': 'nexusomegac27/NEXUS-OMEGA-EVIDENCE',
                'pr_number': 124, 'owner_login': 'nexusomegac27',
                'head_sha': HEAD, 'base_sha': BASE, 'main_sha': MAIN,
                'changed_files': 138, 'checks': checks,
                'r27e_log_excerpt': '{"error": "ValueError: TOO_MANY_PR_CHANGES"}',
                'preentry_log_excerpt': 'UPSTREAM_RESULT: failure\nDENY: R27-E structural intake did not pass'}
    pin = {'head_sha': HEAD, 'base_sha': BASE, 'main_sha': MAIN,
           'check_ids': sorted(i for i, _, _, _ in CHECKS)}
    return snapshot, pin

class FrozenRawCheckOracle(unittest.TestCase):
    def check(self, s, p, expected):
        result = candidate.triage(s, p)
        self.assertEqual(result['status'], expected)
        self.assertFalse(result['merge_authorized'])
        self.assertEqual(result['claim_ceiling'], 'C1_DESCRIPTIVE_ONLY')

    def test_01_observed_two_causal_failures(self):
        s, p = fixture(); self.check(s, p, 'HOLD_ACCUMULATION_C1')
    def test_02_four_duplicate_names_are_not_duplicate_ids(self):
        s, p = fixture(); self.assertEqual(sum(c['name']=='validate' for c in s['checks']), 4)
        self.check(s, p, 'HOLD_ACCUMULATION_C1')
    def test_03_duplicate_check_id_denied(self):
        s, p = fixture(); s['checks'][3]['id'] = s['checks'][2]['id']
        self.check(s, p, 'HOLD_INCOMPLETE_CI')
    def test_04_missing_check_denied(self):
        s, p = fixture(); s['checks'].pop()
        self.check(s, p, 'HOLD_INCOMPLETE_CI')
    def test_05_wrong_check_head_denied(self):
        s, p = fixture(); s['checks'][0]['head_sha'] = 'a'*40
        self.check(s, p, 'HOLD_SOURCE_DRIFT')
    def test_06_current_main_drift_denied(self):
        s, p = fixture(); s['main_sha'] = BASE
        self.check(s, p, 'HOLD_SOURCE_DRIFT')
    def test_07_pr_base_drift_denied(self):
        s, p = fixture(); s['base_sha'] = MAIN
        self.check(s, p, 'HOLD_SOURCE_DRIFT')
    def test_08_unregistered_actor_denied(self):
        s, p = fixture(); s['owner_login'] = 'external-agent'
        self.check(s, p, 'HOLD_ACTOR_SCOPE')
    def test_09_missing_r27e_log_cannot_infer_cause(self):
        s, p = fixture(); s['r27e_log_excerpt'] = ''
        self.check(s, p, 'HOLD_FAILED_CI')
    def test_10_missing_downstream_log_cannot_infer_cause(self):
        s, p = fixture(); s['preentry_log_excerpt'] = ''
        self.check(s, p, 'HOLD_FAILED_CI')
    def test_11_other_failed_check_not_misclassified(self):
        s, p = fixture(); s['checks'][1]['conclusion'] = 'failure'
        self.check(s, p, 'HOLD_FAILED_CI')
    def test_12_all_success_not_auto_approved(self):
        s, p = fixture()
        for c in s['checks']: c['conclusion'] = 'success'
        self.check(s, p, 'HOLD_UNATTRIBUTED_CI')
    def test_13_pending_check_not_complete(self):
        s, p = fixture(); s['checks'][1]['status']='in_progress'; s['checks'][1]['conclusion']=None
        self.check(s, p, 'HOLD_PENDING_CI')
    def test_14_threshold_is_not_arbitrary_success(self):
        s, p = fixture(); s['changed_files'] = 100
        self.check(s, p, 'HOLD_FAILED_CI')
    def test_15_boolean_file_count_denied(self):
        s, p = fixture(); s['changed_files'] = True
        self.check(s, p, 'HOLD_INVALID_METADATA')
    def test_16_app_impersonation_denied(self):
        s, p = fixture(); s['checks'][6]['app_slug'] = 'external-app'
        self.check(s, p, 'HOLD_INCOMPLETE_CI')
    def test_17_partial_downstream_log_is_insufficient(self):
        s, p = fixture(); s['preentry_log_excerpt'] = 'UPSTREAM_RESULT: failure'
        self.check(s, p, 'HOLD_FAILED_CI')
    def test_18_wrong_firewall_marker_denied(self):
        s, p = fixture(); s['r27e_log_excerpt'] = 'ValueError: OTHER_FAILURE'
        self.check(s, p, 'HOLD_FAILED_CI')
    def test_19_unknown_unique_check_id_denied(self):
        s, p = fixture(); s['checks'][0]['id'] += 999
        self.check(s, p, 'HOLD_INCOMPLETE_CI')

if __name__ == '__main__':
    unittest.main(argv=[sys.argv[0]], verbosity=2)
