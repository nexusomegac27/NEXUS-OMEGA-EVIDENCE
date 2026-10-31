#!/usr/bin/env python3
"""Isolated C1 V4: bounded UTF-8 JSON input, preserving V3 scalar and V2 finite checks."""
import json
import sys
from alpha_issue93_double_inventory_guard_v1_20261031 import evaluate, unique, reject_constant
from alpha_issue93_double_inventory_nonfinite_exponent_v2_20261031 import finite_float
from alpha_issue93_unicode_scalar_guard_v3_20261031 import validate_scalars

MAX_INPUT_BYTES = 4 * 1024 * 1024


def main():
    try:
        raw = sys.stdin.buffer.read(MAX_INPUT_BYTES + 1)
        if len(raw) > MAX_INPUT_BYTES:
            raise ValueError('json_input_exceeds_4mib')
        obj = json.loads(raw.decode('utf-8'), object_pairs_hook=unique,
                         parse_constant=reject_constant, parse_float=finite_float)
        validate_scalars(obj)
        print(json.dumps(evaluate(obj), sort_keys=True))
    except RecursionError:
        print(json.dumps({'status': 'FAIL_CLOSED', 'reason': 'json_recursion_limit'}))
        return 2
    except (ValueError, TypeError, KeyError, OverflowError, UnicodeError) as exc:
        print(json.dumps({'status': 'FAIL_CLOSED', 'reason': str(exc)}))
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
