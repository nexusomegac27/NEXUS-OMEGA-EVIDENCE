#!/usr/bin/env python3
"""Read-only structural guard; never turns CI-green into scientific validation."""
import json, re, sys
H40=re.compile(r'^[0-9a-f]{40}$');H64=re.compile(r'^[0-9a-f]{64}$')
def evaluate(data):
    reasons=[]
    head=data.get('head_sha')
    if not isinstance(head,str) or not H40.fullmatch(head):reasons.append('HEAD_NOT_PINNED')
    claim=data.get('claim') if isinstance(data.get('claim'),dict) else {}
    files=data.get('files') if isinstance(data.get('files'),dict) else {}
    result=data.get('result') if isinstance(data.get('result'),dict) else {}
    specs=[('evaluator_path','evaluator_sha256'),('fixture_path','fixture_sha256'),('result_path','result_sha256')]
    paths=[]
    for pkey,hkey in specs:
        path=claim.get(pkey);digest=claim.get(hkey)
        if not isinstance(path,str) or not path or path.startswith('/') or '\\' in path or any(x in ('.','..') for x in path.split('/')):
            reasons.append('INVALID_'+pkey.upper());continue
        paths.append(path)
        if not isinstance(digest,str) or not H64.fullmatch(digest):reasons.append('INVALID_'+hkey.upper());continue
        f=files.get(path)
        if not isinstance(f,dict):reasons.append('MISSING_'+pkey.upper());continue
        if f.get('sha256')!=digest:reasons.append('HASH_MISMATCH_'+pkey.upper())
        if not isinstance(f.get('bytes'),int) or isinstance(f.get('bytes'),bool) or f['bytes']<=0:reasons.append('BYTES_INVALID_'+pkey.upper())
        if not isinstance(f.get('git_blob'),str) or not H40.fullmatch(f['git_blob']):reasons.append('BLOB_INVALID_'+pkey.upper())
        if f.get('readback')!='MATCH':reasons.append('READBACK_MISSING_'+pkey.upper())
    if len(paths)!=3 or len(set(paths))!=3:reasons.append('DUPLICATE_OR_MISSING_PATHS')
    ci=data.get('ci') if isinstance(data.get('ci'),list) else []
    if not any(isinstance(c,dict) and c.get('name')=='alpha-evidence-replay' and c.get('head_sha')==head and c.get('conclusion')=='success' for c in ci):reasons.append('REPLAY_CI_NOT_ATTESTED_AT_HEAD')
    if result.get('head_sha')!=head or result.get('evaluator_sha256')!=claim.get('evaluator_sha256') or result.get('fixture_sha256')!=claim.get('fixture_sha256'):
        reasons.append('RESULT_PROVENANCE_MISMATCH')
    n=result.get('total');p=result.get('passed')
    if not isinstance(n,int) or isinstance(n,bool) or n<=0 or not isinstance(p,int) or isinstance(p,bool) or p!=n:
        reasons.append('RESULT_NOT_FULL_PASS')
    return {'coverage':'GAP' if reasons else 'STRUCTURALLY_COVERED','reasons':sorted(set(reasons)),
            'main_verified':False,'scientific_independence':'NOT_ESTABLISHED',
            'qualification':'STRUCTURAL_CAPTURE_ONLY_NOT_AUTHENTICATED_GITHUB_OR_CI_PROOF'}
if __name__=='__main__':
    try:
        with open(sys.argv[1],encoding='utf-8') as f: x=json.load(f)
        print(json.dumps(evaluate(x),sort_keys=True))
    except (OSError,ValueError,IndexError,TypeError) as e:
        print(json.dumps({'coverage':'GAP','reasons':['INPUT_ERROR'],'error':type(e).__name__}))
        sys.exit(2)
