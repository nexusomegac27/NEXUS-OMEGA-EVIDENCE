#!/usr/bin/env python3
"""Strict JSON envelope for the existing read-only Issue #93 C1 structural auditor.

Reject duplicate JSON object keys at any nesting depth before the existing
structural auditor sees a caller-supplied snapshot. This does not authenticate
GitHub actors, establish completeness, or verify actual main commits.
"""
import importlib.util
import json
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


def audit_bytes(raw):
    if not isinstance(raw, bytes):
        raise TypeError('INPUT_NOT_BYTES')
    if len(raw) > MAX_INPUT_BYTES:
        raise ValueError('INPUT_TOO_LARGE')
    payload = json.loads(raw.decode('utf-8'), object_pairs_hook=unique_pairs)
    spec = importlib.util.spec_from_file_location('pinned_issue93_structural_auditor_v1', BASELINE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.audit(payload)


def main():
    try:
        raw = sys.stdin.buffer.read(MAX_INPUT_BYTES + 1)
        print(json.dumps(audit_bytes(raw), sort_keys=True))
        return 0
    except (ValueError, TypeError, UnicodeError) as exc:
        print('FAIL_CLOSED: ' + str(exc), file=sys.stderr)
        return 2


if __name__ == '__main__': sys.exit(main())
