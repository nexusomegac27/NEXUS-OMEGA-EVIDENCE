#!/usr/bin/env python3
"""Isolated C1 V3: portable GitHub compare-path guard for Windows/Unicode.

Retains pinned V1+V2 checks, adds a conservative Windows/Unicode name
portability filter and casefold-collision detection. A PASS is only structural
consistency of caller-supplied snapshots, NOT API authentication or live main.

PINNED_V2_GIT_BLOB=4e09bb66b18bc6c0b381b5f6e7e358bb385e099e
FROZEN_ORACLE_FIRST_COMMIT=86ad1a732072999b29eddf62dfb36897287b4d9a
"""
import json
import sys
import unicodedata

import alpha_issue93_pr_compare_crosscheck_v2_20261027 as base

RESERVED = {'CON', 'PRN', 'AUX', 'NUL'} | {
    prefix + str(number) for prefix in ('COM', 'LPT') for number in range(1, 10)
}
WINDOWS_FORBIDDEN = set('<>:"|?*')
UNSAFE_CATEGORIES = {'Cc', 'Cf', 'Cs', 'Zl', 'Zp'}


def audit(payload):
    result = base.audit(payload)
    seen_folded = set()
    for entry in payload['compare']['files']:
        name = entry['filename']
        relative = name[len(base.base.ROOT):]
        if (unicodedata.normalize('NFC', relative) != relative or
                any(unicodedata.category(char) in UNSAFE_CATEGORIES or
                    char in WINDOWS_FORBIDDEN for char in relative)):
            base.base.fail('NONPORTABLE_UNICODE_OR_WINDOWS_CHARACTER')
        for component in relative.split('/'):
            if (not component or component.endswith(('.', ' ')) or
                    component.split('.', 1)[0].upper() in RESERVED):
                base.base.fail('NONPORTABLE_WINDOWS_COMPONENT')
        folded = relative.casefold()
        if folded in seen_folded:
            base.base.fail('CROSS_PLATFORM_CASEFOLD_COLLISION')
        seen_folded.add(folded)
    return result


def main():
    try:
        raw = sys.stdin.buffer.read(base.base.MAX_BYTES + 1)
        if len(raw) > base.base.MAX_BYTES:
            base.base.fail('INPUT_TOO_LARGE')
        payload = json.loads(raw.decode('utf-8'),
                             object_pairs_hook=base.base.unique_pairs,
                             parse_constant=base.base.finite_constant)
        print(json.dumps(audit(payload), sort_keys=True, separators=(',', ':')))
        return 0
    except (ValueError, TypeError, UnicodeError, RecursionError) as exc:
        print('FAIL_CLOSED: ' + str(exc), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
