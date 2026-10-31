#!/usr/bin/env python3
"""Frozen independent black-box oracle for C1 ruleset/check-run collision diagnosis."""
import copy
import json
import subprocess
import sys


def sample():
    return {'schema':'NEXUS_ALPHA_CI_RULESET_CHECK_SNAPSHOT_V1',
      'repository':'nexusomegac27/NEXUS-OMEGA-EVIDENCE',
      'pinned_main':'830dfd18dc30f3a8dc878418f09faf128b1ad7e3',
      'pr_head':'a6a04f775d620e1e94cb1fd0ebcd16dfa4518c4d',
      'ruleset':{'id':21252293,'enforcement':'active','ref_include':['refs/heads/main'],
                 'required_status_checks':[{'context':'validate','integration_id':15368}]},
      'check_runs':[{'id':i,'name':n,'app_id':a,'status':'completed','conclusion':'success'} for i,n,a in [
          (124431405622,'nexus-preentry-lab',15368),
          (124431376226,'r27e-external-structural-firewall',15368),
          (124431375890,'validate-repository-structure',15368),
          (124431375427,'validate',15368),
          (124431375425,'validate',15368),
          (124431375353,'validate',15368),
          (124431375274,'validate',15368),
          (124431374173,'semgrep-cloud-platform/scan',4695336)] ]}


def execute(candidate, payload):
    raw = payload if isinstance(payload,str) else json.dumps(payload,sort_keys=True,separators=(',',':'))
    p = subprocess.run([sys.executable,'-S',candidate],input=raw,text=True,capture_output=True,timeout=10)
    assert not p.stderr, p.stderr
    return p.returncode,json.loads(p.stdout)


def main(candidate):
    baseline=sample(); checks=0; negatives=0
    code,out=execute(candidate,baseline)
    assert code==0 and out['state']=='REQUIRED_CHECK_NAME_COLLISION_OBSERVED'
    assert out['collisions']=={'validate':4} and out['required_name_matches']=={'validate':4}
    assert out['observed_checks']==8 and out['successful_checks']==8
    assert out['not_named_as_required_runs']==4 and out['required_contexts']==1
    assert out['hard_gate_coverage']=='NOT_PROVEN_BY_API_SNAPSHOT'
    checks+=1
    unique=copy.deepcopy(baseline)
    unique['check_runs']=[x for x in unique['check_runs'] if x['name']!='validate']+[baseline['check_runs'][3]]
    code,out=execute(candidate,unique)
    assert code==0 and out['state']=='NO_REQUIRED_NAME_COLLISION_IN_SNAPSHOT' and not out['collisions']
    checks+=1
    missing=copy.deepcopy(baseline)
    missing['check_runs']=[x for x in missing['check_runs'] if x['name']!='validate']
    code,out=execute(candidate,missing)
    assert code==0 and out['state']=='REQUIRED_CHECK_MISSING' and out['missing_required']==['validate']
    checks+=1
    mutations=[]
    def mut(f):
        d=copy.deepcopy(baseline);f(d);mutations.append(d)
    mut(lambda d:d['ruleset'].__setitem__('enforcement','disabled'))
    mut(lambda d:d['ruleset'].__setitem__('ref_include',['refs/heads/other']))
    mut(lambda d:d['ruleset'].__setitem__('required_status_checks',[]))
    mut(lambda d:d['ruleset']['required_status_checks'].append({'context':'validate','integration_id':15368}))
    mut(lambda d:d['check_runs'].append(copy.deepcopy(d['check_runs'][0])))
    mut(lambda d:d['check_runs'][0].__setitem__('id',True))
    mut(lambda d:d['check_runs'][0].__setitem__('app_id','15368'))
    mut(lambda d:d['check_runs'][0].__setitem__('status','unknown'))
    mut(lambda d:d['check_runs'][0].__setitem__('status','queued'))
    mut(lambda d:d.__setitem__('pr_head','mutable-main'))
    mut(lambda d:d.__setitem__('repository','external/repo'))
    mut(lambda d:d.__setitem__('schema','other'))
    mut(lambda d:d.__setitem__('check_runs',[]))
    mut(lambda d:d['ruleset'].__setitem__('id',0))
    for d in mutations:
        code,out=execute(candidate,d)
        assert code==2 and out['state']=='FAIL_CLOSED', (d,code,out)
        checks+=1;negatives+=1
    for raw in ('{"schema":1,"schema":2}', '{', '{"x":NaN}', '[]'):
        code,out=execute(candidate,raw)
        assert code==2 and out['state']=='FAIL_CLOSED'
        checks+=1;negatives+=1
    print(json.dumps({'state':'PASS','checks':checks,'negative_failclosed':negatives,'real_snapshot':{'checks':8,'required_contexts':1,'duplicate_required_matches':4,'nonrequired_runs':4}},sort_keys=True))


if __name__=='__main__':
    if len(sys.argv)!=2:raise SystemExit('usage: oracle.py candidate.py')
    main(sys.argv[1])
