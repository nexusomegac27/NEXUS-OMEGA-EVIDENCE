#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--root',type=Path,default=Path('.')); ns=ap.parse_args(); root=ns.root.resolve()
    bind=json.loads((root/'validation/A83_ARTIFACT_BINDING_v1.0.json').read_text(encoding='utf-8'))
    errs=[]
    for a in bind['artifacts']:
        p=root/a['path']
        if not p.exists(): errs.append(f"MISSING:{a['path']}"); continue
        b=p.read_bytes(); h=hashlib.sha256(b).hexdigest()
        if len(b)!=a['post_bytes']: errs.append(f"BYTES:{a['path']}:{len(b)}!={a['post_bytes']}")
        if h!=a['post_sha256']: errs.append(f"SHA256:{a['path']}:{h}!={a['post_sha256']}")
    witness=bind['pre_absence_witness']
    a84=root/'docs/phase2/NEXUS_OMEGA_A84_INDEPENDENT_GITHUB_VALIDATION_RETURN_20260831_R0.md'
    if hashlib.sha256(a84.read_bytes()).hexdigest()!=witness['a84_return_sha256']:
        errs.append('A84_WITNESS_HASH_MISMATCH')
    print(json.dumps({'valid':not errs,'errors':errs,'artifacts_checked':len(bind['artifacts'])},indent=2,sort_keys=True))
    raise SystemExit(1 if errs else 0)
if __name__=='__main__': main()
