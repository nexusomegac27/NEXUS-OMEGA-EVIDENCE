"""C1 research-only successor: bind check-run names and apps to a frozen seven-PR cohort.
Not an authenticated GitHub API reader, branch protection evaluator, or general CI policy.
"""
from collections import Counter
import json
import runpy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
V1 = ROOT / 'alpha_publication_ci_run_identity_guard_v1_20261101.py'
V1_CHECK = runpy.run_path(str(V1))['check']
EXPECTED = Counter({
    ('nexus-preentry-lab', 'github-actions'): 1,
    ('r27e-external-structural-firewall', 'github-actions'): 1,
    ('validate', 'github-actions'): 4,
    ('validate-repository-structure', 'github-actions'): 1,
    ('semgrep-cloud-platform/scan', 'semgrep-code-nexusomegac27'): 1,
})
MAX_INPUT_BYTES = 4 * 1024 * 1024


def check(records):
    if not V1_CHECK(records):
        return False
    for record in records:
        actual = Counter((run['name'], run['app_slug']) for run in record['check_runs'])
        if actual != EXPECTED:
            return False
    return True


def unique_keys(pairs):
    out = {}
    for key, value in pairs:
        if key in out:
            raise ValueError('DUPLICATE_JSON_KEY')
        out[key] = value
    return out


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
                      'scope': 'FROZEN_SEVEN_PR_COHORT_SYNTHETIC_STRUCTURE_ONLY'}))
