#!/usr/bin/env python3
"""Frozen independent black-box evaluator for dual-endpoint additive PR census.

Oracle expectations are fixed independently of the candidate implementation.
"""
import copy
import json
import subprocess
import sys

ROOT = 'research/r16/axiom-alpha-node-c1-adaptation-20261012/'
FILES = [ROOT + 'alpha_publication_full_readback_preflight_v1_20261031.py',
         ROOT + 'alpha_publication_full_readback_preflight_v1_c1_report_20261031.md',
         ROOT + 'frozen_alpha_publication_readback_oracle_v1_20261031.py']
BLOBS = ['4ffbc155a6c20eb6b08bf41a167e85d6ba9cf6a0',
         '9b7fdb089147bad8fb76f441ad821aa2c958811f',
         'a4c98d74fac66c47fd1b46abf011cc258e13ceea']
HEAD = '0af4961cec47093e8e99de8811b593fe167e661f'
BASE = '0e32161a7599291ff581b8c8c1b072c37d2d99ec'
REPO = 'nexusomegac27/NEXUS-OMEGA-EVIDENCE'


def fixture():
    return {'schema_version': '1', 'repository': REPO,
            'pr': {'number': 240, 'base_sha': BASE, 'head_sha': HEAD, 'changed_files': 3},
            'api_file_listing': {'pages': [
                {'page': 1, 'request_url': f'https://api.github.com/repos/{REPO}/pulls/240/files?per_page=100&page=1',
                 'items': [{'filename': f, 'status': 'added', 'sha': b} for f, b in zip(FILES, BLOBS)]},
                {'page': 2, 'request_url': f'https://api.github.com/repos/{REPO}/pulls/240/files?per_page=100&page=2',
                 'items': []}]},
            'compare': {'base_sha': BASE, 'head_sha': HEAD, 'merge_base_sha': BASE,
                        'status': 'ahead', 'ahead_by': 3, 'behind_by': 0,
                        'files': [{'filename': f, 'status': 'added'} for f in FILES]},
            'local_preflight': {'pr_number': 240, 'head_sha': HEAD,
                                'status': 'LOCAL_BYTES_MATCH_UNAUTHENTICATED_INPUT',
                                'changed_file_paths': FILES[:], 'declared_changed_files': 3,
                                'claim_ceiling': 'C1_DESCRIPTIVE_ONLY'}}


def execute(script, obj=None, raw=None):
    p = subprocess.run([sys.executable, script], input=raw if raw is not None else json.dumps(obj),
                       capture_output=True, text=True, timeout=10)
    if not p.stdout.strip():
        raise AssertionError('missing_output:' + p.stderr[:100])
    return p.returncode, json.loads(p.stdout)


def main(script):
    tests = 0
    def check(ok, name):
        nonlocal tests
        tests += 1
        if not ok:
            raise AssertionError(f'{name}: test {tests}')
    x = fixture()
    rc, r = execute(script, x)
    check(rc == 0 and r['status'] == 'DUAL_ENDPOINT_FILE_SET_MATCH_UNAUTHENTICATED_INPUT', 'positive')
    check(r['matched_files'] == 3 and r['api_transport_authenticated'] is False, 'no_auth_promotion')
    check(r['project_automation_rate'] == 'NOT_COMPUTABLE'
          and r['project_full_readback_rate'] == 'NOT_COMPUTABLE', 'no_rate_promotion')
    x = fixture()
    x['local_preflight']['changed_file_paths'].reverse()
    x['compare']['files'].reverse()
    rc, r = execute(script, x)
    check(rc == 0 and r['matched_files'] == 3, 'reordered_positive')
    mutations = [
        ('forged_pr_listing_omission', lambda d: (d['api_file_listing']['pages'][0]['items'].pop(), d['pr'].update(changed_files=2), d['local_preflight']['changed_file_paths'].pop(), d['local_preflight'].update(declared_changed_files=2))),
        ('forged_compare_omission', lambda d: d['compare']['files'].pop()),
        ('forged_pr_count', lambda d: d['pr'].update(changed_files=2)),
        ('wrong_pr_head', lambda d: d['pr'].update(head_sha='b'*40)),
        ('wrong_compare_head', lambda d: d['compare'].update(head_sha='b'*40)),
        ('wrong_compare_base', lambda d: d['compare'].update(base_sha='b'*40)),
        ('wrong_merge_base', lambda d: d['compare'].update(merge_base_sha='b'*40)),
        ('nonlinear_behind', lambda d: d['compare'].update(behind_by=1)),
        ('zero_ahead', lambda d: d['compare'].update(ahead_by=0)),
        ('wrong_compare_status', lambda d: d['compare'].update(status='diverged')),
        ('pr_modified', lambda d: d['api_file_listing']['pages'][0]['items'][0].update(status='modified')),
        ('compare_modified', lambda d: d['compare']['files'][0].update(status='modified')),
        ('invalid_blob', lambda d: d['api_file_listing']['pages'][0]['items'][0].update(sha='bad')),
        ('duplicate_pr_path', lambda d: d['api_file_listing']['pages'][0]['items'][2].update(filename=FILES[0])),
        ('duplicate_compare_path', lambda d: d['compare']['files'][2].update(filename=FILES[0])),
        ('terminal_not_empty', lambda d: d['api_file_listing']['pages'][1].update(items=[{}])),
        ('wrong_page_number', lambda d: d['api_file_listing']['pages'][1].update(page=3)),
        ('wrong_url', lambda d: d['api_file_listing']['pages'][0].update(request_url='https://example.com/forged')),
        ('missing_terminal_page', lambda d: d['api_file_listing'].update(pages=d['api_file_listing']['pages'][:1])),
        ('wrong_repo', lambda d: d.update(repository='other/repo')),
        ('local_omission', lambda d: (d['local_preflight']['changed_file_paths'].pop(), d['local_preflight'].update(declared_changed_files=2))),
        ('local_status', lambda d: d['local_preflight'].update(status='FAIL_CLOSED')),
        ('local_claim_promotion', lambda d: d['local_preflight'].update(claim_ceiling='C2')),
        ('path_traversal', lambda d: d['compare']['files'][0].update(filename='research/../secret')),
        ('bool_count', lambda d: d['pr'].update(changed_files=True)),
        ('local_pr_mismatch', lambda d: d['local_preflight'].update(pr_number=239)),
    ]
    for name, mut in mutations:
        d = fixture()
        mut(d)
        rc, r = execute(script, d)
        check(rc == 2 and r['status'] == 'FAIL_CLOSED', name)
    for name, raw in [('malformed_json', '{bad'),
                      ('duplicate_json_key', '{"schema_version":"1","schema_version":"1"}'),
                      ('nonfinite', '{"x":NaN}')]:
        rc, r = execute(script, raw=raw)
        check(rc == 2 and r['status'] == 'FAIL_CLOSED', name)
    print(json.dumps({'oracle': 'FROZEN_ALPHA_PR_DUAL_ENDPOINT_ORACLE_V1',
                      'passed': tests, 'total': tests, 'negative': len(mutations)+3}, sort_keys=True))


if __name__ == '__main__':
    main(sys.argv[1])
