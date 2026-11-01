"""C1 research-only: bind a declared handoff inventory to separately pinned source bytes.
The caller MUST independently obtain --expected-sha256; this tool does not authenticate
that digest, source, GitHub actor, event completeness, or any live handoff.
"""
import argparse
import base64
import hashlib
import json
import re
import sys

import alpha_handoff_inventory_consistency_guard_v5_20261101 as prior

HEX64 = re.compile(r"[0-9a-f]{64}\Z")
HEX40 = re.compile(r"[0-9a-f]{40}\Z")
MAX_SOURCE_BYTES = 1024 * 1024


def source_ok(data, expected_sha256, expected_commit):
    if type(data) is not dict or not HEX64.fullmatch(expected_sha256):
        return False
    if not HEX40.fullmatch(expected_commit) or data.get('pinned_commit') != expected_commit:
        return False
    encoded = data.get('inventory_source_b64')
    if type(encoded) is not str or len(encoded) > 4 * MAX_SOURCE_BYTES // 3 + 8:
        return False
    try:
        raw = base64.b64decode(encoded, validate=True)
        if not raw or len(raw) > MAX_SOURCE_BYTES:
            return False
        if hashlib.sha256(raw).hexdigest() != expected_sha256:
            return False
        source = json.loads(raw.decode('utf-8'), object_pairs_hook=prior.prior.unique_keys,
                            parse_constant=prior.prior.reject_constant,
                            parse_float=prior.prior.finite_float)
    except (ValueError, TypeError, UnicodeError, OverflowError, RecursionError):
        return False
    if type(source) is not dict or set(source) != {'inventory', 'pinned_commit', 'coverage_source'}:
        return False
    return (source['pinned_commit'] == expected_commit and
            source['coverage_source'] == data.get('coverage_source') and
            source['inventory'] == data.get('inventory') and
            prior.inventory_ok(data))


def evaluate(data, expected_sha256, expected_commit):
    if not source_ok(data, expected_sha256, expected_commit):
        result = prior.fail()
        result['inventory_source_binding'] = False
        result['scope'] = 'SOURCE_BYTES_DIGEST_MATCH_UNAUTHENTICATED'
        return result
    result = prior.evaluate(data)
    result['inventory_source_binding'] = result['status'] != 'NOT_COMPUTABLE'
    result['scope'] = 'SOURCE_BYTES_DIGEST_MATCH_UNAUTHENTICATED'
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--expected-sha256', required=True)
    parser.add_argument('--expected-source-commit', required=True)
    args = parser.parse_args()
    try:
        raw = sys.stdin.buffer.read(prior.prior.MAX_BYTES + 1)
        if len(raw) > prior.prior.MAX_BYTES:
            raise ValueError('INPUT_TOO_LARGE')
        data = json.loads(raw.decode('utf-8'), object_pairs_hook=prior.prior.unique_keys,
                          parse_constant=prior.prior.reject_constant,
                          parse_float=prior.prior.finite_float)
        result = evaluate(data, args.expected_sha256, args.expected_source_commit)
    except (ValueError, TypeError, UnicodeError, OverflowError, RecursionError):
        result = evaluate({}, args.expected_sha256, args.expected_source_commit)
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
