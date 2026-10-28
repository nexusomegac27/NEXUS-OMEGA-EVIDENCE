#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Offline, C1-only crosscheck of caller-supplied GitHub REST-shaped objects.

Does not fetch or authenticate API responses. No external actor ACK or project rate.
"""
import datetime
import json
import re
import sys

MAX_BYTES = 2_000_000
REPO = 'nexusomegac27/NEXUS-OMEGA-EVIDENCE'
OBJECT = 'NEXUS_OMEGA_ALPHA_ISSUE93_API_CROSSCHECK_V1'
SHA = re.compile(r'[0-9a-f]{40}\Z')


def fail(code):
    raise ValueError(code)


def unique(pairs):
    out = {}
    for k, v in pairs:
        if k in out:
            fail('DUPLICATE_JSON_KEY')
        out[k] = v
    return out


def nonfinite(_):
    fail('NONFINITE_JSON')


def sha(x):
    return type(x) is str and SHA.fullmatch(x) is not None


def positive(x):
    return type(x) is int and x > 0


def timestamp(x):
    if type(x) is not str or not x.endswith('Z'):
        fail('INVALID_TIMESTAMP')
    try:
        return datetime.datetime.fromisoformat(x.replace('Z', '+00:00'))
    except ValueError:
        fail('INVALID_TIMESTAMP')


def owner(x):
    return type(x) is dict and x.get('login') == 'nexusomegac27'


def receipt_fields(body):
    if type(body) is not str or len(body) > 100000:
        fail('INVALID_RECEIPT_BODY')
    found = {}
    for line in body.splitlines():
        if '=' not in line:
            continue
        key, value = line.split('=', 1)
        if key in ('PR', 'ACTUAL_MAIN_READBACK', 'PINNED_MAIN_BEFORE',
                   'PREDECESSOR_ISSUE93_RECEIPT', 'CLAIM_CEILING'):
            if key in found:
                fail('DUPLICATE_RECEIPT_FIELD')
            found[key] = value.strip()
    if len(found) != 5:
        fail('MISSING_RECEIPT_FIELD')
    return found


def audit(data):
    if type(data) is not dict or set(data) != {'object', 'repository', 'comment',
            'predecessor_comment', 'pull', 'commit', 'branch', 'pr_files'}:
        fail('INVALID_ENVELOPE')
    if data['object'] != OBJECT or data['repository'] != REPO:
        fail('INVALID_REPOSITORY')
    c, p, pr, commit, branch = (data[k] for k in
                              ('comment', 'predecessor_comment', 'pull', 'commit', 'branch'))
    if not all(type(x) is dict for x in (c, p, pr, commit, branch)):
        fail('INVALID_API_OBJECT')
    if not (positive(c.get('id')) and positive(p.get('id')) and c['id'] > p['id']):
        fail('INVALID_RECEIPT_ORDER')
    issue_url = f'https://api.github.com/repos/{REPO}/issues/93'
    if (c.get('issue_url') != issue_url or p.get('issue_url') != issue_url
            or not owner(c.get('user')) or not owner(p.get('user'))):
        fail('ISSUE_ACTOR_OR_SCOPE_MISMATCH')
    c_time, p_time = timestamp(c.get('created_at')), timestamp(p.get('created_at'))
    if (c_time <= p_time or timestamp(c.get('updated_at')) != c_time
            or timestamp(p.get('updated_at')) != p_time):
        fail('RECEIPT_TIME_OR_EDIT_MISMATCH')
    fields = receipt_fields(c.get('body'))
    if fields['PREDECESSOR_ISSUE93_RECEIPT'] != str(p['id']):
        fail('RECEIPT_PARENT_MISMATCH')
    if fields['CLAIM_CEILING'] != 'C1_DESCRIPTIVE_ONLY':
        fail('CLAIM_PROMOTION')
    number = pr.get('number')
    if (not positive(number) or not owner(pr.get('user'))
            or pr.get('merged_at') is None
            or fields['PR'] != f'https://github.com/{REPO}/pull/{number}'):
        fail('PR_SCOPE_MISMATCH')
    merge = pr.get('merge_commit_sha')
    if not sha(merge) or not sha(fields['PINNED_MAIN_BEFORE']):
        fail('INVALID_COMMIT_SHA')
    if (commit.get('sha') != merge or fields['ACTUAL_MAIN_READBACK'] != merge
            or branch.get('commit', {}).get('sha') != merge):
        fail('MAIN_PR_COMMIT_MISMATCH')
    parents = commit.get('parents')
    if (type(parents) is not list or len(parents) != 1
            or parents[0].get('sha') != fields['PINNED_MAIN_BEFORE']):
        fail('MAIN_PARENT_MISMATCH')
    verification = commit.get('commit', {}).get('verification', {})
    if verification.get('verified') is not True or verification.get('reason') != 'valid':
        fail('COMMIT_SIGNATURE_UNVERIFIED')
    files = commit.get('files')
    pr_files = data['pr_files']
    if (type(files) is not list or type(pr_files) is not list
            or not 1 <= len(files) <= 20 or len(files) != len(pr_files)):
        fail('INVALID_FILE_INVENTORY')
    def paths(xs):
        out = []
        for x in xs:
            if (type(x) is not dict or x.get('status') != 'added'
                    or type(x.get('filename')) is not str
                    or not x['filename'].startswith('research/r16/axiom-alpha-node-c1-adaptation-20261012/')):
                fail('INVALID_ADDITIVE_PATH')
            out.append(x['filename'])
        if len(out) != len(set(out)):
            fail('DUPLICATE_PATH')
        return sorted(out)
    if paths(files) != paths(pr_files):
        fail('PR_COMMIT_FILE_MISMATCH')
    return {'state': 'C1_SCOPED_API_SHAPED_METADATA_CROSSCHECK_PASS',
            'receipt_id': c['id'], 'pr': number, 'files_crosschecked': len(files),
            'api_origin_authenticated': False,
            'original_file_bytes_verified': False,
            'independent_expert_ack': False,
            'project_automation_rate': 'NOT_COMPUTABLE',
            'project_readback_rate': 'NOT_COMPUTABLE',
            'claim_ceiling': 'C1_DESCRIPTIVE_ONLY'}


def main():
    try:
        raw = sys.stdin.buffer.read(MAX_BYTES + 1)
        if len(raw) > MAX_BYTES:
            fail('INPUT_TOO_LARGE')
        obj = json.loads(raw.decode('utf-8'), object_pairs_hook=unique,
                         parse_constant=nonfinite)
        print(json.dumps(audit(obj), sort_keys=True, separators=(',', ':')))
        return 0
    except (ValueError, TypeError, UnicodeError, RecursionError, AttributeError) as e:
        print('FAIL_CLOSED: ' + str(e), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
