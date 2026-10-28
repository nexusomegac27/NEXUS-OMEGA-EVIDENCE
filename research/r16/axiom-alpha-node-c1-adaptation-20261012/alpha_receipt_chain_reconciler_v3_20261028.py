#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""C1 isolated V3: portable path guard over pinned V2 receipt-chain audit.

This is a caller-supplied metadata check, not authenticated GitHub evidence.
The V2 source and its oracle remain immutable. No productive integration.
"""
import json
import re
import sys

import alpha_receipt_chain_reconciler_v2_20261028 as predecessor

WINDOWS_INVALID = frozenset('<>:"|?*')
WINDOWS_DEVICES = frozenset(('CON', 'PRN', 'AUX', 'NUL')) | frozenset(
    f'{prefix}{n}' for prefix in ('COM', 'LPT') for n in range(1, 10))


def validate_portable_path(path):
    # The predecessor already checks ASCII, exact canonical root, traversal,
    # slash separation and literal duplicate paths before this extension.
    for segment in path.split('/'):
        if segment.endswith(('.', ' ')):
            predecessor.fail('WINDOWS_TRAILING_DOT_SPACE')
        if any(char in WINDOWS_INVALID for char in segment):
            predecessor.fail('WINDOWS_INVALID_CHARACTER')
        if segment.split('.', 1)[0].upper() in WINDOWS_DEVICES:
            predecessor.fail('WINDOWS_DEVICE_NAME')


def audit(obj):
    result = predecessor.audit(obj)
    seen_portable = set()
    for record in obj['records']:
        for file_record in record['files']:
            path = file_record['path']
            validate_portable_path(path)
            key = path.casefold()  # V2 permits ASCII only; NFC adds no value.
            if key in seen_portable:
                predecessor.fail('PORTABLE_PATH_COLLISION')
            seen_portable.add(key)
    result['state'] = 'C1_CALLER_SUPPLIED_PORTABLE_INVENTORY_CHAIN_MATCH'
    result['portable_path_guard'] = 'PASS_SYNTHETIC_METADATA_ONLY'
    return result


def main():
    try:
        raw = sys.stdin.buffer.read(predecessor.MAX_BYTES + 1)
        if len(raw) > predecessor.MAX_BYTES:
            predecessor.fail('INPUT_TOO_LARGE')
        obj = json.loads(raw.decode('utf-8'),
                         object_pairs_hook=predecessor.unique_pairs,
                         parse_constant=predecessor.nonfinite)
        print(json.dumps(audit(obj), sort_keys=True, separators=(',', ':')))
        return 0
    except (ValueError, TypeError, UnicodeError, RecursionError) as exc:
        print('FAIL_CLOSED: ' + str(exc), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
