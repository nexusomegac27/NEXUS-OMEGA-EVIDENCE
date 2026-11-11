#!/usr/bin/env python3
"""Independent, predeclared oracle for the PR-description JSON-kind bug.

This file is frozen before the V2 candidate is created. Expected statuses are
explicit; the evaluator does not derive its oracle from candidate output.
This is a local deterministic test, NOT external scientific adjudication.
"""
import copy
import importlib.util
import json
import sys
from pathlib import Path

MAIN = 'd355400dabed3c280e1fce5030cab69ea099428b'
HEAD = '37588aa57d2bcf188da5944e40f4c125575057cf'
ROOT = 'research/r16/axiom-alpha-node-c1-adaptation-20261012/'


def fixture(kind='JSON', extension='.json', count='two'):
    body = (f'Research-only C1 candidate from pinned main {MAIN} to pinned head {HEAD}. '
            f'GitHub compare: 2 commits ahead, 0 behind; {count} added {kind} files only '
            f'under the existing {ROOT} lane. CLAIM_CEILING=C1_DESCRIPTIVE_ONLY.')
    return {'body': body, 'base_sha': MAIN, 'head_sha': HEAD, 'commits': 2,
            'files': [{'filename': ROOT+'one'+extension, 'status':'added'},
                      {'filename': ROOT+'two'+extension, 'status':'added'}]}


def make_cases():
    cases=[]
    def add(name, expected, edit=None, **kwargs):
        obj=fixture(**kwargs)
        if edit:edit(obj)
        cases.append({'name':name,'expected':expected,'snapshot':obj})
    add('json_exact_upper','CONSISTENT')
    add('json_lower','CONSISTENT',kind='json')
    add('json_title','CONSISTENT',kind='Json')
    add('json_mixed','CONSISTENT',kind='jSoN')
    add('json_numeric_count','CONSISTENT',count='2')
    add('json_zero_file_claim','DRIFT',count='zero')
    add('json_three_file_claim','DRIFT',count='three')
    add('json_wrong_extension','DRIFT',lambda x:x['files'][0].update(filename=ROOT+'one.py'))
    add('json_modified_status','DRIFT',lambda x:x['files'][0].update(status='modified'))
    add('json_outside_scope','DRIFT',lambda x:x['files'][0].update(filename='scripts/one.json'))
    add('json_stale_head','DRIFT',lambda x:x.update(head_sha='a'*40))
    add('json_stale_base','DRIFT',lambda x:x.update(base_sha='b'*40))
    add('json_stale_commit_count','DRIFT',lambda x:x.update(commits=3))
    add('json_duplicate_file','INCOMPLETE',lambda x:x['files'][1].update(filename=ROOT+'one.json'))
    add('json_missing_files','INCOMPLETE',lambda x:x.pop('files'))
    add('json_missing_claim','INCOMPLETE',lambda x:x.update(body=x['body'].replace('two added JSON files only','files')))
    add('json_bad_status','INCOMPLETE',lambda x:x['files'][0].update(status='copied'))
    add('json_bad_type','INCOMPLETE',lambda x:x.update(commits='2'))
    add('markdown_control','CONSISTENT',kind='Markdown',extension='.md')
    add('python_control','CONSISTENT',kind='Python',extension='.py')
    add('markdown_wrong_extension','DRIFT',lambda x:x['files'][0].update(filename=ROOT+'one.json'),kind='Markdown',extension='.md')
    add('python_modified','DRIFT',lambda x:x['files'][0].update(status='modified'),kind='Python',extension='.py')
    return cases


def evaluate(path):
    spec=importlib.util.spec_from_file_location('candidate',str(path))
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    results=[]
    for case in make_cases():
        try:
            result=module.audit_pr_description(copy.deepcopy(case['snapshot']))
            actual=result['status']
        except Exception as exc:
            actual='EXCEPTION:'+type(exc).__name__
        results.append({'name':case['name'],'expected':case['expected'],
                        'actual':actual,'pass':actual==case['expected']})
    return {'cases':len(results),'correct':sum(x['pass'] for x in results),'results':results}

if __name__=='__main__':
    report=evaluate(Path(sys.argv[1]))
    print(json.dumps(report,indent=2))
    sys.exit(0 if report['correct']==report['cases'] else 1)
