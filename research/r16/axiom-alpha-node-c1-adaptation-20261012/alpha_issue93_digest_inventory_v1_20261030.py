#!/usr/bin/env python3
"""Offline, digest-only inventory of public Issue #93 API comment bodies.

No GitHub fetch or actor authentication. No original comment bodies in output.
The independently retained inventory is only a future comparison reference.
"""
import hashlib
import json
import re
import sys

SOURCE = 'nexusomegac27/NEXUS-OMEGA-EVIDENCE/issues/93'
HEX40 = re.compile(r'[0-9a-f]{40}\\Z')

class Reject(ValueError):
    pass

def unique_pairs(pairs):
    out = {}
    for key, value in pairs:
        if key in out:
            raise Reject('DUPLICATE_JSON_KEY')
        out[key] = value
    return out

def require(test, error):
    if not test:
        raise Reject(error)

def produce(obj):
    require(type(obj) is dict, 'BAD_ROOT')
    require(set(obj) == {'source', 'main_sha', 'declared_count', 'comments'}, 'BAD_FIELDS')
    require(obj['source'] == SOURCE, 'SOURCE_MISMATCH')
    require(type(obj['main_sha']) is str and HEX40.fullmatch(obj['main_sha']), 'BAD_MAIN_SHA')
    n = obj['declared_count']
    require(type(n) is int and 1 <= n <= 100000, 'BAD_COUNT')
    rows = obj['comments']
    require(type(rows) is list and len(rows) == n, 'POPULATION_INCOMPLETE')
    pins, last = [], 0
    for row in rows:
        require(type(row) is dict and set(row) == {'id', 'body'}, 'BAD_ROW')
        ident, body = row['id'], row['body']
        require(type(ident) is int and ident > last, 'ID_ORDER_OR_DUPLICATE')
        require(type(body) is str, 'BAD_BODY')
        raw = body.encode('utf-8')
        pins.append({'id': ident, 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()})
        last = ident
    return {'schema_version':'alpha_issue93_real_body_inventory_v1',
            'source':SOURCE, 'pinned_main_before':obj['main_sha'],
            'declared_count':n, 'last_comment_id':last, 'pins':pins,
            'source_transport_authenticated':False,
            'github_actor_authenticated':False,
            'project_handoff_denominator':'NOT_COMPUTABLE'}

def main():
    try:
        obj = json.load(sys.stdin, object_pairs_hook=unique_pairs,
                        parse_constant=lambda x: (_ for _ in ()).throw(Reject('NONFINITE_JSON')))
        print(json.dumps(produce(obj), ensure_ascii=False, sort_keys=True, separators=(',',':')))
        return 0
    except (Reject, ValueError, TypeError, UnicodeError, OverflowError) as exc:
        print(json.dumps({'status':'FAIL_CLOSED','error':str(exc)}, sort_keys=True))
        return 2

if __name__ == '__main__':
    sys.exit(main())
