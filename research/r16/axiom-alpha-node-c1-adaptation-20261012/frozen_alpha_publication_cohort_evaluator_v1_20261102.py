"""Frozen C1 structural evaluator; cannot authenticate GitHub bytes or actors."""
import copy, json, re, sys
H40 = re.compile(r'[0-9a-f]{40}\Z')
H64 = re.compile(r'[0-9a-f]{64}\Z')
MAIN = '7961026bf0f630aee160e083122c2900744d2da1'
COUNTS = [5,5,5,3,3,3,3,3,3,3]
ROOT = 'research/r16/axiom-alpha-node-c1-adaptation-20261012/'

def evaluate(d):
    if type(d) is not dict or set(d) != {'object','claim_ceiling','cohort','pinned_main','prs','limitations'}: return False,'ROOT'
    if d['claim_ceiling'] != 'C1_DESCRIPTIVE_ONLY' or d['pinned_main'] != MAIN: return False,'AUTHORITY'
    if d['cohort'] != {'start_pr':274,'end_pr':283,'selection':'EXPLICIT_BOUNDED_NOT_PROJECT_WIDE'}: return False,'COHORT'
    if type(d['limitations']) is not list or not {'NOT_PROJECT_WIDE','NO_ACTOR_AUTHENTICATION'}.issubset(d['limitations']): return False,'LIMITATIONS'
    if type(d['prs']) is not list or len(d['prs']) != 10: return False,'PR_COUNT'
    prev=None; paths=set(); receipts=set()
    for i,p in enumerate(d['prs']):
        if type(p) is not dict or set(p) != {'number','merge_commit','parent_commit','receipt_id','merged','files'}: return False,'PR_SHAPE'
        if type(p['number']) is not int or p['number'] != i+274 or p['merged'] is not True: return False,'PR_ID'
        if not all(type(p[k]) is str and H40.fullmatch(p[k]) for k in ('merge_commit','parent_commit')): return False,'COMMIT'
        if prev and p['parent_commit'] != prev: return False,'CHAIN'
        prev=p['merge_commit']
        if type(p['receipt_id']) is not int or p['receipt_id'] in receipts: return False,'RECEIPT'
        receipts.add(p['receipt_id'])
        if type(p['files']) is not list or len(p['files']) != COUNTS[i]: return False,'FILE_COUNT'
        for f in p['files']:
            if type(f) is not dict or set(f) != {'path','bytes','sha256','git_blob_sha1','github_blob_sha1','independent_byte_check'}: return False,'FILE_SHAPE'
            if type(f['path']) is not str or not f['path'].startswith(ROOT) or f['path'] in paths: return False,'PATH'
            paths.add(f['path'])
            if type(f['bytes']) is not int or f['bytes'] <= 0 or type(f['sha256']) is not str or not H64.fullmatch(f['sha256']): return False,'BYTES'
            if type(f['git_blob_sha1']) is not str or not H40.fullmatch(f['git_blob_sha1']) or f['git_blob_sha1'] != f['github_blob_sha1'] or f['independent_byte_check'] is not True: return False,'BLOB'
    return (True,'PASS_STRUCTURAL_ONLY') if prev == MAIN else (False,'LAST_MAIN')

def fixture():
    ps=[]
    for i,n in enumerate(COUNTS):
        ps.append(dict(number=274+i,merge_commit=MAIN if i==9 else str(i+1)*40,parent_commit=ps[-1]['merge_commit'] if i else '9'*40,receipt_id=i+100,merged=True,files=[dict(path=ROOT+f'f_{i}_{j}',bytes=1,sha256='a'*64,git_blob_sha1='b'*40,github_blob_sha1='b'*40,independent_byte_check=True) for j in range(n)]))
    return dict(object='COHORT_V1',claim_ceiling='C1_DESCRIPTIVE_ONLY',cohort=dict(start_pr=274,end_pr=283,selection='EXPLICIT_BOUNDED_NOT_PROJECT_WIDE'),pinned_main=MAIN,prs=ps,limitations=['NOT_PROJECT_WIDE','NO_ACTOR_AUTHENTICATION'])

def selftest():
    tests=[('positive',lambda x:None,True),('missing_pr',lambda x:x['prs'].pop(),False),('missing_file',lambda x:x['prs'][0]['files'].pop(),False),('duplicate_receipt',lambda x:x['prs'][1].update(receipt_id=100),False),('broken_chain',lambda x:x['prs'][1].update(parent_commit='0'*40),False),('false_byte_check',lambda x:x['prs'][0]['files'][0].update(independent_byte_check=False),False),('blob_mismatch',lambda x:x['prs'][0]['files'][0].update(github_blob_sha1='c'*40),False),('claim_promotion',lambda x:x.update(claim_ceiling='C2'),False),('scope_swap',lambda x:x['cohort'].update(end_pr=282),False),('last_main_swap',lambda x:x['prs'][-1].update(merge_commit='0'*40),False)]
    n=0
    for name,change,expected in tests:
        x=fixture();change(x);ok,reason=evaluate(x);passed=ok is expected;n+=passed;print(json.dumps(dict(test=name,pass_test=passed,reason=reason)))
    print(json.dumps(dict(passed=n,total=len(tests),result='PASS' if n==len(tests) else 'FAIL',scope='STRUCTURAL_ONLY')))
    return 0 if n==len(tests) else 1
if __name__=='__main__':
    if len(sys.argv)==2 and sys.argv[1]=='--selftest':sys.exit(selftest())
    if len(sys.argv)!=2:sys.exit('USAGE: evaluator manifest.json | --selftest')
    try:
        with open(sys.argv[1],encoding='utf8') as f:d=json.load(f)
        ok,reason=evaluate(d)
    except (OSError,ValueError,TypeError,RecursionError) as e:ok,reason=False,type(e).__name__
    print(json.dumps(dict(pass_test=ok,reason=reason,scope='STRUCTURAL_ONLY')))
    sys.exit(0 if ok else 1)
