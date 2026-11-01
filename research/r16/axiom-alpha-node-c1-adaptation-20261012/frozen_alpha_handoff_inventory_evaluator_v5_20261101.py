"""Frozen C1 subprocess oracle for declared handoff census/inventory consistency.
Freeze before candidate commit. Synthetic inputs; never asserts real inventory completeness.
"""
import copy
import json
import subprocess
import sys
from pathlib import Path

HEAD = '71feb351c3e2436344a10b22b53ba19c946d73df'
ROW = {'routine': True, 'public': True, 'authorized': True,
       'accessible': True, 'completed': True, 'operator_nudge': False,
       'receipt_verified': True}
BASE = {
    'coverage_complete': True, 'coverage_source': 'SYNTHETIC_DECLARED_ONLY',
    'pinned_commit': HEAD,
    'attempts': [dict(ROW, attempt_id='A', evidence_ref='ref-A'),
                 dict(ROW, attempt_id='B', evidence_ref='ref-B', completed=False)],
    'inventory': {'source_commit': HEAD, 'source_ref': 'SYNTHETIC_UNVERIFIED',
                  'expected_count': 2, 'expected_attempt_ids': ['A', 'B']}}


def cases():
    yield 'complete_two_attempts_50pct', copy.deepcopy(BASE), ('METRIC_READY_STRUCTURAL_ONLY', 2, 1)
    p = copy.deepcopy(BASE); p['attempts'][1]['completed'] = True
    yield 'complete_two_success_100pct', p, ('METRIC_READY_STRUCTURAL_ONLY', 2, 2)
    p = copy.deepcopy(BASE); p['attempts'][1]['operator_nudge'] = True; p['attempts'][1]['completed'] = True
    yield 'manual_attempt_stays_in_denominator', p, ('METRIC_READY_STRUCTURAL_ONLY', 2, 1)
    p = copy.deepcopy(BASE); p['attempts'][1]['accessible'] = False
    yield 'ineligible_excluded', p, ('METRIC_READY_STRUCTURAL_ONLY', 1, 1)
    p = copy.deepcopy(BASE); p['attempts'][0]['accessible'] = False; p['attempts'][1]['accessible'] = False
    yield 'zero_eligible_not_computable', p, ('NOT_COMPUTABLE', None, None)
    mutations = [
        ('missing_inventory', lambda p: p.pop('inventory')),
        ('missing_ids', lambda p: p['inventory'].pop('expected_attempt_ids')),
        ('missing_count', lambda p: p['inventory'].pop('expected_count')),
        ('wrong_count', lambda p: p['inventory'].__setitem__('expected_count', 1)),
        ('duplicate_inventory_ids', lambda p: p['inventory'].__setitem__('expected_attempt_ids', ['A', 'A'])),
        ('omitted_failed_attempt', lambda p: p['attempts'].pop()),
        ('extra_uninventoried_attempt', lambda p: p['attempts'].append(dict(ROW, attempt_id='C', evidence_ref='ref-C'))),
        ('inventory_id_typo', lambda p: p['inventory'].__setitem__('expected_attempt_ids', ['A', 'X'])),
        ('foreign_inventory_commit', lambda p: p['inventory'].__setitem__('source_commit', '0' * 40)),
        ('noncanonical_inventory_id', lambda p: p['inventory'].__setitem__('expected_attempt_ids', ['A ', 'B'])),
        ('inventory_ids_wrong_type', lambda p: p['inventory'].__setitem__('expected_attempt_ids', 'AB')),
        ('boolean_expected_count', lambda p: p['inventory'].__setitem__('expected_count', True)),
    ]
    for name, mutate in mutations:
        p = copy.deepcopy(BASE); mutate(p)
        yield name, p, ('NOT_COMPUTABLE', None, None)


def main(candidate):
    total = passed = 0
    for name, payload, expected in cases():
        total += 1
        proc = subprocess.run([sys.executable, str(candidate)], input=json.dumps(payload).encode(),
                              capture_output=True, timeout=10, check=False)
        try:
            obj = json.loads(proc.stdout) if proc.returncode == 0 else {}
            actual = (obj.get('status'), obj.get('eligible_denominator'), obj.get('automated_numerator'))
        except (ValueError, UnicodeError):
            actual = (None, None, None)
        ok = actual == expected
        passed += int(ok)
        print(json.dumps({'case': name, 'expected': expected, 'actual': actual, 'pass': ok}, sort_keys=True))
    print(json.dumps({'passed': passed, 'total': total, 'scope': 'SYNTHETIC_INVENTORY_CONSISTENCY_NOT_AUTHENTICATED'}, sort_keys=True))
    return 0 if passed == total else 1


if __name__ == '__main__':
    sys.exit(main(Path(sys.argv[1])))
