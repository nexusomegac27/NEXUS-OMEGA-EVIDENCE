#!/usr/bin/env python3
"""Isolated C1 successor: reject noncanonical GitHub compare file paths.

This wrapper retains the pinned V1 structural checks and adds a conservative
path/partial-compare guard. It does not authenticate caller-supplied API data,
verify live main, modify the repository or promote scientific claims.

PINNED_V1_GIT_BLOB=bd0e426f79123e472138e216ea9f42d529724efa
FROZEN_ORACLE_FIRST_COMMIT=f1eb35e507193aff228cb16c1e3c4106ba746557
"""
import json
import posixpath
import sys

import alpha_issue93_pr_compare_crosscheck_v1_20261027 as base


def audit(payload):
    result = base.audit(payload)
    compare = payload['compare']
    if compare.get('too_large') not in (None, False) or type(compare.get('too_large')) not in (type(None), bool):
        base.fail('COMPARE_COMPLETENESS_NOT_ESTABLISHED')
    for entry in compare['files']:
        name = entry['filename']
        if (posixpath.normpath(name) != name or
                '\\' in name or
                any(ord(char) < 32 or ord(char) == 127 for char in name) or
                not name.startswith(base.ROOT)):
            base.fail('NONCANONICAL_COMPARE_PATH')
    return result


def main():
    try:
        raw = sys.stdin.buffer.read(base.MAX_BYTES + 1)
        if len(raw) > base.MAX_BYTES:
            base.fail('INPUT_TOO_LARGE')
        payload = json.loads(raw.decode('utf-8'), object_pairs_hook=base.unique_pairs,
                             parse_constant=base.finite_constant)
        print(json.dumps(audit(payload), sort_keys=True, separators=(',', ':')))
        return 0
    except (ValueError, TypeError, UnicodeError, RecursionError) as exc:
        print('FAIL_CLOSED: ' + str(exc), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
