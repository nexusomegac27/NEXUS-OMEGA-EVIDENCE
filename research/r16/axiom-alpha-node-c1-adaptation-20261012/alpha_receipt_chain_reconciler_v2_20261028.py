#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""C1 offline PR/receipt chain with variable additive-file inventory.

Caller-supplied metadata only: no GitHub API authentication, CI or file-byte proof.
"""
import json
import re
import sys

OBJECT = 'NEXUS_OMEGA_ALPHA_RECEIPT_CHAIN_V2'
REPO = 'nexusomegac27/NEXUS-OMEGA-EVIDENCE'
ROOT = 'research/r16/axiom-alpha-node-c1-adaptation-20261012/'
MAX_BYTES = 1_048_576
SHA = re.compile(r'[0-9a-f]{40}\Z')


def fail(code):
    raise ValueError(code)


def unique_pairs(pairs):
    out = {}
    for key, value in pairs:
        if key in out:
            fail('DUPLICATE_JSON_KEY')
        out[key] = value
    return out


def nonfinite(_):
    fail('NONFINITE_JSON')


def fields(obj, expected, code):
    if type(obj) is not dict or set(obj) != expected:
        fail(code)


def sha(value):
    return type(value) is str and bool(SHA.fullmatch(value))


def integer(value, minimum=0):
    return type(value) is int and value >= minimum


def path_valid(value):
    if type(value) is not str or not value.startswith(ROOT) or len(value) > 512:
        return False
    parts = value.split('/')
    return (all(p not in ('', '.', '..') for p in parts)
            and all(32 <= ord(c) < 127 and c != '\\' for c in value))


def audit(obj):
    fields(obj, {'object', 'repository', 'scope', 'records'}, 'INVALID_ENVELOPE')
    if obj['object'] != OBJECT or obj['repository'] != REPO:
        fail('INVALID_REPOSITORY')
    scope = obj['scope']
    fields(scope, {'first_pr', 'last_pr', 'base_sha', 'head_sha',
                   'predecessor_receipt_id'}, 'INVALID_SCOPE')
    if not (integer(scope['first_pr'], 1) and integer(scope['last_pr'], 1)
            and scope['first_pr'] <= scope['last_pr']
            and sha(scope['base_sha']) and sha(scope['head_sha'])
            and integer(scope['predecessor_receipt_id'], 1)):
        fail('INVALID_SCOPE')
    records = obj['records']
    if type(records) is not list or not 1 <= len(records) <= 100:
        fail('INVALID_RECORD_COUNT')
    if len(records) != scope['last_pr'] - scope['first_pr'] + 1:
        fail('MISSING_PR_RECORD')
    prev_main = scope['base_sha']
    prev_receipt = scope['predecessor_receipt_id']
    receipt_ids = set()
    all_paths = set()
    total_files = 0
    for offset, record in enumerate(records):
        fields(record, {'pr', 'merged', 'merge_sha', 'receipt_id',
                        'receipt_predecessor_id', 'receipt_main_sha',
                        'receipt_parent_sha', 'compare', 'files'}, 'INVALID_RECORD')
        if type(record['pr']) is not int or record['pr'] != scope['first_pr'] + offset:
            fail('PR_ORDER_MISMATCH')
        if record['merged'] is not True or not sha(record['merge_sha']):
            fail('PR_MERGE_UNESTABLISHED')
        if not integer(record['receipt_id'], 1) or record['receipt_id'] in receipt_ids:
            fail('RECEIPT_ID_INVALID')
        receipt_ids.add(record['receipt_id'])
        if type(record['receipt_predecessor_id']) is not int or record['receipt_predecessor_id'] != prev_receipt:
            fail('RECEIPT_PREDECESSOR_MISMATCH')
        if record['receipt_parent_sha'] != prev_main:
            fail('MAIN_PARENT_MISMATCH')
        if record['receipt_main_sha'] != record['merge_sha']:
            fail('RECEIPT_MERGE_MISMATCH')
        compare = record['compare']
        fields(compare, {'ahead', 'behind', 'files_added', 'files_modified',
                         'files_deleted'}, 'INVALID_COMPARE')
        if any(not integer(compare[k]) for k in compare):
            fail('INVALID_COMPARE')
        files = record['files']
        if type(files) is not list or not 1 <= len(files) <= 20:
            fail('INVALID_FILE_INVENTORY')
        if (compare['ahead'], compare['behind'], compare['files_added'],
                compare['files_modified'], compare['files_deleted']) != (1, 0, len(files), 0, 0):
            fail('COMPARE_INVENTORY_MISMATCH')
        for f in files:
            fields(f, {'path', 'status'}, 'INVALID_FILE_RECORD')
            if f['status'] != 'added' or not path_valid(f['path']):
                fail('INVALID_ADDITIVE_PATH')
            if f['path'] in all_paths:
                fail('DUPLICATE_ADDITIVE_PATH')
            all_paths.add(f['path'])
        total_files += len(files)
        prev_main = record['merge_sha']
        prev_receipt = record['receipt_id']
    if prev_main != scope['head_sha']:
        fail('PINNED_HEAD_MISMATCH')
    return {'state': 'C1_CALLER_SUPPLIED_INVENTORY_CHAIN_MATCH',
            'claim_ceiling': 'C1_DESCRIPTIVE_ONLY',
            'first_pr': scope['first_pr'], 'last_pr': scope['last_pr'],
            'records_checked': len(records), 'files_checked': total_files,
            'metadata_chain_match': f'{len(records)}/{len(records)}',
            'api_origin_authenticated': False,
            'source_file_byte_readback_verified': False,
            'external_receiver_ack_established': False,
            'project_automation_rate': 'NOT_COMPUTABLE',
            'project_readback_rate': 'NOT_COMPUTABLE'}


def main():
    try:
        raw = sys.stdin.buffer.read(MAX_BYTES + 1)
        if len(raw) > MAX_BYTES:
            fail('INPUT_TOO_LARGE')
        obj = json.loads(raw.decode('utf-8'), object_pairs_hook=unique_pairs,
                         parse_constant=nonfinite)
        print(json.dumps(audit(obj), sort_keys=True, separators=(',', ':')))
        return 0
    except (ValueError, TypeError, UnicodeError, RecursionError) as exc:
        print('FAIL_CLOSED: ' + str(exc), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
