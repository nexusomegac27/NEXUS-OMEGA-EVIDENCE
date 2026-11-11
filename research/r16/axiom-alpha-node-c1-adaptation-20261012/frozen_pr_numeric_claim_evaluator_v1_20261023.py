#!/usr/bin/env python3
"""Predeclared C1 numeric-claim grammar oracle; no candidate imports.

Frozen before the V3 candidate. Synthetic cases test bounded ASCII unsigned
claims and rejection of Unicode/overflow/signed/decimal ambiguity. Does not
fetch GitHub or establish a real-world publication authorization.
"""
import copy
import importlib.util
import json
import sys
from pathlib import Path

MAIN='d355400dabed3c280e1fce5030cab69ea099428b'
HEAD='37588aa57d2bcf188da5944e40f4c125575057cf'
ROOT='research/r16/axiom-alpha-node-c1-adaptation-20261012/'

def fixture(commits='2',files='two'):
    return {'body':(f'Research-only C1 candidate from pinned main {MAIN} to pinned head {HEAD}. '
                    f'GitHub compare: {commits} commits ahead, 0 behind; {files} added JSON files only '
                    f'under the existing {ROOT} lane. CLAIM_CEILING=C1_DESCRIPTIVE_ONLY.'),
            'base_sha':MAIN,'head_sha':HEAD,'commits':2,
            'files':[{'filename':ROOT+'one.json','status':'added'},
                     {'filename':ROOT+'two.json','status':'added'}]}

# Expected outputs are literal, never inferred from candidate behavior.
CASES=[
    ('ascii_control','CONSISTENT','2','two'),
    ('ascii_file_count','CONSISTENT','2','2'),
    ('ascii_commit_zero','DRIFT','0','two'),
    ('ascii_file_zero','DRIFT','2','zero'),
    ('arabic_indic_commits','INCOMPLETE','٢','two'),
    ('arabic_indic_files','INCOMPLETE','2','٢'),
    ('fullwidth_commits','INCOMPLETE','２','two'),
    ('fullwidth_files','INCOMPLETE','2','２'),
    ('devanagari_commits','INCOMPLETE','२','two'),
    ('devanagari_files','INCOMPLETE','2','२'),
    ('huge_commit_overflow','INCOMPLETE','9'*4301,'two'),
    ('huge_file_overflow','INCOMPLETE','2','9'*4301),
    ('fifty_digit_commit','INCOMPLETE','9'*50,'two'),
    ('fifty_digit_file','INCOMPLETE','2','9'*50),
    ('commit_over_bound','INCOMPLETE','1000000','two'),
    ('file_over_bound','INCOMPLETE','2','3001'),
    ('file_in_bound_mismatch','DRIFT','2','3000'),
    ('signed_negative_commits','INCOMPLETE','-2','two'),
    ('signed_negative_files','INCOMPLETE','2','-2'),
    ('signed_positive_commits','INCOMPLETE','+2','two'),
    ('signed_positive_files','INCOMPLETE','2','+2'),
    ('decimal_commits','INCOMPLETE','2.0','two'),
    ('decimal_files','INCOMPLETE','2','2.0'),
    ('superscript_commits','INCOMPLETE','²','two'),
    ('superscript_files','INCOMPLETE','2','²'),
]

def evaluate(path):
    spec=importlib.util.spec_from_file_location('guard_under_test',str(path))
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    rows=[]
    for name,expected,commit_claim,file_claim in CASES:
        try:
            actual=module.audit_pr_description(copy.deepcopy(fixture(commit_claim,file_claim)))['status']
        except Exception as exc:
            actual='EXCEPTION:'+type(exc).__name__
        rows.append({'name':name,'expected':expected,'actual':actual,'pass':expected==actual})
    return {'cases':len(rows),'correct':sum(r['pass'] for r in rows),'rows':rows}

if __name__=='__main__':
    out=evaluate(Path(sys.argv[1]))
    print(json.dumps(out,ensure_ascii=False,indent=2))
    sys.exit(0 if out['correct']==out['cases'] else 1)
