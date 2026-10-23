#!/usr/bin/env python3
"""Frozen independent evaluator: scalar-type confusion in C1 PR preflight.

Fixtures are synthetic and are not authenticated GitHub observations.
This evaluator is an external test oracle, not publication authority.
"""
import copy
import importlib
import json
import sys

MODULE = sys.argv[1] if len(sys.argv) > 1 else 'alpha_pr_publication_preflight_guard_v2_20261023'
fn = importlib.import_module(MODULE).check_pr_publication_preflight
MAIN = 'd355400dabed3c280e1fce5030cab69ea099428b'
HEAD = '5bb4f32d37cb13c38196714c24d7d73b290c2eae'
BRANCH = 'axiom/alpha-export-surface-closure-c1-20261021'
REPO = 'nexusomegac27/NEXUS-OMEGA-EVIDENCE'
PATH = 'research/r16/axiom-alpha-node-c1-adaptation-20261012/frozen_scalar_type_preflight_evaluator_v1_20261023.py'
NOW = '2026-10-23T10:58:35Z'
BASE = {
    'repo': {'repository_full_name': REPO, 'owner': {'login': 'nexusomegac27'},
             'permissions': {'push': True}, 'default_branch': 'main'},
    'pr': {'number': 124, 'state': 'open', 'merged': False, 'draft': True,
           'base': 'main', 'base_sha': MAIN, 'head': BRANCH, 'head_sha': HEAD,
           'head_repo_full_name': REPO, 'user': {'login': 'nexusomegac27'}},
    'main': {'name': 'main', 'sha': MAIN},
    'branch': {'name': BRANCH, 'sha': HEAD},
    'target': {'pinned_main': MAIN, 'pinned_head': HEAD,
               'repository_full_name': REPO, 'pr_number': 124,
               'branch': BRANCH, 'path': PATH, 'path_absent_confirmed': True,
               'observed_at': '2026-10-23T10:58:20Z'}
}
CASES = [
    ('valid', {}, 'READY_FOR_CONTENT_CHECK'),
    ('push_false_bool', {'repo.permissions.push': False}, 'ACTOR_SCOPE_HOLD'),
    ('push_false_string', {'repo.permissions.push': 'false'}, 'ACTOR_SCOPE_HOLD'),
    ('push_true_string', {'repo.permissions.push': 'true'}, 'ACTOR_SCOPE_HOLD'),
    ('push_one_integer', {'repo.permissions.push': 1}, 'ACTOR_SCOPE_HOLD'),
    ('push_nonempty_list', {'repo.permissions.push': [1]}, 'ACTOR_SCOPE_HOLD'),
    ('push_object', {'repo.permissions.push': {'push': True}}, 'ACTOR_SCOPE_HOLD'),
    ('push_none', {'repo.permissions.push': None}, 'ACTOR_SCOPE_HOLD'),
    ('pr_float', {'pr.number': 124.0}, 'PR_STATE_HOLD'),
    ('target_float', {'target.pr_number': 124.0}, 'PR_STATE_HOLD'),
    ('pr_target_float', {'pr.number': 124.0, 'target.pr_number': 124.0}, 'PR_STATE_HOLD'),
    ('pr_numeric_string', {'pr.number': '124'}, 'PR_STATE_HOLD'),
    ('target_numeric_string', {'target.pr_number': '124'}, 'PR_STATE_HOLD'),
    ('pr_negative', {'pr.number': -124}, 'PR_STATE_HOLD'),
    ('pr_bool', {'pr.number': True}, 'PR_STATE_HOLD'),
    ('missing_push', {'repo.permissions': {}}, 'INCOMPLETE'),
    ('missing_pr', {'pr': None}, 'INCOMPLETE'),
    ('wrong_branch', {'target.branch': 'codex/incorrect'}, 'WRONG_BRANCH'),
    ('main_drift', {'main.sha': '0'*40}, 'MAIN_DRIFT'),
    ('naive_timestamp', {'target.observed_at': '2026-10-23T10:58:20'}, 'TIMEZONE_REQUIRED'),
    ('stale_timestamp', {'target.observed_at': '2026-10-23T10:55:20Z'}, 'STALE_SNAPSHOT'),
    ('path_unverified', {'target.path_absent_confirmed': False}, 'PATH_EXISTS_OR_UNVERIFIED'),
    ('repo_mismatch', {'repo.repository_full_name': 'other/repo'}, 'REPO_SCOPE_MISMATCH'),
    ('valid_utc_offset', {'target.observed_at': '2026-10-23T12:58:20+02:00'}, 'READY_FOR_CONTENT_CHECK'),
]
results = []
for name, changes, expected in CASES:
    snap = copy.deepcopy(BASE)
    for dotted, value in changes.items():
        keys = dotted.split('.')
        dst = snap
        for k in keys[:-1]:
            dst = dst[k]
        dst[keys[-1]] = value
    before = copy.deepcopy(snap)
    try:
        actual = fn(snap, NOW)['status']
    except Exception as e:
        actual = 'EXCEPTION:'+type(e).__name__
    unchanged = snap == before
    results.append({'name': name, 'expected': expected, 'actual': actual,
                    'pass': actual == expected and unchanged})
report = {'module': MODULE, 'total': len(results),
          'passed': sum(r['pass'] for r in results), 'results': results}
print(json.dumps(report, sort_keys=True, indent=2))
if report['passed'] != report['total']:
    sys.exit(1)
