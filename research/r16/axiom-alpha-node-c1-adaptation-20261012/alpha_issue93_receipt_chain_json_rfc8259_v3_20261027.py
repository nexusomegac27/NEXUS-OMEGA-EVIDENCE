#!/usr/bin/env python3
"""Fail-closed finite-JSON intake for the existing read-only Issue #93 auditor.

C1 research only. Reject duplicate keys, non-RFC numeric constants, float
conversion overflow and excessive nesting. The supplied snapshot remains
unauthenticated; this does not verify GitHub actors, commits, or completeness.
"""
import importlib.util
import json
import math
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
BASELINE = HERE / 'alpha_issue93_receipt_chain_audit_v1_20261026.py'
MAX_INPUT_BYTES = 1048576


def unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('DUPLICATE_JSON_KEY:' + key)
        result[key] = value
    return result


def reject_nonfinite_constant(token):
    raise ValueError('NONFINITE_JSON_CONSTANT:' + token)


def finite_float(token):
    number = float(token)
    if not math.isfinite(number):
        raise ValueError('NONFINITE_JSON_NUMBER')
    return number


def audit_bytes(raw):
    if not isinstance(raw, bytes):
        raise TypeError('INPUT_NOT_BYTES')
    if len(raw) > MAX_INPUT_BYTES:
        raise ValueError('INPUT_TOO_LARGE')
    payload = json.loads(raw.decode('utf-8'), object_pairs_hook=unique_pairs,
                         parse_constant=reject_nonfinite_constant,
                         parse_float=finite_float)
    spec = importlib.util.spec_from_file_location('pinned_issue93_structural_auditor_v1', BASELINE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.audit(payload)


def main():
    try:
        raw = sys.stdin.buffer.read(MAX_INPUT_BYTES + 1)
        print(json.dumps(audit_bytes(raw), sort_keys=True))
        return 0
    except (ValueError, TypeError, UnicodeError, RecursionError) as exc:
        print('FAIL_CLOSED: ' + str(exc), file=sys.stderr)
        return 2


if __name__ == '__main__': sys.exit(main())
