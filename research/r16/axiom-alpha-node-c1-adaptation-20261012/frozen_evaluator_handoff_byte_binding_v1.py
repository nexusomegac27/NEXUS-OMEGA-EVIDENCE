#!/usr/bin/env python3
"""Pre-implementation independent offline oracle: evidence-bound handoff counts.

Synthetic fixtures only. Never treats local bytes as authenticated GitHub transport.
"""
import hashlib, importlib.util, json, pathlib, sys
path = pathlib.Path(sys.argv[1]).resolve()
spec = importlib.util.spec_from_file_location('under_test', path)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
SHA = 'd355400dabed3c280e1fce5030cab69ea099428b'
SRC = b'published source\n'
TEST = b'{"tests":3,"passed":3,"failed":0}\n'
def digest(b): return hashlib.sha256(b).hexdigest()
def blob(b): return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\x00'+b).hexdigest()
BASE = dict(artifact='A', routine=True, public=True, authorized=True,
            source_accessible=True, write_access_verified=True,
            branch_published=False, main_published=True,
            source_hash_readback=True, test_readback=True, commit_readback=True,
            issue93_receipt_readback=True, source_gap=False, claim_promotion=False)
def rec(**kw): return dict(BASE,**kw)
def proof():
    receipt = {'main_sha':SHA,'source_sha256':digest(SRC),
               'test_sha256':digest(TEST),'claim_ceiling':'C1_DESCRIPTIVE_ONLY'}
    rb = (json.dumps(receipt,sort_keys=True)+'\n').encode()
    return {'repository':'nexusomegac27/NEXUS-OMEGA-EVIDENCE',
            'path':'research/r16/axiom-alpha-node-c1-adaptation-20261012/fixture.md',
            'source_bytes':SRC,'source_sha256':digest(SRC),
            'source_blob_sha1':blob(SRC),'source_byte_count':len(SRC),
            'test_bytes':TEST,'test_sha256':digest(TEST),
            'issue_comment_bytes':rb,'issue_comment_sha256':digest(rb),
            'issue_comment_id':12345,'commit_sha':SHA}

def variant(**changes):
    p=proof();p.update(changes);return p

cases = [
 ('valid_local_binding',[rec()],{'A':proof()},SHA,(1,1),set()),
 ('missing_proof',[rec()],{},SHA,(1,0),{'PROOF_NOT_PRESENT'}),
 ('source_bytes_tampered',[rec()],{'A':variant(source_bytes=b'evil')},SHA,(1,0),{'SOURCE_BYTES_MISMATCH'}),
 ('source_digest_forged',[rec()],{'A':variant(source_sha256='0'*64)},SHA,(1,0),{'SOURCE_BYTES_MISMATCH'}),
 ('blob_id_forged',[rec()],{'A':variant(source_blob_sha1='0'*40)},SHA,(1,0),{'SOURCE_BLOB_MISMATCH'}),
 ('wrong_size',[rec()],{'A':variant(source_byte_count=len(SRC)+1)},SHA,(1,0),{'SOURCE_BYTES_MISMATCH'}),
 ('test_bytes_tampered',[rec()],{'A':variant(test_bytes=b'failed')},SHA,(1,0),{'TEST_BYTES_MISMATCH'}),
 ('comment_bytes_tampered',[rec()],{'A':variant(issue_comment_bytes=b'forged')},SHA,(1,0),{'ISSUE_RECEIPT_BYTES_MISMATCH'}),
 ('comment_binding_forged',[rec()],{'A':variant(issue_comment_bytes=b'{"main_sha":"wrong"}',issue_comment_sha256=digest(b'{"main_sha":"wrong"}'))},SHA,(1,0),{'ISSUE_RECEIPT_BINDING_MISMATCH'}),
 ('missing_issue_id',[rec()],{'A':variant(issue_comment_id=0)},SHA,(1,0),{'ISSUE_RECEIPT_ID_INVALID'}),
 ('wrong_commit',[rec()],{'A':variant(commit_sha='a'*40)},SHA,(1,0),{'MAIN_COMMIT_MISMATCH'}),
 ('unobserved_main',[rec()],{'A':proof()},None,(1,0),{'MAIN_READBACK_NOT_ESTABLISHED'}),
 ('branch_only',[rec(main_published=False,branch_published=True)],{},SHA,(1,0),set()),
 ('excluded_private',[rec(public=False,main_published=False)],{},SHA,(0,0),set()),
 ('claim_promotion',[rec(claim_promotion=True)],{'A':proof()},SHA,(1,0),{'CLAIM_PROMOTION_PROHIBITED'}),
 ('invalid_proof_type',[rec()],{'A':'forged'},SHA,(1,0),{'PROOF_INVALID'}),
]
fails=[]
for name,records,proofs,observed,expected,required in cases:
    try:
        out=mod.measure_bound(records,proofs,observed)
        counts=(out['eligible_denominator'],out['byte_bound_numerator'])
        codes={f['code'] for f in out['flags']}
        ok=counts==expected and required.issubset(codes) and out['project_handoff_rate'] is None and out['external_authentication_established'] is False
    except Exception as e:
        counts=None;codes=set();ok=False;error=f'{type(e).__name__}:{e}'
    if not ok:fails.append(name)
    print(json.dumps({'case':name,'pass':ok,'counts':counts,'expected':expected,'codes':sorted(codes),'error':locals().get('error') if not ok else None},sort_keys=True))
    error=None
print(json.dumps({'total':len(cases),'passed':len(cases)-len(fails),'failed':fails},sort_keys=True))
sys.exit(bool(fails))
