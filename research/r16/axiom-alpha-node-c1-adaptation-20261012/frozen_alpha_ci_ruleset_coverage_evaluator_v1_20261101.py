"""Independent frozen C1 oracle: normalized historical CI/ruleset snapshot.
Expected outputs fixed from GitHub source inspection before candidate execution.
Synthetic mutations do not authenticate the source or prescribe governance.
"""
import copy
import json
import subprocess
import sys
from pathlib import Path

HEAD = 'd95c31615c793c12e6ebdcf2fbf8ae356bde7f01'
BASE = {
    'head_sha': HEAD,
    'ruleset': {'enforcement': 'active', 'target': 'branch',
                'include_refs': ['refs/heads/main'],
                'required_status_checks': [{'context': 'validate', 'integration_id': 15368}]},
    'check_runs': [
        {'id': 124857863010, 'name': 'nexus-preentry-lab', 'app_id': 15368},
        {'id': 124857826221, 'name': 'r27e-external-structural-firewall', 'app_id': 15368},
        {'id': 124857825507, 'name': 'semgrep-cloud-platform/scan', 'app_id': 4695336},
        {'id': 124857825307, 'name': 'validate', 'app_id': 15368},
        {'id': 124857825278, 'name': 'validate-repository-structure', 'app_id': 15368},
        {'id': 124857825206, 'name': 'validate', 'app_id': 15368},
        {'id': 124857825118, 'name': 'validate', 'app_id': 15368},
        {'id': 124857824993, 'name': 'validate', 'app_id': 15368},
    ]
}
for r in BASE['check_runs']:
    r.update(head_sha=HEAD, status='completed', conclusion='success')
MISSING = ['nexus-preentry-lab', 'r27e-external-structural-firewall',
           'semgrep-cloud-platform/scan', 'validate-repository-structure']


def cases():
    b = copy.deepcopy(BASE)
    yield 'observed_ruleset_gap', b, 'GAP_OBSERVED', MISSING, 4
    b = copy.deepcopy(BASE)
    b['ruleset']['required_status_checks'] += [
        {'context': r['name'], 'integration_id': r['app_id']}
        for r in b['check_runs'] if r['name'] != 'validate']
    yield 'all_names_required_but_duplicate_validate', b, 'GAP_OBSERVED', [], 4
    b['check_runs'] = [r for r in b['check_runs'] if r['name'] != 'validate' or r['id'] == 124857825307]
    yield 'synthetic_all_unique_required', b, 'OBSERVED_CONTEXTS_COVERED', [], 0
    b = copy.deepcopy(BASE)
    b['ruleset']['enforcement'] = 'disabled'
    yield 'inactive_ruleset', b, 'NOT_COMPUTABLE', None, None
    b = copy.deepcopy(BASE)
    b['ruleset']['include_refs'] = ['refs/heads/dev']
    yield 'wrong_branch', b, 'NOT_COMPUTABLE', None, None
    b = copy.deepcopy(BASE)
    b['ruleset']['required_status_checks'][0]['integration_id'] = 999
    yield 'wrong_required_app', b, 'GAP_OBSERVED', sorted(MISSING + ['validate']), 4
    b = copy.deepcopy(BASE)
    b['check_runs'][0]['conclusion'] = 'failure'
    yield 'failed_run', b, 'NOT_COMPUTABLE', None, None
    b = copy.deepcopy(BASE)
    b['check_runs'][0]['head_sha'] = 'a' * 40
    yield 'head_mismatch', b, 'NOT_COMPUTABLE', None, None
    b = copy.deepcopy(BASE)
    b['check_runs'][1]['id'] = b['check_runs'][0]['id']
    yield 'duplicate_run_id', b, 'NOT_COMPUTABLE', None, None
    b = copy.deepcopy(BASE)
    b['ruleset']['required_status_checks'] = []
    yield 'empty_required_checks', b, 'NOT_COMPUTABLE', None, None
    b = copy.deepcopy(BASE)
    b['check_runs'][0]['app_id'] = True
    yield 'bool_app_id', b, 'NOT_COMPUTABLE', None, None


def main(path):
    total = passed = 0
    for name, payload, expected_status, expected_missing, expected_dup in cases():
        total += 1
        run = subprocess.run([sys.executable, str(path)],
                             input=json.dumps(payload).encode('utf-8'),
                             capture_output=True, timeout=10, check=False)
        try:
            got = json.loads(run.stdout) if run.returncode == 0 else {}
        except ValueError:
            got = {}
        duplicates = got.get('duplicate_contexts')
        observed = (got.get('status'), got.get('missing_required_names'),
                    duplicates[0]['count'] if isinstance(duplicates, list) and duplicates else
                    (0 if duplicates == [] else None))
        expected = (expected_status, expected_missing, expected_dup)
        ok = observed == expected
        passed += ok
        print(json.dumps({'case': name, 'expected': expected,
                          'observed': observed, 'pass': ok}, sort_keys=True))
    print(json.dumps({'passed': passed, 'total': total, 'scope': 'SYNTHETIC_NORMALIZED_API_FIELDS_ONLY'}, sort_keys=True))
    return 0 if passed == total else 1


if __name__ == '__main__':
    sys.exit(main(Path(sys.argv[1])))
