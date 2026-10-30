#!/usr/bin/env python3
"""Isolated C1 V3: bind commit locator SHA to the declared source_commit.

Syntax-only correction atop V2; no source retrieval, actor authentication, or project rate.
"""
import json
import sys
from urllib.parse import urlsplit
from alpha_handoff_attempt_denominator_v1_20261030 import no_duplicates, reject_constant
from alpha_handoff_denominator_scope_binding_v2_20261030 import reduce as reduce_v2


def reduce(data):
    result = reduce_v2(data)
    for row in data['attempts']:
        parts = urlsplit(row['source_ref']).path.split('/')
        # V2 has already validated canonical repository origin, URL and source_commit.
        if parts[3] == 'commit' and parts[4] != row['source_commit']:
            raise ValueError('COMMIT_URL_SOURCE_COMMIT_MISMATCH')
    result['schema'] = 'ALPHA_HANDOFF_ATTEMPT_DENOMINATOR_RESULT_V3'
    result['commit_ref_binding'] = 'COMMIT_URL_EQUALS_SOURCE_COMMIT_SYNTAX_ONLY'
    return result


def main():
    try:
        data = json.load(sys.stdin, object_pairs_hook=no_duplicates,
                         parse_constant=reject_constant)
        result = reduce(data)
    except (ValueError, TypeError, KeyError, IndexError, json.JSONDecodeError) as exc:
        print(json.dumps({'error':str(exc),'state':'FAIL_CLOSED'},sort_keys=True))
        return 2
    print(json.dumps(result,sort_keys=True,separators=(',',':')))
    return 0


if __name__ == '__main__':
    sys.exit(main())
