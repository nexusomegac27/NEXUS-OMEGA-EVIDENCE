#!/usr/bin/env python3
"""Isolated C1 V2: preserve pinned V1 inventory logic; reject overflow JSON floats."""
import json
import math
import sys
from alpha_issue93_double_inventory_guard_v1_20261031 import evaluate, unique, reject_constant


def finite_float(token):
    value = float(token)
    if not math.isfinite(value):
        raise ValueError('nonfinite_exponent_json')
    return value


def main():
    try:
        obj = json.loads(sys.stdin.read(), object_pairs_hook=unique,
                         parse_constant=reject_constant, parse_float=finite_float)
        print(json.dumps(evaluate(obj), sort_keys=True))
    except (ValueError, TypeError, KeyError, OverflowError) as exc:
        print(json.dumps({'status': 'FAIL_CLOSED', 'reason': str(exc)}))
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
