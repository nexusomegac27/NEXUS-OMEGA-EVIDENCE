#!/usr/bin/env python3
"""Frozen independent C1 oracle: compare claimed PR inventory against actual API snapshot.

Frozen BEFORE implementation. Tests use predeclared expected outcomes and include
an exact observed GitHub PR #124 metadata snapshot from 2026-10-23.
"""
import copy
import importlib.util
import json
import sys
from pathlib import Path

MAIN='d355400dabed3c280e1fce5030cab69ea099428b'
HEAD='afdcdf236d1dd538aa9c91c4e48b9b24c1182327'
OLD='5fb35be25870e3a8785f0b41a82bcba652b43088'
ROOT='research/r16/axiom-alpha-node-c1-adaptation-20261012/'
BASE_BODY=(f'Research-only C1 candidate from pinned main {MAIN} to pinned head {HEAD}. '
           'GitHub compare: 2 commits ahead, 0 behind; two added Markdown files only under '
           'the existing research/r16/axiom-alpha-node-c1-adaptation-20261012/ lane. '
           'CLAIM_CEILING=C1_DESCRIPTIVE_ONLY.')
FILES=[{'filename':ROOT+'a.md','status':'added'}, {'filename':ROOT+'b.md','status':'added'}]
BASE={'body':BASE_BODY,'base_sha':MAIN,'head_sha':HEAD,'commits':2,'files':FILES}

def make_cases():
    c=[]
    def add(name,expect,mutate):
        snap=copy.deepcopy(BASE);mutate(snap);c.append({'name':name,'expected':expect,'snapshot':snap})
    add('matching_pinned_description','CONSISTENT',lambda x:None)
    add('actual_pr124_stale_head_and_inventory','DRIFT',lambda x:(x.update({'body':x['body'].replace(HEAD,OLD),'commits':31}),x['files'].extend({'filename':ROOT+f'extra_{i}.py','status':'added'} for i in range(32))))
    add('head_changed','DRIFT',lambda x:x.update(head_sha='a'*40))
    add('base_changed','DRIFT',lambda x:x.update(base_sha='b'*40))
    add('commit_count_changed','DRIFT',lambda x:x.update(commits=3))
    add('one_extra_markdown','DRIFT',lambda x:x['files'].append({'filename':ROOT+'c.md','status':'added'}))
    add('file_extension_changed','DRIFT',lambda x:x['files'][0].update(filename=ROOT+'a.py'))
    add('file_status_modified','DRIFT',lambda x:x['files'][0].update(status='modified'))
    add('path_scope_violation','DRIFT',lambda x:x['files'][0].update(filename='scripts/a.md'))
    add('duplicate_path','INCOMPLETE',lambda x:x['files'][1].update(filename=ROOT+'a.md'))
    add('missing_files','INCOMPLETE',lambda x:x.pop('files'))
    add('missing_body','INCOMPLETE',lambda x:x.pop('body'))
    add('missing_head_claim','INCOMPLETE',lambda x:x.update(body=x['body'].replace('to pinned head '+HEAD,'to latest head')))
    add('missing_file_claim','INCOMPLETE',lambda x:x.update(body=x['body'].replace('two added Markdown files only','files added')))
    add('missing_commit_claim','INCOMPLETE',lambda x:x.update(body=x['body'].replace('2 commits ahead','some commits ahead')))
    add('bad_commit_type','INCOMPLETE',lambda x:x.update(commits='2'))
    add('bad_files_type','INCOMPLETE',lambda x:x.update(files='a.md'))
    add('bad_sha','INCOMPLETE',lambda x:x.update(head_sha='badsha'))
    add('bad_filename','INCOMPLETE',lambda x:x['files'][0].update(filename='../escape.md'))
    add('no_claim_ceiling','INCOMPLETE',lambda x:x.update(body=x['body'].replace('CLAIM_CEILING=C1_DESCRIPTIVE_ONLY','')))
    return c

def baseline(snapshot):
    """Minimal metadata-only baseline, not a representation of all existing validators."""
    b=snapshot.get('body')
    return 'CONSISTENT' if isinstance(b,str) and 'C1_DESCRIPTIVE_ONLY' in b and isinstance(snapshot.get('base_sha'),str) else 'INCOMPLETE'

def evaluate(path):
    spec=importlib.util.spec_from_file_location('candidate',path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    cases=make_cases();results=[]
    for item in cases:
        try:
            out=module.audit_pr_description(copy.deepcopy(item['snapshot']))
            got=out.get('status') if isinstance(out,dict) else None
        except Exception as exc:got='EXCEPTION:'+type(exc).__name__
        base=baseline(item['snapshot'])
        results.append({'name':item['name'],'expected':item['expected'],'baseline':base,'candidate':got,
                        'baseline_pass':base==item['expected'],'candidate_pass':got==item['expected']})
    return {'total':len(results),'baseline_pass':sum(x['baseline_pass'] for x in results),
            'candidate_pass':sum(x['candidate_pass'] for x in results),'results':results}

if __name__=='__main__':
    result=evaluate(Path(sys.argv[1]))
    print(json.dumps(result,indent=2))
    sys.exit(0 if result['candidate_pass']==result['total'] else 1)
