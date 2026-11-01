"""Independent subprocess oracle, frozen before candidate publication.
Only synthetic data. Expected outcomes defined independently of candidate code.
"""
import copy
import json
import subprocess
import sys
from pathlib import Path

GUARD = Path(__file__).with_name('alpha_handoff_denominator_guard_v1_20261101.py')
BASE = {'coverage_complete': True, 'coverage_source': 'SYNTHETIC_INDEPENDENT_CENSUS',
        'pinned_commit': 'a' * 40,
        'attempts': [{'attempt_id': str(i), 'evidence_ref': 'SYNTHETIC:' + str(i),
                      'routine': True, 'public': True, 'authorized': True,
                      'accessible': True, 'completed': True, 'operator_nudge': False,
                      'receipt_verified': True} for i in range(10)]}


def cases():
    yield 'positive_10_of_10', BASE, ('METRIC_READY_STRUCTURAL_ONLY', 10, 10)
    failure = copy.deepcopy(BASE)
    failure['attempts'].append({**failure['attempts'][0], 'attempt_id': 'failed',
                                'evidence_ref': 'SYNTHETIC:failed', 'completed': False,
                                'receipt_verified': False})
    yield 'eligible_failure_must_count', failure, ('METRIC_READY_STRUCTURAL_ONLY', 11, 10)
    nudged = copy.deepcopy(BASE)
    nudged['attempts'][0]['operator_nudge'] = True
    yield 'manual_nudge_not_automated', nudged, ('METRIC_READY_STRUCTURAL_ONLY', 10, 9)
    missing_receipt = copy.deepcopy(BASE)
    missing_receipt['attempts'][0]['receipt_verified'] = False
    yield 'unverified_receipt_not_automated', missing_receipt, ('METRIC_READY_STRUCTURAL_ONLY', 10, 9)
    private = copy.deepcopy(BASE)
    private['attempts'][0]['public'] = False
    yield 'private_excluded', private, ('METRIC_READY_STRUCTURAL_ONLY', 9, 9)
    incomplete = copy.deepcopy(BASE)
    incomplete['coverage_complete'] = False
    yield 'coverage_missing', incomplete, ('NOT_COMPUTABLE', None, None)
    dup = copy.deepcopy(BASE)
    dup['attempts'][1]['attempt_id'] = '0'
    yield 'duplicate_attempt', dup, ('NOT_COMPUTABLE', None, None)
    nonbool = copy.deepcopy(BASE)
    nonbool['attempts'][1]['authorized'] = 'true'
    yield 'string_boolean', nonbool, ('NOT_COMPUTABLE', None, None)
    unknown = copy.deepcopy(BASE)
    del unknown['attempts'][1]['accessible']
    yield 'unknown_accessibility', unknown, ('NOT_COMPUTABLE', None, None)
    missing = copy.deepcopy(BASE)
    del missing['coverage_source']
    yield 'missing_source', missing, ('NOT_COMPUTABLE', None, None)
    yield 'no_actual_denominator', {'coverage_complete': False, 'attempts': []}, ('NOT_COMPUTABLE', None, None)


def main():
    count = 0
    total = 0
    for label, obj, expected in cases():
        raw = json.dumps(obj, separators=(',', ':')).encode('utf-8')
        process = subprocess.run([sys.executable, str(GUARD)], input=raw,
                                 capture_output=True, timeout=10, check=False)
        actual = json.loads(process.stdout) if process.returncode == 0 else {}
        got = (actual.get('status'), actual.get('eligible_denominator'),
               actual.get('automated_numerator'))
        ok = got == expected
        count += int(ok)
        total += 1
        print(json.dumps({'fixture': label, 'expected': expected, 'observed': got,
                          'pass': ok}, sort_keys=True))
    print(json.dumps({'total': total, 'pass': count, 'scope': 'SYNTHETIC_ONLY'}, sort_keys=True))
    return 0 if count == total else 1


if __name__ == '__main__':
    sys.exit(main())
