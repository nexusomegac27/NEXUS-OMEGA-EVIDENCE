#!/usr/bin/env python3
"""Frozen, research-only C1 oracle for a fixed 10-receipt GitHub snapshot.

No network, no GitHub authentication, no import from the candidate dataset.
The independently collected PR/compare pins below must be frozen before
publishing the candidate JSON. This script does not certify source origin.
"""
import copy
import json
import re
import sys
from pathlib import Path

REPO = 'nexusomegac27/NEXUS-OMEGA-EVIDENCE'
MAIN_AT_CUTOFF = '1d31c841cbd4c25cbe5550177a17cc5638f57667'
# (PR, Issue #93 receipt ID, immutable base, observed PR merge commit, added files)
EXPECTED = [
    (212,6517745738,'06eee8d929c3bf6877cd01767aeea82e3f9e01bf','eab11408bf56d3ce1e848fe391e2fe185f7237e0',4),
    (213,6518388427,'eab11408bf56d3ce1e848fe391e2fe185f7237e0','a5aa9c289d93ba3931dea3947e7b0037a47f030d',3),
    (214,6519349549,'a5aa9c289d93ba3931dea3947e7b0037a47f030d','a04d9874f19a04101d8e106809c6b0f6d58feb0b',3),
    (215,6520594552,'a04d9874f19a04101d8e106809c6b0f6d58feb0b','5e044225bece1cc0d9ce1944ce77043bf4d4bcf2',3),
    (216,6522407193,'5e044225bece1cc0d9ce1944ce77043bf4d4bcf2','dab73d377c66fc146c7c647d3873988db181b8bb',3),
    (217,6523624851,'dab73d377c66fc146c7c647d3873988db181b8bb','70bf5b69f16e548f2f3d671995e0db08c8eeecd9',4),
    (218,6523871576,'70bf5b69f16e548f2f3d671995e0db08c8eeecd9','d9de0f0f2f28f184559e9b44e0c96c2bf873cf93',4),
    (219,6525110654,'d9de0f0f2f28f184559e9b44e0c96c2bf873cf93','8ceb184409c15c95ecdcf314e6209fb41bfed9bf',4),
    (220,6526826821,'8ceb184409c15c95ecdcf314e6209fb41bfed9bf','e726697213b2d637d42f2929c98a8c0f5f63a477',3),
    (221,6527434004,'e726697213b2d637d42f2929c98a8c0f5f63a477','1d31c841cbd4c25cbe5550177a17cc5638f57667',3),
]
ROOT_KEYS = {'schema_version','repository','pinned_main_at_cutoff','claim_ceiling','population','rows','limitations'}
ROW_KEYS = {'pr','receipt_id','receipt_actor','receipt_claimed_predecessor','receipt_claimed_main','pr_api_merged','pr_api_merge_sha','compare_api_ahead','compare_api_behind','compare_api_added','compare_api_nonadded'}

def no_duplicates(pairs):
    obj = {}
    for k, v in pairs:
        if k in obj:
            raise ValueError('duplicate JSON key')
        obj[k] = v
    return obj

