#!/usr/bin/env python3
"""C1-only strict Unicode-scalar intake for caller-supplied Issue #93 JSON.

Reject unpaired UTF-16 surrogate escapes in JSON object keys and values;
accept valid escaped pairs/non-BMP scalars. Structural audit is unchanged.
This does not authenticate GitHub comments, actors, or main commits.
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


def require_unicode_scalars(payload):
    # Iterative traversal avoids introducing a second recursion-depth failure.
    pending = [payload]
    while pending:
        value = pending.pop()
        if isinstance(value, str):
            if any(0xD800 <= ord(ch) <= 0xDFFF for ch in value):
                raise ValueError('UNPAIRED_UNICODE_SURROGATE')
        elif isinstance(value, dict):
            pending.extend(value.keys())
            pending.extend(value.values())
        elif isinstance(value, list):
            pending.extend(value)


def audit_bytes(raw):
    if not isinstance(raw, bytes):
        raise TypeError('INPUT_NOT_BYTES')
    if len(raw) > MAX_INPUT_BYTES:
        raise ValueError('INPUT_TOO_LARGE')
    payload = json.loads(raw.decode('utf-8'), object_pairs_hook=unique_pairs,
                         parse_constant=reject_nonfinite_constant,
                         parse_float=finite_float)
    require_unicode_scalars(payload)
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
