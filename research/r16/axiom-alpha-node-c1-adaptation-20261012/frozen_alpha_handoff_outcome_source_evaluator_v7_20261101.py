"""Frozen synthetic oracle: outcome-byte binding, committed before V7 candidate.
No live GitHub event authentication or completeness claims. Execute in subprocesses.
"""
import argparse
import base64
import copy
import hashlib
import json
import subprocess
import sys
from pathlib import Path

COMMIT = '265d760ce6a1e0e0bf4e526e48881d9ef55e3144'
ROW = {'routine': True, 'public': True, 'authorized': True,
       'accessible': True, 'completed': True, 'operator_nudge': False,
       'receipt_verified': True}
INV = {'source_commit': COMMIT, 'source_ref': 'SYNTHETIC_NOT_AUTHENTICATED',
       'expected_count': 2, 'expected_attempt_ids': ['A', 'B']}
BASE = {'pinned_commit': COMMIT, 'coverage_complete': True,
        'coverage_source': 'SYNTHETIC_DECLARED_ONLY',
        'inventory': INV,
        'attempts': [dict(ROW, attempt_id='A', evidence_ref='ref-A'),
                     dict(ROW, attempt_id='B', evidence_ref='ref-B', completed=False)]}


def encode(obj):
    raw = json.dumps(obj, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()
    return base64.b64encode(raw).decode(), hashlib.sha256(raw).hexdigest()


def make_payload(mode, modified, source=None):
    payload = copy.deepcopy(modified)
    src = copy.deepcopy(source if source is not None else BASE)
    source_doc = {'pinned_commit': src['pinned_commit'],
                  'coverage_source': src['coverage_source'],
                  'inventory': src['inventory']}
    if mode == 'v7':
        source_doc['attempts'] = src['attempts']
    b64, pin = encode(source_doc)
    payload['inventory_source_b64'] = b64
    return payload, pin


def cases():
    yield 'valid_1_of_2', copy.deepcopy(BASE), None, (2, 1)
    p = copy.deepcopy(BASE); p['attempts'][1]['completed'] = True
    yield 'valid_2_of_2', p, copy.deepcopy(p), (2, 2)
    p = copy.deepcopy(BASE); p['attempts'][1]['accessible'] = False
    yield 'valid_eligible_1_of_1', p, copy.deepcopy(p), (1, 1)
    p = copy.deepcopy(BASE); p['attempts'].reverse()
    yield 'valid_source_order_matches', p, copy.deepcopy(p), (2, 1)
    p = copy.deepcopy(BASE); p['attempts'][1]['completed'] = True
    yield 'forged_completion', p, None, None
    p = copy.deepcopy(BASE); p['attempts'][0]['receipt_verified'] = False
    yield 'forged_receipt_status', p, None, None
    p = copy.deepcopy(BASE); p['attempts'][0]['operator_nudge'] = True
    yield 'hidden_operator_nudge', p, None, None
    p = copy.deepcopy(BASE); p['attempts'][1]['authorized'] = False
    yield 'changed_authorization', p, None, None
    p = copy.deepcopy(BASE); p['attempts'][1]['accessible'] = False
    yield 'changed_accessibility', p, None, None
    p = copy.deepcopy(BASE); p['attempts'][0]['routine'] = False
    yield 'changed_routine_scope', p, None, None
    p = copy.deepcopy(BASE); p['attempts'][1]['evidence_ref'] = 'ref-B2'
    yield 'changed_evidence_ref', p, None, None
    p = copy.deepcopy(BASE); p['attempts'][1]['extra_metadata'] = 'unbound'
    yield 'unbound_row_extension', p, None, None
    p = copy.deepcopy(BASE); p['attempts'].reverse()
    yield 'unbound_order_change', p, None, None
    p = copy.deepcopy(BASE); p['attempts'].pop()
    yield 'omitted_attempt', p, None, None
    p = copy.deepcopy(BASE); p['inventory']['expected_count'] = 1
    yield 'inventory_count_mismatch', p, None, None
    p = copy.deepcopy(BASE); p['attempts'][1]['completed'] = 1
    yield 'wrong_boolean_type', p, None, None
    p = copy.deepcopy(BASE); p['coverage_source'] = 'CHANGED'
    yield 'coverage_source_mismatch', p, None, None
    p = copy.deepcopy(BASE); p['pinned_commit'] = '0' * 40
    yield 'commit_mismatch', p, None, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('candidate', type=Path)
    ap.add_argument('--mode', choices=['v6', 'v7'], required=True)
    args = ap.parse_args()
    total = passed = 0
    for name, modified, source, expected in cases():
        total += 1
        payload, pin = make_payload(args.mode, modified, source)
        proc = subprocess.run([sys.executable, str(args.candidate),
                               '--expected-sha256', pin,
                               '--expected-source-commit', COMMIT],
                              input=json.dumps(payload).encode(), capture_output=True,
                              timeout=10)
        try:
            result = json.loads(proc.stdout) if proc.returncode == 0 else {}
            actual = ((result.get('eligible_denominator'), result.get('automated_numerator'))
                      if result.get('status') == 'METRIC_READY_STRUCTURAL_ONLY' else None)
        except (ValueError, UnicodeError):
            actual = None
        ok = actual == expected
        passed += int(ok)
        print(json.dumps({'case': name, 'expected': expected,
                          'actual': actual, 'pass': ok}, sort_keys=True))
    print(json.dumps({'passed': passed, 'total': total,
                      'mode': args.mode, 'scope': 'SYNTHETIC_OUTCOME_BINDING_ONLY'}, sort_keys=True))
    return 0 if passed == total else 1


if __name__ == '__main__':
    sys.exit(main())
