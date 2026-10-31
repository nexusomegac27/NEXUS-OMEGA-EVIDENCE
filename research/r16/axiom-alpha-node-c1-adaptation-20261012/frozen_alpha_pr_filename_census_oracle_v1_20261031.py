#!/usr/bin/env python3
"""Frozen black-box evaluator for PR filename census consistency (C1 only)."""
import copy
import json
import subprocess
import sys

ROOT = 'research/r16/axiom-alpha-node-c1-adaptation-20261012/'
FILES = [ROOT + 'alpha_publication_full_readback_preflight_v1_20261031.py',
         ROOT + 'alpha_publication_full_readback_preflight_v1_c1_report_20261031.md',
         ROOT + 'frozen_alpha_publication_readback_oracle_v1_20261031.py']


def fixture():
    return {'schema_version': '1', 'repository': 'nexusomegac27/NEXUS-OMEGA-EVIDENCE',
            'pr': {'number': 240, 'head_sha': '0af4961cec47093e8e99de8811b593fe167e661f',
                   'changed_files': 3},
            'api_file_listing': {'all_pages_fetched': True, 'next_cursor': None,
                                 'page_count': 1, 'filenames': FILES[:]},
            'local_preflight': {'pr_number': 240,
                                'head_sha': '0af4961cec47093e8e99de8811b593fe167e661f',
                                'status': 'LOCAL_BYTES_MATCH_UNAUTHENTICATED_INPUT',
                                'declared_changed_files': 3,
                                'changed_file_paths': FILES[:],
                                'claim_ceiling': 'C1_DESCRIPTIVE_ONLY'}}


def run(script, obj=None, raw=None):
    p = subprocess.run([sys.executable, script], input=raw if raw is not None else json.dumps(obj),
                       text=True, capture_output=True, timeout=10)
    if not p.stdout.strip():
        raise AssertionError('missing_stdout:' + p.stderr[:100])
    return p.returncode, json.loads(p.stdout)


def main(script):
    tests = 0
    def check(condition, label):
        nonlocal tests
        tests += 1
        if not condition:
            raise AssertionError(label)
    x = fixture()
    rc, result = run(script, x)
    check(rc == 0 and result['status'] == 'API_FILENAME_CENSUS_MATCH_UNAUTHENTICATED_PROJECTION', 'positive')
    check(result['matched_files'] == 3 and result['api_transport_authenticated'] is False, 'no_auth_promotion')
    check(result['project_full_readback_rate'] == 'NOT_COMPUTABLE', 'no_rate_promotion')
    x2 = fixture()
    x2['local_preflight']['changed_file_paths'].reverse()
    rc, result = run(script, x2)
    check(rc == 0 and result['matched_files'] == 3, 'order_independent')
    mutations = [
        ('omitted_local_file_and_count', lambda d: (d['local_preflight']['changed_file_paths'].pop(), d['local_preflight'].update(declared_changed_files=2))),
        ('omitted_api_file_and_count', lambda d: (d['api_file_listing']['filenames'].pop(), d['pr'].update(changed_files=2))),
        ('added_ghost_local', lambda d: (d['local_preflight']['changed_file_paths'].append(ROOT + 'ghost.py'), d['local_preflight'].update(declared_changed_files=4))),
        ('duplicate_api_file', lambda d: d['api_file_listing']['filenames'].__setitem__(2, d['api_file_listing']['filenames'][0])),
        ('duplicate_local_file', lambda d: d['local_preflight']['changed_file_paths'].__setitem__(2, d['local_preflight']['changed_file_paths'][0])),
        ('api_count_inconsistent', lambda d: d['pr'].update(changed_files=4)),
        ('local_count_inconsistent', lambda d: d['local_preflight'].update(declared_changed_files=4)),
        ('pagination_not_complete', lambda d: d['api_file_listing'].update(all_pages_fetched=False)),
        ('next_cursor_pending', lambda d: d['api_file_listing'].update(next_cursor='abc')),
        ('zero_pages', lambda d: d['api_file_listing'].update(page_count=0)),
        ('head_mismatch', lambda d: d['local_preflight'].update(head_sha='b' * 40)),
        ('wrong_repo', lambda d: d.update(repository='other/repo')),
        ('c2_promotion', lambda d: d['local_preflight'].update(claim_ceiling='C2')),
        ('path_traversal', lambda d: d['api_file_listing']['filenames'].__setitem__(0, 'research/../secret')),
        ('preflight_not_success', lambda d: d['local_preflight'].update(status='FAIL_CLOSED')),
        ('nonboolean_complete', lambda d: d['api_file_listing'].update(all_pages_fetched=1)),
    ]
    for label, mutate in mutations:
        x = fixture()
        mutate(x)
        rc, result = run(script, x)
        check(rc == 2 and result['status'] == 'FAIL_CLOSED', label)
    for label, raw in [('duplicate_json_key', '{"schema_version":"1","schema_version":"1"}'),
                       ('nonfinite', '{"x":NaN}'), ('malformed', '{bad')]:
        rc, result = run(script, raw=raw)
        check(rc == 2 and result['status'] == 'FAIL_CLOSED', label)
    print(json.dumps({'oracle': 'FROZEN_ALPHA_PR_FILENAME_CENSUS_ORACLE_V1',
                      'passed': tests, 'tests': tests}, sort_keys=True))

if __name__ == '__main__':
    main(sys.argv[1])
