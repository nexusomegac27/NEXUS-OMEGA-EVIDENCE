#!/usr/bin/env python3
"""Frozen adversarial oracle for byte-capture consistency. No network, no candidate imports."""
import base64, copy, hashlib, json, pathlib, subprocess, sys, tempfile
HEAD = 'a4e17477de073e2c07f3f1c97453bb83c756b3ad'
ROOT = 'research/r16/axiom-alpha-node-c1-adaptation-20261012/'
PATHS = [ROOT+'eval.py',ROOT+'fixtures.json',ROOT+'result.json']
PAYLOADS = [b'fixed-evaluator-v1\n', b'{"fixtures":["positive","negative"]}\n', b'{"passed":2,"total":2}\n']

def blob(raw):
    return hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()

def fixture():
    files={}
    for path,raw in zip(PATHS,PAYLOADS):
        files[path]={'sha256':hashlib.sha256(raw).hexdigest(),'git_blob':blob(raw),
                     'bytes':len(raw),'readback':'MATCH','raw_base64':base64.b64encode(raw).decode('ascii')}
    claim={'evaluator_path':PATHS[0],'fixture_path':PATHS[1],'result_path':PATHS[2],
           'evaluator_sha256':files[PATHS[0]]['sha256'],
           'fixture_sha256':files[PATHS[1]]['sha256'],
           'result_sha256':files[PATHS[2]]['sha256']}
    return {'head_sha':HEAD,'files':files,'claim':claim,
            'ci':[{'name':'alpha-evidence-replay','head_sha':HEAD,'conclusion':'success'}],
            'result':{'head_sha':HEAD,'evaluator_sha256':claim['evaluator_sha256'],
                      'fixture_sha256':claim['fixture_sha256'],'passed':2,'total':2}}

def cases():
    x=fixture();out=[('complete_positive',x,'BYTE_CAPTURE_CONSISTENT')]
    def add(name,fn):
        y=copy.deepcopy(x);fn(y);out.append((name,y,'GAP'))
    add('raw_bytes_tampered_without_hash_update',lambda y:y['files'][PATHS[0]].update(raw_base64=base64.b64encode(b'malicious\n').decode()))
    add('raw_bytes_missing',lambda y:y['files'][PATHS[1]].pop('raw_base64'))
    add('raw_base64_invalid',lambda y:y['files'][PATHS[2]].update(raw_base64='!!!'))
    add('raw_bytes_empty',lambda y:y['files'][PATHS[2]].update(raw_base64=''))
    add('raw_base64_noncanonical',lambda y:y['files'][PATHS[0]].update(raw_base64=y['files'][PATHS[0]]['raw_base64']+'\n'))
    add('raw_bytes_valid_but_size_mismatch',lambda y:y['files'][PATHS[1]].update(bytes=999))
    add('raw_bytes_valid_but_sha_mismatch',lambda y:(y['files'][PATHS[1]].update(sha256='f'*64),y['claim'].update(fixture_sha256='f'*64)))
    add('raw_bytes_valid_but_blob_mismatch',lambda y:y['files'][PATHS[2]].update(git_blob='e'*40))
    add('raw_bytes_over_limit',lambda y:y['files'][PATHS[2]].update(raw_base64='A'*1500000))
    add('legacy_guard_missing',lambda y:y.update(_test_missing_guard=True))
    add('wrong_ci_head',lambda y:y['ci'][0].update(head_sha='0'*40))
    add('wrong_result_head',lambda y:y['result'].update(head_sha='0'*40))
    add('duplicate_paths',lambda y:y['claim'].update(fixture_path=PATHS[0],fixture_sha256=y['claim']['evaluator_sha256']))
    add('unsafe_path',lambda y:y['claim'].update(evaluator_path='../evil.py'))
    add('zero_denominator',lambda y:y['result'].update(passed=0,total=0))
    return out

def run(candidate,legacy):
    outcomes=[]
    for name,data,expected in cases():
        with tempfile.TemporaryDirectory() as td:
            f=pathlib.Path(td)/'capture.json';f.write_text(json.dumps(data),encoding='utf-8')
            use_legacy=str(pathlib.Path(td)/'absent.py') if data.get('_test_missing_guard') else legacy
            p=subprocess.run([sys.executable,candidate,str(f),use_legacy],capture_output=True,text=True,timeout=12)
            try: got=json.loads(p.stdout).get('coverage')
            except (json.JSONDecodeError,AttributeError):got='OUTPUT_ERROR'
            ok=(p.returncode==0 and got==expected) if expected=='BYTE_CAPTURE_CONSISTENT' else (got=='GAP' and p.returncode!=0)
            outcomes.append({'case':name,'expected':expected,'observed':got,'exit':p.returncode,'pass':ok})
    return {'oracle':'frozen_byte_capture_v1','passed':sum(x['pass'] for x in outcomes),'total':len(outcomes),'cases':outcomes}

if __name__=='__main__':
    z=run(sys.argv[1],sys.argv[2]);print(json.dumps(z,indent=2));sys.exit(0 if z['passed']==z['total'] else 1)
