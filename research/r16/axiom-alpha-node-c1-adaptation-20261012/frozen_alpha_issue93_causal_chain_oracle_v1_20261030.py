#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Offline, fail-closed comparison of an API-derived PR/receipt chain.

This validates internal consistency of caller-supplied snapshots only.
It does NOT authenticate GitHub, verify original comment bytes, or prove completeness.
"""
import copy
import json
import re
import sys

OBJ = 'NEXUS_OMEGA_ALPHA_ISSUE93_CAUSAL_CHAIN_CENSUS_V1'
HEX40 = re.compile(r'[0-9a-f]{40}\Z')

class Fail(Exception):
    pass

def unique_pairs(pairs):
    result = {}
    for k, v in pairs:
        if k in result:
            raise Fail('DUPLICATE_JSON_KEY')
        result[k] = v
    return result

def check(doc):
    if not isinstance(doc, dict) or doc.get('object') != OBJ:
        raise Fail('INVALID_OBJECT')
    expected = doc.get('expected_prs')
    rows = doc.get('rows')
    if not isinstance(expected, list) or not expected or len(expected) > 100 or not isinstance(rows, list):
        raise Fail('INVALID_COHORT')
    if any(type(x) is not int or x < 1 for x in expected) or len(set(expected)) != len(expected):
        raise Fail('INVALID_EXPECTED_IDS')
    if len(rows) != len(expected):
        raise Fail('MISSING_OR_EXTRA_ROW')
    start = doc.get('start_main')
    end = doc.get('end_main')
    prev_receipt = doc.get('predecessor_receipt')
    if not all(isinstance(x, str) and HEX40.fullmatch(x) for x in (start, end)):
        raise Fail('INVALID_MAIN_SHA')
    if type(prev_receipt) is not int or prev_receipt < 1:
        raise Fail('INVALID_PREDECESSOR_RECEIPT')
    previous_main = start
    seen_receipts = set()
    seen_merges = set()
    for idx, (number, row) in enumerate(zip(expected, rows)):
        if not isinstance(row, dict) or row.get('pr') != number:
            raise Fail('PR_COHORT_MISMATCH')
        receipt = row.get('receipt_id')
        if type(receipt) is not int or receipt <= 0 or receipt in seen_receipts:
            raise Fail('DUPLICATE_OR_INVALID_RECEIPT')
        seen_receipts.add(receipt)
        if row.get('receipt_predecessor') != prev_receipt:
            raise Fail('RECEIPT_PREDECESSOR_MISMATCH')
        if row.get('merged') is not True:
            raise Fail('NOT_MERGED')
        if row.get('receipt_main_before') != previous_main or row.get('pr_base') != previous_main:
            raise Fail('MAIN_PREDECESSOR_MISMATCH')
        merge = row.get('pr_merge')
        if not isinstance(merge, str) or not HEX40.fullmatch(merge) or merge in seen_merges:
            raise Fail('INVALID_OR_DUPLICATE_MERGE')
        seen_merges.add(merge)
        if row.get('receipt_main_after') != merge:
            raise Fail('RECEIPT_MERGE_MISMATCH')
        if row.get('receipt_head') != row.get('pr_head') or not isinstance(row.get('pr_head'), str) or not HEX40.fullmatch(row['pr_head']):
            raise Fail('PR_HEAD_MISMATCH')
        if row.get('receipt_actor') != 'nexusomegac27':
            raise Fail('UNEXPECTED_RECEIPT_ACTOR')
        prev_receipt = receipt
        previous_main = merge
    if previous_main != end:
        raise Fail('FINAL_MAIN_MISMATCH')
    return {'status':'MATCH','checked_prs':len(rows),'checked_receipts':len(seen_receipts),
            'start_main':start,'end_main':end,
            'source_class':'CALLER_SUPPLIED_API_METADATA_NOT_INDEPENDENT_GITHUB_AUTHENTICATION',
            'project_automation_rate':'NOT_COMPUTABLE','claim_ceiling':'C1_DESCRIPTIVE_ONLY'}

def selftest():
    a='a'*40; b='b'*40; c='c'*40; d='d'*40
    row={'pr':1,'receipt_id':10,'receipt_predecessor':9,'merged':True,
         'receipt_main_before':a,'pr_base':a,'pr_merge':b,'receipt_main_after':b,
         'pr_head':c,'receipt_head':c,'receipt_actor':'nexusomegac27'}
    base={'object':OBJ,'expected_prs':[1],'rows':[row], 'start_main':a,'end_main':b,'predecessor_receipt':9}
    assert check(base)['checked_prs'] == 1
    mutations=[
      ('missing',lambda x:x['rows'].clear(),'MISSING_OR_EXTRA_ROW'),
      ('duplicate_pr',lambda x:x['expected_prs'].append(1),'INVALID_EXPECTED_IDS'),
      ('wrong_pr',lambda x:x['rows'][0].update(pr=2),'PR_COHORT_MISMATCH'),
      ('duplicate_receipt',lambda x:x['rows'][0].update(receipt_id=0),'DUPLICATE_OR_INVALID_RECEIPT'),
      ('broken_receipt_link',lambda x:x['rows'][0].update(receipt_predecessor=8),'RECEIPT_PREDECESSOR_MISMATCH'),
      ('unmerged',lambda x:x['rows'][0].update(merged=False),'NOT_MERGED'),
      ('wrong_base',lambda x:x['rows'][0].update(pr_base=d),'MAIN_PREDECESSOR_MISMATCH'),
      ('wrong_receipt_before',lambda x:x['rows'][0].update(receipt_main_before=d),'MAIN_PREDECESSOR_MISMATCH'),
      ('wrong_merge',lambda x:x['rows'][0].update(receipt_main_after=d),'RECEIPT_MERGE_MISMATCH'),
      ('wrong_head',lambda x:x['rows'][0].update(receipt_head=d),'PR_HEAD_MISMATCH'),
      ('wrong_actor',lambda x:x['rows'][0].update(receipt_actor='unregistered'),'UNEXPECTED_RECEIPT_ACTOR'),
      ('wrong_final',lambda x:x.update(end_main=d),'FINAL_MAIN_MISMATCH'),
      ('invalid_main',lambda x:x.update(start_main='z'*40),'INVALID_MAIN_SHA'),
      ('invalid_object',lambda x:x.update(object='OTHER'),'INVALID_OBJECT'),
    ]
    for name, mutate, expected in mutations:
        doc=copy.deepcopy(base);mutate(doc)
        try: check(doc)
        except Fail as e: assert str(e)==expected,(name,str(e),expected)
        else: raise AssertionError(name+' unexpectedly passed')
    try: json.loads('{"x":1,"x":2}',object_pairs_hook=unique_pairs)
    except Fail as e: assert str(e)=='DUPLICATE_JSON_KEY'
    else: raise AssertionError('duplicate JSON key accepted')
    print('SELFTEST_PASS 16/16 (1 positive, 15 negative)')

def main():
    if sys.argv[1:]==['--selftest']:
        selftest();return 0
    try:
        data=sys.stdin.buffer.read(131073)
        if len(data)>131072: raise Fail('INPUT_LIMIT')
        doc=json.loads(data.decode('utf-8'),object_pairs_hook=unique_pairs)
        result=check(doc)
    except (Fail,UnicodeError,ValueError) as e:
        print('FAIL_CLOSED: '+str(e),file=sys.stderr);return 2
    print(json.dumps(result,sort_keys=True,separators=(',',':')))
    return 0
if __name__=='__main__': sys.exit(main())
