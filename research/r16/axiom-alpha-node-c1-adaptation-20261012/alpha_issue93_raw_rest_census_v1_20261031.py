#!/usr/bin/env python3
"""Isolated C1 GitHub REST issue-comment census. No network, writes, or identity claims."""
import hashlib
import json
import re
import sys
from datetime import datetime

SCHEMA = 'alpha_issue93_raw_rest_census_v1'
OWNER = 'nexusomegac27'

def unique(pairs):
    out = {}
    for key, val in pairs:
        if key in out:
            raise ValueError('duplicate_json_key')
        out[key] = val
    return out

def require(ok, reason):
    if not ok:
        raise ValueError(reason)

def timestamp(s):
    require(isinstance(s, str) and bool(re.fullmatch(r'\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ', s)), 'timestamp_format')
    return datetime.fromisoformat(s.replace('Z', '+00:00'))

def evaluate(obj):
    require(isinstance(obj, dict) and obj.get('schema_version') == SCHEMA, 'schema')
    issue = obj.get('issue')
    require(isinstance(issue, dict) and issue.get('number') == 93 and type(issue.get('comments')) is int and issue['comments'] >= 0, 'issue_count')
    pages = obj.get('pages')
    require(isinstance(pages, list) and pages, 'pages')
    h = hashlib.sha256()
    ids = set()
    prior = 0
    count = edited = nonowner = 0
    for i, page in enumerate(pages, 1):
        require(isinstance(page, dict) and page.get('page') == i and page.get('per_page') == 100, 'page_sequence')
        items = page.get('items')
        require(isinstance(items, list) and 0 < len(items) <= 100, 'page_items')
        require(i == len(pages) or len(items) == 100, 'nonterminal_page_short')
        for item in items:
            require(isinstance(item, dict), 'comment')
            cid = item.get('id')
            require(type(cid) is int and cid > prior and cid not in ids, 'comment_id_order')
            prior = cid
            ids.add(cid)
            created, updated = timestamp(item.get('created_at')), timestamp(item.get('updated_at'))
            require(updated >= created, 'time_reversal')
            edited += updated > created
            user = item.get('user')
            require(isinstance(user, dict) and isinstance(user.get('login'), str) and user['login'], 'actor_metadata')
            nonowner += user['login'] != OWNER
            body = item.get('body')
            require(isinstance(body, str), 'body_missing')
            digest = hashlib.sha256(body.encode('utf-8')).hexdigest()
            h.update(f'{cid}:{digest}\n'.encode('ascii'))
            count += 1
    require(count == issue['comments'], 'declared_count_mismatch')
    return {'status': 'C1_SCOPED_RAW_REST_CENSUS' if not edited else 'EDITED_COMMENT_OBSERVED',
            'observed': count, 'declared': issue['comments'], 'edited_timestamps': edited,
            'nonowner_comments': nonowner, 'owner_comments': count - nonowner,
            'body_inventory_sha256': h.hexdigest(), 'authenticated_external_expert': False,
            'historical_immutability_proven': False, 'api_completeness_independently_proven': False,
            'project_rate': 'NOT_COMPUTABLE', 'claim_ceiling': 'C1_DESCRIPTIVE_ONLY'}

def main():
    try:
        obj = json.loads(sys.stdin.read(), object_pairs_hook=unique,
                         parse_constant=lambda _: (_ for _ in ()).throw(ValueError('nonfinite')))
        out = evaluate(obj)
    except (ValueError, TypeError, OverflowError, RecursionError, UnicodeError) as e:
        out = {'status': 'FAIL_CLOSED', 'reason': str(e)[:120]}
    print(json.dumps(out, sort_keys=True))
    return 0 if out['status'] == 'C1_SCOPED_RAW_REST_CENSUS' else 2

if __name__ == '__main__':
    sys.exit(main())
