"""C1 isolated structural CI-run identity guard; no GitHub API access or authentication.
Requires V2's unchanged seven-PR matrix, plus per-PR check-run identities.
"""
import json
import re
import runpy
import sys
from pathlib import Path

BASE = Path(__file__).with_name('alpha_publication_census_matrix_guard_v2_20261101.py')
V2_CHECK = runpy.run_path(str(BASE))['check']
HEX40 = re.compile(r'[0-9a-f]{40}\Z')
MAX_INPUT_BYTES = 4 * 1024 * 1024


def check(records):
    if not V2_CHECK(records):
        return False
    observed_ids = set()
    for record in records:
        head = record.get('pr_head_sha')
        if not isinstance(head, str) or HEX40.fullmatch(head) is None:
            return False
        runs = record.get('check_runs')
        if not isinstance(runs, list) or len(runs) != len(record['checks']):
            return False
        for run in runs:
            if not isinstance(run, dict):
                return False
            run_id = run.get('id')
            if type(run_id) is not int or run_id <= 0 or run_id in observed_ids:
                return False
            observed_ids.add(run_id)
            if run.get('head_sha') != head:
                return False
            if run.get('status') != 'completed' or run.get('conclusion') != 'success':
                return False
            if not isinstance(run.get('name'), str) or not run['name'].strip():
                return False
            if not isinstance(run.get('app_slug'), str) or not run['app_slug'].strip():
                return False
    return True


def unique_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('DUPLICATE_JSON_KEY')
        result[key] = value
    return result


def reject_constant(value):
    raise ValueError('NONFINITE_JSON_CONSTANT')


if __name__ == '__main__':
    try:
        raw = sys.stdin.buffer.read(MAX_INPUT_BYTES + 1)
        if len(raw) > MAX_INPUT_BYTES:
            raise ValueError('INPUT_TOO_LARGE')
        records = json.loads(raw.decode('utf-8'), object_pairs_hook=unique_keys,
                             parse_constant=reject_constant)
        accepted = check(records)
    except (ValueError, TypeError, RecursionError, UnicodeError):
        accepted = False
    print(json.dumps({'accepted': accepted,
                      'scope': 'SYNTHETIC_STRUCTURE_ONLY_NO_GITHUB_AUTHENTICATION'}))
