#!/usr/bin/env python3
"""Isolated C1 Issue #93 two-phase census guard. Input is untrusted JSON, no network/writes."""
import hashlib
import json
import re
import sys
from datetime import datetime

SCHEMA = 'alpha_issue93_two_phase_snapshot_v1'
REPO = 'nexusomegac27/NEXUS-OMEGA-EVIDENCE'

def unique(pairs):
    out = {}
    for k, v in pairs:
        if k in out:
            raise ValueError('duplicate_json_key')
        out[k] = v
    return out

def reject_constant(value):
    raise ValueError('nonfinite_json')

def require(condition, code):
    if not condition:
        raise ValueError(code)

def timestamp(value):
    require(isinstance(value, str) and re.fullmatch(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z', value), 'timestamp_format')
    return datetime.fromisoformat(value.replace('Z', '+00:00'))

def evaluate(obj):
    require(isinstance(obj, dict) and obj.get('schema_version') == SCHEMA, 'schema')
    require(obj.get('repository_full_name') == REPO, 'repo')
    pre, post = obj.get('pre'), obj.get('post')
    for label, meta in [('pre', pre), ('post', post)]:
        require(isinstance(meta, dict) and type(meta.get('issue_number')) is int and meta['issue_number'] == 93, label + '_issue')
        require(type(meta.get('comments')) is int and meta['comments'] >= 0, label + '_count')
    require(pre['comments'] == post['comments'], 'snapshot_count_drift')
    expected = pre['comments']
    pages = obj.get('pages')
    require(isinstance(pages, list) and len(pages) == (expected + 99)//100, 'page_count')
    prior = 0
    seen = set()
    edited = nonowner = total = 0
    fingerprint = hashlib.sha256()
    for i, page in enumerate(pages):
        require(isinstance(page, dict) and type(page.get('page')) is int and page['page'] == i+1 and type(page.get('per_page')) is int and page['per_page'] == 100, 'page_sequence')
        items = page.get('items')
        expected_length = min(100, expected - 100*i)
        require(isinstance(items, list) and len(items) == expected_length, 'page_length')
        for item in items:
            require(isinstance(item, dict), 'comment_type')
            cid = item.get('id')
            require(type(cid) is int and cid > prior and cid not in seen, 'id_order')
            prior = cid
            seen.add(cid)
            user = item.get('user')
            require(isinstance(user, dict) and isinstance(user.get('login'), str) and bool(user['login']), 'actor_label')
            require(isinstance(item.get('body'), str), 'body')
            created, updated = timestamp(item.get('created_at')), timestamp(item.get('updated_at'))
            require(updated >= created, 'timestamp_reversal')
            edited += int(updated != created)
            nonowner += int(user['login'] != 'nexusomegac27')
            bodyhash = hashlib.sha256(item['body'].encode('utf-8')).hexdigest()
            fingerprint.update((str(cid)+':'+bodyhash+'\n').encode('ascii'))
            total += 1
    require(total == expected, 'count')
    return {'status': 'CENSUS_CONSISTENT_NOT_AUTHENTICATED', 'count': total,
            'edited_count': edited, 'nonowner_count': nonowner,
            'body_inventory_sha256': fingerprint.hexdigest(),
            'atomic_snapshot_proven': False, 'actor_authenticated_as_expert': False}

if __name__ == '__main__':
    try:
        data = json.loads(sys.stdin.read(), object_pairs_hook=unique, parse_constant=reject_constant)
        result = evaluate(data)
        print(json.dumps(result, sort_keys=True))
    except (ValueError, TypeError, KeyError, OverflowError) as e:
        print(json.dumps({'status': 'FAIL_CLOSED', 'reason': str(e)}))
        sys.exit(2)
