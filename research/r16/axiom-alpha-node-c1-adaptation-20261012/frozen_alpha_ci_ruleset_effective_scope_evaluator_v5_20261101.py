"""Fixed-expectation, separate-process evaluator for V5 ruleset scope/bypass guard.

C1 synthetic REST-shaped fixtures; no live API authentication, no ruleset mutation.
Freeze this evaluator in a predecessor commit before committing V5 candidate.
"""
import copy
import json
import subprocess
import sys
from pathlib import Path

HEAD = '3cc35487e8cae54aeac95377b6a8c376f412dc4f'
URL = ('https://api.github.com/repos/nexusomegac27/NEXUS-OMEGA-EVIDENCE/'
       f'commits/{HEAD}/check-runs?per_page=100&page=1')
BASE = {
    'head_sha': HEAD,
    'fetch': {'url': URL, 'page': 1, 'per_page': 100, 'next_page': None},
    'ruleset_response': {
        'id': 21252293, 'enforcement': 'active', 'target': 'branch',
        'bypass_actors': [],
        'conditions': {'ref_name': {'include': ['refs/heads/main'], 'exclude': []}},
        'rules': [{'type': 'required_status_checks',
                   'parameters': {'strict_required_status_checks_policy': True,
                                  'required_status_checks': [
                                      {'context': 'validate', 'integration_id': 15368}]}}]},
    'check_runs_response': {'total_count': 1, 'check_runs': [
        {'id': 101, 'name': 'validate', 'app': {'id': 15368}, 'head_sha': HEAD,
         'status': 'completed', 'conclusion': 'success'}]}}


def cases():
    yield 'valid_main_no_exclusions_no_bypass', copy.deepcopy(BASE), 'OBSERVED_CONTEXTS_COVERED'
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

    def altered(name, mutator):
        p = copy.deepcopy(BASE)
        mutator(p)
        return name, p, 'NOT_COMPUTABLE'

    yield altered('excluded_main', lambda p: p['ruleset_response']['conditions']['ref_name']['exclude'].append('refs/heads/main'))
    yield altered('excluded_other_unmodeled_pattern', lambda p: p['ruleset_response']['conditions']['ref_name']['exclude'].append('refs/heads/release'))
    yield altered('excluded_all', lambda p: p['ruleset_response']['conditions']['ref_name']['exclude'].append('~ALL'))
    yield altered('exclude_string_type', lambda p: p['ruleset_response']['conditions']['ref_name'].__setitem__('exclude', ''))
    yield altered('exclude_missing', lambda p: p['ruleset_response']['conditions']['ref_name'].pop('exclude'))
    yield altered('bypass_actor_present', lambda p: p['ruleset_response'].__setitem__('bypass_actors', [{'actor_id': 123, 'actor_type': 'Team', 'bypass_mode': 'always'}]))
    yield altered('bypass_missing', lambda p: p['ruleset_response'].pop('bypass_actors'))
    yield altered('bypass_null', lambda p: p['ruleset_response'].__setitem__('bypass_actors', None))
    yield altered('bypass_wrong_type', lambda p: p['ruleset_response'].__setitem__('bypass_actors', {}))
    yield altered('include_string_type', lambda p: p['ruleset_response']['conditions']['ref_name'].__setitem__('include', 'refs/heads/main'))
    yield altered('include_dict_type', lambda p: p['ruleset_response']['conditions']['ref_name'].__setitem__('include', {'refs/heads/main': True}))
    yield altered('include_duplicate', lambda p: p['ruleset_response']['conditions']['ref_name']['include'].append('refs/heads/main'))
    yield altered('include_mixed_type', lambda p: p['ruleset_response']['conditions']['ref_name']['include'].append(None))


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
                      'scope': 'SYNTHETIC_RULESET_SCOPE_AND_BYPASS_NOT_AUTHENTICATED'}, sort_keys=True))
    return 0 if passed == total else 1


if __name__ == '__main__':
    sys.exit(main(Path(sys.argv[1])))
