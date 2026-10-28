#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Isolated C1 check: historical PR merge remains ancestor of later main.

Inputs are caller-supplied GitHub REST-shaped projections. This code does not
fetch or authenticate GitHub, attest scientific validity, or infer project rates.
"""
import json
import re
import sys

OBJECT = 'NEXUS_OMEGA_ALPHA_ISSUE93_HISTORICAL_LINEAGE_V2'
REPO = 'nexusomegac27/NEXUS-OMEGA-EVIDENCE'
SHA40 = re.compile(r'[0-9a-f]{40}\Z')
MAX_BYTES = 32768


def fail(code):
    raise ValueError(code)


def unique(pairs):
    obj = {}
    for key, val in pairs:
        if key in obj:
            fail('DUPLICATE_JSON_KEY')
        obj[key] = val
    return obj


def sha(x):
    return type(x) is str and SHA40.fullmatch(x) is not None


def audit(obj):
    if type(obj) is not dict or set(obj) != {'object', 'repository', 'receipt', 'main', 'compare'}:
        fail('INVALID_ENVELOPE')
    if obj['object'] != OBJECT or obj['repository'] != REPO:
        fail('INVALID_SCOPE')
    receipt, main, cmp = obj['receipt'], obj['main'], obj['compare']
    if (type(receipt) is not dict or set(receipt) != {'id', 'pr', 'merge_commit_sha'}
            or type(receipt['id']) is not int or receipt['id'] <= 0
            or type(receipt['pr']) is not int or receipt['pr'] <= 0
            or not sha(receipt['merge_commit_sha'])):
        fail('INVALID_RECEIPT')
    if type(main) is not dict or set(main) != {'sha'} or not sha(main['sha']):
        fail('INVALID_MAIN')
    expected = {'base', 'head', 'status', 'ahead_by', 'behind_by',
                'total_commits', 'base_commit', 'merge_base_commit'}
    if type(cmp) is not dict or set(cmp) != expected:
        fail('INVALID_COMPARE')
    for k in ('base_commit', 'merge_base_commit'):
        if type(cmp[k]) is not dict or set(cmp[k]) != {'sha'} or not sha(cmp[k]['sha']):
            fail('INVALID_COMPARE')
    for k in ('base', 'head'):
        if not sha(cmp[k]):
            fail('INVALID_COMPARE')
    for k in ('ahead_by', 'behind_by', 'total_commits'):
        if type(cmp[k]) is not int or cmp[k] < 0:
            fail('INVALID_COMPARE_COUNT')
    merge = receipt['merge_commit_sha']
    if (cmp['base'] != merge or cmp['base_commit']['sha'] != merge
            or cmp['merge_base_commit']['sha'] != merge or cmp['head'] != main['sha']):
        fail('LINEAGE_SHA_MISMATCH')
    if cmp['behind_by'] != 0 or cmp['ahead_by'] != cmp['total_commits']:
        fail('LINEAGE_COUNT_MISMATCH')
    status = cmp['status']
    if not ((status == 'identical' and cmp['ahead_by'] == 0 and merge == main['sha'])
            or (status == 'ahead' and cmp['ahead_by'] > 0 and merge != main['sha'])):
        fail('LINEAGE_STATUS_MISMATCH')
    return {'state': 'C1_CALLER_SUPPLIED_COMPARE_CONSISTENT',
            'historical_main_readback': 'ANCESTOR_CONFIRMED_IN_SUPPLIED_COMPARE',
            'receipt_id': receipt['id'], 'pr': receipt['pr'],
            'merge_commit_sha': merge, 'observed_main_sha': main['sha'],
            'commits_after_merge': cmp['ahead_by'],
            'api_origin_authenticated': False,
            'original_bytes_verified': False,
            'project_automation_rate': 'NOT_COMPUTABLE',
            'project_readback_rate': 'NOT_COMPUTABLE',
            'claim_ceiling': 'C1_DESCRIPTIVE_ONLY'}


def main():
    try:
        raw = sys.stdin.buffer.read(MAX_BYTES + 1)
        if len(raw) > MAX_BYTES:
            fail('INPUT_TOO_LARGE')
        obj = json.loads(raw.decode('utf-8'), object_pairs_hook=unique,
                         parse_constant=lambda _: fail('NONFINITE_JSON'))
        print(json.dumps(audit(obj), sort_keys=True, separators=(',', ':')))
        return 0
    except (ValueError, TypeError, UnicodeError, RecursionError, KeyError) as e:
        print('FAIL_CLOSED: ' + str(e), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
