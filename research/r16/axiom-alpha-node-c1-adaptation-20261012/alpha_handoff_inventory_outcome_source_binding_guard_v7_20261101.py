"""C1 isolated V7: source-byte bind both handoff census and outcome rows.
The caller MUST independently pin the SHA-256 and commit; this offline validator
cannot authenticate that pin, event completeness, GitHub actors, or live receipts.
"""
import argparse
import base64
import hashlib
import json
import sys

import alpha_handoff_inventory_source_binding_guard_v6_20261101 as prior


def strict_equal(left, right):
    """JSON structural equality without Python's bool == int / 1 == 1.0 aliases."""
    return (json.dumps(left, sort_keys=True, separators=(',', ':'), ensure_ascii=False) ==
            json.dumps(right, sort_keys=True, separators=(',', ':'), ensure_ascii=False))


def source_ok(data, expected_sha256, expected_commit):
    if type(data) is not dict or type(expected_sha256) is not str:
        return False
    if not prior.HEX64.fullmatch(expected_sha256) or not prior.HEX40.fullmatch(expected_commit):
        return False
    if data.get('pinned_commit') != expected_commit:
        return False
    encoded = data.get('inventory_source_b64')
    if type(encoded) is not str or len(encoded) > 4 * prior.MAX_SOURCE_BYTES // 3 + 8:
        return False
    try:
        raw = base64.b64decode(encoded, validate=True)
        if not raw or len(raw) > prior.MAX_SOURCE_BYTES:
            return False
        if hashlib.sha256(raw).hexdigest() != expected_sha256:
            return False
        source = json.loads(raw.decode('utf-8'),
                            object_pairs_hook=prior.prior.prior.unique_keys,
                            parse_constant=prior.prior.prior.reject_constant,
                            parse_float=prior.prior.prior.finite_float)
        if type(source) is not dict or set(source) != {
                'inventory', 'attempts', 'pinned_commit', 'coverage_source'}:
            return False
        return (source['pinned_commit'] == expected_commit and
                source['coverage_source'] == data.get('coverage_source') and
                type(source['attempts']) is list and
                strict_equal(source['inventory'], data.get('inventory')) and
                strict_equal(source['attempts'], data.get('attempts')) and
                prior.prior.inventory_ok(data))
    except (ValueError, TypeError, UnicodeError, OverflowError, RecursionError):
        return False


def evaluate(data, expected_sha256, expected_commit):
    if not source_ok(data, expected_sha256, expected_commit):
        result = prior.prior.fail()
        result['inventory_and_outcome_source_binding'] = False
        result['scope'] = 'SOURCE_INVENTORY_AND_OUTCOMES_DIGEST_MATCH_UNAUTHENTICATED'
        return result
    result = prior.prior.evaluate(data)
    result['inventory_and_outcome_source_binding'] = result['status'] != 'NOT_COMPUTABLE'
    result['scope'] = 'SOURCE_INVENTORY_AND_OUTCOMES_DIGEST_MATCH_UNAUTHENTICATED'
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--expected-sha256', required=True)
    parser.add_argument('--expected-source-commit', required=True)
    args = parser.parse_args()
    try:
        raw = sys.stdin.buffer.read(prior.prior.prior.MAX_BYTES + 1)
        if len(raw) > prior.prior.prior.MAX_BYTES:
            raise ValueError('INPUT_TOO_LARGE')
        data = json.loads(raw.decode('utf-8'),
                          object_pairs_hook=prior.prior.prior.unique_keys,
                          parse_constant=prior.prior.prior.reject_constant,
                          parse_float=prior.prior.prior.finite_float)
        result = evaluate(data, args.expected_sha256, args.expected_source_commit)
    except (ValueError, TypeError, UnicodeError, OverflowError, RecursionError):
        result = evaluate({}, args.expected_sha256, args.expected_source_commit)
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
