# SPDX-License-Identifier: Apache-2.0
"""Execute local checks and print a report. Never installs dependencies or writes reports."""
import datetime
import hashlib
import importlib.metadata
import json
import platform
import sqlite3
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
commands = [('reference_tests', ['-m','unittest','discover','-s',str(ROOT/'tests'),'-v'])]
if (REPO/'scripts/validate_repository_structure.py').is_file():
    commands += [('repository_structure',['scripts/validate_repository_structure.py','--root','.']),
                 ('repository_structure_tests',['-m','unittest','tests.test_repository_structure'])]
report = {'schema_version':'forum-local-checks/1','claim_ceiling':'C1_DESCRIPTIVE_ONLY',
          'executed_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'environment':{'python':platform.python_version(),'sqlite':sqlite3.sqlite_version,
                         'jsonschema':importlib.metadata.version('jsonschema'),'platform':platform.system()},
          'checks':[], 'source_files':[],
          'not_executed':['R10_BUILD','R10_UNIT_RERUN','BROWSER_QA','SCREENREADER','AUTH_SERVICE',
                          'POWER_LOSS','BACKUP_RESTORE','FULL_HISTORICAL_CORPUS_AUDIT',
                          'CROSS_SUBSTRATE_TRIAL_001','MISTRAL_VIBE_REVIEW','HOSTED_CI']}
for label, args in commands:
    done=subprocess.run([sys.executable,*args],cwd=REPO if (REPO/'AGENTS.md').is_file() else ROOT,
                        capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=90)
    # Strip local root from logs for public delivery; never expose user checkout paths.
    output=(done.stdout+done.stderr).replace(str(REPO),'[repository]').replace(str(ROOT),'[candidate]')
    display='python '+' '.join(args).replace(str(ROOT),'research/r5/forum-symbiosis')
    report['checks'].append({'id':label,'command':display,'exit_code':done.returncode,'output':output})
for directory in ('scripts','tests','schema','examples'):
    for p in sorted((ROOT/directory).rglob('*')):
        if p.is_file() and '__pycache__' not in p.parts and p.suffix != '.pyc':
            report['source_files'].append({'path':p.relative_to(ROOT).as_posix(),
                                         'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
tokens=json.loads((ROOT/'examples/ui-tokens.json').read_text())
def luminance(color):
    c=[int(color[i:i+2],16)/255 for i in (1,3,5)]
    c=[v/12.92 if v<=0.04045 else ((v+0.055)/1.055)**2.4 for v in c]
    return sum(a*b for a,b in zip(c,(0.2126,0.7152,0.0722)))
report['design_token_contrast']=[]
for bg in ('background','surface'):
    for fg in ('text','muted','accent','focus','error'):
        high,low=sorted((luminance(tokens[fg]),luminance(tokens[bg])),reverse=True)
        ratio=(high+0.05)/(low+0.05)
        report['design_token_contrast'].append({'foreground':fg,'background':bg,'ratio':ratio,'pass_4_5':ratio>=4.5})
report['status']='PASS' if all(c['exit_code']==0 for c in report['checks']) else 'FAIL'
print(json.dumps(report,ensure_ascii=False,indent=2))
sys.exit(0 if report['status']=='PASS' else 1)
