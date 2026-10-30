#!/usr/bin/env python3
"""Isolated C1 preflight: compare observed Issue #93 body bytes to separately pinned digests.

This is NOT a GitHub identity, transport authenticity, immutability or completeness proof.
Pins must originate from an independently retained trusted snapshot.
"""
import hashlib
import json
import re
import sys

SOURCE = 'nexusomegac27/NEXUS-OMEGA-EVIDENCE/issues/93'
HEX64 = re.compile(r'[0-9a-f]{64}\Z')

class Reject(ValueError):
    pass

def pairs_unique(pairs):
    out = {}
    for k, v in pairs:
        if k in out:
            raise Reject('DUPLICATE_JSON_KEY')
        out[k] = v
    return out

def require(cond, error):
    if not cond:
        raise Reject(error)

def check(payload):
    require(type(payload) is dict, 'BAD_ROOT')
    require(payload.get('schema_version') == 'alpha_issue93_body_pin_v1', 'BAD_SCHEMA')
    require(payload.get('source') == SOURCE, 'SOURCE_MISMATCH')
    n = payload.get('declared_count')
    require(type(n) is int and 1 <= n <= 100000, 'BAD_COUNT')
    pins, observed = payload.get('pinned'), payload.get('observed')
    require(type(pins) is list and type(observed) is list, 'BAD_POPULATION')
    require(len(pins) == n and len(observed) == n, 'POPULATION_INCOMPLETE')
    last = 0
    for pin, row in zip(pins, observed):
        require(type(pin) is dict and type(row) is dict, 'BAD_ROW')
        pid, oid = pin.get('id'), row.get('id')
        require(type(pid) is int and pid > last and type(oid) is int and oid == pid, 'ID_ORDER_OR_BINDING_MISMATCH')
        body = row.get('body')
        require(type(body) is str, 'BAD_BODY')
        b = body.encode('utf-8')
        size = pin.get('bytes')
        require(type(size) is int and size == len(b), 'BODY_BYTE_COUNT_MISMATCH')
        digest = pin.get('sha256')
        require(type(digest) is str and HEX64.fullmatch(digest) is not None, 'BAD_DIGEST')
        require(hashlib.sha256(b).hexdigest() == digest, 'BODY_SHA256_MISMATCH')
        last = pid
    return {'status':'PASS_BODY_PIN_MATCH', 'checked':n,
            'github_actor_authenticated':False, 'pin_origin_authenticated':False,
            'project_handoff_denominator':'NOT_COMPUTABLE'}

def main():
    try:
        obj = json.load(sys.stdin, object_pairs_hook=pairs_unique)
        print(json.dumps(check(obj),sort_keys=True))
        return 0
    except (Reject, ValueError, TypeError, UnicodeError) as exc:
        print(json.dumps({'status':'FAIL_CLOSED','error':str(exc)},sort_keys=True))
        return 2

if __name__ == '__main__':
    sys.exit(main())
