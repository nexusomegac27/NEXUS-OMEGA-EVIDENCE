"""C1 isolated V3 wrapper: fail closed on structurally incomplete check-run inventories.
Requires explicit page inventory; does NOT authenticate API provenance or rule enforcement.
V2 source is imported unchanged from the same research directory.
"""
import json
import sys

import alpha_ci_ruleset_required_absence_guard_v2_20261101 as prior

API_KIND = 'GITHUB_REST_CHECK_RUNS_V1'


def fail():
    result = prior.fail()
    result['inventory_complete_structural'] = False
    result['snapshot_scope'] = 'UNAUTHENTICATED_STRUCTURAL_ONLY'
    return result


def inventory_complete(data):
    if not isinstance(data, dict):
        return False
    runs, head, inventory = data.get('check_runs'), data.get('head_sha'), data.get('inventory')
    if not isinstance(runs, list) or not runs or not isinstance(inventory, dict):
        return False
    total, per_page, page_count = (inventory.get('total_count'), inventory.get('per_page'),
                                   inventory.get('page_count'))
    pages = inventory.get('ids_by_page')
    if (inventory.get('source_api') != API_KIND or inventory.get('head_sha') != head or
            inventory.get('next_page') is not None or inventory.get('complete') is not True):
        return False
    if (type(total) is not int or type(per_page) is not int or type(page_count) is not int or
            total <= 0 or not 1 <= per_page <= 100 or page_count <= 0):
        return False
    if not isinstance(pages, list) or len(pages) != page_count:
        return False
    if total != len(runs) or page_count != (total + per_page - 1) // per_page:
        return False
    flattened = []
    for index, page in enumerate(pages):
        if not isinstance(page, list) or not 1 <= len(page) <= per_page:
            return False
        if index < len(pages) - 1 and len(page) != per_page:
            return False
        if any(type(item) is not int or item <= 0 for item in page):
            return False
        flattened.extend(page)
    return flattened == [run.get('id') if isinstance(run, dict) else None for run in runs]


def evaluate(data):
    if not inventory_complete(data):
        return fail()
    result = prior.evaluate(data)
    result['inventory_complete_structural'] = result['status'] != 'NOT_COMPUTABLE'
    result['snapshot_scope'] = 'UNAUTHENTICATED_STRUCTURAL_ONLY'
    return result


def main():
    try:
        raw = sys.stdin.buffer.read(prior.MAX_BYTES + 1)
        if len(raw) > prior.MAX_BYTES:
            raise ValueError('INPUT_TOO_LARGE')
        data = json.loads(raw.decode('utf-8'), object_pairs_hook=prior.unique_pairs,
                          parse_constant=prior.reject_nonfinite, parse_float=prior.reject_nonfinite)
        result = evaluate(data)
    except (ValueError, TypeError, UnicodeError, OverflowError, RecursionError, KeyError):
        result = fail()
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
