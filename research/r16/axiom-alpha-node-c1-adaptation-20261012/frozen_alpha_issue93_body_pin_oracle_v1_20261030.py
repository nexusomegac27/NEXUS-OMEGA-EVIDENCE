#!/usr/bin/env python3
"""Frozen independent subprocess oracle. No import of the candidate or mutation of its code."""
import copy
import hashlib
import json
import subprocess
import sys

SOURCE='nexusomegac27/NEXUS-OMEGA-EVIDENCE/issues/93'
def digest(s): return hashlib.sha256(s.encode('utf-8')).hexdigest()
def base():
    bodies=['hello', 'Grüße Ω']
    return {'schema_version':'alpha_issue93_body_pin_v1','source':SOURCE,'declared_count':2,
            'pinned':[{'id':100+i,'bytes':len(b.encode('utf-8')),'sha256':digest(b)} for i,b in enumerate(bodies)],
            'observed':[{'id':100+i,'body':b} for i,b in enumerate(bodies)]}
def run(path, obj):
    raw=obj if isinstance(obj,str) else json.dumps(obj,ensure_ascii=False)
    p=subprocess.run([sys.executable,path],input=raw,text=True,capture_output=True,timeout=10)
    try: out=json.loads(p.stdout)
    except ValueError: raise AssertionError('invalid candidate JSON '+p.stdout[:200])
    return p.returncode,out

def main(path):
    good=base()
    cases=[('positive',good,True,None)]
    mutations=[
        ('same_length_tamper',lambda x:x['observed'][0].update(body='HELLO'),'BODY_SHA256_MISMATCH'),
        ('unicode_character_byte_mismatch',lambda x:x['pinned'][1].update(bytes=len('Grüße Ω')),'BODY_BYTE_COUNT_MISMATCH'),
        ('wrong_digest',lambda x:x['pinned'][0].update(sha256='0'*64),'BODY_SHA256_MISMATCH'),
        ('missing_row',lambda x:x['observed'].pop(),'POPULATION_INCOMPLETE'),
        ('duplicate_id',lambda x:x['pinned'][1].update(id=100),'ID_ORDER_OR_BINDING_MISMATCH'),
        ('cross_id_swap',lambda x:x['observed'][1].update(id=102),'ID_ORDER_OR_BINDING_MISMATCH'),
        ('wrong_source',lambda x:x.update(source='other/repo/issues/93'),'SOURCE_MISMATCH'),
        ('boolean_id',lambda x:x['pinned'][0].update(id=True),'ID_ORDER_OR_BINDING_MISMATCH'),
        ('boolean_bytes',lambda x:x['pinned'][0].update(bytes=True),'BODY_BYTE_COUNT_MISMATCH'),
        ('invalid_digest',lambda x:x['pinned'][0].update(sha256='bad'),'BAD_DIGEST'),
        ('bad_body_type',lambda x:x['observed'][0].update(body=12),'BAD_BODY'),
    ]
    for name,mutation,error in mutations:
        obj=copy.deepcopy(good);mutation(obj);cases.append((name,obj,False,error))
    cases.extend([
        ('duplicate_json_key','{"schema_version":"alpha_issue93_body_pin_v1","source":"'+SOURCE+'","source":"other"}',False,'DUPLICATE_JSON_KEY'),
        ('malformed_json','{not-json}',False,None)
    ])
    count=0
    for name,obj,positive,error in cases:
        rc,out=run(path,obj)
        ok=(rc==0 and out.get('status')=='PASS_BODY_PIN_MATCH') if positive else (rc!=0 and out.get('status')=='FAIL_CLOSED' and (error is None or out.get('error')==error))
        print(name, 'PASS' if ok else 'FAIL', out)
        count+=ok
    print(f'RESULT={count}/{len(cases)}')
    return 0 if count==len(cases) else 1

if __name__=='__main__':
    if len(sys.argv)!=2: raise SystemExit('usage: oracle.py candidate.py')
    raise SystemExit(main(sys.argv[1]))
