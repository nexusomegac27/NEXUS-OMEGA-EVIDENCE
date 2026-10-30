#!/usr/bin/env python3
"""Independent black-box C1 oracle. Subprocess only; no candidate import or edits."""
import json
import subprocess
import sys

PIN = '68719c2aedaf8aa325d3319d3e49d98e3ded70bd'
OTHER = '0' * 40
BASE = 'https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE'
FLAGS = ('unauthorized_write', 'hidden_source_gap', 'source_overwrite', 'claim_promotion')


def row(ident, ref=None, commit=PIN, **overrides):
    result = dict(attempt_id=ident, source_ref=ref or BASE+'/commit/'+PIN,
                  source_commit=commit, public=True, routine=True, authorized=True,
                  accessible=True, autonomous=False, handoff_verified=False,
                  published=False, full_readback=False, **{k:False for k in FLAGS})
    result.update(overrides)
    return result


def payload(*rows):
    return dict(schema='ALPHA_HANDOFF_ATTEMPT_DENOMINATOR_V1',
                scope='FROZEN_SYNTHETIC_C1', pinned_main=PIN,
                coverage='INCOMPLETE', attempts=list(rows))


def run(path, data):
    wire = data if isinstance(data,str) else json.dumps(data,separators=(',',':'))
    p = subprocess.run([sys.executable,'-S',path], input=wire, text=True,
                       capture_output=True, timeout=6)
    assert p.stdout.strip(), ('empty output',p.stderr)
    return p.returncode, json.loads(p.stdout)


def main(candidate, predecessor):
    checks=0; negatives=0
    # Baseline falsifier: V2 accepts a commit URL inconsistent with its source_commit.
    mismatch=payload(row('mismatch',BASE+'/commit/'+OTHER,commit=PIN))
    code,old=run(predecessor,mismatch)
    assert code==0 and old['eligible']==1 and old['schema'].endswith('V2')
    checks+=1
    bad=[
        payload(row('wrong_oid',BASE+'/commit/'+OTHER)),
        payload(row('wrong_declared',BASE+'/commit/'+PIN,commit=OTHER)),
        payload(row('mixed',BASE+'/commit/'+OTHER),row('good')),
        payload(row('excluded',BASE+'/commit/'+OTHER,accessible=False)),
        payload(row('unknown',BASE+'/commit/'+OTHER,authorized=None)),
        payload(row('published',BASE+'/commit/'+OTHER,published=True,full_readback=True)),
    ]
    for p in bad:
        code,out=run(candidate,p)
        assert code!=0 and out.get('state')=='FAIL_CLOSED',(code,out)
        checks+=1; negatives+=1
    valid=[BASE+'/commit/'+PIN,BASE+'/issues/93',BASE+'/pull/115',
           BASE+'/issues/93#issuecomment-6532872551',
           BASE+'/blob/'+PIN+'/research/r16/report.md']
    for i,ref in enumerate(valid):
        code,out=run(candidate,payload(row('valid'+str(i),ref)))
        assert code==0 and out['eligible']==1 and out['schema'].endswith('V3'),(ref,code,out)
        assert out['project_automation_rate'] is None and out['project_full_readback_rate'] is None
        assert out['commit_ref_binding']=='COMMIT_URL_EQUALS_SOURCE_COMMIT_SYNTAX_ONLY'
        checks+=1
    sample=payload(row('success',autonomous=True,handoff_verified=True),
                   row('failed',published=True,full_readback=False),
                   row('unknown',authorized=None))
    code,out=run(candidate,sample)
    assert code==0 and (out['eligible'],out['unknown'])==(2,1)
    assert out['sample_autonomous_rate']==0.5 and out['sample_readback_rate']==0.0
    assert out['project_zero_violation_claim']=='NOT_ESTABLISHED'
    checks+=1
    invalid=[
      payload(row('foreign','https://github.com/other/repo/commit/'+PIN)),
      payload(row('mutable',BASE+'/blob/main/readme.md')),
      payload(row('badtype',source_commit=7)),
      payload(row('dup'),row('dup')),
      '{"schema":"ALPHA_HANDOFF_ATTEMPT_DENOMINATOR_V1","schema":"ALPHA_HANDOFF_ATTEMPT_DENOMINATOR_V1"}',
      '{"schema":"ALPHA_HANDOFF_ATTEMPT_DENOMINATOR_V1","attempts":[],"bad":NaN}',
    ]
    for p in invalid:
        code,out=run(candidate,p)
        assert code!=0 and out.get('state')=='FAIL_CLOSED',(code,out)
        checks+=1; negatives+=1
    print(f'FROZEN_SUBPROCESS_ORACLE={checks}/{checks} PASS; NEGATIVE_FAIL_CLOSED={negatives}/{negatives}; '
          'V2_MISMATCH_ACCEPTS=1/1; V3_MISMATCH_ACCEPTS=0/6; VALID=5/5; '
          'SYNTHETIC_DENOMINATOR_PRESERVED=2/2; PROJECT_RATES=NOT_COMPUTABLE')


if __name__=='__main__':
    if len(sys.argv)!=3: raise SystemExit('usage: oracle.py candidate_v3.py predecessor_v2.py')
    main(sys.argv[1],sys.argv[2])
