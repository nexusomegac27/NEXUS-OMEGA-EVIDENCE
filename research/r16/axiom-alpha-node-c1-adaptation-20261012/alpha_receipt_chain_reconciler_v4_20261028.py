#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""C1 isolated V4: reject file/directory prefix conflicts in additive inventories.

Caller-supplied metadata only; this does not authenticate GitHub API origins,
file bytes, external actors, or project-wide handoff denominators.
"""
import json
import sys

import alpha_receipt_chain_reconciler_v3_20261028 as predecessor


def audit(obj):
    result = predecessor.audit(obj)
    file_keys = {f['path'].casefold() for r in obj['records'] for f in r['files']}
    for record in obj['records']:
        for file_record in record['files']:
            components = file_record['path'].split('/')
            for end in range(1, len(components)):
                if '/'.join(components[:end]).casefold() in file_keys:
                    predecessor.predecessor.fail('FILE_DIRECTORY_PREFIX_CONFLICT')
    result['state'] = 'C1_CALLER_SUPPLIED_PREFIX_SAFE_INVENTORY_CHAIN_MATCH'
    result['prefix_guard'] = 'PASS_SYNTHETIC_METADATA_ONLY'
    return result


def main():
    try:
        raw = sys.stdin.buffer.read(predecessor.predecessor.MAX_BYTES + 1)
        if len(raw) > predecessor.predecessor.MAX_BYTES:
            predecessor.predecessor.fail('INPUT_TOO_LARGE')
        obj = json.loads(raw.decode('utf-8'),
                         object_pairs_hook=predecessor.predecessor.unique_pairs,
                         parse_constant=predecessor.predecessor.nonfinite)
        print(json.dumps(audit(obj), sort_keys=True, separators=(',', ':')))
        return 0
    except (ValueError, TypeError, UnicodeError, RecursionError) as exc:
        print('FAIL_CLOSED: ' + str(exc), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
