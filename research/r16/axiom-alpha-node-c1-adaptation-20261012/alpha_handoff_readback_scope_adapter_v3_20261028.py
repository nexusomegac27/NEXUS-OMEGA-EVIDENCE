#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Isolated v3 C1 readback scope guard over immutable v2 census source.

Caller-supplied data only; no GitHub authentication or project-wide claims.
"""
import json
import sys
import alpha_handoff_page_census_witness_v2_20261028 as base


def audit(obj):
    result = base.audit(obj)
    scoped = result['readback_rate'] if obj['scope']['coverage'] == 'DECLARED_COMPLETE' else 'NOT_COMPUTABLE'
    result['readback_rate'] = scoped
    result['scope_readback_rate'] = scoped
    result['project_readback_rate'] = 'NOT_COMPUTABLE'
    return result


def main():
    try:
        raw = sys.stdin.buffer.read(base.MAX_INPUT + 1)
        if len(raw) > base.MAX_INPUT:
            base.fail('INPUT_TOO_LARGE')
        obj = json.loads(raw.decode('utf-8'), object_pairs_hook=base.unique_pairs,
                         parse_constant=base.nonfinite)
        print(json.dumps(audit(obj), sort_keys=True, separators=(',', ':')))
        return 0
    except (ValueError, TypeError, UnicodeError, RecursionError) as exc:
        print('FAIL_CLOSED: ' + str(exc), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
