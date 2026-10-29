#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Offline C1 exact-key Issue #93 receipt census; caller-supplied API projection.

No GitHub fetch, identity authentication, project-rate inference, or writes.
Only an entire line PR=<URL> binds a receipt to a PR. PREDECESSOR_PR=
is historical context and must never be treated as the current PR.
"""
import json
import re
import sys

OBJECT = 'NEXUS_OMEGA_ALPHA_ISSUE93_EXACT_KEY_RECEIPT_CENSUS_V1'
REPO = 'nexusomegac27/NEXUS-OMEGA-EVIDENCE'
SHA40 = re.compile(r'[0-9a-f]{40}\Z')
PR_URL = re.compile(r'https://github\.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/pull/([1-9][0-9]*)\Z')
MAX_BYTES = 4_000_000


def fail(reason):
    raise ValueError(reason)


def unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            fail('DUPLICATE_JSON_KEY')
        result[key] = value
    return result


def nonfinite(_):
    fail('NONFINITE_JSON')


def positive_int(value):
    return type(value) is int and value > 0


def fields(body):
    if type(body) is not str or len(body) > 250_000:
        fail('INVALID_COMMENT_BODY')
    out = {}
    for line in body.splitlines():
        if '=' not in line:
            continue
        key, value = line.split('=', 1)
        if key in ('PR', 'ACTUAL_MAIN_READBACK', 'CLAIM_CEILING'):
            if key in out:
                fail('DUPLICATE_RECEIPT_FIELD')
            out[key] = value.strip()
    return out


def audit(obj):
    if type(obj) is not dict or set(obj) != {'object', 'repository', 'issue_number', 'expected_prs', 'pulls', 'comments'}:
        fail('INVALID_ENVELOPE')
    if obj['object'] != OBJECT or obj['repository'] != REPO or obj['issue_number'] != 93:
        fail('INVALID_SCOPE')
    expected = obj['expected_prs']
    if (type(expected) is not list or not 1 <= len(expected) <= 200 or
            any(not positive_int(n) for n in expected) or expected != sorted(set(expected))):
        fail('INVALID_EXPECTED_PRS')
    pulls = obj['pulls']
    if type(pulls) is not list or len(pulls) != len(expected):
        fail('INVALID_PULL_INVENTORY')
    by_pr = {}
    for pr in pulls:
        if (type(pr) is not dict or set(pr) != {'number', 'merged', 'merge_commit_sha'} or
                not positive_int(pr['number']) or type(pr['merged']) is not bool or
                not pr['merged'] or type(pr['merge_commit_sha']) is not str or
                not SHA40.fullmatch(pr['merge_commit_sha']) or pr['number'] in by_pr):
            fail('INVALID_PULL_INVENTORY')
        by_pr[pr['number']] = pr['merge_commit_sha']
    if sorted(by_pr) != expected:
        fail('PULL_SCOPE_MISMATCH')
    comments = obj['comments']
    if type(comments) is not list or not 1 <= len(comments) <= 5000:
        fail('INVALID_COMMENT_INVENTORY')
    receipts, seen_ids, ignored = {}, set(), 0
    predecessor_only = 0
    for comment in comments:
        if type(comment) is not dict or set(comment) != {'id', 'user', 'body'} or not positive_int(comment['id']):
            fail('INVALID_COMMENT')
        if comment['id'] in seen_ids:
            fail('DUPLICATE_COMMENT_ID')
        seen_ids.add(comment['id'])
        data = fields(comment['body'])
        if 'PR' not in data:
            ignored += 1
            if any(line.startswith('PREDECESSOR_PR=') for line in comment['body'].splitlines()):
                predecessor_only += 1
            continue
        if (type(comment['user']) is not dict or comment['user'].get('login') != 'nexusomegac27'):
            fail('RECEIPT_ACTOR_MISMATCH')
        match = PR_URL.fullmatch(data['PR'])
        if not match:
            fail('INVALID_RECEIPT_PR_URL')
        number = int(match.group(1))
        if number not in by_pr:
            fail('UNEXPECTED_RECEIPT_PR')
        if number in receipts:
            fail('DUPLICATE_PR_RECEIPT')
        if data.get('CLAIM_CEILING') != 'C1_DESCRIPTIVE_ONLY':
            fail('CLAIM_CEILING_MISMATCH')
        commit = data.get('ACTUAL_MAIN_READBACK')
        if type(commit) is not str or not SHA40.fullmatch(commit) or commit != by_pr[number]:
            fail('PR_MAIN_READBACK_MISMATCH')
        receipts[number] = comment['id']
    missing = sorted(set(expected) - set(receipts))
    if missing:
        fail('MISSING_EXPECTED_PR_RECEIPT')
    ordered_ids = [receipts[n] for n in expected]
    if any(b <= a for a, b in zip(ordered_ids, ordered_ids[1:])):
        fail('NONMONOTONIC_RECEIPT_ORDER')
    return {'state': 'C1_CALLER_SUPPLIED_EXACT_KEY_CENSUS_MATCH',
            'claim_ceiling': 'C1_DESCRIPTIVE_ONLY',
            'expected_pr_count': len(expected), 'matched_receipt_count': len(receipts),
            'ignored_comments': ignored, 'predecessor_only_comments': predecessor_only,
            'receipt_ids': {str(k): receipts[k] for k in expected},
            'api_origin_authenticated': False, 'source_bytes_rehashed': False,
            'all_attempts_enumerated': False,
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
