#!/usr/bin/env python3
"""Independent subprocess oracle; candidate never imported or patched."""
import copy
import hashlib
import json
import subprocess
import sys

SOURCE='nexusomegac27/NEXUS-OMEGA-EVIDENCE/issues/93'
SHA='06eee8d929c3bf6877cd01767aeea82e3f9e01bf'

def base():
    return {'source':SOURCE,'main_sha':SHA,'declared_count':2,
            'comments':[{'id':10,'body':'hello'},{'id':11,'body':'Grüße Ω'}]}

def run(path,obj):
    raw=obj if isinstance(obj,str) else json.dumps(obj,ensure_ascii=False)
    p=subprocess.run([sys.executable,path],input=raw,text=True,capture_output=True,timeout=10)
    try: out=json.loads(p.stdout)
    except ValueError: raise AssertionError('INVALID_OUTPUT '+p.stdout[:200])
    return p.returncode,out

def main(path):
    good=base()
    cases=[('positive',good,None)]
    mutations=[
        ('missing',lambda x:x['comments'].pop(),'POPULATION_INCOMPLETE'),
        ('extra',lambda x:x['comments'].append({'id':12,'body':'extra'}),'POPULATION_INCOMPLETE'),
        ('duplicate_id',lambda x:x['comments'][1].update(id=10),'ID_ORDER_OR_DUPLICATE'),
        ('reverse_order',lambda x:x['comments'].reverse(),'ID_ORDER_OR_DUPLICATE'),
        ('wrong_source',lambda x:x.update(source='other/repo/issues/93'),'SOURCE_MISMATCH'),
        ('bad_sha',lambda x:x.update(main_sha='0'*39),'BAD_MAIN_SHA'),
        ('bool_id',lambda x:x['comments'][0].update(id=True),'ID_ORDER_OR_DUPLICATE'),
        ('bool_count',lambda x:x.update(declared_count=True),'BAD_COUNT'),
        ('bad_body',lambda x:x['comments'][0].update(body=5),'BAD_BODY'),
        ('extra_field',lambda x:x['comments'][0].update(actor='owner'),'BAD_ROW'),
    ]
    for name,mutation,error in mutations:
        x=copy.deepcopy(good);mutation(x);cases.append((name,x,error))
    cases.extend([
        ('duplicate_json_key','{"source":"'+SOURCE+'","source":"other"}', 'DUPLICATE_JSON_KEY'),
        ('nonfinite', '{"source":NaN}', 'NONFINITE_JSON'),
        ('malformed','{invalid}',None),
    ])
    passed=0
    for name,obj,error in cases:
        rc,out=run(path,obj)
        if error is None and name=='positive':
            pins=out.get('pins',[])
            ok=(rc==0 and len(pins)==2 and pins[0]['sha256']==hashlib.sha256(b'hello').hexdigest()
                and pins[1]['bytes']==len('Grüße Ω'.encode('utf-8')) and not out['source_transport_authenticated'])
        else:
            ok=rc!=0 and out.get('status')=='FAIL_CLOSED' and (error is None or out.get('error')==error)
        print(name,'PASS' if ok else 'FAIL',out.get('error',''))
        passed+=bool(ok)
    print('RESULT=%d/%d'%(passed,len(cases)))
    return 0 if passed==len(cases) else 1

if __name__=='__main__':
    if len(sys.argv)!=2: raise SystemExit('usage: oracle.py candidate.py')
    raise SystemExit(main(sys.argv[1]))
