#!/usr/bin/env python3
"""Frozen independent evaluator: V5 must not accept unverified 'added only' claims.

The fixture oracle is based on the PR narrative semantics, not on the V6
implementation. This evaluator does not authenticate API transport or grant merge.
"""
import copy
import importlib.util
import json
import sys

BASE = 'd355400dabed3c280e1fce5030cab69ea099428b'
HEAD = '5fb35be25870e3a8785f0b41a82bcba652b43088'
LANE = 'research/r16/axiom-alpha-node-c1-adaptation-20261012/'
A = LANE + 'a.md'
B = LANE + 'b.md'
BODY = (f'Research-only C1 candidate from pinned main {BASE} to pinned head {HEAD}. '
        f'GitHub compare: 2 commits ahead; two added Markdown files only under '
        f'the existing {LANE} lane.')


def seed():
    return {'body': BODY, 'base_sha': BASE, 'head_sha': HEAD, 'commits': 2,
            'changed_files': 2, 'filenames': [A, B],
            'file_changes': [{'filename': A, 'status': 'added'},
                             {'filename': B, 'status': 'added'}],
            'file_pages_complete': True}


def fixtures():
    s = seed()
    yield 'positive_exact', s, 'MATCH'
    for status in ('modified', 'removed', 'renamed', 'copied', 'changed', 'unchanged'):
        v = copy.deepcopy(s); v['file_changes'][1]['status'] = status
        yield 'negative_status_'+status, v, 'DRIFT'
    for name, edit in [
        ('missing_changes', lambda v: v.pop('file_changes')),
        ('missing_pagination_proof', lambda v: v.pop('file_pages_complete')),
        ('pagination_false', lambda v: v.update(file_pages_complete=False)),
        ('pagination_numeric', lambda v: v.update(file_pages_complete=1)),
        ('empty_changes', lambda v: v.update(file_changes=[])),
        ('mismatched_path', lambda v: v['file_changes'][1].update(filename=LANE+'other.md')),
        ('duplicate_path', lambda v: v['file_changes'][1].update(filename=A)),
        ('unknown_status', lambda v: v['file_changes'][1].update(status='unknown')),
        ('missing_status', lambda v: v['file_changes'][1].pop('status')),
        ('wrong_type_changes', lambda v: v.update(file_changes='two files')),
        ('wrong_type_entry', lambda v: v['file_changes'].__setitem__(1, 'added')),
    ]:
        v = copy.deepcopy(s); edit(v)
        yield name, v, 'INCOMPLETE'
    v = copy.deepcopy(s); v['head_sha'] = 'a'*40
    yield 'head_drift_control', v, 'DRIFT'
    v = copy.deepcopy(s); v['body'] += f' to pinned head {HEAD}'
    yield 'repeated_head_control', v, 'INCOMPLETE'


def evaluate(path):
    spec = importlib.util.spec_from_file_location('guard_under_test', path)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    rows = []
    for name, snap, expected in fixtures():
        try:
            output = mod.check_scope(copy.deepcopy(snap))
            actual = output.get('status') if isinstance(output, dict) else 'INVALID_RESPONSE'
        except Exception as exc:
            actual = 'EXCEPTION_'+type(exc).__name__
        rows.append({'fixture': name, 'expected': expected, 'actual': actual, 'pass': actual == expected})
    return {'oracle': 'FROZEN_FILE_CHANGE_KIND_V1', 'total': len(rows),
            'passed': sum(x['pass'] for x in rows), 'rows': rows}

if __name__ == '__main__':
    result = evaluate(sys.argv[1]); print(json.dumps(result, indent=2))
    sys.exit(0 if result['passed'] == result['total'] else 1)
