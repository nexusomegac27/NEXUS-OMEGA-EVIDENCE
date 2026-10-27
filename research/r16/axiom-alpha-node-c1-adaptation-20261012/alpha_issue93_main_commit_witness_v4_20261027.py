#!/usr/bin/env python3
"""Isolated C1 V4: cross-check receipt/PR/compare with branch and commit witnesses.

The V3 validator and its frozen evaluators remain unchanged. Caller supplies
separately acquired GitHub API snapshots; this tool cannot authenticate their
origin, ensure complete pagination, verify current main or authorize a merge.
PINNED_V3_GIT_BLOB=b3e31eb9d8094a493065c1f66f73a605b3aaa145
FROZEN_EVALUATOR_FIRST_COMMIT=98b0c723b67b998f81b94904c44c8388a060587a
"""
import json
import sys

import alpha_issue93_pr_compare_crosscheck_v3_20261027 as baseline

CORE = {'repository', 'issue_number', 'receipt', 'pr', 'compare'}
ALL = CORE | {'branch', 'commit'}
fail = baseline.base.base.fail
sha = baseline.base.base.sha


def audit(payload):
    if type(payload) is not dict or set(payload) != ALL:
        fail('INVALID_WITNESS_ENVELOPE')
    result = baseline.audit({key: payload[key] for key in CORE})
    branch, commit = payload['branch'], payload['commit']
    main, parent = result['compared_main_sha'], result['compared_predecessor_sha']
    if (type(branch) is not dict or branch.get('name') != 'main' or
            type(branch.get('commit')) is not dict or
            sha(branch['commit'].get('sha'), 'BRANCH_TIP') != main):
        fail('BRANCH_MAIN_TIP_MISMATCH')
    if type(commit) is not dict or sha(commit.get('sha'), 'COMMIT_SHA') != main:
        fail('COMMIT_SHA_MISMATCH')
    parents = commit.get('parents')
    if (type(parents) is not list or len(parents) != 1 or
            type(parents[0]) is not dict or
            sha(parents[0].get('sha'), 'COMMIT_PARENT') != parent):
        fail('COMMIT_PARENT_MISMATCH')
    if (commit.get('too_large') is not None and commit.get('too_large') is not False):
        fail('COMMIT_FILE_COMPLETENESS_NOT_ESTABLISHED')
    files = commit.get('files')
    compare_files = payload['compare']['files']
    if type(files) is not list or len(files) != len(compare_files):
        fail('COMMIT_FILE_COUNT_MISMATCH')
    expected = {item['filename'] for item in compare_files}
    observed = set()
    for item in files:
        if type(item) is not dict or type(item.get('filename')) is not str:
            fail('INVALID_COMMIT_FILE_ENTRY')
        name = item['filename']
        if name not in expected or name in observed or item.get('status') != 'added':
            fail('COMMIT_FILE_SET_MISMATCH')
        sha(item.get('sha'), 'COMMIT_FILE_BLOB')
        observed.add(name)
    if observed != expected:
        fail('COMMIT_FILE_SET_MISMATCH')
    result['state'] = 'PASS_MAIN_COMMIT_WITNESS_CONSISTENCY_C1'
    result['checked_commit_blobs'] = len(observed)
    result['api_origin_authenticated'] = False
    result['live_main_verified'] = False
    return result


def main():
    try:
        raw = sys.stdin.buffer.read(baseline.base.base.MAX_BYTES + 1)
        if len(raw) > baseline.base.base.MAX_BYTES:
            fail('INPUT_TOO_LARGE')
        payload = json.loads(raw.decode('utf-8'),
                             object_pairs_hook=baseline.base.base.unique_pairs,
                             parse_constant=baseline.base.base.finite_constant)
        print(json.dumps(audit(payload), sort_keys=True, separators=(',', ':')))
        return 0
    except (ValueError, TypeError, UnicodeError, RecursionError) as exc:
        print('FAIL_CLOSED: ' + str(exc), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
