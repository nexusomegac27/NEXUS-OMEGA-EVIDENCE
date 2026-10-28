#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""C1 isolated V5: fail closed on repeated main commit IDs in additive PR chains.

Git commit graphs cannot contain self-parents or cycles. This only checks
caller-supplied metadata; it cannot authenticate a GitHub API response.
"""
import json
import sys

import alpha_receipt_chain_reconciler_v4_20261028 as predecessor


def audit(obj):
    result = predecessor.audit(obj)
    seen = {obj['scope']['base_sha']}
    for record in obj['records']:
        commit = record['merge_sha']
        if commit in seen:
            predecessor.predecessor.predecessor.fail('REPEATED_MAIN_COMMIT_SHA')
        seen.add(commit)
    result['state'] = 'C1_CALLER_SUPPLIED_ACYCLIC_ADDITIVE_CHAIN_MATCH'
    result['commit_acyclic_guard'] = 'PASS_SYNTHETIC_METADATA_ONLY'
    return result


def main():
    parser = predecessor.predecessor.predecessor
    try:
        payload = sys.stdin.buffer.read(parser.MAX_BYTES + 1)
        if len(payload) > parser.MAX_BYTES:
            parser.fail('INPUT_TOO_LARGE')
        obj = json.loads(payload.decode('utf-8'),
                         object_pairs_hook=parser.unique_pairs,
                         parse_constant=parser.nonfinite)
        print(json.dumps(audit(obj), sort_keys=True, separators=(',', ':')))
        return 0
    except (ValueError, TypeError, UnicodeError, RecursionError) as exc:
        print('FAIL_CLOSED: ' + str(exc), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
