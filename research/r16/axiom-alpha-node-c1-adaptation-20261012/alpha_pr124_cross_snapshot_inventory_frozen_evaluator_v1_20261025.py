#!/usr/bin/env python3
"""Frozen, independently specified black-box oracle for Run142.
Only synthetic fixtures; no authentication, production release or merge authority.
Usage: python alpha_pr124_cross_snapshot_inventory_frozen_evaluator_v1_20261025.py CANDIDATE.py
"""
import copy
import importlib.util
import json
import sys

SHA = 'a' * 64
BLOB = 'b' * 40
ROOT = 'research/r16/axiom-alpha-node-c1-adaptation-20261012/'

def row(s):
    return {'path': ROOT + s + '.py', 'bytes': 10, 'sha256': SHA, 'git_blob_sha1': BLOB}

def base():
    groups = [{'name': 'historical', 'files': [row('one'), row('two')]},
              {'name': 'delta', 'files': [row('three')]},
              {'name': 'current_additions', 'files': [row('four')]}]
    return groups, [r['path'] for g in groups for r in g['files']]

def case(fn):
    groups, current = base()
    fn(groups, current)
    return groups, current

# Expected statuses fixed before candidate publication; no candidate-derived oracle.
CASES = [
 ('valid_complete', 'COMPLETE_C1', lambda g,p: None),
 ('valid_permuted_current', 'COMPLETE_C1', lambda g,p: p.reverse()),
 ('valid_empty_delta_group', 'COMPLETE_C1', lambda g,p: (p.remove(g[1]['files'][0]['path']),g[1]['files'].clear())),
 ('overlap_historical_delta', 'FAIL_CLOSED', lambda g,p: (g[1]['files'].__setitem__(0,copy.deepcopy(g[0]['files'][0])),p.remove(ROOT+'three.py'))),
 ('overlap_delta_new', 'FAIL_CLOSED', lambda g,p: (g[2]['files'].__setitem__(0,copy.deepcopy(g[1]['files'][0])),p.remove(ROOT+'four.py'))),
 ('duplicate_within_group', 'FAIL_CLOSED', lambda g,p: (g[0]['files'].__setitem__(1,copy.deepcopy(g[0]['files'][0])),p.remove(ROOT+'two.py'))),
 ('duplicate_current_path', 'FAIL_CLOSED', lambda g,p: p.__setitem__(1,p[0])),
 ('missing_current_path', 'FAIL_CLOSED', lambda g,p: p.pop()),
 ('unexpected_current_path', 'FAIL_CLOSED', lambda g,p: p.append(ROOT+'ghost.py')),
 ('duplicate_group_name', 'FAIL_CLOSED', lambda g,p: g[1].update(name='historical')),
 ('bad_hash', 'FAIL_CLOSED', lambda g,p: g[1]['files'][0].update(sha256='abc')),
 ('bool_bytes', 'FAIL_CLOSED', lambda g,p: g[0]['files'][0].update(bytes=True)),
 ('path_traversal', 'FAIL_CLOSED', lambda g,p: (p.__setitem__(0,ROOT+'../escape.py'),g[0]['files'][0].update(path=ROOT+'../escape.py'))),
 ('missing_blob', 'FAIL_CLOSED', lambda g,p: g[0]['files'][0].pop('git_blob_sha1')),
 ('bad_groups_container', 'FAIL_CLOSED', lambda g,p: g.clear()),
]

def run(path):
    spec=importlib.util.spec_from_file_location('candidate_under_test',path)
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    results=[]
    for name, expected, mutate in CASES:
        groups, current=case(mutate)
        try:
            outcome=mod.audit_inventory(groups,current)
        except BaseException as exc:
            results.append({'case':name,'expected':expected,'actual':'UNCAUGHT_'+type(exc).__name__,'pass':False})
            continue
        status=outcome.get('status') if isinstance(outcome,dict) else 'MALFORMED_RETURN'
        safe=(isinstance(outcome,dict) and outcome.get('source_authentication')=='NOT_ESTABLISHED'
              and outcome.get('project_automation_rate')=='NOT_COMPUTABLE')
        counts=(status!='COMPLETE_C1' or (outcome.get('historical_count')==len(groups[0]['files'])
                and outcome.get('current_count')==len(current)))
        results.append({'case':name,'expected':expected,'actual':status,'pass':status==expected and safe and counts})
    summary={'pass':sum(x['pass'] for x in results),'total':len(results),'results':results,
             'oracle':'FROZEN_BEFORE_CANDIDATE_COMMIT','claim_ceiling':'C1_DESCRIPTIVE_ONLY'}
    print(json.dumps(summary,indent=2))
    return 0 if summary['pass']==summary['total'] else 1

if __name__=='__main__':
    if len(sys.argv)!=2:
        raise SystemExit('Usage: evaluator.py candidate.py')
    raise SystemExit(run(sys.argv[1]))
