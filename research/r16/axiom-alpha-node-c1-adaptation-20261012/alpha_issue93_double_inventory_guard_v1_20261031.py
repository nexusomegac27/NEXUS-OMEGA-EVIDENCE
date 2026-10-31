#!/usr/bin/env python3
"""Isolated C1 double-inventory consistency guard; untrusted JSON, no I/O beyond stdin/stdout."""
import hashlib
import json
import re
import sys
from datetime import datetime

SCHEMA = 'alpha_issue93_double_inventory_v1'
REPO = 'nexusomegac27/NEXUS-OMEGA-EVIDENCE'


def unique(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('duplicate_json_key')
        result[key] = value
    return result


def reject_constant(value):
    raise ValueError('nonfinite_json')


def require(ok, label):
    if not ok:
        raise ValueError(label)


def timestamp(value):
    require(isinstance(value, str) and re.fullmatch(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z', value), 'timestamp_format')
    try:
        return datetime.fromisoformat(value.replace('Z', '+00:00'))
    except ValueError:
        raise ValueError('timestamp_value')


def read_pass(pages, count):
    require(isinstance(pages, list) and len(pages) == (count + 99)//100, 'page_count')
    records = []
    last_id = 0
    edited = nonowner = 0
    for index, page in enumerate(pages):
        require(isinstance(page, dict), 'page_type')
        require(type(page.get('page')) is int and page['page'] == index+1, 'page_sequence')
        require(type(page.get('per_page')) is int and page['per_page'] == 100, 'page_size')
        items = page.get('items')
        require(isinstance(items, list) and len(items) == min(100, count-100*index), 'page_length')
        for item in items:
            require(isinstance(item, dict), 'comment_type')
            cid = item.get('id')
            require(type(cid) is int and cid > last_id, 'id_order')
            last_id = cid
            user = item.get('user')
            require(isinstance(user, dict) and isinstance(user.get('login'), str) and bool(user['login']), 'actor_label')
            body = item.get('body')
            require(isinstance(body, str), 'body')
            created, updated = item.get('created_at'), item.get('updated_at')
            require(timestamp(updated) >= timestamp(created), 'timestamp_reversal')
            edited += int(updated != created)
            nonowner += int(user['login'] != 'nexusomegac27')
            records.append((cid, user['login'], created, updated, body))
    require(len(records) == count, 'total_count')
    return records, edited, nonowner


def evaluate(obj):
    require(isinstance(obj, dict) and obj.get('schema_version') == SCHEMA, 'schema')
    require(obj.get('repository_full_name') == REPO, 'repository')
    pre, post = obj.get('pre'), obj.get('post')
    for label, meta in (('pre', pre), ('post', post)):
        require(isinstance(meta, dict), label + '_type')
        require(type(meta.get('issue_number')) is int and meta['issue_number'] == 93, label + '_issue')
        require(type(meta.get('comments')) is int and meta['comments'] >= 0, label + '_count')
    require(pre['comments'] == post['comments'], 'count_drift')
    passes = obj.get('passes')
    require(isinstance(passes, list) and len(passes) == 2, 'pass_count')
    first, edited, nonowner = read_pass(passes[0], pre['comments'])
    second, _, _ = read_pass(passes[1], post['comments'])
    require(first == second, 'inventory_drift')
    digest = hashlib.sha256()
    for record in first:
        digest.update(json.dumps(record, ensure_ascii=False, separators=(',', ':')).encode('utf-8') + b'\n')
    return {'status': 'DOUBLE_INVENTORY_STABLE_NOT_ATOMIC', 'count': len(first),
            'edited_count': edited, 'nonowner_count': nonowner,
            'inventory_sha256': digest.hexdigest(),
            'atomic_snapshot_proven': False, 'actor_authenticated_as_expert': False}


if __name__ == '__main__':
    try:
        obj = json.loads(sys.stdin.read(), object_pairs_hook=unique, parse_constant=reject_constant)
        print(json.dumps(evaluate(obj), sort_keys=True))
    except (ValueError, TypeError, KeyError, OverflowError) as exc:
        print(json.dumps({'status': 'FAIL_CLOSED', 'reason': str(exc)}))
        sys.exit(2)
