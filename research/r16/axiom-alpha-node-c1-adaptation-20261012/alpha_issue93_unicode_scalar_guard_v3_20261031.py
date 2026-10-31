#!/usr/bin/env python3
"""Isolated C1 V3: V2 finite JSON guard plus strict Unicode scalar validation."""
import json
import sys
from alpha_issue93_double_inventory_guard_v1_20261031 import evaluate, unique, reject_constant
from alpha_issue93_double_inventory_nonfinite_exponent_v2_20261031 import finite_float


def validate_scalars(value):
    if isinstance(value, str):
        if any(0xD800 <= ord(character) <= 0xDFFF for character in value):
            raise ValueError('unpaired_unicode_surrogate')
    elif isinstance(value, list):
        for child in value:
            validate_scalars(child)
    elif isinstance(value, dict):
        for key, child in value.items():
            validate_scalars(key)
            validate_scalars(child)


def main():
    try:
        obj = json.loads(sys.stdin.read(), object_pairs_hook=unique,
                         parse_constant=reject_constant, parse_float=finite_float)
        validate_scalars(obj)
        print(json.dumps(evaluate(obj), sort_keys=True))
    except (ValueError, TypeError, KeyError, OverflowError, UnicodeError) as exc:
        print(json.dumps({'status': 'FAIL_CLOSED', 'reason': str(exc)}))
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
