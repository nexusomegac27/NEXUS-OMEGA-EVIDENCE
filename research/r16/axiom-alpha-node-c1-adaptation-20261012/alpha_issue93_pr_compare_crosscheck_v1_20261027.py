#!/usr/bin/env python3
"""Offline C1 cross-source consistency guard for an Issue #93 merge receipt.

Caller must separately fetch the exact issue comment, PR metadata and GitHub
compare response; this tool cannot authenticate those snapshots or live main.
No network, repository writes, scientific approval or KPI promotion.
"""
import json
import re
import sys

REPO = 'nexusomegac27/NEXUS-OMEGA-EVIDENCE'
ROOT = 'research/r16/axiom-alpha-node-c1-adaptation-20261012/'
FIELD = re.compile(r'^([A-Z][A-Z0-9_]*)=(.*)$', re.MULTILINE)
HEX40 = re.compile(r'[0-9a-f]{40}\Z')
COUNTS = re.compile(r'([0-9]+)_ADDED_([0-9]+)_MODIFIED_([0-9]+)_DELETED\Z')
MAX_BYTES = 1048576


def fail(reason):
    raise ValueError(reason)


def unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            fail('DUPLICATE_JSON_KEY')
        result[key] = value
    return result


def finite_constant(_):
    fail('NONFINITE_JSON')


def sha(value, name):
    if type(value) is not str or HEX40.fullmatch(value) is None:
        fail('INVALID_' + name)
    return value


def field(body, name):
    values = [v for k, v in FIELD.findall(body) if k == name]
    if len(values) != 1:
        fail('MISSING_OR_DUPLICATE_' + name)
    return values[0]


def audit(p):
    if type(p) is not dict or set(p) != {'repository', 'issue_number', 'receipt', 'pr', 'compare'}:
        fail('INVALID_ENVELOPE')
    if p['repository'] != REPO or type(p['issue_number']) is not int or p['issue_number'] != 93:
        fail('INVALID_REPOSITORY_OR_ISSUE')
    r, pr, c = p['receipt'], p['pr'], p['compare']
    if not all(type(x) is dict for x in (r, pr, c)):
        fail('INVALID_SOURCE_OBJECT')
    if type(r.get('id')) is not int or r['id'] <= 0 or r.get('actor_login') != 'nexusomegac27':
        fail('INVALID_RECEIPT_METADATA')
    body = r.get('body')
    if type(body) is not str or len(body) > 32768:
        fail('INVALID_RECEIPT_BODY')
    if not field(body, 'OBJECT').startswith('NEXUS_') or field(body, 'CLAIM_CEILING') != 'C1_DESCRIPTIVE_ONLY':
        fail('INVALID_OBJECT_OR_CEILING')
    n = pr.get('number')
    if type(n) is not int or n <= 0 or n > 1000000:
        fail('INVALID_PR_NUMBER')
    if field(body, 'PR' + str(n)) != 'https://github.com/' + REPO + '/pull/' + str(n):
        fail('PR_URL_MISMATCH')
    parent = sha(field(body, 'PINNED_MAIN_BEFORE'), 'RECEIPT_PARENT')
    if sha(field(body, 'ACTUAL_MAIN_PARENT'), 'MAIN_PARENT') != parent:
        fail('RECEIPT_PARENT_CONTRADICTION')
    main = sha(field(body, 'ACTUAL_MAIN_READBACK'), 'MAIN')
    head = sha(field(body, 'PR' + str(n) + '_HEAD_AT_MERGE'), 'PR_HEAD')
    if (pr.get('merged') is not True or pr.get('state') != 'closed' or pr.get('base') != 'main' or
            pr.get('head_repo_full_name') != REPO or
            sha(pr.get('base_sha'), 'PR_BASE') != parent or
            sha(pr.get('head_sha'), 'PR_HEAD_API') != head or
            sha(pr.get('merge_commit_sha'), 'PR_MERGE') != main):
        fail('PR_SOURCE_MISMATCH')
    if (c.get('repository_full_name') != REPO or c.get('status') != 'ahead' or
            type(c.get('ahead_by')) is not int or c['ahead_by'] != 1 or
            type(c.get('behind_by')) is not int or c['behind_by'] != 0 or
            type(c.get('total_commits')) is not int or c['total_commits'] != 1 or
            sha(c.get('base'), 'COMPARE_BASE') != parent or
            sha(c.get('head'), 'COMPARE_HEAD') != main):
        fail('COMPARE_SOURCE_MISMATCH')
    if (type(c.get('base_commit')) is not dict or type(c.get('merge_base_commit')) is not dict or
            sha(c['base_commit'].get('sha'), 'COMPARE_BASE_COMMIT') != parent or
            sha(c['merge_base_commit'].get('sha'), 'COMPARE_MERGE_BASE') != parent):
        fail('COMPARE_ANCESTRY_MISMATCH')
    counts = COUNTS.fullmatch(field(body, 'MAIN_CHANGED_FILES'))
    if counts is None:
        fail('INVALID_FILE_COUNT_RECEIPT')
    added, modified, deleted = (int(x) for x in counts.groups())
    files = c.get('files')
    if (type(files) is not list or not 1 <= len(files) <= 100 or
            (added, modified, deleted) != (len(files), 0, 0)):
        fail('FILE_COUNT_MISMATCH')
    names = set()
    for f in files:
        if (type(f) is not dict or f.get('status') != 'added' or
                type(f.get('filename')) is not str or
                not f['filename'].startswith(ROOT) or f['filename'] in names):
            fail('FILE_CHANGE_MISMATCH')
        names.add(f['filename'])
    return {'state': 'PASS_PR_COMPARE_RECEIPT_CONSISTENCY_C1',
            'receipt_id': r['id'], 'pr_number': n, 'compared_main_sha': main,
            'compared_predecessor_sha': parent, 'checked_files': len(files),
            'claim_ceiling': 'C1_DESCRIPTIVE_ONLY',
            'api_origin_authenticated': False, 'live_main_verified': False,
            'project_automation_rate': 'NOT_COMPUTABLE'}


def main():
    try:
        raw = sys.stdin.buffer.read(MAX_BYTES + 1)
        if len(raw) > MAX_BYTES:
            fail('INPUT_TOO_LARGE')
        p = json.loads(raw.decode('utf-8'), object_pairs_hook=unique_pairs,
                       parse_constant=finite_constant)
        print(json.dumps(audit(p), sort_keys=True, separators=(',', ':')))
        return 0
    except (ValueError, TypeError, UnicodeError, RecursionError) as exc:
        print('FAIL_CLOSED: ' + str(exc), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
