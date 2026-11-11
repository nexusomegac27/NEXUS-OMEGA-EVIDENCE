#!/usr/bin/env python3
"""Independent held-out C1 evaluator: path-scope claim vs PR file-list.

Does not import the candidate's expectations or mutate its code. Evaluates only
whether a PR description asserting a particular research lane can be labelled
MATCH when supplied filenames escape that lane. No GitHub auth or merge proof.
"""
import copy
import importlib.util
import json
import sys

LANE = 'research/r16/axiom-alpha-node-c1-adaptation-20261012/'
MAIN = 'd355400dabed3c280e1fce5030cab69ea099428b'
HEAD = '5fb35be25870e3a8785f0b41a82bcba652b43088'
BODY = (f'Research-only, append-only C1 candidate from pinned main {MAIN} '
        f'to pinned head {HEAD}. GitHub compare: 2 commits ahead, 0 behind; '
        f'two added Markdown files only under the existing {LANE} lane.')
BASE = {'body': BODY, 'base_sha': MAIN, 'head_sha': HEAD,
        'commits': 2, 'changed_files': 2,
        'filenames': [LANE + 'a.md', LANE + 'b.md']}

CASES = [
    ('positive_exact_lane', [LANE + 'a.md', LANE + 'b.md'], True),
    ('positive_nested_in_lane', [LANE + 'notes/a.md', LANE + 'notes/b.md'], True),
    ('negative_github_workflow', [LANE + 'a.md', '.github/workflows/disable.md'], False),
    ('negative_governance', [LANE + 'a.md', 'docs/governance/policy.md'], False),
    ('negative_other_research_phase', [LANE + 'a.md', 'research/r17/other.md'], False),
    ('negative_prefix_confusion', [LANE + 'a.md', LANE[:-1] + '-evil/b.md'], False),
    ('negative_parent_traversal', [LANE + 'a.md', LANE + '../other.md'], False),
    ('negative_absolute_path', [LANE + 'a.md', '/absolute.md'], False),
    ('negative_duplicate_path', [LANE + 'a.md', LANE + 'a.md'], False),
    ('negative_windows_path', [LANE + 'a.md', 'research\\r16\\other.md'], False),
]

def run(path):
    spec = importlib.util.spec_from_file_location('isolated_candidate', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rows=[]
    for name,paths,should_match in CASES:
        fixture=copy.deepcopy(BASE)
        fixture['filenames']=paths
        try:
            got=module.check_scope(fixture)
            status=got.get('status') if isinstance(got,dict) else 'INVALID_RESULT'
        except Exception as e:
            status='EXCEPTION_'+type(e).__name__
        passed=(status=='MATCH') if should_match else (status in ('DRIFT','INCOMPLETE'))
        rows.append({'fixture':name,'positive':should_match,'status':status,'pass':passed})
    return {'total':len(rows),'passed':sum(r['pass'] for r in rows),
            'positive':sum(r['positive'] for r in rows),
            'negative':sum(not r['positive'] for r in rows),
            'negative_detected':sum(r['pass'] for r in rows if not r['positive']),
            'rows':rows,'oracle':'INDEPENDENT_PATH_SCOPE_REQUIREMENT_NOT_CANDIDATE_CONTROLLED'}

if __name__=='__main__':
    result=run(sys.argv[1])
    print(json.dumps(result,indent=2))
    sys.exit(0 if result['passed']==result['total'] else 1)
