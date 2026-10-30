#!/usr/bin/env python3
"""Frozen black-box oracle. Independently pinned GitHub API tuple, not a trust authority.

This oracle imports no candidate code and runs predecessor/candidate in subprocesses.
The external expected pin SHA-256 is fixed here before the candidate is written.
"""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT_SHA = '60b0fddfe38708d4de486e0355ff684e8eb12b98'
COMMIT = '167cd7672f701bf27b67f147568ce9cee00a2d59'
REL = 'research/r16/axiom-alpha-node-c1-adaptation-20261012/alpha_handoff_commit_ref_binding_v3_20261030.py'
SIZE = 1452
SHA = '425e60df8d363866b90924d739b237a051033def77d5b7d0bb71d63979fba0c3'
BLOB = '73ef222f9117f566930390e60899d571ecc77402'
OLD_SHA = '5584b4c2c6c2f6d2f5cb5a4b3e9919a69e8772c2fd0305f97a4862b426d77cc8'
PIN_SHA = 'd1bf6a811f42c575a5d8c6506f6ae6f67edff514470406e691830419257563dc'
BASE = 'https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/blob/'


def manifest(raw):
    return {'schema':'NEXUS_ALPHA_SOURCE_BYTE_PROOF_V1',
            'repository':'nexusomegac27/NEXUS-OMEGA-EVIDENCE',
            'source_ref':BASE+COMMIT+'/'+REL, 'source_commit':COMMIT, 'path':REL,
            'bytes':len(raw), 'sha256':hashlib.sha256(raw).hexdigest(),
            'git_blob_sha1':hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\x00'+raw).hexdigest(),
            'claim_ceiling':'C1_DESCRIPTIVE_ONLY'}


def run(script, args, payload):
    wire = payload if isinstance(payload,str) else json.dumps(payload,sort_keys=True,separators=(',',':'))
    p=subprocess.run([sys.executable,'-S',str(script),*map(str,args)],input=wire,
                     text=True,capture_output=True,timeout=8)
    assert p.stdout.strip(),(p.returncode,p.stderr)
    return p.returncode,json.loads(p.stdout)


def main(candidate, predecessor, pin_file, root):
    checks=0; negatives=0
    raw=(root/REL).read_bytes()
    assert len(raw)==SIZE and hashlib.sha256(raw).hexdigest()==SHA
    assert hashlib.sha256(predecessor.read_bytes()).hexdigest()==OLD_SHA
    pin_raw=pin_file.read_bytes()
    assert hashlib.sha256(pin_raw).hexdigest()==PIN_SHA
    pin=json.loads(pin_raw)
    assert pin['source_commit']==COMMIT and pin['root_tree_sha1']==ROOT_SHA
    assert pin['path']==REL and pin['api_tree_entry_sha1']==BLOB and not pin['api_tree_truncated']
    assert pin['api_tree_entry_mode']=='100644' and pin['api_tree_entry_type']=='blob'
    checks+=1
    good=manifest(raw)
    code,out=run(predecessor,[root],good)
    assert code==0 and out['state']=='LOCAL_SOURCE_BYTES_MATCH'
    checks+=1
    code,out=run(candidate,[root,pin_file,PIN_SHA,predecessor],good)
    assert code==0 and out['state']=='TRUSTED_PIN_SOURCE_BYTES_MATCH'
    assert out['commit_tree_membership']=='API_PROJECTION_MATCH_NOT_CRYPTOGRAPHICALLY_RECONSTRUCTED'
    checks+=1
    # The crucial adversary controls source bytes AND its producer manifest.
    with tempfile.TemporaryDirectory() as td:
        tmp=Path(td); target=tmp/REL; target.parent.mkdir(parents=True)
        mutated=bytearray(raw);mutated[100]^=1;target.write_bytes(mutated)
        forged=manifest(bytes(mutated))
        code,out=run(predecessor,[tmp],forged)
        assert code==0 and out['state']=='LOCAL_SOURCE_BYTES_MATCH'
        checks+=1
        code,out=run(candidate,[tmp,pin_file,PIN_SHA,predecessor],forged)
        assert code!=0 and out['state']=='FAIL_CLOSED' and out['reason']=='TRUSTED_PIN_MANIFEST_MISMATCH'
        checks+=1;negatives+=1
        target.unlink();target.symlink_to(root/REL)
        code,out=run(candidate,[tmp,pin_file,PIN_SHA,predecessor],good)
        assert code!=0 and out['state']=='FAIL_CLOSED'
        checks+=1;negatives+=1
    bad=[]
    def wrong(**kw):
        o=good.copy();o.update(kw);bad.append(o)
    wrong(source_commit='0'*40)
    wrong(path='another/path.py')
    wrong(sha256='0'*64)
    wrong(git_blob_sha1='0'*40)
    wrong(bytes=SIZE+1)
    wrong(repository='other/repo')
    wrong(claim_ceiling='C2')
    wrong(source_ref=BASE+'0'*40+'/'+REL)
    bad.extend(['{"schema":"x","schema":"y"}', '{"schema":"x","bytes":NaN}', '{broken'])
    for item in bad:
        code,out=run(candidate,[root,pin_file,PIN_SHA,predecessor],item)
        assert code!=0 and out['state']=='FAIL_CLOSED',(item,code,out)
        checks+=1;negatives+=1
    # Same valid source, but tampered witness must fail against frozen expected digest.
    with tempfile.TemporaryDirectory() as td:
        fake=Path(td)/'pin.json';data=pin.copy();data['root_tree_sha1']='0'*40
        fake.write_text(json.dumps(data,sort_keys=True,separators=(',',':'))+'\n')
        code,out=run(candidate,[root,fake,PIN_SHA,predecessor],good)
        assert code!=0 and out['reason']=='TRUSTED_PIN_DIGEST_MISMATCH'
        checks+=1;negatives+=1
        # Changed predecessor executable cannot be accepted as a trusted source-byte gate.
        altered=Path(td)/'predecessor.py';altered.write_bytes(predecessor.read_bytes()+b'\n# altered\n')
        code,out=run(candidate,[root,pin_file,PIN_SHA,altered],good)
        assert code!=0 and out['reason']=='PREDECESSOR_DIGEST_MISMATCH'
        checks+=1;negatives+=1
    print('FROZEN_ORACLE_CHECKS=%d/%d PASS; NEGATIVES=%d/%d FAIL_CLOSED; '
          'REAL_SOURCE=%d_BYTES_SHA256_BLOB_MATCH; OLD_FORGED_MANIFEST_ACCEPT=1/1; '
          'NEW_FORGED_MANIFEST_REJECT=1/1; API_TREE_PROJECTION=PINNED_NOT_CRYPTOGRAPHICALLY_RECONSTRUCTED' %
          (checks,checks,negatives,negatives,SIZE))


if __name__=='__main__':
    if len(sys.argv)!=5:raise SystemExit('oracle candidate.py predecessor.py pin.json repo_root')
    main(*(Path(x).resolve() for x in sys.argv[1:]))
