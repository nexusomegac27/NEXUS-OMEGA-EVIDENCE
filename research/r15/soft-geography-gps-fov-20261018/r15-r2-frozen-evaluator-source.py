"""R15-R2 independent, frozen-before-candidate synthetic byte ledger oracle.
Does not authenticate telemetry, certify network traffic or claim real device savings.
"""
import copy
import json
import subprocess
import sys
import tempfile
from pathlib import Path

HASH_A = 'a'*64
HASH_B = 'b'*64

def run(name, n, size):
    return {
        'capture_id': name,
        'dataset_sha256': HASH_A,
        'view_snapshot_sha256': HASH_B,
        'lod_profile': 'SYNTHETIC_IDENTICAL_LOD',
        'cache_state': 'COLD_CLEAN',
        'coverage_oracle': 'SYNTHETIC_FIXED_VIEW_V1',
        'coverage_passed': True,
        'capture_complete': True,
        'requests': [{'id':f'{name}-{i}', 'resource': f'local://tile/{i:03d}',
                      'response_body_bytes': size} for i in range(n)]
    }

def sample():
    return {
        'profile': 'R15_R2_SYNTHETIC_NO_REAL_GPS',
        'claim_ceiling': 'C1_DESCRIPTIVE_ONLY',
        'personal_location_included': False,
        'baseline': run('circle', 88, 100),
        'candidate': run('fov',28,100)
    }

def execute(script,p):
    with tempfile.TemporaryDirectory() as t:
        f=Path(t)/'input.json';f.write_text(json.dumps(p,sort_keys=True),encoding='utf-8')
        r=subprocess.run([sys.executable,str(script),str(f)],capture_output=True,text=True,timeout=8)
        try: obj=json.loads(r.stdout)
        except Exception: return None,r.returncode,'not_json '+r.stdout[:100]+' '+r.stderr[:100]
        return obj,r.returncode,r.stderr[:100]

def test(script,name,modify,expected,bytes_b=None,bytes_c=None):
    p=sample()
    modify(p)
    result,rc,_=execute(script,p)
    ok = result is not None and result.get('state')==expected and result.get('claim_ceiling')=='C1_DESCRIPTIVE_ONLY' and result.get('real_network_bytes_verified') is False
    if expected=='SYNTHETIC_ACCOUNTED_C1':
        ok &= rc==0 and result.get('baseline_response_body_bytes')==bytes_b and result.get('candidate_response_body_bytes')==bytes_c
    else:
        ok &= rc==2 and result.get('baseline_response_body_bytes') is None and result.get('candidate_response_body_bytes') is None
    return name,bool(ok),result

def main():
    script=Path(sys.argv[1]).resolve()
    tests = [
     ('valid_synthetic', lambda p: None, 'SYNTHETIC_ACCOUNTED_C1',8800,2800),
     ('candidate_more_bytes',lambda p: [r.update(response_body_bytes=400) for r in p['candidate']['requests']], 'SYNTHETIC_ACCOUNTED_C1',8800,11200),
     ('zero_bytes',lambda p:[r.update(response_body_bytes=0) for r in p['candidate']['requests']], 'SYNTHETIC_ACCOUNTED_C1',8800,0),
     ('privacy_gps',lambda p:p.update(personal_location_included=True),'HOLD_SCOPED',None,None),
     ('higher_claim',lambda p:p.update(claim_ceiling='C2_AUTHORITATIVE'),'HOLD_SCOPED',None,None),
     ('wrong_profile',lambda p:p.update(profile='REAL_WORLD_GPS'),'HOLD_SCOPED',None,None),
     ('wrong_dataset',lambda p:p['candidate'].update(dataset_sha256='c'*64),'HOLD_SCOPED',None,None),
     ('wrong_view',lambda p:p['candidate'].update(view_snapshot_sha256='d'*64),'HOLD_SCOPED',None,None),
     ('different_lod',lambda p:p['candidate'].update(lod_profile='BETTER'),'HOLD_SCOPED',None,None),
     ('warm_candidate',lambda p:p['candidate'].update(cache_state='WARM'),'HOLD_SCOPED',None,None),
     ('missing_baseline_trace',lambda p:p['baseline'].update(capture_complete=False),'HOLD_SCOPED',None,None),
     ('missing_candidate_trace',lambda p:p['candidate'].update(capture_complete=False),'HOLD_SCOPED',None,None),
     ('weak_coverage',lambda p:p['candidate'].update(coverage_passed=False),'HOLD_SCOPED',None,None),
     ('different_oracle',lambda p:p['candidate'].update(coverage_oracle='UNTRUSTED'),'HOLD_SCOPED',None,None),
     ('remote_resource',lambda p:p['candidate']['requests'][0].update(resource='https://private.example/position'),'HOLD_SCOPED',None,None),
     ('duplicate_id',lambda p:p['candidate']['requests'][1].update(id=p['candidate']['requests'][0]['id']),'HOLD_SCOPED',None,None),
     ('negative_bytes',lambda p:p['candidate']['requests'][0].update(response_body_bytes=-1),'HOLD_SCOPED',None,None),
     ('float_bytes',lambda p:p['candidate']['requests'][0].update(response_body_bytes=2.5),'HOLD_SCOPED',None,None),
     ('boolean_bytes',lambda p:p['candidate']['requests'][0].update(response_body_bytes=True),'HOLD_SCOPED',None,None),
     ('extra_undeclared_http',lambda p:p['candidate']['requests'].append({'id':'x','resource':'local://tile/099','response_body_bytes':4,'url':'https://a.example'}),'HOLD_SCOPED',None,None),
     ('empty_baseline',lambda p:p['baseline'].update(requests=[]),'HOLD_SCOPED',None,None),
     ('not_exact_sha',lambda p:p['baseline'].update(dataset_sha256='a'*63),'HOLD_SCOPED',None,None),
    ]
    fails=[]
    for name,change,expected,b,c in tests:
        n,ok,got=test(script,name,change,expected,b,c)
        print(('PASS' if ok else 'FAIL')+' '+n + ('' if ok else ' got='+str(got)[:400]))
        if not ok:fails.append(n)
    print('FINAL',len(tests)-len(fails),'/',len(tests))
    return 0 if not fails else 1

if __name__=='__main__': sys.exit(main())
