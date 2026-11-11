"""C1 isolated V7: preserve V6 checks and fail closed on Decimal exponent overflow.

Only a structured error-boundary repair. No source mutation, network, or claims.
"""
import json
import sys
from decimal import InvalidOperation
from alpha_pr124_manifest_crossrow_path_guard_v3_20261024 import _reject_duplicate_keys
from alpha_pr124_manifest_crossrow_safe_integer_guard_v4_20261024 import _safe_int
from alpha_pr124_manifest_row_composed_guard_v5_20261024 import check_composed
from alpha_pr124_manifest_float_roundtrip_guard_v6_20261024 import _parse_roundtrip_float


def main():
    try:
        payload = json.load(sys.stdin, object_pairs_hook=_reject_duplicate_keys,
                            parse_float=_parse_roundtrip_float, parse_int=_safe_int,
                            parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))
        result = check_composed(payload)
    except (ValueError, TypeError, json.JSONDecodeError, InvalidOperation, OverflowError):
        result = {'status': 'FAIL_CLOSED', 'reason_codes': ['INVALID_JSON'],
                  'row_count': 0, 'distinct_casefold_count': 0}
    print(json.dumps(result, sort_keys=True, allow_nan=False))
    return 0 if result['status'] == 'PASS_C1' else 1


if __name__ == '__main__':
    sys.exit(main())
