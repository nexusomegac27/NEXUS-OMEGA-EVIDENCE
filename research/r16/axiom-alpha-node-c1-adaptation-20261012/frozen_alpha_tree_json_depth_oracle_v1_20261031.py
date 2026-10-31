#!/usr/bin/env python3
"""Independent C1 black-box oracle for bounded Git-tree JSON failure envelopes.
Uses Git CLI for positive tree IDs. Does not import candidate or its parsing code.
Freeze before candidate. No external transport or production runtime.
"""
import copy
import json
import subprocess
import sys
from pathlib import Path

PATH='research/r16/axiom-alpha-node-c1-adaptation-20261012/alpha_handoff_commit_ref_binding_v3_20261030.py'
LEAF='73ef222f9117f566930390e60899d571ecc77402'

def oid(entries):
    buf=b''
    for e in sorted(entries,key=lambda v:(v['path']+('/' if v['mode']=='040000' else '')).encode('utf-8')):
        mode='40000' if e['mode']=='040000' else e['mode']
        buf+=(mode+' '+e['path']).encode('utf-8')+b'\0'+bytes.fromhex(e['sha'])
    p=subprocess.run(['git','hash-object','-t','tree','--stdin'],input=buf,capture_output=True,check=True)
    return p.stdout.decode('ascii').strip()

def fixture():
    parts=PATH.split('/')
    trees=[None]*len(parts)
    next_oid=LEAF
    for i in range(len(parts)-1,-1,-1):
        last=i==len(parts)-1
        mode='100644' if last else '040000'
        entries=[{'path':'README.md','mode':'100644','type':'blob','sha':'a'*40},
                 {'path':parts[i],'mode':mode,'type':'blob' if last else 'tree','sha':next_oid}]
        next_oid=oid(entries)
        trees[i]={'sha':next_oid,'truncated':False,'entries':entries}
    return json.dumps({'schema':'NEXUS_ALPHA_GIT_TREE_CLOSURE_V1','trees':trees},separators=(',',':')).encode('utf-8'),next_oid

def invoke(candidate,raw,root):
    p=subprocess.run([sys.executable,'-S',str(candidate),root,PATH,LEAF],input=raw,capture_output=True,timeout=10)
    try:out=json.loads(p.stdout.decode('utf-8'))
    except (ValueError,UnicodeError):out=None
    return p.returncode,out,p.stderr

def main(candidate):
    valid,root=fixture()
    positives=0;negatives=0
    code,out,err=invoke(candidate,valid,root)
    assert code==0 and out and out['state']=='GIT_TREE_OID_CHAIN_RECONSTRUCTED_C1'
    assert out['verified_tree_count']==4 and not err
    positives+=1
    # Depth > CPython's parser recursion limit; under the one-MiB input cap.
    for n in (10000,20000,40000):
        code,out,err=invoke(candidate,b'['*n+b'0'+b']'*n,root)
        assert code==2 and out and out['state']=='FAIL_CLOSED' and out['reason']=='JSON_NESTING_LIMIT' and not err,(n,code,out,err[-180:])
        negatives+=1
    for raw in (b'{"schema":"a","schema":"b"}',b'{"schema":NaN}',b'{broken',b'[]',b'\xff',b'['*600000+b']'*600000):
        code,out,err=invoke(candidate,raw,root)
        assert code==2 and out and out['state']=='FAIL_CLOSED' and not err,(len(raw),code,out,err[-180:])
        negatives+=1
    code,out,err=invoke(candidate,valid,'0'*40)
    assert code==2 and out and out['state']=='FAIL_CLOSED' and not err
    negatives+=1
    print(f'FROZEN_JSON_DEPTH_ORACLE={positives+negatives}/{positives+negatives}_PASS POSITIVE={positives}/{positives} NEGATIVE={negatives}/{negatives}_FAIL_CLOSED')

if __name__=='__main__':
    if len(sys.argv)!=2:raise SystemExit('usage: frozen_oracle.py candidate.py')
    main(Path(sys.argv[1]).resolve())
