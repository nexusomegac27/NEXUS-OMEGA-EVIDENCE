#!/usr/bin/env python3
"""Source-exact Gate V2 manifest generator: offline only, no deploy.
Usage: python build_gate_release_v2.py --source-root <checkout/.../site> --commit <40hex>
Only writes a local artifact in source-root/gate/release-v2.json.
"""
import argparse, hashlib, json, pathlib, re
FILES=('index.html','assets/github-implant.css','assets/github-implant.js',
       'nexus-temporal-anchor-r11.css','nexus-temporal-anchor-r11.mjs','temporal-anchor-r11.json',
       'gate/index.html','gate/gate.css','gate/gate.js','gate/gate-core.mjs')

def build(root, ref):
    if not re.fullmatch(r'[0-9a-f]{40}', ref): raise ValueError('PIN_MUST_BE_40_HEX')
    root=pathlib.Path(root).resolve(strict=True)
    records={}
    for rel in FILES:
        p=(root/rel).resolve(strict=True)
        if not p.is_relative_to(root):raise ValueError('PATH_ESCAPE')
        b=p.read_bytes()
        if not 0<len(b)<=600000:raise ValueError('INVALID_BYTES:'+rel)
        records[rel]={'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
    return {'schema':'nexus-gate-release-v2','claim_ceiling':'C1_DESCRIPTIVE_ONLY',
            'target_root':'/forum/github-implant/','release_ref':ref,'files':records}
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--source-root',required=True);ap.add_argument('--commit',required=True);a=ap.parse_args()
    m=build(a.source_root,a.commit)
    outfile=pathlib.Path(a.source_root)/'gate/release-v2.json'
    outfile.write_text(json.dumps(m,sort_keys=True,separators=(',',':'),ensure_ascii=True)+'\n',encoding='utf-8')
    print('CREATED',outfile,'SHA256',hashlib.sha256(outfile.read_bytes()).hexdigest(),'FILESET',len(FILES))
