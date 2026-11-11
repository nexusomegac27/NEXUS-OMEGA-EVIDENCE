#!/usr/bin/env python3
"""Frozen C1 adversarial oracle for two-read GitHub PR metadata consistency.
Independent test expectations specified before candidate implementation.
Synthetic fixtures only; caller must authenticate the API retrieval separately.
"""
import copy
import importlib.util
import json
import sys
from pathlib import Path

REPO='nexusomegac27/NEXUS-OMEGA-EVIDENCE'
BASE='d355400dabed3c280e1fce5030cab69ea099428b'
HEAD='eb2eee35038443e518a1dfad15b3793eb997ede1'
HEAD2='a'*40
FILES=['research/r16/axiom-alpha-node-c1-adaptation-20261012/a.py','research/r16/axiom-alpha-node-c1-adaptation-20261012/b.py']

def valid():
    m={'repository':REPO,'number':124,'base_sha':BASE,'head_sha':HEAD,'changed_files':2}
    return {'before':copy.deepcopy(m),'after':copy.deepcopy(m),'filenames':list(FILES),
            'expected_repo':REPO,'expected_pr':124,'expected_base':BASE,'expected_head':HEAD}

CASES=[]
def case(name,change,expected):
    v=valid();change(v);CASES.append((name,v,expected))

case('stable',lambda x:None,'STABLE_COUNT_MATCH')
case('head_changed_between_reads',lambda x:x['after'].__setitem__('head_sha',HEAD2),'INCOMPLETE')
case('head_mismatch_with_pinned_commit',lambda x:x.__setitem__('expected_head',HEAD2),'INCOMPLETE')
case('base_changed_between_reads',lambda x:x['after'].__setitem__('base_sha',HEAD2),'INCOMPLETE')
case('file_count_changed_between_reads',lambda x:x['after'].__setitem__('changed_files',3),'INCOMPLETE')
case('partial_inventory',lambda x:x['filenames'].pop(),'INCOMPLETE')
case('duplicate_filenames',lambda x:x['filenames'].__setitem__(1,x['filenames'][0]),'INCOMPLETE')
case('path_traversal',lambda x:x['filenames'].__setitem__(1,'research/r16/../x.py'),'INCOMPLETE')
case('boolean_count',lambda x:x['before'].__setitem__('changed_files',True),'INCOMPLETE')
case('repo_changed_between_reads',lambda x:x['after'].__setitem__('repository','attacker/repo'),'INCOMPLETE')
case('pr_number_changed_between_reads',lambda x:x['after'].__setitem__('number',125),'INCOMPLETE')
case('missing_second_read',lambda x:x.__setitem__('after',None),'INCOMPLETE')
case('empty_valid_inventory',lambda x:(x['before'].__setitem__('changed_files',0),x['after'].__setitem__('changed_files',0),x.__setitem__('filenames',[])),'STABLE_COUNT_MATCH')

def baseline(v):
    try:return 'STABLE_COUNT_MATCH' if len(v['filenames'])==v['before']['changed_files'] else 'INCOMPLETE'
    except Exception:return 'INCOMPLETE'

def evaluate(path):
    spec=importlib.util.spec_from_file_location('candidate',str(path));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    results=[]
    for name,snapshot,expected in CASES:
        b=baseline(snapshot)
        try:
            observed=m.check(snapshot)['status']
        except Exception as exc:
            observed='EXCEPTION:'+type(exc).__name__
        results.append({'fixture':name,'expected':expected,'baseline':b,'candidate':observed,'candidate_pass':observed==expected,'baseline_pass':b==expected})
    return {'cases':len(results),'baseline_correct':sum(x['baseline_pass'] for x in results),'candidate_correct':sum(x['candidate_pass'] for x in results),'results':results}

if __name__=='__main__':
    report=evaluate(Path(sys.argv[1]));print(json.dumps(report,indent=2));sys.exit(0 if report['candidate_correct']==report['cases'] else 1)
