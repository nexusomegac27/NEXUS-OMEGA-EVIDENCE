"""C1 isolated raw GitHub REST-shape adapter for the existing V3 CI inventory guard.

Read-only, one-page-only and fail-closed. This script does NOT perform an HTTP
request, authenticate input bytes, or attest a live GitHub merge policy.
"""
import json
import re
import sys

import alpha_ci_checkrun_inventory_completeness_guard_v3_20261101 as prior

REPO = 'nexusomegac27/NEXUS-OMEGA-EVIDENCE'
SHA = re.compile(r'^[0-9a-f]{40}$')


def fail():
    result = prior.fail()
    result['snapshot_scope'] = 'REST_SHAPED_INPUT_UNAUTHENTICATED_ONE_PAGE_ONLY'
    result['raw_rest_adapter'] = False
    return result


def normalize(data):
    if not isinstance(data, dict):
        return None
    head, ruleset, response, fetch = (data.get('head_sha'), data.get('ruleset_response'),
                                      data.get('check_runs_response'), data.get('fetch'))
    if not isinstance(head, str) or not SHA.fullmatch(head):
        return None
    if not all(isinstance(x, dict) for x in (ruleset, response, fetch)):
        return None
    expected_url = (f'https://api.github.com/repos/{REPO}/commits/{head}/check-runs'
                    '?per_page=100&page=1')
    if (fetch.get('url') != expected_url or fetch.get('page') != 1 or
            type(fetch.get('page')) is not int or fetch.get('per_page') != 100 or
            type(fetch.get('per_page')) is not int or fetch.get('next_page') is not None):
        return None
    total, raw_runs = response.get('total_count'), response.get('check_runs')
    if (type(total) is not int or not 1 <= total <= 100 or
            not isinstance(raw_runs, list) or len(raw_runs) != total):
        return None
    if (ruleset.get('id') != 21252293 or type(ruleset.get('id')) is not int or
            ruleset.get('enforcement') != 'active' or ruleset.get('target') != 'branch'):
        return None
    conditions, rules = ruleset.get('conditions'), ruleset.get('rules')
    if not isinstance(conditions, dict) or not isinstance(rules, list):
        return None
    ref_name = conditions.get('ref_name')
    if (not isinstance(ref_name, dict) or
            'refs/heads/main' not in ref_name.get('include', [])):
        return None
    required_rules = [x for x in rules if isinstance(x, dict) and x.get('type') == 'required_status_checks']
    if len(required_rules) != 1 or not isinstance(required_rules[0].get('parameters'), dict):
        return None
    required = required_rules[0]['parameters'].get('required_status_checks')
    if not isinstance(required, list):
        return None
    normalized = []
    for run in raw_runs:
        if not isinstance(run, dict) or not isinstance(run.get('app'), dict):
            return None
        normalized.append({'id': run.get('id'), 'name': run.get('name'),
                           'app_id': run['app'].get('id'), 'head_sha': run.get('head_sha'),
                           'status': run.get('status'), 'conclusion': run.get('conclusion')})
    return {'head_sha': head,
            'ruleset': {'enforcement': ruleset['enforcement'], 'target': ruleset['target'],
                        'include_refs': ref_name['include'], 'required_status_checks': required},
            'check_runs': normalized,
            'inventory': {'source_api': prior.API_KIND, 'head_sha': head,
                          'total_count': total, 'per_page': 100, 'page_count': 1,
                          'ids_by_page': [[run['id'] for run in normalized]],
                          'next_page': None, 'complete': True}}


def evaluate(data):
    normalized = normalize(data)
    if normalized is None:
        return fail()
    result = prior.evaluate(normalized)
    result['snapshot_scope'] = 'REST_SHAPED_INPUT_UNAUTHENTICATED_ONE_PAGE_ONLY'
    result['raw_rest_adapter'] = result['status'] != 'NOT_COMPUTABLE'
    return result


def main():
    try:
        raw = sys.stdin.buffer.read(prior.prior.MAX_BYTES + 1)
        if len(raw) > prior.prior.MAX_BYTES:
            raise ValueError('INPUT_TOO_LARGE')
        data = json.loads(raw.decode('utf-8'), object_pairs_hook=prior.prior.unique_pairs,
                          parse_constant=prior.prior.reject_nonfinite,
                          parse_float=prior.prior.reject_nonfinite)
        result = evaluate(data)
    except (ValueError, TypeError, UnicodeError, OverflowError, RecursionError, KeyError):
        result = fail()
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
