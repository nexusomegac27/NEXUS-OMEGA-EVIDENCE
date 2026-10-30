#!/usr/bin/env python3
"""Frozen independent black-box oracle for isolated source byte proof (subprocess only).

Never imports candidate. Positive source identity pinned from GitHub original; Git CLI is
an independent Git-blob countercheck when available. Synthetic negatives are explicit.
"""
import copy
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

COMMIT = '167cd7672f701bf27b67f147568ce9cee00a2d59'
REL = 'research/r16/axiom-alpha-node-c1-adaptation-20261012/alpha_handoff_commit_ref_binding_v3_20261030.py'
SHA256 = '425e60df8d363866b90924d739b237a051033def77d5b7d0bb71d63979fba0c3'
BLOB = '73ef222f9117f566930390e60899d571ecc77402'
SIZE = 1452
BASE = 'https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/blob/'


def manifest():
    return {'schema':'NEXUS_ALPHA_SOURCE_BYTE_PROOF_V1',
            'repository':'nexusomegac27/NEXUS-OMEGA-EVIDENCE',
            'source_ref':BASE+COMMIT+'/'+REL, 'source_commit':COMMIT, 'path':REL,
            'bytes':SIZE, 'sha256':SHA256, 'git_blob_sha1':BLOB,
            'claim_ceiling':'C1_DESCRIPTIVE_ONLY'}


def run(script, root, payload):
    wire = payload if isinstance(payload,str) else json.dumps(payload,separators=(',',':'))
    p = subprocess.run([sys.executable,'-S',str(script),str(root)],input=wire,
                       text=True,capture_output=True,timeout=7)
    assert p.stdout.strip(), (p.returncode,p.stderr)
    return p.returncode,json.loads(p.stdout)


def main(candidate, predecessor, repo_root):
    source=repo_root/REL
    raw=source.read_bytes()
    assert len(raw)==SIZE and hashlib.sha256(raw).hexdigest()==SHA256
    git=subprocess.run(['git','hash-object','--stdin'],input=raw,capture_output=True,timeout=7)
    assert git.returncode==0 and git.stdout.decode().strip()==BLOB
    checks=0; negatives=0
    old=subprocess.run([sys.executable,'-S',str(predecessor)],
        input=json.dumps({'source_ref':manifest()['source_ref'],'source_commit':COMMIT}),
        text=True,capture_output=True,timeout=7)
    assert old.returncode==0 and json.loads(old.stdout)['status']=='CANONICAL_REPO_SOURCE_URL_SCOPE_PASS'
    checks+=1
    code,out=run(candidate,repo_root,manifest())
    assert code==0 and out['state']=='LOCAL_SOURCE_BYTES_MATCH'
    assert out['bytes']==SIZE and out['sha256']==SHA256 and out['git_blob_sha1']==BLOB
    assert out['commit_tree_membership']=='NOT_VERIFIED' and out['transport_authentication']=='NOT_VERIFIED'
    checks+=1
    negatives_payload=[]
    def bad(**kw):
        m=manifest();m.update(kw);negatives_payload.append(m)
    bad(bytes=SIZE+1)
    bad(bytes=True)
    bad(sha256='0'*64)
    bad(git_blob_sha1='0'*40)
    bad(source_commit='0'*40)
    bad(source_ref=BASE+'0'*40+'/'+REL)
    bad(source_ref='https://github.com/another/repo/blob/'+COMMIT+'/'+REL)
    bad(source_ref=manifest()['source_ref']+'?raw=1')
    bad(source_ref=manifest()['source_ref']+'#L1')
    bad(source_ref=manifest()['source_ref'].replace('/blob/','/commit/'))
    bad(path='../'+REL)
    bad(path=REL.replace('alpha_handoff','missing_handoff'))
    bad(repository='other/repo')
    bad(claim_ceiling='C2')
    bad(schema='NEXUS_ALPHA_SOURCE_BYTE_PROOF_V2')
    extra=manifest();extra['authenticated_actor']='owner';negatives_payload.append(extra)
    negatives_payload.extend([
        '{"schema":"x","schema":"y"}',
        '{"schema":"x","bytes":NaN}',
        '{broken',
    ])
    for p in negatives_payload:
        code,out=run(candidate,repo_root,p)
        assert code!=0 and out.get('state')=='FAIL_CLOSED',(p,code,out)
        checks+=1;negatives+=1
    with tempfile.TemporaryDirectory() as td:
        root=Path(td);target=root/REL;target.parent.mkdir(parents=True)
        # Same-length mutation: URL and all producer-declared metadata unchanged.
        mutated=bytearray(raw);mutated[100]^=1;target.write_bytes(mutated)
        code,out=run(candidate,root,manifest())
        assert code!=0 and out['state']=='FAIL_CLOSED' and out['reason']=='SHA256_MISMATCH'
        checks+=1;negatives+=1
        target.unlink()
        target.symlink_to(source)
        code,out=run(candidate,root,manifest())
        assert code!=0 and out['state']=='FAIL_CLOSED' and out['reason']=='SYMLINK'
        checks+=1;negatives+=1
    print('FROZEN_BLACKBOX_CHECKS=%d/%d PASS; NEGATIVES=%d/%d FAIL_CLOSED; '
          'REAL_SOURCE_BYTES=%d SHA256_MATCH GIT_CLI_BLOB_MATCH; '
          'OLD_URL_SYNTAX_ACCEPTS=1/1; NEW_BYTE_PROOF_REJECTS_SAME_LENGTH_MUTATION=1/1; '
          'COMMIT_MEMBERSHIP_AND_TRANSPORT_AUTH=NOT_VERIFIED' %
          (checks,checks,negatives,negatives,SIZE))


if __name__=='__main__':
    if len(sys.argv)!=4:raise SystemExit('oracle candidate.py old_guard.py repo_root')
    main(Path(sys.argv[1]).resolve(),Path(sys.argv[2]).resolve(),Path(sys.argv[3]).resolve())
