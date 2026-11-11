#!/usr/bin/env python3
"""Frozen, separate black-box evaluator for PR-scope metadata guard V2.

Derived from historical V1 frozen test set, plus four independent malformed
API-type negative fixtures. Does not import or modify the candidate oracle.
This synthetic evaluation cannot authenticate GitHub, establish rights or merge.
"""
import copy
import importlib.util
import json
import sys

MAIN = 'd355400dabed3c280e1fce5030cab69ea099428b'
HEAD = '5fb35be25870e3a8785f0b41a82bcba652b43088'
BODY = (f'Research-only, append-only C1 candidate from pinned main {MAIN} '
        f'to pinned head {HEAD}. GitHub compare: 2 commits ahead, 0 behind; '
        'two added Markdown files only under the existing research lane.')
GOOD = dict(body=BODY, base_sha=MAIN, head_sha=HEAD, commits=2,
            changed_files=2, filenames=['research/r16/a.md', 'research/r16/b.md'])

cases=[]
def add(name, mutate, expected):
    snapshot=copy.deepcopy(GOOD)
    mutate(snapshot)
    cases.append((name,snapshot,expected))

add('valid_exact', lambda s: None, 'MATCH')
add('valid_same_after_metadata_only', lambda s: s.update(extra_metadata='ignored'), 'MATCH')
add('head_drift', lambda s: s.update(head_sha='9'*40), 'DRIFT')
add('commit_drift', lambda s: s.update(commits=9), 'DRIFT')
add('file_count_drift', lambda s: s.update(changed_files=12,filenames=['a.md']*12), 'DRIFT')
add('file_type_drift', lambda s: s.update(filenames=['a.md','b.py']), 'DRIFT')
add('base_drift', lambda s: s.update(base_sha='8'*40), 'DRIFT')
add('missing_body', lambda s: s.update(body=''), 'INCOMPLETE')
add('unparseable_body', lambda s: s.update(body='Two files. All fine.'), 'INCOMPLETE')
add('api_inconsistent_file_list', lambda s: s.update(filenames=['a.md']), 'INCOMPLETE')
add('malformed_head', lambda s: s.update(head_sha='not-a-sha'), 'INCOMPLETE')
add('wrong_commit_type', lambda s: s.update(commits='2'), 'INCOMPLETE')
# New held-out adversarial inputs: these caused unhandled TypeError in V1.
add('numeric_base_sha', lambda s: s.update(base_sha=5), 'INCOMPLETE')
add('numeric_head_sha', lambda s: s.update(head_sha=5), 'INCOMPLETE')
add('array_base_sha', lambda s: s.update(base_sha=['0'*40]), 'INCOMPLETE')
add('object_head_sha', lambda s: s.update(head_sha={'sha':'0'*40}), 'INCOMPLETE')

def evaluate(module_path):
    spec=importlib.util.spec_from_file_location('candidate_guard',module_path)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rows=[]
    for name,snapshot,expected in cases:
        try:
            result=module.check_scope(snapshot)
            observed=result.get('status') if isinstance(result,dict) else 'INVALID_RESULT'
        except Exception as exc:
            observed='EXCEPTION_'+type(exc).__name__
        rows.append(dict(name=name,expected=expected,observed=observed,pass_test=(observed==expected)))
    return dict(tests=len(rows),passed=sum(r['pass_test'] for r in rows),
                negative_tests=14,negative_rejected=sum(r['pass_test'] for r in rows[2:]),
                results=rows,oracle='FROZEN_SEPARATE_V2_SYNTHETIC_NOT_THIRD_PARTY')

if __name__=='__main__':
    result=evaluate(sys.argv[1])
    print(json.dumps(result,indent=2))
    sys.exit(0 if result['passed']==result['tests'] else 1)
