#!/usr/bin/env python3
"""Isolated C1 additive-PR census guard; checks two caller-supplied API projections.

This program does NOT authenticate the GitHub transport, API pagination, or actors.
It intentionally supports only additive PRs with 1..100 files and linear base..head.
"""
import json
import re
import sys

SHA = re.compile(r'[0-9a-f]{40}\\Z')
PATH = re.compile(r'research/[a-z0-9_./-]+\\Z')
REPO = 'nexusomegac27/NEXUS-OMEGA-EVIDENCE'


def fail_if_not(condition, label):
    if not condition:
        raise ValueError(label)


def unique_pairs(pairs):
    d = {}
    for k, v in pairs:
        if k in d:
            raise ValueError('duplicate_json_key')
        d[k] = v
    return d


def valid_sha(x):
    return isinstance(x, str) and SHA.fullmatch(x) is not None


def valid_path(x):
    return (isinstance(x, str) and PATH.fullmatch(x) is not None
            and all(segment not in ('', '.', '..') for segment in x.split('/'))


def inventory(files, label, require_blob):
    fail_if_not(isinstance(files, list) and 0 < len(files) <= 100, label + '_size')
    out = {}
    for f in files:
        fail_if_not(isinstance(f, dict), label + '_entry')
        path = f.get('filename')
        fail_if_not(valid_path(path), label + '_path')
        fail_if_not(path not in out, label + '_duplicate')
        fail_if_not(f.get('status') == 'added', label + '_non_additive')
        if require_blob:
            fail_if_not(valid_sha(f.get('sha')), label + '_blob_sha')
        out[path] = f
    return out


def verify(x):
    fail_if_not(isinstance(x, dict) and x.get('schema_version') == '1'
                and x.get('repository') == REPO, 'envelope')
    pr, api, cmp, local = (x.get(k) for k in ('pr', 'api_file_listing', 'compare', 'local_preflight'))
    fail_if_not(all(isinstance(v, dict) for v in (pr, api, cmp, local)), 'sections')
    n, count, base, head = (pr.get(k) for k in ('number', 'changed_files', 'base_sha', 'head_sha'))
    fail_if_not(type(n) is int and n > 0 and type(count) is int and 0 < count <= 100
                and valid_sha(base) and valid_sha(head) and base != head, 'pr_scope')
    pages = api.get('pages')
    fail_if_not(isinstance(pages, list) and len(pages) == 2, 'page_count')
    first, terminal = pages
    fail_if_not(all(isinstance(p, dict) for p in pages), 'page_structure')
    root = f'https://api.github.com/repos/{REPO}/pulls/{n}/files?per_page=100&page='
    fail_if_not(first.get('page') == 1 and type(first.get('page')) is int
                and first.get('request_url') == root + '1'
                and terminal.get('page') == 2 and type(terminal.get('page')) is int
                and terminal.get('request_url') == root + '2'
                and terminal.get('items') == [], 'page_terminal')
    source = inventory(first.get('items'), 'pr_files', True)
    fail_if_not(len(source) == count, 'pr_files_count')
    fail_if_not(cmp.get('base_sha') == base and cmp.get('head_sha') == head
                and cmp.get('merge_base_sha') == base, 'compare_identity')
    fail_if_not(cmp.get('status') == 'ahead' and type(cmp.get('ahead_by')) is int
                and cmp['ahead_by'] > 0 and type(cmp.get('behind_by')) is int
                and cmp['behind_by'] == 0, 'compare_ancestry')
    comparison = inventory(cmp.get('files'), 'compare_files', False)
    fail_if_not(len(comparison) == count and set(comparison) == set(source), 'dual_endpoint_mismatch')
    fail_if_not(local.get('pr_number') == n and type(local.get('pr_number')) is int
                and local.get('head_sha') == head
                and local.get('status') == 'LOCAL_BYTES_MATCH_UNAUTHENTICATED_INPUT'
                and local.get('claim_ceiling') == 'C1_DESCRIPTIVE_ONLY', 'local_binding')
    local_files = local.get('changed_file_paths')
    fail_if_not(isinstance(local_files, list) and len(local_files) == count
                and all(valid_path(p) for p in local_files)
                and len(set(local_files)) == count and set(local_files) == set(source), 'local_file_set')
    fail_if_not(type(local.get('declared_changed_files')) is int
                and local['declared_changed_files'] == count, 'local_count')
    return {'status': 'DUAL_ENDPOINT_FILE_SET_MATCH_UNAUTHENTICATED_INPUT',
            'matched_files': count, 'pr_number': n, 'pr_head_sha': head,
            'api_transport_authenticated': False, 'pagination_authenticated': False,
            'actor_authenticated': False, 'original_bytes_rehashed_by_this_guard': False,
            'project_automation_rate': 'NOT_COMPUTABLE',
            'project_full_readback_rate': 'NOT_COMPUTABLE',
            'claim_ceiling': 'C1_DESCRIPTIVE_ONLY'}


def main():
    try:
        obj = json.loads(sys.stdin.read(), object_pairs_hook=unique_pairs,
                         parse_constant=lambda _: (_ for _ in ()).throw(ValueError('nonfinite_json')))
        result = verify(obj)
    except (ValueError, TypeError, KeyError, RecursionError) as exc:
        result = {'status': 'FAIL_CLOSED', 'reason': str(exc)[:120]}
    print(json.dumps(result, sort_keys=True))
    return 2 if result['status'] == 'FAIL_CLOSED' else 0


if __name__ == '__main__':
    sys.exit(main())
