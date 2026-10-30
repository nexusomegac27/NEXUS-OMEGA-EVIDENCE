#!/usr/bin/env python3
"""Independent black-box URL-scope oracle. Does not import the candidate."""
import json
import subprocess
import sys

PIN = '8ceb184409c15c95ecdcf314e6209fb41bfed9bf'
BASE = 'https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE'

def run(candidate, ref, sha=PIN):
    p = subprocess.run([sys.executable, '-S', candidate], input=json.dumps({'source_ref':ref,'source_commit':sha}), text=True, capture_output=True, timeout=5)
    try: obj=json.loads(p.stdout)
    except ValueError: raise AssertionError('invalid JSON output: '+p.stdout)
    return p.returncode, obj

def main(candidate):
    positive = [
        BASE+'/issues/93',
        BASE+'/issues/93#issuecomment-6525110654',
        BASE+'/pull/115',
        BASE+'/commit/'+PIN,
        BASE+'/blob/'+PIN+'/research/r16/alpha_report.md',
    ]
    negative = [
        'https://github.com.evil.invalid/nexusomegac27/NEXUS-OMEGA-EVIDENCE/issues/93',
        'https://github.com@evil.invalid/nexusomegac27/NEXUS-OMEGA-EVIDENCE/issues/93',
        'http://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/issues/93',
        BASE+'/issues/93?redirect=https://evil.invalid',
        BASE+'/issues/93#unrecognized',
        BASE+'/issues/93/',
        BASE+'/issues/0',
        BASE+'/issues/93/../../evil',
        BASE+'/issues/%39%33',
        BASE+'/issues//93',
        'https://github.com/other/NEXUS-OMEGA-EVIDENCE/issues/93',
        BASE+'/blob/main/research/r16/report.md',
        BASE+'/blob/'+'0'*40+'/research/r16/report.md',
        BASE+'/commit/'+'f'*40+'/evil',
        BASE+'/pull/115#issuecomment-0',
        BASE+'/issues/93\\@evil.invalid',
        BASE+'/issues/93\nX',
        'https://github.com:443/nexusomegac27/NEXUS-OMEGA-EVIDENCE/issues/93',
    ]
    count=0
    for ref in positive:
        code,out=run(candidate,ref)
        assert code==0 and out.get('status')=='CANONICAL_REPO_SOURCE_URL_SCOPE_PASS' and out.get('source_commit')==PIN, (ref,code,out)
        count+=1
    for ref in negative:
        code,out=run(candidate,ref)
        assert code!=0 and out.get('status')=='FAIL_CLOSED', (ref,code,out)
        count+=1
    code,out=run(candidate,BASE+'/issues/93',sha='bad')
    assert code!=0 and out.get('status')=='FAIL_CLOSED'
    count+=1
    print(f'INDEPENDENT_SUBPROCESS_ORACLE={count}/{count} PASS; NEGATIVE_FAIL_CLOSED={len(negative)+1}/{len(negative)+1}; VALID={len(positive)}/{len(positive)}')
    # Exact V1 condition in alpha_handoff_attempt_denominator_v1_20261030.py.
    wrong_repo='https://github.com/other/NEXUS-OMEGA-EVIDENCE/issues/93'
    assert wrong_repo.startswith('https://github.com/')
    print('V1_WRONG_REPOSITORY_ACCEPTED_BY_PREFIX_CHECK=TRUE; V2_REJECTED=TRUE')

if __name__=='__main__':
    main(sys.argv[1])
