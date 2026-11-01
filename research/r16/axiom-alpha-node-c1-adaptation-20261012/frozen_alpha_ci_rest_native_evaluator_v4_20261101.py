"""Independent, fixed-expectation subprocess oracle for raw REST-shape V4.

Committed before the candidate. Synthetic data cannot authenticate GitHub.
"""
import copy
import json
import subprocess
import sys
from pathlib import Path

HEAD = '964fe47c4bdbad599e0689b132ff73c0822f3518'
URL = ('https://api.github.com/repos/nexusomegac27/NEXUS-OMEGA-EVIDENCE/'
       f'commits/{HEAD}/check-runs?per_page=100&page=1')
BASE = {
    'head_sha': HEAD,
    'fetch': {'url': URL, 'page': 1, 'per_page': 100, 'next_page': None},
    'ruleset_response': {'id': 21252293, 'enforcement': 'active', 'target': 'branch',
                         'conditions': {'ref_name': {'include': ['refs/heads/main'], 'exclude': []}},
                         'rules': [{'type': 'required_status_checks',
                                    'parameters': {'required_status_checks': [
                                        {'context': 'validate', 'integration_id': 15368}]}}]},
    'check_runs_response': {'total_count': 1, 'check_runs': [
        {'id': 101, 'name': 'validate', 'app': {'id': 15368}, 'head_sha': HEAD,
         'status': 'completed', 'conclusion': 'success'}]}}


def cases():
    yield 'raw_positive', copy.deepcopy(BASE), 'OBSERVED_CONTEXTS_COVERED'
    b = copy.deepcopy(BASE)
    b['check_runs_response']['check_runs'].append(dict(b['check_runs_response']['check_runs'][0], id=102, name='build'))
    b['check_runs_response']['total_count'] = 2
    yield 'raw_extra_context_gap', b, 'GAP_OBSERVED'
    b = copy.deepcopy(BASE)
    b['check_runs_response']['check_runs'][0]['name'] = 'build'
    yield 'raw_required_absent_gap', b, 'GAP_OBSERVED'
    b = copy.deepcopy(BASE)
    b['check_runs_response']['total_count'] = 2
    yield 'truncated_response', b, 'NOT_COMPUTABLE'
    b = copy.deepcopy(BASE)
    b['check_runs_response']['total_count'] = 101
    yield 'multipage_fail_closed', b, 'NOT_COMPUTABLE'
    b = copy.deepcopy(BASE)
    b['fetch']['next_page'] = '2'
    yield 'unfetched_page', b, 'NOT_COMPUTABLE'
    b = copy.deepcopy(BASE)
    b['fetch']['page'] = 2
    yield 'wrong_page', b, 'NOT_COMPUTABLE'
    b = copy.deepcopy(BASE)
    b['fetch']['url'] = b['fetch']['url'].replace(HEAD, 'a' * 40)
    yield 'stale_url', b, 'NOT_COMPUTABLE'
    b = copy.deepcopy(BASE)
    b['check_runs_response']['check_runs'][0]['app'] = {'id': True}
    yield 'bool_app_id', b, 'NOT_COMPUTABLE'
    b = copy.deepcopy(BASE)
    b['check_runs_response']['check_runs'][0]['head_sha'] = 'a' * 40
    yield 'wrong_run_head', b, 'NOT_COMPUTABLE'
    b = copy.deepcopy(BASE)
    b['ruleset_response']['id'] = 999
    yield 'wrong_ruleset_id', b, 'NOT_COMPUTABLE'
    b = copy.deepcopy(BASE)
    b['ruleset_response']['rules'] = []
    yield 'missing_required_rule', b, 'NOT_COMPUTABLE'
    b = copy.deepcopy(BASE)
    b['ruleset_response']['enforcement'] = 'evaluate'
    yield 'ruleset_not_active', b, 'NOT_COMPUTABLE'
    b = copy.deepcopy(BASE)
    b['check_runs_response']['check_runs'][0]['conclusion'] = 'failure'
    yield 'failed_run', b, 'NOT_COMPUTABLE'
    b = copy.deepcopy(BASE)
    b['check_runs_response']['check_runs'].append(dict(b['check_runs_response']['check_runs'][0]))
    b['check_runs_response']['total_count'] = 2
    yield 'duplicate_run_id', b, 'NOT_COMPUTABLE'
    b = copy.deepcopy(BASE)
    b['check_runs_response']['total_count'] = True
    yield 'bool_total', b, 'NOT_COMPUTABLE'


def main(path):
    passed = 0
    total = 0
    for name, payload, expected in cases():
        total += 1
        proc = subprocess.run([sys.executable, str(path)], input=json.dumps(payload).encode(),
                              capture_output=True, timeout=10, check=False)
        try:
            actual = json.loads(proc.stdout)['status'] if proc.returncode == 0 else None
        except (ValueError, KeyError, UnicodeError):
            actual = None
        passed += int(actual == expected)
        print(json.dumps({'case': name, 'expected': expected, 'actual': actual,
                          'pass': actual == expected}, sort_keys=True))
    print(json.dumps({'passed': passed, 'total': total,
                      'scope': 'SYNTHETIC_RAW_REST_SHAPES_NOT_AUTHENTICATED'}, sort_keys=True))
    return 0 if passed == total else 1


if __name__ == '__main__':
    sys.exit(main(Path(sys.argv[1])))
