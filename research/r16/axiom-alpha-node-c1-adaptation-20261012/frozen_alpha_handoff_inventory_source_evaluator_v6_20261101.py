"""Frozen C1 synthetic oracle for source-byte-bound inventory versus prior V5.
Commit this evaluator before the candidate; no producer-controlled oracle edits.
"""
import base64
import copy
import hashlib
import json
import subprocess
import sys
from pathlib import Path

COMMIT = 'b23cf96871608a18d21350f9c3df0fb075d9cec1'
ROW = {'routine': True, 'public': True, 'authorized': True,
       'accessible': True, 'completed': True, 'operator_nudge': False,
       'receipt_verified': True}
SOURCE = {'pinned_commit': COMMIT, 'coverage_source': 'SYNTHETIC_DECLARED_ONLY',
          'inventory': {'source_commit': COMMIT, 'source_ref': 'SYNTHETIC_UNVERIFIED',
                        'expected_count': 2, 'expected_attempt_ids': ['A', 'B']}}
RAW = json.dumps(SOURCE, sort_keys=True, separators=(',', ':')).encode()
PIN = hashlib.sha256(RAW).hexdigest()
BASE = {'pinned_commit': COMMIT, 'coverage_complete': True,
        'coverage_source': SOURCE['coverage_source'],
        'inventory': copy.deepcopy(SOURCE['inventory']),
        'attempts': [dict(ROW, attempt_id='A', evidence_ref='ref-A'),
                     dict(ROW, attempt_id='B', evidence_ref='ref-B', completed=False)],
        'inventory_source_b64': base64.b64encode(RAW).decode()}


def cases():
    yield 'source_bound_2_attempts', copy.deepcopy(BASE), PIN, COMMIT, (2, 1)
    p = copy.deepcopy(BASE); p['attempts'][1]['completed'] = True
    yield 'source_bound_2_success', p, PIN, COMMIT, (2, 2)
    p = copy.deepcopy(BASE); p['attempts'].reverse()
    yield 'source_bound_order_independent', p, PIN, COMMIT, (2, 1)
    p = copy.deepcopy(BASE); p['attempts'][1]['accessible'] = False
    yield 'ineligible_still_in_census', p, PIN, COMMIT, (1, 1)
    p = copy.deepcopy(BASE); p['attempts'] = p['attempts'][:1]; p['inventory']['expected_attempt_ids'] = ['A']; p['inventory']['expected_count'] = 1
    yield 'coordinated_inventory_attempt_truncation', p, PIN, COMMIT, None
    p = copy.deepcopy(BASE); p['inventory']['source_ref'] = 'ALTERED'
    yield 'altered_inventory_source_ref', p, PIN, COMMIT, None
    p = copy.deepcopy(BASE); p['coverage_source'] = 'ALTERED'
    yield 'altered_coverage_source', p, PIN, COMMIT, None
    p = copy.deepcopy(BASE); p['inventory_source_b64'] = base64.b64encode(RAW + b' ').decode()
    yield 'changed_source_bytes', p, PIN, COMMIT, None
    p = copy.deepcopy(BASE)
    yield 'wrong_expected_digest', p, '0' * 64, COMMIT, None
    p = copy.deepcopy(BASE)
    yield 'wrong_expected_commit', p, PIN, '0' * 40, None
    p = copy.deepcopy(BASE); p.pop('inventory_source_b64')
    yield 'missing_source_bytes', p, PIN, COMMIT, None
    p = copy.deepcopy(BASE); p['inventory_source_b64'] = '%%%'
    yield 'invalid_base64', p, PIN, COMMIT, None
    p = copy.deepcopy(BASE); p['inventory_source_b64'] = base64.b64encode(b'{"inventory":{},"inventory":{}}').decode()
    yield 'duplicate_key_source', p, hashlib.sha256(b'{"inventory":{},"inventory":{}}').hexdigest(), COMMIT, None
    p = copy.deepcopy(BASE); p['attempts'].pop()
    yield 'omitted_failed_attempt', p, PIN, COMMIT, None
    p = copy.deepcopy(BASE); p['inventory']['expected_attempt_ids'] = ['A', 'A']
    yield 'duplicate_inventory_ids', p, PIN, COMMIT, None


def main(candidate):
    total = passed = 0
    for name, payload, pin, commit, expected in cases():
        total += 1
        cmd = [sys.executable, str(candidate)]
        if 'inventory_consistency_guard_v5' not in candidate.name:
            cmd += ['--expected-sha256', pin, '--expected-source-commit', commit]
        proc = subprocess.run(cmd, input=json.dumps(payload).encode(),
                              capture_output=True, timeout=10)
        try:
            obj = json.loads(proc.stdout) if proc.returncode == 0 else {}
            actual = (obj.get('eligible_denominator'), obj.get('automated_numerator')) if obj.get('status') == 'METRIC_READY_STRUCTURAL_ONLY' else None
        except (ValueError, UnicodeError):
            actual = None
        ok = actual == expected
        passed += int(ok)
        print(json.dumps({'case': name, 'expected': expected, 'actual': actual, 'pass': ok}, sort_keys=True))
    print(json.dumps({'passed': passed, 'total': total, 'scope': 'SYNTHETIC_SOURCE_DIGEST_BINDING_ONLY'}, sort_keys=True))
    return 0 if passed == total else 1


if __name__ == '__main__':
    sys.exit(main(Path(sys.argv[1])))
