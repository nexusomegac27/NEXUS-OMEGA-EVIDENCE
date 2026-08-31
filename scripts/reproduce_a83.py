#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, subprocess, sys
from pathlib import Path

def sha256_file(p: Path)->str:
    return hashlib.sha256(p.read_bytes()).hexdigest()

def run(cmd:list[str], cwd:Path)->dict:
    cp=subprocess.run(cmd,cwd=cwd,text=True,capture_output=True)
    return {'command':cmd,'exit_code':cp.returncode,'stdout':cp.stdout[-4000:],'stderr':cp.stderr[-4000:]}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--root',type=Path,default=Path('.')); ap.add_argument('--write-status',action='store_true'); ns=ap.parse_args(); root=ns.root.resolve()
    steps=[]
    steps.append({'name':'compileall','details':run([sys.executable,'-m','compileall','-q','scripts','tests'],root)})
    steps.append({'name':'pytest','details':run([sys.executable,'-m','pytest','-q','tests/test_a83_handoff.py'],root)})
    if (root/'scripts/validate_scientific_ledger.py').exists():
        steps.append({'name':'existing_ledger_validation','details':run([sys.executable,'scripts/validate_scientific_ledger.py','--root','.'],root)})
    schema=json.loads((root/'schema/A83_handoff_envelope_v1.schema.json').read_text(encoding='utf-8'))
    steps.append({'name':'schema_json_parse','exit_code':0 if schema.get('$schema') else 1})
    failed=[]
    for s in steps:
        code=s.get('exit_code',s.get('details',{}).get('exit_code',1))
        if code!=0: failed.append(s['name'])
    verdict='C1.2_CLOSED' if failed else 'C1.1_ARTIFACT_VALIDATED_STRUCTURE_ONLY'
    result={'object':'NEXUS_OMEGA_A83_REPRODUCE_ALL_RESULT_V1','claim_ceiling':'C1','claim_promotion':False,'network_write':False,'verdict':verdict,'failed_steps':failed,'steps':steps}
    print(json.dumps(result,indent=2,sort_keys=True))
    if ns.write_status:
        (root/'validation/A83_FINAL_STATUS_v1.0.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    raise SystemExit(1 if failed else 0)
if __name__=='__main__': main()
