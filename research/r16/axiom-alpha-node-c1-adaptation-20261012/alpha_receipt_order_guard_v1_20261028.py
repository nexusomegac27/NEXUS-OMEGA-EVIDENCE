#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""C1 isolated receipt-order witness; complement, NOT replacement for V5.

Reject self-referential or backwards GitHub issue-comment IDs in an additive
receipt chain. All inputs are caller-supplied, not authenticated GitHub API
responses. This guard alone does not verify PRs, commits, hashes or sources.
"""
import json
import sys

MAX_BYTES = 1_048_576
OBJECT = 'NEXUS_OMEGA_ALPHA_RECEIPT_ORDER_GUARD_V1'


def fail(code):
    raise ValueError(code)


def unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            fail('DUPLICATE_JSON_KEY')
        result[key] = value
    return result


def nonfinite(_):
    fail('NONFINITE_JSON')


def fields(obj, keys, code):
    if type(obj) is not dict or set(obj) != keys:
        fail(code)


def positive_int(value):
    return type(value) is int and value > 0


def audit(obj):
    fields(obj, {'object', 'scope', 'records'}, 'INVALID_ENVELOPE')
    if obj['object'] != OBJECT:
        fail('INVALID_OBJECT')
    fields(obj['scope'], {'predecessor_receipt_id'}, 'INVALID_SCOPE')
    previous = obj['scope']['predecessor_receipt_id']
    if not positive_int(previous):
        fail('INVALID_SCOPE')
    records = obj['records']
    if type(records) is not list or not 1 <= len(records) <= 100:
        fail('INVALID_RECORD_COUNT')
    for record in records:
        fields(record, {'receipt_id', 'receipt_predecessor_id'}, 'INVALID_RECORD')
        current, parent = record['receipt_id'], record['receipt_predecessor_id']
        if not positive_int(current) or not positive_int(parent):
            fail('INVALID_RECEIPT_ID')
        if parent != previous:
            fail('RECEIPT_PREDECESSOR_MISMATCH')
        if current <= parent:
            fail('RECEIPT_NOT_CHRONOLOGICAL')
        previous = current
    return {'state': 'C1_RECEIPT_ORDER_SCOPED_MATCH',
            'receipt_order_guard': 'PASS_CALLER_SUPPLIED_METADATA_ONLY',
            'records_checked': len(records),
            'api_origin_authenticated': False,
            'project_automation_rate': 'NOT_COMPUTABLE',
            'project_readback_rate': 'NOT_COMPUTABLE',
            'claim_ceiling': 'C1_DESCRIPTIVE_ONLY'}


def main():
    try:
        payload = sys.stdin.buffer.read(MAX_BYTES + 1)
        if len(payload) > MAX_BYTES:
            fail('INPUT_TOO_LARGE')
        obj = json.loads(payload.decode('utf-8'),
                         object_pairs_hook=unique_pairs, parse_constant=nonfinite)
        print(json.dumps(audit(obj), sort_keys=True, separators=(',', ':')))
        return 0
    except (ValueError, TypeError, UnicodeError, RecursionError) as exc:
        print('FAIL_CLOSED: ' + str(exc), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
