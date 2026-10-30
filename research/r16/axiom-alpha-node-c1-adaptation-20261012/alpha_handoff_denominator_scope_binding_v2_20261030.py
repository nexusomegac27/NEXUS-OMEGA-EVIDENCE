#!/usr/bin/env python3
"""Isolated C1 wrapper: V1 attempt accounting + existing repository-scoped URL preflight.

Neither source syntax nor producer-declared attempt flags authenticate a GitHub actor,
source bytes, completeness of attempts, or any project-wide target metric.
"""
import json
import sys
from alpha_handoff_attempt_denominator_v1_20261030 import reduce as reduce_v1, no_duplicates, reject_constant
from alpha_handoff_source_url_guard_v1_20261030 import validate as validate_url


def reduce(data):
    result = reduce_v1(data)
    for row in data['attempts']:
        validate_url({'source_ref':row.get('source_ref'),
                      'source_commit':row.get('source_commit')})
    result['schema'] = 'ALPHA_HANDOFF_ATTEMPT_DENOMINATOR_RESULT_V2'
    result['source_scope_preflight'] = 'CANONICAL_REPO_SYNTAX_ONLY_NOT_AUTHENTICATED'
    return result


def main():
    try:
        data = json.load(sys.stdin, object_pairs_hook=no_duplicates,
                         parse_constant=reject_constant)
        result = reduce(data)
    except (ValueError, TypeError, KeyError, json.JSONDecodeError) as exc:
        print(json.dumps({'error':str(exc),'state':'FAIL_CLOSED'},sort_keys=True))
        return 2
    print(json.dumps(result,sort_keys=True,separators=(',',':')))
    return 0


if __name__=='__main__':
    sys.exit(main())
