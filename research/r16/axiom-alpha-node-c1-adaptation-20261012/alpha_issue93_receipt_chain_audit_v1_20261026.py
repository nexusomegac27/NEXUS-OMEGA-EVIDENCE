#!/usr/bin/env python3
"""Read-only, offline C1 structural audit of a caller-supplied Issue #93 snapshot.

Does NOT authenticate GitHub actors, verify Git commit ancestry, prove original
comment bytes, or establish automation KPI. Caller must independently pin and
verify the GitHub API source before interpreting this structural result.
"""
import json
import re
import sys

REPO = 'nexusomegac27/NEXUS-OMEGA-EVIDENCE'
HEX40 = re.compile(r'[0-9a-f]{40}\Z')
FIELD = re.compile(r'^([A-Z][A-Z0-9_]*)=(.*)$', re.MULTILINE)
MAX_COMMENTS = 256
MAX_BODY_CHARS = 32768


def require_int(value, label):
    if type(value) is not int or value <= 0:
        raise ValueError('INVALID_' + label)
    return value


def unique_field(body, key):
    values = [v for k, v in FIELD.findall(body) if k == key]
    if len(values) != 1:
        raise ValueError('MISSING_OR_DUPLICATE_' + key)
    return values[0]


def audit(payload):
    if not isinstance(payload, dict):
        raise TypeError('SNAPSHOT_NOT_OBJECT')
    if payload.get('repository') != REPO or payload.get('issue_number') != 93:
        raise ValueError('UNEXPECTED_ISSUE_OR_REPOSITORY')
    anchor = require_int(payload.get('anchor_predecessor_id'), 'ANCHOR')
    tail = require_int(payload.get('expected_tail_id'), 'TAIL')
    comments = payload.get('comments')
    if not isinstance(comments, list) or not 1 <= len(comments) <= MAX_COMMENTS:
        raise ValueError('INVALID_COMMENT_COUNT')
    prev = anchor
    for entry in comments:
        if not isinstance(entry, dict):
            raise ValueError('INVALID_COMMENT_OBJECT')
        cid = require_int(entry.get('id'), 'COMMENT_ID')
        if cid <= prev:
            raise ValueError('DUPLICATE_OR_NONMONOTONIC_ID')
        actor = entry.get('actor_login')
        if not isinstance(actor, str) or not actor or len(actor) > 80:
            raise ValueError('INVALID_ACTOR_METADATA')
        body = entry.get('body')
        if not isinstance(body, str) or len(body) > MAX_BODY_CHARS:
            raise ValueError('INVALID_BODY')
        pred = unique_field(body, 'PREDECESSOR_ISSUE93_RECEIPT')
        if pred != str(prev):
            raise ValueError('BROKEN_PREDECESSOR_EDGE:' + str(cid))
        if not unique_field(body, 'OBJECT').startswith('NEXUS_'):
            raise ValueError('INVALID_OBJECT')
        if unique_field(body, 'CLAIM_CEILING') != 'C1_DESCRIPTIVE_ONLY':
            raise ValueError('CLAIM_PROMOTION_OR_MISSING_CEILING')
        if not HEX40.fullmatch(unique_field(body, 'ACTUAL_MAIN_READBACK')):
            raise ValueError('MALFORMED_MAIN_SHA')
        prev = cid
    if prev != tail:
        raise ValueError('TAIL_NOT_MATCHED')
    return {'state': 'PASS_RECEIPT_CHAIN_STRUCTURE_C1',
            'checked_edges': len(comments), 'anchor_predecessor_id': anchor,
            'last_comment_id': prev, 'claim_ceiling': 'C1_DESCRIPTIVE_ONLY',
            'source_authentication': 'NOT_ESTABLISHED_BY_CALLER_SNAPSHOT',
            'github_main_readback': 'NOT_ESTABLISHED_BY_THIS_TOOL',
            'project_automation_rate': 'NOT_COMPUTABLE'}


def main():
    try:
        raw = sys.stdin.buffer.read(1048577)
        if len(raw) > 1048576:
            raise ValueError('INPUT_TOO_LARGE')
        result = audit(json.loads(raw.decode('utf-8')))
        print(json.dumps(result, sort_keys=True))
        return 0
    except (ValueError, TypeError, UnicodeError) as exc:
        print('FAIL_CLOSED: ' + str(exc), file=sys.stderr)
        return 2

if __name__ == '__main__': sys.exit(main())
