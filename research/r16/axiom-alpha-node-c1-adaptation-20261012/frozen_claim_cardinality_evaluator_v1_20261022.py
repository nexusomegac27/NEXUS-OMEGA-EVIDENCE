#!/usr/bin/env python3
"""Independent C1 PR-scope cardinality test, frozen before V5 implementation.

An API/narrative match must never be issued when a narrative repeats any
of the four machine-consumed scope assertions, even with identical values.
The evaluator is not part of the candidate implementation and does not grant
publication, merge, or scientific authority.
"""
import copy
import importlib.util
import json
import sys

BASE = 'd355400dabed3c280e1fce5030cab69ea099428b'
HEAD = '5fb35be25870e3a8785f0b41a82bcba652b43088'
LANE = 'research/r16/axiom-alpha-node-c1-adaptation-20261012/'
ORIGINAL = (f'Research-only C1 candidate from pinned main {BASE} to pinned head {HEAD}. '
            f'GitHub compare: 2 commits ahead; two added Markdown files only under '
            f'the existing {LANE} lane.')

CASES = [
    ('valid_original', ORIGINAL, 'MATCH'),
    ('valid_extra_prose', ORIGINAL + ' Source-bound only; no promotion.', 'MATCH'),
    ('valid_unicode_path_prose', ORIGINAL + ' Café is merely a label.', 'MATCH'),
    ('duplicate_base_same', ORIGINAL + f' from pinned main {BASE}', 'INCOMPLETE'),
    ('duplicate_base_conflict', ORIGINAL + f' from pinned main {"a" * 40}', 'INCOMPLETE'),
    ('duplicate_head_same', ORIGINAL + f' to pinned head {HEAD}', 'INCOMPLETE'),
    ('duplicate_head_conflict', ORIGINAL + f' to pinned head {"b" * 40}', 'INCOMPLETE'),
    ('duplicate_commits_same', ORIGINAL + ' 2 commits ahead', 'INCOMPLETE'),
    ('duplicate_commits_conflict', ORIGINAL + ' 200 commits ahead', 'INCOMPLETE'),
    ('duplicate_files_same', ORIGINAL + ' two added Markdown files only', 'INCOMPLETE'),
    ('duplicate_files_conflict', ORIGINAL + ' 500 added Markdown files only', 'INCOMPLETE'),
    ('missing_head', ORIGINAL.replace(f'to pinned head {HEAD}', 'to a tentative head'), 'INCOMPLETE'),
    ('mismatched_head', ORIGINAL.replace(f'to pinned head {HEAD}', f'to pinned head {"f" * 40}'), 'DRIFT'),
]

def evaluate(path):
    spec = importlib.util.spec_from_file_location('candidate_under_test', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rows = []
    for name, body, expected in CASES:
        snap = {'body': body, 'base_sha': BASE, 'head_sha': HEAD,
                'commits': 2, 'changed_files': 2,
                'filenames': [LANE + 'a.md', LANE + 'b.md']}
        try:
            response = module.check_scope(copy.deepcopy(snap))
            actual = response.get('status') if isinstance(response, dict) else 'INVALID_RESPONSE'
        except Exception as e:
            actual = 'EXCEPTION_' + type(e).__name__
        rows.append({'case': name, 'expected': expected, 'actual': actual,
                     'passed': actual == expected})
    return {'total': len(rows), 'passed': sum(r['passed'] for r in rows),
            'duplicate_total': 8,
            'duplicate_rejected': sum(r['passed'] for r in rows if r['case'].startswith('duplicate_')),
            'rows': rows,
            'oracle': 'INDEPENDENT_CARDINALITY_REQUIREMENT_FROZEN_BEFORE_V5'}

if __name__ == '__main__':
    result = evaluate(sys.argv[1]); print(json.dumps(result, indent=2, ensure_ascii=True))
    sys.exit(0 if result['passed'] == result['total'] else 1)
