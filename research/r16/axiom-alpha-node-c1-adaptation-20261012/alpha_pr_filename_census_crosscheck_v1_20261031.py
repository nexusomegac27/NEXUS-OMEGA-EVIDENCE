#!/usr/bin/env python3
"""C1 isolated guard: compare PR paginated filename inventory with a local preflight.

The supplied API projection is not independently authenticated by this program.
"""
import json
import re
import sys

SHA = re.compile(r'[0-9a-f]{40}\Z')
PATH = re.compile(r'research/[a-z0-9_./-]+\Z')
REPO = 'nexusomegac27/NEXUS-OMEGA-EVIDENCE'


def unique_pairs(pairs):
    out = {}
    for key, value in pairs:
        if key in out:
            raise ValueError('duplicate_json_key')
        out[key] = value
    return out


def require(ok, reason):
    if not ok:
        raise ValueError(reason)


def check_paths(paths, label):
    require(isinstance(paths, list) and len(paths) > 0, label + '_missing')
    require(all(isinstance(p, str) and PATH.fullmatch(p)
                and all(x not in ('', '.', '..') for x in p.split('/')) for p in paths), label + '_invalid')
    require(len(set(paths)) == len(paths), label + '_duplicates')
    return set(paths)


def verify(x):
    require(isinstance(x, dict) and x.get('schema_version') == '1' and x.get('repository') == REPO, 'envelope')
    pr, api, local = x.get('pr'), x.get('api_file_listing'), x.get('local_preflight')
    require(all(isinstance(v, dict) for v in (pr, api, local)), 'sections')
    number, head, count = pr.get('number'), pr.get('head_sha'), pr.get('changed_files')
    require(type(number) is int and number > 0 and isinstance(head, str) and SHA.fullmatch(head), 'pr_identity')
    require(type(count) is int and count > 0, 'pr_file_count')
    require(api.get('all_pages_fetched') is True and api.get('next_cursor') is None
            and type(api.get('page_count')) is int and api['page_count'] > 0, 'pagination_incomplete')
    source = check_paths(api.get('filenames'), 'api')
    declared = check_paths(local.get('changed_file_paths'), 'local')
    require(len(source) == count, 'api_count_mismatch')
    require(local.get('pr_number') == number and type(local.get('pr_number')) is int
            and local.get('head_sha') == head, 'preflight_pr_mismatch')
    require(local.get('status') == 'LOCAL_BYTES_MATCH_UNAUTHENTICATED_INPUT'
            and local.get('claim_ceiling') == 'C1_DESCRIPTIVE_ONLY', 'preflight_status_or_ceiling')
    require(type(local.get('declared_changed_files')) is int
            and local['declared_changed_files'] == len(declared), 'local_count_mismatch')
    require(source == declared, 'file_set_mismatch')
    return {'status': 'API_FILENAME_CENSUS_MATCH_UNAUTHENTICATED_PROJECTION',
            'matched_files': len(source), 'pr_number': number, 'pr_head_sha': head,
            'api_transport_authenticated': False, 'pagination_authenticated': False,
            'original_bytes_rehashed_by_this_guard': False,
            'complete_api_changed_file_census': 'NOT_ESTABLISHED',
            'project_full_readback_rate': 'NOT_COMPUTABLE', 'claim_ceiling': 'C1_DESCRIPTIVE_ONLY'}


def main():
    try:
        x = json.loads(sys.stdin.read(), object_pairs_hook=unique_pairs,
                       parse_constant=lambda _: (_ for _ in ()).throw(ValueError('nonfinite_json')))
        result = verify(x)
    except (ValueError, TypeError, KeyError, RecursionError) as exc:
        result = {'status': 'FAIL_CLOSED', 'reason': str(exc)[:120]}
    print(json.dumps(result, sort_keys=True))
    return 2 if result['status'] == 'FAIL_CLOSED' else 0

if __name__ == '__main__':
    sys.exit(main())
