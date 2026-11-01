"""Frozen C1 evaluator: distinct check-run identities, not GitHub authentication.
Commit this file before the candidate. Usage:
python frozen_alpha_ci_run_identity_evaluator_v1_20261101.py PINNED_V2.py CANDIDATE.py
"""
import copy
import json
import runpy
import subprocess
import sys
from pathlib import Path

baseline_path, candidate_path = map(Path, sys.argv[1:3])
old = runpy.run_path(str(baseline_path))
records = []
for row_i, (pr, parent, main, receipt, count) in enumerate(old['CHAIN']):
    head = f'{row_i+1:040x}'  # SYNTHETIC, not an actual GitHub commit
    runs = [dict(id=1000000+row_i*8+j, name='validate', head_sha=head,
                 status='completed', conclusion='success', app_slug='github-actions')
            for j in range(8)]
    records.append(dict(pr=pr, parent=parent, main=main, receipt_id=receipt,
                        files=[dict(sha_match=True, blob_match=True, bytes_match=True) for _ in range(count)],
                        checks=['success']*8, additive=True, signature=True,
                        pr_head_sha=head, check_runs=runs))

def fixture(mutator):
    value = copy.deepcopy(records)
    mutator(value)
    return value

cases = [
 ('positive_distinct_ids_same_names', copy.deepcopy(records), True),
 ('duplicate_id_same_pr', fixture(lambda d:d[0]['check_runs'][1].update(id=d[0]['check_runs'][0]['id'])), False),
 ('duplicate_id_cross_pr', fixture(lambda d:d[1]['check_runs'][0].update(id=d[0]['check_runs'][0]['id'])), False),
 ('wrong_head', fixture(lambda d:d[2]['check_runs'][0].update(head_sha='f'*40)), False),
 ('missing_id', fixture(lambda d:d[3]['check_runs'][0].pop('id')), False),
 ('string_id', fixture(lambda d:d[4]['check_runs'][0].update(id='1000000')), False),
 ('zero_id', fixture(lambda d:d[5]['check_runs'][0].update(id=0)), False),
 ('missing_run_inventory', fixture(lambda d:d[6].pop('check_runs')), False),
 ('missing_one_run', fixture(lambda d:d[0]['check_runs'].pop()), False),
 ('pending_run', fixture(lambda d:d[1]['check_runs'][0].update(status='queued')), False),
 ('failed_run', fixture(lambda d:d[2]['check_runs'][0].update(conclusion='failure')), False),
 ('empty_name', fixture(lambda d:d[3]['check_runs'][0].update(name='')), False),
 ('empty_app_slug', fixture(lambda d:d[4]['check_runs'][0].update(app_slug='')), False),
 ('malformed_pr_head', fixture(lambda d:d[5].update(pr_head_sha='z'*40)), False),
 ('missing_pr_head', fixture(lambda d:d[6].pop('pr_head_sha')), False),
]

results = []
for name, data, expected in cases:
    baseline = old['check'](data)
    p = subprocess.run([sys.executable, str(candidate_path)], input=json.dumps(data),
                       text=True, capture_output=True, timeout=10, check=False)
    try:
        result = json.loads(p.stdout)['accepted']
    except (ValueError, KeyError, TypeError):
        result = None
    passed = p.returncode == 0 and type(result) is bool and result == expected
    results.append(dict(case=name, expected=expected, baseline=baseline,
                        candidate=result, passed=passed))

summary = dict(total=len(results), passed=sum(x['passed'] for x in results),
               negative_total=sum(not x['expected'] for x in results),
               baseline_false_accepts=sum(x['baseline'] and not x['expected'] for x in results),
               candidate_false_accepts=sum(x['candidate'] is True and not x['expected'] for x in results),
               results=results, scope='SYNTHETIC_STRUCTURE_ONLY_NO_GITHUB_AUTHENTICATION')
print(json.dumps(summary, sort_keys=True))
assert all(x['passed'] for x in results), 'FROZEN_ORACLE_FAILED'