def validate(d):
    if type(d) is not dict or set(d) != ROOT_KEYS:
        raise ValueError('root fields')
    if d['schema_version'] != 'alpha_issue93_pr_receipt_chain_v1' or d['repository'] != REPO:
        raise ValueError('source scope')
    if d['pinned_main_at_cutoff'] != MAIN_AT_CUTOFF or d['claim_ceiling'] != 'C1_DESCRIPTIVE_ONLY':
        raise ValueError('baseline or ceiling')
    if d['population'] != 'LAST_10_OWNER_RECEIPTS_PR212_TO_PR221_FIXED_CUTOFF':
        raise ValueError('population')
    if d['limitations'] != 'API_METADATA_CONSISTENCY_ONLY_NOT_SOURCE_AUTHENTICATION_NOT_PROJECT_DENOMINATOR':
        raise ValueError('claim inflation')
    if type(d['rows']) is not list or len(d['rows']) != len(EXPECTED):
        raise ValueError('row count')
    for row, (pr, receipt, base, main, files) in zip(d['rows'], EXPECTED):
        if type(row) is not dict or set(row) != ROW_KEYS:
            raise ValueError('row fields')
        if type(row['pr']) is not int or row['pr'] != pr or type(row['receipt_id']) is not int or row['receipt_id'] != receipt:
            raise ValueError('row identity/order')
        if row['receipt_actor'] != 'nexusomegac27':
            raise ValueError('actor')
        if row['receipt_claimed_predecessor'] != base or row['receipt_claimed_main'] != main:
            raise ValueError('receipt claims mismatch')
        if row['pr_api_merged'] is not True or row['pr_api_merge_sha'] != main:
            raise ValueError('PR merge not independently matched')
        if type(row['compare_api_ahead']) is not int or row['compare_api_ahead'] != 1:
            raise ValueError('ahead')
        if type(row['compare_api_behind']) is not int or row['compare_api_behind'] != 0:
            raise ValueError('behind')
        if type(row['compare_api_added']) is not int or row['compare_api_added'] != files:
            raise ValueError('added file count')
        if type(row['compare_api_nonadded']) is not int or row['compare_api_nonadded'] != 0:
            raise ValueError('nonadditive mutation')
    return True

def must_reject(label, obj):
    try:
        validate(obj)
    except (ValueError, TypeError, KeyError):
        return
    raise AssertionError('FAILED NEGATIVE: ' + label)

def main():
    raw = Path(sys.argv[1]).read_text(encoding='utf-8')
    d = json.loads(raw, object_pairs_hook=no_duplicates, parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))
    validate(d)
    tests = 1
    cases = []
    def mutate(label, fn):
        nonlocal tests
        v = copy.deepcopy(d)
        fn(v)
        must_reject(label, v)
        tests += 1
        cases.append(label)
    mutate('wrong repo', lambda x: x.update(repository='attacker/fork'))
    mutate('wrong main cutoff', lambda x: x.update(pinned_main_at_cutoff='0'*40))
    mutate('claim promotion', lambda x: x.update(claim_ceiling='C2'))
    mutate('fabricated population', lambda x: x.update(population='COMPLETE_PROJECT'))
    mutate('false source authentication', lambda x: x.update(limitations='AUTHENTICATED'))
    mutate('drop failed receipt', lambda x: x['rows'].pop(4))
    mutate('duplicate receipt', lambda x: x['rows'].__setitem__(3,copy.deepcopy(x['rows'][2])))
    mutate('reorder receipts', lambda x: x['rows'].reverse())
    mutate('forged receipt actor', lambda x: x['rows'][0].update(receipt_actor='expert-bot'))
    mutate('forged predecessor', lambda x: x['rows'][5].update(receipt_claimed_predecessor='f'*40))
    mutate('forged receipt main', lambda x: x['rows'][6].update(receipt_claimed_main='f'*40))
    mutate('forged PR API merge SHA', lambda x: x['rows'][7].update(pr_api_merge_sha='f'*40))
    mutate('unmerged PR', lambda x: x['rows'][8].update(pr_api_merged=False))
    mutate('hidden nonadditive file', lambda x: x['rows'][9].update(compare_api_nonadded=1))
    mutate('boolean compare count', lambda x: x['rows'][0].update(compare_api_ahead=True))
    try:
        json.loads('{"x":1,"x":2}', object_pairs_hook=no_duplicates)
        raise AssertionError('duplicate JSON key accepted')
    except ValueError:
        tests += 1
    try:
        json.loads('{"x":NaN}', parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))
        raise AssertionError('nonfinite JSON accepted')
    except ValueError:
        tests += 1
    print(f'{tests}/{tests} PASS; 10/10 fixed real API/receipt rows; {tests-1} negative/parse controls rejected')
if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit('usage: oracle.py candidate.json')
    main()
