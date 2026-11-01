"""Independent precommitted C1 oracle for required-context completeness.
Uses synthetic normalized GitHub check-run/ruleset fields, not authenticated API responses.
Run against the pinned V1 and V2 scripts separately; never edits either.
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
    'check_runs': [{'id': 101, 'name': 'validate', 'app_id': 15368,
                    'head_sha': HEAD, 'status': 'completed', 'conclusion': 'success'}],
}


def cases():
    b = copy.deepcopy(BASE)
    yield 'positive_exact_required', b, 'OBSERVED_CONTEXTS_COVERED', []
    b = copy.deepcopy(BASE)
    b['ruleset']['required_status_checks'].append({'context': 'semgrep', 'integration_id': 4695336})
    yield 'absent_second_required', b, 'GAP_OBSERVED', [('semgrep', 4695336)]
    b = copy.deepcopy(BASE)
    b['ruleset']['required_status_checks'][0]['context'] = 'semgrep'
    yield 'absent_only_required_wrong_name', b, 'GAP_OBSERVED', [('semgrep', 15368)]
    b = copy.deepcopy(BASE)
    b['ruleset']['required_status_checks'][0]['integration_id'] = 4695336
    yield 'absent_only_required_wrong_app', b, 'GAP_OBSERVED', [('validate', 4695336)]
    b = copy.deepcopy(BASE)
    b['ruleset']['required_status_checks'].append({'context': 'semgrep', 'integration_id': 4695336})
    b['check_runs'].append({'id': 102, 'name': 'semgrep', 'app_id': 4695336,
                            'head_sha': HEAD, 'status': 'completed', 'conclusion': 'success'})
    yield 'positive_two_required', b, 'OBSERVED_CONTEXTS_COVERED', []
    b = copy.deepcopy(BASE)
    b['ruleset']['required_status_checks'].append({'context': 'semgrep', 'integration_id': 4695336})
    b['check_runs'].append({'id': 102, 'name': 'semgrep', 'app_id': 4695336,
                            'head_sha': HEAD, 'status': 'completed', 'conclusion': 'success'})
    b['check_runs'].append({'id': 103, 'name': 'extra', 'app_id': 15368,
                            'head_sha': HEAD, 'status': 'completed', 'conclusion': 'success'})
    yield 'extra_unrequired_context', b, 'GAP_OBSERVED', []
    b = copy.deepcopy(BASE)
    b['check_runs'].append(dict(b['check_runs'][0], id=102))
    yield 'duplicate_required_name', b, 'GAP_OBSERVED', []
    b = copy.deepcopy(BASE)
    b['check_runs'][0]['conclusion'] = 'failure'
    yield 'failed_required_check', b, 'NOT_COMPUTABLE', None
    b = copy.deepcopy(BASE)
    b['check_runs'] = []
    yield 'empty_inventory', b, 'NOT_COMPUTABLE', None
    b = copy.deepcopy(BASE)
    b['check_runs'][0]['head_sha'] = 'a'*40
    yield 'wrong_head', b, 'NOT_COMPUTABLE', None
    b = copy.deepcopy(BASE)
    b['ruleset']['required_status_checks'].append({'context': 'validate', 'integration_id': 15368})
    yield 'duplicate_required_rule', b, 'NOT_COMPUTABLE', None
    b = copy.deepcopy(BASE)
    b['ruleset']['required_status_checks'][0]['integration_id'] = True
    yield 'bool_integration_id', b, 'NOT_COMPUTABLE', None


def main(path):
    total = passed = 0
    for name, payload, expected_status, expected_absent in cases():
        total += 1
        run = subprocess.run([sys.executable, str(path)], input=json.dumps(payload).encode(),
                             capture_output=True, timeout=10, check=False)
        try:
            got = json.loads(run.stdout) if run.returncode == 0 else {}
        except (ValueError, UnicodeError):
            got = {}
        observed_status = got.get('status')
        absent = got.get('absent_required_contexts')
        observed_absent = (sorted((r['name'], r['app_id']) for r in absent)
                           if isinstance(absent, list) else None)
        expected = (expected_status, expected_absent)
        observed = (observed_status, observed_absent)
        # Legacy V1 has no absent-required field; require that field only when
        # a missing required context is the negative-control target.
        ok = (observed_status == expected_status and
              (not expected_absent or observed_absent == expected_absent))
        passed += int(ok)
        print(json.dumps({'case': name, 'expected': expected, 'observed': observed,
                          'pass': ok}, sort_keys=True))
    print(json.dumps({'passed': passed, 'total': total,
                      'scope': 'SYNTHETIC_NORMALIZED_FIELDS_NOT_AUTHENTICATED'}, sort_keys=True))
    return 0 if passed == total else 1


if __name__ == '__main__':
    sys.exit(main(Path(sys.argv[1])))
