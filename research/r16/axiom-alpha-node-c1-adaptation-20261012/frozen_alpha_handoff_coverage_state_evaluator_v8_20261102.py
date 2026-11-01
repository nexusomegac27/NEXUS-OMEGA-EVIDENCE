"""Frozen independent C1 oracle for V7->V8 coverage-state source binding.
Commit before V8 candidate; only synthetic fixtures, no live handoff or authenticated census.
The test oracle is data-driven and executes each version in a separate subprocess.
"""
import argparse
import base64
import copy
import hashlib
import json
import subprocess
import sys
from pathlib import Path

COMMIT = '9e5110ce84f2bd63bad1882d80a7ee6a219b448d'
ROW = {'routine': True, 'public': True, 'authorized': True,
       'accessible': True, 'completed': True, 'operator_nudge': False,
       'receipt_verified': True}
BASE = {'pinned_commit': COMMIT, 'coverage_complete': True,
        'coverage_source': 'SYNTHETIC_DECLARED_ONLY',
        'inventory': {'source_commit': COMMIT, 'source_ref': 'SYNTHETIC_ONLY',
                      'expected_count': 2, 'expected_attempt_ids': ['A', 'B']},
        'attempts': [dict(ROW, attempt_id='A', evidence_ref='ref-A'),
                     dict(ROW, attempt_id='B', evidence_ref='ref-B', completed=False)]}


def source_snapshot(mode, src):
    result = {key: copy.deepcopy(src[key]) for key in
              ('inventory', 'attempts', 'pinned_commit', 'coverage_source')}
    if mode == 'v8' and 'coverage_complete' in src:
        result['coverage_complete'] = copy.deepcopy(src['coverage_complete'])
    return result


def casebook():
    # name, payload modification, original-source modification, expected metric
    yield 'valid_1_of_2', {}, {}, (2, 1)
    p = [dict(ROW, attempt_id='A', evidence_ref='ref-A'),
         dict(ROW, attempt_id='B', evidence_ref='ref-B')]
    yield 'valid_2_of_2', {'attempts': p}, {'attempts': p}, (2, 2)
    p = copy.deepcopy(BASE['attempts']); p[1]['accessible'] = False
    yield 'valid_eligible_1_of_1', {'attempts': p}, {'attempts': p}, (1, 1)
    p = list(reversed(copy.deepcopy(BASE['attempts'])))
    yield 'valid_reordered_source_matches', {'attempts': p}, {'attempts': p}, (2, 1)
    p = copy.deepcopy(BASE['attempts']); p[0]['completed'] = False
    yield 'valid_0_of_2', {'attempts': p}, {'attempts': p}, (2, 0)
    for name, original in (
        ('forged_coverage_false', False),
        ('forged_coverage_missing', '__OMIT__'),
        ('forged_coverage_integer_one', 1),
        ('forged_coverage_string_true', 'true'),
        ('forged_coverage_null', None),
        ('forged_coverage_empty_list', []),
        ('forged_coverage_empty_object', {}),
        ('forged_coverage_zero', 0),
        ('forged_coverage_string_false', 'false'),
        ('forged_coverage_float_one', 1.0),
    ):
        yield name, {'coverage_complete': True}, {'coverage_complete': original}, None
    p = copy.deepcopy(BASE['attempts']); p[1]['completed'] = True
    yield 'forged_coverage_and_success', ({'coverage_complete': True, 'attempts': p}), ({'coverage_complete': False, 'attempts': p}), None
    yield 'source_true_payload_false', {'coverage_complete': False}, {}, None
    p = copy.deepcopy(BASE['attempts']); p[1]['completed'] = True
    yield 'outcome_unbound', {'attempts': p}, {}, None
    yield 'commit_mismatch', {'pinned_commit': '0' * 40}, {}, None


def run(candidate, mode, name, changes, source_changes, expected):
    payload = copy.deepcopy(BASE)
    source = copy.deepcopy(BASE)
    payload.update(copy.deepcopy(changes))
    source.update(copy.deepcopy(source_changes))
    if source.get('coverage_complete') == '__OMIT__':
        del source['coverage_complete']
    src = source_snapshot(mode, source)
    raw = json.dumps(src, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode('utf-8')
    payload['inventory_source_b64'] = base64.b64encode(raw).decode('ascii')
    digest = hashlib.sha256(raw).hexdigest()
    proc = subprocess.run([sys.executable, str(candidate), '--expected-sha256', digest,
                           '--expected-source-commit', COMMIT],
                          input=json.dumps(payload).encode('utf-8'),
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10)
    try:
        out = json.loads(proc.stdout) if proc.returncode == 0 else {}
        actual = ((out.get('eligible_denominator'), out.get('automated_numerator'))
                  if out.get('status') == 'METRIC_READY_STRUCTURAL_ONLY' else None)
    except (ValueError, UnicodeError):
        actual = None
    return {'case': name, 'expected': expected, 'actual': actual,
            'pass': actual == expected}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('candidate', type=Path)
    ap.add_argument('--mode', required=True, choices=('v7', 'v8'))
    args = ap.parse_args()
    results = [run(args.candidate, args.mode, *case) for case in casebook()]
    for result in results:
        print(json.dumps(result, sort_keys=True))
    passed = sum(x['pass'] for x in results)
    print(json.dumps({'mode': args.mode, 'passed': passed, 'total': len(results),
                      'scope': 'SYNTHETIC_COVERAGE_STATE_SOURCE_BINDING_ONLY'}, sort_keys=True))
    return 0 if passed == len(results) else 1


if __name__ == '__main__':
    sys.exit(main())
