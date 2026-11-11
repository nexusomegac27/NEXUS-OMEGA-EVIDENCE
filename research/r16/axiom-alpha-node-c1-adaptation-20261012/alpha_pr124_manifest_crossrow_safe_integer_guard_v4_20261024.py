"""C1 isolated V4: add safe-integer JSON parsing to pinned V3 path guard.

Rejects integers outside the cross-runtime exact JSON range even in metadata.
Imports only the append-only V3 sibling; no source rewrite, runtime or network.
"""
import json
import sys
from alpha_pr124_manifest_crossrow_path_guard_v3_20261024 import (
    _reject_duplicate_keys, _parse_finite_float, check_manifest_paths)

SAFE = (1 << 53) - 1


def _safe_int(token):
    value = int(token)
    if not -SAFE <= value <= SAFE:
        raise ValueError('unsafe JSON integer')
    return value


def main():
    try:
        payload = json.load(sys.stdin, object_pairs_hook=_reject_duplicate_keys,
                            parse_float=_parse_finite_float, parse_int=_safe_int,
                            parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))
        result = check_manifest_paths(payload)
    except (ValueError, TypeError, json.JSONDecodeError):
        result = {'status': 'FAIL_CLOSED', 'reason_codes': ['INVALID_JSON'],
                  'row_count': 0, 'distinct_casefold_count': 0}
    print(json.dumps(result, sort_keys=True, allow_nan=False))
    return 0 if result['status'] == 'PASS_C1' else 1


if __name__ == '__main__':
    sys.exit(main())
