#!/usr/bin/env python3
"""Offline C1 tree-chain OID reconstruction from caller-supplied GitHub API projections.
The root SHA and leaf SHA must be pinned outside this input. No transport authentication.
"""
import hashlib
import json
import re
import sys

HEX40=re.compile(r'[0-9a-f]{40}\Z')
MODES={'040000':'tree','100644':'blob','100755':'blob','120000':'blob','160000':'commit'}

def pairs_unique(pairs):
    d={}
    for k,v in pairs:
        if k in d:raise ValueError('DUPLICATE_JSON_KEY')
        d[k]=v
    return d

def no_constant(_):raise ValueError('NONFINITE_JSON')

def sha40(s):
    if type(s) is not str or not HEX40.fullmatch(s):raise ValueError('INVALID_SHA1')
    return s

def component(s):
    if type(s) is not str or not s or s in ('.','..') or '/' in s or '\0' in s:
        raise ValueError('INVALID_PATH_COMPONENT')
    raw=s.encode('utf-8','strict')
    if len(raw)>255:raise ValueError('OVERSIZE_PATH_COMPONENT')
    return raw

def tree_oid(obj):
    if type(obj) is not dict or set(obj)!={'sha','truncated','entries'} or obj['truncated'] is not False:
        raise ValueError('INCOMPLETE_TREE')
    claimed=sha40(obj['sha'])
    entries=obj['entries']
    if type(entries) is not list or not 1<=len(entries)<=5000:raise ValueError('INVALID_TREE_ENTRIES')
    collected=[];seen=set()
    for e in entries:
        if type(e) is not dict or set(e)!={'path','mode','type','sha'}:
            raise ValueError('INVALID_TREE_ENTRY_FIELDS')
        name=component(e['path'])
        if name in seen:raise ValueError('DUPLICATE_TREE_ENTRY')
        seen.add(name)
        mode=e['mode']
        if type(mode) is not str or MODES.get(mode)!=e['type']:
            raise ValueError('INVALID_MODE_TYPE')
        target=bytes.fromhex(sha40(e['sha']))
        sort_key=name+(b'/' if mode=='040000' else b'')
        raw=(('40000' if mode=='040000' else mode).encode('ascii')+b' '+name+b'\0'+target)
        collected.append((sort_key,raw,e))
    collected.sort(key=lambda x:x[0])
    body=b''.join(item[1] for item in collected)
    digest=hashlib.sha1(b'tree '+str(len(body)).encode('ascii')+b'\0'+body).hexdigest()
    if digest!=claimed:raise ValueError('GIT_TREE_OID_MISMATCH')
    return {item[2]['path']:item[2] for item in collected},len(body),digest

def verify(raw,root,path,leaf):
    root=sha40(root);leaf=sha40(leaf)
    if type(path) is not str or len(path)>512 or not path.startswith('research/r16/axiom-alpha-node-c1-adaptation-20261012/'):
        raise ValueError('SOURCE_PATH_SCOPE')
    parts=path.split('/')
    if not 2<=len(parts)<=16:raise ValueError('SOURCE_PATH_DEPTH')
    for p in parts:component(p)
    if len(raw)>1048576:raise ValueError('OVERSIZE_PROJECTION')
    obj=json.loads(raw.decode('utf-8','strict'),object_pairs_hook=pairs_unique,parse_constant=no_constant)
    if type(obj) is not dict or set(obj)!={'schema','trees'} or obj['schema']!='NEXUS_ALPHA_GIT_TREE_CLOSURE_V1':
        raise ValueError('INVALID_PROJECTION_SCHEMA')
    trees=obj['trees']
    if type(trees) is not list or len(trees)!=len(parts):raise ValueError('TREE_CHAIN_LENGTH')
    expected=root; witness=[]
    for i,(part,tree) in enumerate(zip(parts,trees)):
        entries,raw_bytes,calculated=tree_oid(tree)
        if calculated!=expected:raise ValueError('BROKEN_TREE_PARENT_LINK')
        if part not in entries:raise ValueError('SOURCE_PATH_NOT_IN_TREE')
        e=entries[part]
        if i<len(parts)-1 and (e['mode']!='040000' or e['type']!='tree'):
            raise ValueError('INTERMEDIATE_NOT_TREE')
        if i==len(parts)-1 and (e['mode']!='100644' or e['type']!='blob' or e['sha']!=leaf):
            raise ValueError('LEAF_BLOB_PIN_MISMATCH')
        witness.append({'tree_sha1':calculated,'entry_count':len(tree['entries']),'raw_tree_bytes':raw_bytes})
        expected=e['sha']
    return {'state':'GIT_TREE_OID_CHAIN_RECONSTRUCTED_C1','verified_tree_count':len(witness),
            'root_tree_sha1':root,'leaf_blob_sha1':leaf,'trees':witness,
            'transport_authentication':'NOT_VERIFIED','root_pin_authority':'CALLER_MUST_VERIFY_INDEPENDENTLY',
            'claim_ceiling':'C1_DESCRIPTIVE_ONLY'}

def main():
    try:
        if len(sys.argv)!=4:raise ValueError('USAGE_ROOT_PATH_BLOB')
        raw=sys.stdin.buffer.read(1048577)
        result=verify(raw,*sys.argv[1:])
        print(json.dumps(result,sort_keys=True,separators=(',',':')))
        return 0
    except RecursionError:
        print(json.dumps({'state':'FAIL_CLOSED','reason':'JSON_NESTING_LIMIT'},sort_keys=True))
        return 2
    except (ValueError,TypeError,KeyError,UnicodeError,OverflowError) as e:
        print(json.dumps({'state':'FAIL_CLOSED','reason':str(e)},sort_keys=True))
        return 2

if __name__=='__main__':sys.exit(main())
