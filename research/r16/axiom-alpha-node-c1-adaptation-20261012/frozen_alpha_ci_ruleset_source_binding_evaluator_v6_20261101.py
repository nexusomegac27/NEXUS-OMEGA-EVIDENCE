"""Frozen C1 evaluator: source/repository identity binding of REST-shaped rulesets.

Fixed expectations, independent subprocesses. Freeze before V6 candidate commit.
Synthetic, unauthenticated inputs; no claim of GitHub API authentication.
"""
import copy
import json
import subprocess
import sys
from pathlib import Path

REPO = 'nexusomegac27/NEXUS-OMEGA-EVIDENCE'
HEAD = '3fef33f230f5cfbec75167811d0a12787f1847db'
BASE = {
    'head_sha': HEAD,
    'fetch': {'url': f'https://api.github.com/repos/{REPO}/commits/{HEAD}/check-runs?per_page=100&page=1',
              'page': 1, 'per_page': 100, 'next_page': None},
    'ruleset_response': {
        'id': 21252293, 'url': f'https://api.github.com/repos/{REPO}/rulesets/21252293',
        'source': REPO, 'source_type': 'Repository',
        'enforcement': 'active', 'target': 'branch', 'bypass_actors': [],
        'conditions': {'ref_name': {'include': ['refs/heads/main'], 'exclude': []}},
        'rules': [{'type': 'required_status_checks', 'parameters': {
            'required_status_checks': [{'context': 'validate', 'integration_id': 15368}]}}]},
    'check_runs_response': {'total_count': 1, 'check_runs': [
        {'id': 101, 'name': 'validate', 'app': {'id': 15368}, 'head_sha': HEAD,
         'status': 'completed', 'conclusion': 'success'}]}}


def cases():
    yield 'valid_exact_repo', copy.deepcopy(BASE), 'OBSERVED_CONTEXTS_COVERED'
    p = copy.deepcopy(BASE)
    p['check_runs_response']['check_runs'].append(dict(p['check_runs_response']['check_runs'][0], id=102, name='build'))
    p['check_runs_response']['total_count'] = 2
    yield 'valid_extra_check_gap', p, 'GAP_OBSERVED'
    p = copy.deepcopy(BASE)
    p['check_runs_response']['check_runs'][0]['name'] = 'build'
    yield 'valid_required_absent_gap', p, 'GAP_OBSERVED'
    p = copy.deepcopy(BASE)
    p['ruleset_response']['conditions']['ref_name']['include'].append('refs/heads/release')
    yield 'valid_multiple_includes', p, 'OBSERVED_CONTEXTS_COVERED'

    changes = [
        ('source_missing', lambda r: r.pop('source')),
        ('source_null', lambda r: r.__setitem__('source', None)),
        ('source_foreign_repo', lambda r: r.__setitem__('source', 'other/repository')),
        ('source_case_drift', lambda r: r.__setitem__('source', 'NEXUSOMEGAC27/NEXUS-OMEGA-EVIDENCE')),
        ('source_trailing_space', lambda r: r.__setitem__('source', REPO + ' ')),
        ('source_boolean', lambda r: r.__setitem__('source', True)),
        ('source_type_missing', lambda r: r.pop('source_type')),
        ('source_type_org', lambda r: r.__setitem__('source_type', 'Organization')),
        ('source_type_null', lambda r: r.__setitem__('source_type', None)),
        ('source_type_boolean', lambda r: r.__setitem__('source_type', True)),
        ('ruleset_url_missing', lambda r: r.pop('url')),
        ('ruleset_url_foreign', lambda r: r.__setitem__('url', 'https://api.github.com/repos/other/repository/rulesets/21252293')),
    ]
    for name, change in changes:
        p = copy.deepcopy(BASE)
        change(p['ruleset_response'])
        yield name, p, 'NOT_COMPUTABLE'


def main(path):
    total = passed = 0
    for name, payload, expected in cases():
        total += 1
        proc = subprocess.run([sys.executable, str(path)], input=json.dumps(payload).encode('utf-8'),
                              capture_output=True, timeout=10, check=False)
        try:
            actual = json.loads(proc.stdout)['status'] if proc.returncode == 0 else None
        except (ValueError, KeyError, UnicodeError):
            actual = None
        ok = actual == expected
        passed += int(ok)
        print(json.dumps({'case': name, 'expected': expected, 'actual': actual, 'pass': ok}, sort_keys=True))
    print(json.dumps({'passed': passed, 'total': total,
                      'scope': 'SYNTHETIC_RULESET_SOURCE_IDENTITY_NOT_AUTHENTICATED'}, sort_keys=True))
    return 0 if passed == total else 1


if __name__ == '__main__':
    sys.exit(main(Path(sys.argv[1])))
