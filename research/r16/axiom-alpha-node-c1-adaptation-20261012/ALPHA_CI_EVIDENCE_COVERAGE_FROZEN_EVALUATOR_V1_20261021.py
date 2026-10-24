#!/usr/bin/env python3
"""Frozen, candidate-independent oracle: CI success is not evaluator replay evidence."""
import copy, json, pathlib, subprocess, sys, tempfile
H = '5fb35be25870e3a8785f0b41a82bcba652b43088'
A='a'*64; B='b'*64; C='c'*64
P='research/r16/axiom-alpha-node-c1-adaptation-20261012/'
E=P+'frozen_evaluator.py'; F=P+'fixture_cases.json'; R=P+'test_results.json'
def complete():
    return {'head_sha':H,'draft':True,'merged':False,'files':{
        E:{'sha256':A,'bytes':100,'git_blob':'1'*40,'readback':'MATCH'},
        F:{'sha256':B,'bytes':200,'git_blob':'2'*40,'readback':'MATCH'},
        R:{'sha256':C,'bytes':300,'git_blob':'3'*40,'readback':'MATCH'}},
        'ci':[{'name':'validate','head_sha':H,'conclusion':'success'},
              {'name':'alpha-evidence-replay','head_sha':H,'conclusion':'success'}],
        'claim':{'evaluator_path':E,'fixture_path':F,'result_path':R,
                 'evaluator_sha256':A,'fixture_sha256':B,'result_sha256':C},
        'result':{'head_sha':H,'evaluator_sha256':A,'fixture_sha256':B,'passed':18,'total':18}}

def fixtures():
    cases=[]
    def add(name,mutate,expect):
        x=complete();mutate(x);cases.append((name,x,expect))
    add('complete_positive',lambda x:None,'STRUCTURALLY_COVERED')
    add('real_pr124_only_markdown',lambda x:(x.update(files={'report1.md':{},'report2.md':{}},ci=[{'name':'validate','head_sha':H,'conclusion':'success'}]),x.pop('result')),'GAP')
    add('missing_evaluator',lambda x:x['files'].pop(E),'GAP')
    add('missing_fixture',lambda x:x['files'].pop(F),'GAP')
    add('missing_result',lambda x:x['files'].pop(R),'GAP')
    add('bad_evaluator_hash',lambda x:x['files'][E].update(sha256='d'*64),'GAP')
    add('bad_fixture_hash',lambda x:x['files'][F].update(sha256='d'*64),'GAP')
    add('bad_result_hash',lambda x:x['files'][R].update(sha256='d'*64),'GAP')
    add('missing_readback',lambda x:x['files'][E].update(readback='NOT_ESTABLISHED'),'GAP')
    add('zero_byte_file',lambda x:x['files'][F].update(bytes=0),'GAP')
    add('invalid_blob',lambda x:x['files'][F].update(git_blob='bad'),'GAP')
    add('missing_replay_ci',lambda x:x.update(ci=x['ci'][:1]),'GAP')
    add('stale_replay_ci',lambda x:x['ci'][1].update(head_sha='0'*40),'GAP')
    add('failed_replay_ci',lambda x:x['ci'][1].update(conclusion='failure'),'GAP')
    add('wrong_result_head',lambda x:x['result'].update(head_sha='0'*40),'GAP')
    add('wrong_result_evaluator',lambda x:x['result'].update(evaluator_sha256='d'*64),'GAP')
    add('failed_test',lambda x:x['result'].update(passed=17),'GAP')
    add('zero_test_denominator',lambda x:x['result'].update(passed=0,total=0),'GAP')
    add('duplicate_evidence_paths',lambda x:x['claim'].update(fixture_path=E,fixture_sha256=A),'GAP')
    add('invalid_head',lambda x:x.update(head_sha='invalid'),'GAP')
    return cases

def main(candidate):
    cases=fixtures();results=[]
    for name,data,expected in cases:
        with tempfile.TemporaryDirectory() as td:
            path=pathlib.Path(td)/'input.json';path.write_text(json.dumps(data),encoding='utf-8')
            cp=subprocess.run([sys.executable,candidate,str(path)],capture_output=True,text=True,timeout=10)
            try:out=json.loads(cp.stdout);observed=out.get('coverage')
            except Exception:observed='ERROR'
            ok=(cp.returncode==0 and observed==expected)
            results.append({'case':name,'expected':expected,'observed':observed,'pass':ok})
    n=sum(x['pass'] for x in results)
    print(json.dumps({'frozen_evaluator':'ci_coverage_v1','passed':n,'total':len(results),'cases':results},indent=2))
    return 0 if n==len(results) else 1
if __name__=='__main__':sys.exit(main(sys.argv[1]))
