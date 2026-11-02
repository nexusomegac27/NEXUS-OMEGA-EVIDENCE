"""Frozen, independent C1 oracle for first-boundary anchor; commit BEFORE candidate.

Does not authenticate provider, source file bytes, receipts or real Git history.
Expected outcomes are fixed here; candidate must not edit this file.
"""
import copy
import importlib
import json
import sys
import frozen_alpha_publication_cohort_evaluator_v1_20261102 as baseline

FIRST_PARENT = '964fe47c4bdbad599e0689b132ff73c0822f3518'
FIRST_MERGE = '3cc35487e8cae54aeac95377b6a8c376f412dc4f'


def positive():
    d = baseline.fixture()
    d['prs'][0]['parent_commit'] = FIRST_PARENT
    d['prs'][0]['merge_commit'] = FIRST_MERGE
    d['prs'][1]['parent_commit'] = FIRST_MERGE
    return d


def mutate(name, d):
    p = d['prs']
    if name == 'positive': pass
    elif name == 'forged_first_parent': p[0]['parent_commit'] = '0'*40
    elif name == 'forged_first_merge': p[0]['merge_commit'] = '0'*40; p[1]['parent_commit'] = '0'*40
    elif name == 'forged_middle_chain': p[4]['merge_commit'] = 'e'*40; p[5]['parent_commit'] = 'e'*40
    elif name == 'missing_pr': p.pop()
    elif name == 'duplicate_receipt': p[1]['receipt_id'] = p[0]['receipt_id']
    elif name == 'missing_file': p[0]['files'].pop()
    elif name == 'claim_promotion': d['claim_ceiling'] = 'C2'
    elif name == 'blob_mismatch': p[0]['files'][0]['github_blob_sha1'] = 'c'*40
    elif name == 'last_main_swap': p[-1]['merge_commit'] = '0'*40
    else: raise AssertionError(name)
    return d

# Expected baseline/candidate results fixed before candidate exists.
EXPECTED = [
    ('positive', True, True),
    ('forged_first_parent', True, False),
    ('forged_first_merge', True, False),
    ('forged_middle_chain', True, True),  # known residual falsifier
    ('missing_pr', False, False),
    ('duplicate_receipt', False, False),
    ('missing_file', False, False),
    ('claim_promotion', False, False),
    ('blob_mismatch', False, False),
    ('last_main_swap', False, False),
]

def run(mode):
    if mode == 'baseline': checker = baseline
    elif mode == 'candidate': checker = importlib.import_module('alpha_publication_cohort_boundary_anchor_guard_v2_20261102')
    else: raise ValueError(mode)
    passed = 0
    for name, old_expected, new_expected in EXPECTED:
        d = mutate(name, positive())
        observed, reason = checker.evaluate(copy.deepcopy(d))
        expected = old_expected if mode == 'baseline' else new_expected
        ok = observed is expected
        passed += ok
        print(json.dumps({'fixture':name,'expected':expected,'observed':observed,'reason':reason,'pass':ok},sort_keys=True))
    print(json.dumps({'mode':mode,'passed':passed,'total':len(EXPECTED),'result':'PASS' if passed==len(EXPECTED) else 'FAIL'},sort_keys=True))
    return 0 if passed==len(EXPECTED) else 1

if __name__ == '__main__':
    if len(sys.argv)!=2 or sys.argv[1] not in ('baseline','candidate'):
        sys.exit('USAGE: frozen...py baseline|candidate')
    sys.exit(run(sys.argv[1]))
