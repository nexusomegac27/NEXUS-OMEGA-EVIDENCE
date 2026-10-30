#!/usr/bin/env python3
"""Isolated C1 research guard for repository-scoped GitHub source links.

Syntax and scope validation only: no HTTP retrieval, authentication, or byte readback.
"""
import json
import re
import sys
from urllib.parse import urlsplit

SHA40 = re.compile(r'[0-9a-f]{40}\Z')
POSINT = re.compile(r'[1-9][0-9]*\Z')
SAFE_PATH = re.compile(r'[A-Za-z0-9._/-]+\Z')
REPO = ('nexusomegac27', 'NEXUS-OMEGA-EVIDENCE')

def no_duplicates(pairs):
    obj={}
    for k,v in pairs:
        if k in obj: raise ValueError('duplicate JSON key')
        obj[k]=v
    return obj

def reject_constant(_):
    raise ValueError('nonfinite JSON')

def validate(o):
    if type(o) is not dict or set(o) != {'source_ref','source_commit'}:
        raise ValueError('unexpected input fields')
    url,commit=o['source_ref'],o['source_commit']
    if type(url) is not str or type(commit) is not str or not SHA40.fullmatch(commit):
        raise ValueError('invalid input types or commit')
    if len(url)>1024 or any(ord(c)<33 or ord(c)>126 for c in url) or '\\' in url or '%' in url:
        raise ValueError('noncanonical URL bytes')
    u=urlsplit(url)
    if u.scheme!='https' or u.netloc!='github.com' or u.username or u.password or u.port is not None or u.query:
        raise ValueError('noncanonical GitHub origin')
    parts=u.path.split('/')
    if len(parts)<5 or parts[0]!='' or tuple(parts[1:3])!=REPO or any(p in ('','.','..') for p in parts[3:]):
        raise ValueError('wrong repository or invalid path')
    kind=parts[3]
    if kind in ('issues','pull'):
        if len(parts)!=5 or not POSINT.fullmatch(parts[4]):
            raise ValueError('invalid issue or PR locator')
        if u.fragment and not re.fullmatch(r'issuecomment-[1-9][0-9]*',u.fragment):
            raise ValueError('unrecognized fragment')
    elif kind=='commit':
        if len(parts)!=5 or not SHA40.fullmatch(parts[4]) or u.fragment:
            raise ValueError('invalid commit locator')
    elif kind=='blob':
        if len(parts)<6 or parts[4]!=commit or u.fragment or not SAFE_PATH.fullmatch('/'.join(parts[5:])):
            raise ValueError('blob ref must equal pinned commit')
    else:
        raise ValueError('unsupported source locator')
    return {'status':'CANONICAL_REPO_SOURCE_URL_SCOPE_PASS','source_ref':url,'source_commit':commit,
            'provenance':'URL_SYNTAX_ONLY_NOT_AUTHENTICATED','claim_ceiling':'C1_DESCRIPTIVE_ONLY'}

def main():
    try:
        data=sys.stdin.buffer.read(8193)
        if len(data)>8192: raise ValueError('oversize input')
        o=json.loads(data.decode('utf-8','strict'),object_pairs_hook=no_duplicates,parse_constant=reject_constant)
        print(json.dumps(validate(o),sort_keys=True))
        return 0
    except (ValueError,TypeError,UnicodeError) as exc:
        print(json.dumps({'status':'FAIL_CLOSED','reason':str(exc)},sort_keys=True))
        return 2

if __name__=='__main__':
    sys.exit(main())
