#!/usr/bin/env python3
"""Frozen independent black-box oracle: Git CLI supplies tree OIDs, not candidate code.
C1 isolated research only. This evaluator must be committed BEFORE the candidate.
"""
import copy
import json
import subprocess
import sys
import tempfile
from pathlib import Path

TARGET = 'research/r16/axiom-alpha-node-c1-adaptation-20261012/alpha_handoff_commit_ref_binding_v3_20261030.py'
LEAF = '73ef222f9117f566930390e60899d571ecc77402'

def git_tree_oid(entries):
    raw = bytearray()
    # Independent test builder uses git canonical directory-aware byte sorting.
    for e in sorted(entries, key=lambda v: (v['path'] + ('/' if v['mode']=='040000' else '')).encode()):
        raw += (('40000' if e['mode']=='040000' else e['mode'])+' '+e['path']).encode()+b'\0'+bytes.fromhex(e['sha'])
    p=subprocess.run(['git','hash-object','-t','tree','--stdin'],input=bytes(raw),capture_output=True,check=True)
    return p.stdout.decode().strip()

def build():
    parts=TARGET.split('/')
    trees=[None]*len(parts)
    next_sha=LEAF
    for i in range(len(parts)-1,-1,-1):
        mode='100644' if i==len(parts)-1 else '040000'
        typ='blob' if i==len(parts)-1 else 'tree'
        entries=[{'path':'README.md','mode':'100644','type':'blob','sha':'f'*40},
                 {'path':parts[i],'mode':mode,'type':typ,'sha':next_sha}]
        if parts[i]=='README.md':raise AssertionError('bad fixture')
        sha=git_tree_oid(entries)
        trees[i]={'sha':sha,'truncated':False,'entries':entries}
        next_sha=sha
    return {'schema':'NEXUS_ALPHA_GIT_TREE_CLOSURE_V1','trees':trees},next_sha

def run(candidate, projection, root, path=TARGET, blob=LEAF, as_raw=None):
    payload=as_raw if as_raw is not None else json.dumps(projection,ensure_ascii=True,separators=(',',':'))
    p=subprocess.run([sys.executable,'-S',str(candidate),root,path,blob],input=payload,text=True,capture_output=True,timeout=8)
    try:out=json.loads(p.stdout)
    except Exception as e:raise AssertionError((p.returncode,p.stdout,p.stderr)) from e
    return p.returncode,out

def main(candidate):
    good,root=build();checks=0;neg=0
    code,out=run(candidate,good,root)
    assert code==0 and out['state']=='GIT_TREE_OID_CHAIN_RECONSTRUCTED_C1'
    assert out['verified_tree_count']==4 and out['leaf_blob_sha1']==LEAF
    checks+=1
    bad=[]
    def modify(fn):
        x=copy.deepcopy(good);fn(x);bad.append(x)
    modify(lambda x:x['trees'][0]['entries'][1].update(sha='0'*40))
    modify(lambda x:x['trees'][1]['entries'][1].update(sha='0'*40))
    modify(lambda x:x['trees'][2]['entries'][1].update(sha='0'*40))
    modify(lambda x:x['trees'][3]['entries'][1].update(sha='0'*40))
    modify(lambda x:x['trees'][3]['entries'][1].update(mode='120000',type='blob'))
    modify(lambda x:x['trees'][3].update(truncated=True))
    modify(lambda x:x['trees'][3].update(truncated=1))
    modify(lambda x:x['trees'][2]['entries'].append(copy.deepcopy(x['trees'][2]['entries'][1])))
    modify(lambda x:x['trees'][1]['entries'][1].update(path='../r16'))
    modify(lambda x:x['trees'][1]['entries'][1].update(type='blob'))
    modify(lambda x:x['trees'][0]['entries'][1].update(mode='100644',type='blob'))
    modify(lambda x:x['trees'][2].update(sha='0'*40))
    modify(lambda x:x['trees'].pop())
    modify(lambda x:x['trees'].append(copy.deepcopy(x['trees'][-1])))
    modify(lambda x:x.update(schema='C2'))
    modify(lambda x:x['trees'][3]['entries'][1].update(sha='g'*40))
    modify(lambda x:x['trees'][3]['entries'][1].update(path='missing.py'))
    modify(lambda x:x['trees'][0]['entries'][1].update(path='research/other'))
    modify(lambda x:x['trees'][3]['entries'][1].update(path='\ud800'))
    for x in bad:
        code,out=run(candidate,x,root)
        assert code!=0 and out['state']=='FAIL_CLOSED',(x,code,out)
        checks+=1;neg+=1
    for kwargs in ({'root':'0'*40},{'path':'research/r16/other/file.py'},{'blob':'0'*40}):
        code,out=run(candidate,good,kwargs.get('root',root),kwargs.get('path',TARGET),kwargs.get('blob',LEAF))
        assert code!=0 and out['state']=='FAIL_CLOSED'
        checks+=1;neg+=1
    for wire in ['{"schema":"x","schema":"y"}', '{"schema":"x","truncated":NaN}', '{broken', '[]']:
        code,out=run(candidate,good,root,as_raw=wire)
        assert code!=0 and out['state']=='FAIL_CLOSED'
        checks+=1;neg+=1
    with tempfile.TemporaryDirectory() as td:
        # No repo access: oracle itself has no dependency on NEXUS source checkout.
        assert Path(td).exists()
    print(f'FROZEN_ORACLE={checks}/{checks}_PASS NEGATIVES={neg}/{neg}_FAIL_CLOSED GIT_CLI_REFERENCE=4/4_MATCH')

if __name__=='__main__':
    if len(sys.argv)!=2:raise SystemExit('usage: frozen_oracle.py candidate.py')
    main(Path(sys.argv[1]).resolve())
