#!/usr/bin/env python3
"""Frozen black-box C1 evaluator. Never imports or modifies the candidate."""
import copy
import json
import subprocess
import sys

PIN = '4235539c67d8a2af203898886f55252ec495d17a'
BASE = 'https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE'
FLAGS = ('unauthorized_write','hidden_source_gap','source_overwrite','claim_promotion')


def row(ident, ref=None, **changes):
    out = dict(attempt_id=ident, source_ref=ref or BASE+'/issues/93', source_commit=PIN,
               public=True, routine=True, authorized=True, accessible=True,
               autonomous=False, handoff_verified=False, published=False,
               full_readback=False, **{k:False for k in FLAGS})
    out.update(changes)
    return out


def payload(*rows):
    return dict(schema='ALPHA_HANDOFF_ATTEMPT_DENOMINATOR_V1',scope='FROZEN_SYNTHETIC_C1',
                pinned_main=PIN,coverage='DECLARED_COMPLETE_NOT_AUTHENTICATED',attempts=list(rows))


def run(path, data):
    wire = data if isinstance(data,str) else json.dumps(data,separators=(',',':'))
    p = subprocess.run([sys.executable,'-S',path],input=wire,text=True,
                       capture_output=True,timeout=6)
    try: result=json.loads(p.stdout)
    except ValueError as exc: raise AssertionError(f'non-JSON output {p.stdout!r}') from exc
    return p.returncode,result


def main(candidate, predecessor):
    tests = 0
    negatives = 0
    sample = payload(row('success',autonomous=True,handoff_verified=True),
                     row('failed',published=True,full_readback=False))
    code, out = run(candidate,sample)
    assert code==0 and out['eligible']==2 and out['autonomous_verified']==1
    assert out['sample_autonomous_rate']==0.5 and out['sample_safety_qualified_rate']==0.5
    assert out['published']==1 and out['complete_readback']==0 and out['sample_readback_rate']==0.0
    assert out['project_automation_rate'] is None and out['project_full_readback_rate'] is None
    assert out['project_zero_violation_claim']=='NOT_ESTABLISHED'
    assert out['source_scope_preflight']=='CANONICAL_REPO_SYNTAX_ONLY_NOT_AUTHENTICATED'
    assert out['schema']=='ALPHA_HANDOFF_ATTEMPT_DENOMINATOR_RESULT_V2'
    tests+=1

    mixed = payload(row('eligible',autonomous=True,handoff_verified=True,hidden_source_gap=True),
                    row('excluded',accessible=False),row('unknown',authorized=None))
    code,out=run(candidate,mixed)
    assert code==0 and (out['eligible'],out['excluded'],out['unknown'])==(1,1,1)
    assert out['autonomous_verified']==1 and out['safety_qualified_autonomous']==0
    assert out['observed_violations']==1 and out['project_automation_rate'] is None
    tests+=1

    valid=[BASE+'/issues/93',BASE+'/issues/93#issuecomment-6531871051',BASE+'/pull/115',
           BASE+'/commit/'+PIN,BASE+'/blob/'+PIN+'/research/r16/report.md']
    for i,ref in enumerate(valid):
        code,out=run(candidate,payload(row('valid'+str(i),ref)))
        assert code==0 and out['eligible']==1 and out['sample_autonomous_rate']==0.0,(ref,code,out)
        tests+=1

    bad=[
      'https://github.com/other/NEXUS-OMEGA-EVIDENCE/issues/93',
      BASE+'/blob/main/research/r16/report.md',
      BASE+'/blob/'+'0'*40+'/research/r16/report.md',
      'https://github.com.evil.invalid/nexusomegac27/NEXUS-OMEGA-EVIDENCE/issues/93',
      BASE+'/issues/93?query=1',BASE+'/issues/%39%33',
      BASE+'/issues/93#unrecognized',BASE+'/issues/93/',
      'https://github.com:443/nexusomegac27/NEXUS-OMEGA-EVIDENCE/issues/93',
      BASE+'/commit/'+'0'*40+'/extra',
    ]
    for i,ref in enumerate(bad):
        code,out=run(candidate,payload(row('bad'+str(i),ref)))
        assert code!=0 and out.get('state')=='FAIL_CLOSED',(ref,code,out)
        tests+=1; negatives+=1

    bad_inputs=[
      payload(row('badcommit',source_commit='main')),
      payload(row('badbool',autonomous=1)),
      payload(row('dup'),row('dup')),
      {'schema':'WRONG','scope':'x','pinned_main':PIN,'coverage':'INCOMPLETE','attempts':[]},
      payload(row('missing',source_ref=None)),
      '{"schema":"ALPHA_HANDOFF_ATTEMPT_DENOMINATOR_V1","schema":"ALPHA_HANDOFF_ATTEMPT_DENOMINATOR_V1"}',
      '{"schema":"ALPHA_HANDOFF_ATTEMPT_DENOMINATOR_V1","scope":"x","pinned_main":"'+PIN+'","coverage":"INCOMPLETE","attempts":[],"extra":NaN}',
    ]
    # A None ref in row() uses default by design: force missing explicitly.
    bad_inputs[4]['attempts'][0]['source_ref']=None
    for data in bad_inputs:
        code,out=run(candidate,data)
        assert code!=0 and out.get('state')=='FAIL_CLOSED',(data,code,out)
        tests+=1; negatives+=1

    # Negative baseline: exact historical V1 must accept the wrong repository in its sample.
    code,old=run(predecessor,payload(row('old',bad[0])))
    assert code==0 and old['eligible']==1 and old['sample_autonomous_rate']==0.0
    tests+=1
    # A canonical URL remains a locator only; project-level success is never asserted.
    assert old['project_automation_rate'] is None
    print(f'FROZEN_SUBPROCESS_ORACLE={tests}/{tests} PASS; NEGATIVE_FAIL_CLOSED={negatives}/{negatives}; '
          f'CANONICAL_VALID={len(valid)}/{len(valid)}; V1_WRONG_REPO_ACCEPTS=1/1; V2_WRONG_REPO_ACCEPTS=0/1')

if __name__=='__main__':
    if len(sys.argv)!=3: raise SystemExit('usage: oracle.py candidate.py predecessor_v1.py')
    main(sys.argv[1],sys.argv[2])
