"""Precommitted independent subprocess oracle for CI inventory completeness V3.
Synthetic normalized fields; never authenticates actual GitHub REST payloads.
Expected results are fixed in this file, not imported from the candidate.
"""
import copy
import json
import subprocess
import sys
from pathlib import Path

HEAD = 'd95c31615c793c12e6ebdcf2fbf8ae356bde7f01'
API = 'GITHUB_REST_CHECK_RUNS_V1'
BASE = {
    'head_sha': HEAD,
    'ruleset': {'enforcement': 'active', 'target': 'branch',
                'include_refs': ['refs/heads/main'],
                'required_status_checks': [{'context': 'validate', 'integration_id': 15368}]},
    'check_runs': [{'id': 101, 'name': 'validate', 'app_id': 15368,
                    'head_sha': HEAD, 'status': 'completed', 'conclusion': 'success'}],
    'inventory': {'source_api': API, 'head_sha': HEAD, 'total_count': 1,
                  'per_page': 1, 'page_count': 1, 'ids_by_page': [[101]],
                  'next_page': None, 'complete': True},
}


def cases():
    yield 'complete_one_page_positive', copy.deepcopy(BASE), 'OBSERVED_CONTEXTS_COVERED'
    b = copy.deepcopy(BASE)
    b['check_runs'].append(dict(b['check_runs'][0], id=102, name='extra'))
    b['inventory'].update(total_count=2, page_count=2, ids_by_page=[[101], [102]])
    yield 'complete_two_page_gap', b, 'GAP_OBSERVED'
    b = copy.deepcopy(BASE)
    del b['inventory']
    yield 'missing_inventory', b, 'NOT_COMPUTABLE'
    b = copy.deepcopy(BASE)
    b['inventory']['total_count'] = 2
    yield 'truncated_total_count', b, 'NOT_COMPUTABLE'
    b = copy.deepcopy(BASE)
    b['inventory']['total_count'] = 0
    yield 'understated_total_count', b, 'NOT_COMPUTABLE'
    b = copy.deepcopy(BASE)
    b['inventory']['next_page'] = 'page2'
    yield 'next_page_unfetched', b, 'NOT_COMPUTABLE'
    b = copy.deepcopy(BASE)
    b['inventory']['complete'] = False
    yield 'not_complete', b, 'NOT_COMPUTABLE'
    b = copy.deepcopy(BASE)
    b['inventory']['ids_by_page'] = [[102]]
    yield 'page_id_mismatch', b, 'NOT_COMPUTABLE'
    b = copy.deepcopy(BASE)
    b['inventory']['page_count'] = 2
    yield 'missing_page', b, 'NOT_COMPUTABLE'
    b = copy.deepcopy(BASE)
    b['inventory']['per_page'] = True
    yield 'bool_page_size', b, 'NOT_COMPUTABLE'
    b = copy.deepcopy(BASE)
    b['inventory']['total_count'] = True
    yield 'bool_total_count', b, 'NOT_COMPUTABLE'
    b = copy.deepcopy(BASE)
    b['inventory']['source_api'] = 'OTHER_API'
    yield 'wrong_api_label', b, 'NOT_COMPUTABLE'
    b = copy.deepcopy(BASE)
    b['inventory']['head_sha'] = 'a'*40
    yield 'wrong_inventory_head', b, 'NOT_COMPUTABLE'
    b = copy.deepcopy(BASE)
    b['check_runs'][0]['conclusion'] = 'failure'
    yield 'existing_failed_run_regression', b, 'NOT_COMPUTABLE'
    b = copy.deepcopy(BASE)
    b['check_runs'].append(dict(b['check_runs'][0], id=102, name='extra'))
    b['inventory'].update(total_count=2, per_page=2, page_count=1, ids_by_page=[[101, 102]])
    yield 'complete_single_page_extra_gap', b, 'GAP_OBSERVED'
    b = copy.deepcopy(BASE)
    b['inventory']['ids_by_page'] = [[101, 101]]
    yield 'extra_page_id', b, 'NOT_COMPUTABLE'


def main(path):
    passed = total = 0
    for name, payload, expected in cases():
        total += 1
        run = subprocess.run([sys.executable, str(path)], input=json.dumps(payload).encode('utf-8'),
                             capture_output=True, timeout=10, check=False)
        try:
            actual = json.loads(run.stdout).get('status') if run.returncode == 0 else None
        except (ValueError, UnicodeError):
            actual = None
        ok = actual == expected
        passed += int(ok)
        print(json.dumps({'case': name, 'expected': expected, 'actual': actual,
                          'pass': ok}, sort_keys=True))
    print(json.dumps({'passed': passed, 'total': total,
                      'scope': 'SYNTHETIC_NORMALIZED_FIELDS_UNAUTHENTICATED'}, sort_keys=True))
    return 0 if passed == total else 1


if __name__ == '__main__':
    sys.exit(main(Path(sys.argv[1])))
