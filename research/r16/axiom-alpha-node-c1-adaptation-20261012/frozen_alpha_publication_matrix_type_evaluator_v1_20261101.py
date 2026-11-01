"""Frozen independent subprocess evaluator. Evaluates C1 matrix structure, not GitHub originals.
Usage: python frozen_alpha_publication_matrix_type_evaluator_v1_20261101.py ORIGINAL.py CANDIDATE.py
"""
import copy
import json
import runpy
import subprocess
import sys
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

original_path, candidate_path = map(Path, sys.argv[1:3])
with redirect_stdout(StringIO()):
    original = runpy.run_path(str(original_path))
base = original['base']

def fixture(mutator):
    data = copy.deepcopy(base)
    mutator(data)
    return data

cases = {
    'positive_unchanged': (copy.deepcopy(base), True),
    'existing_bad_sha': (fixture(lambda d: d[2]['files'][0].update(sha_match=False)), False),
    'existing_missing_receipt': (fixture(lambda d: d[3].update(receipt_id=None)), False),
    'existing_failed_ci': (fixture(lambda d: d[4]['checks'].__setitem__(7,'failure')), False),
    'existing_broken_parent': (fixture(lambda d: d[5].update(parent='0'*40)), False),
    'existing_historical_rewrite': (fixture(lambda d: d[6].update(additive=False)), False),
    'missing_sha_key': (fixture(lambda d: d[0]['files'][0].pop('sha_match')), False),
    'missing_blob_key': (fixture(lambda d: d[1]['files'][0].pop('blob_match')), False),
    'missing_bytes_key': (fixture(lambda d: d[2]['files'][0].pop('bytes_match')), False),
    'empty_file_claim': (fixture(lambda d: d[3]['files'].__setitem__(0, {})), False),
    'string_false_sha': (fixture(lambda d: d[4]['files'][0].update(sha_match='false')), False),
    'string_false_additive': (fixture(lambda d: d[5].update(additive='false')), False),
    'string_false_signature': (fixture(lambda d: d[6].update(signature='false')), False),
}
results = []
for name, (records, expected) in cases.items():
    baseline = bool(original['check'](records))
    proc = subprocess.run([sys.executable, str(candidate_path)], input=json.dumps(records), text=True,
                          capture_output=True, timeout=10, check=False)
    try:
        parsed = json.loads(proc.stdout)
        actual = parsed['accepted']
    except Exception:
        actual = 'INVALID_OUTPUT'
    ok = (proc.returncode == 0 and type(actual) is bool and actual == expected)
    results.append({'case':name, 'expected':expected, 'v1':baseline, 'v2':actual, 'pass':ok})
print(json.dumps({'source':'PINNED_V1_SHA256_96b2b69f0ebb201ea4289c08908d8133e0caf67a5acb704bfefefbe123d74995',
                  'results':results, 'passed':sum(r['pass'] for r in results), 'total':len(results),
                  'negative_count':sum(not expected for _,expected in cases.values()),
                  'v1_false_accepts':sum((not expected and original['check'](records)) for records,expected in cases.values()),
                  'scope':'STRUCTURAL_MATRIX_ONLY_NOT_GITHUB_BYTE_REHASH'}, sort_keys=True))
assert all(r['pass'] for r in results), 'CANDIDATE_FAILED_FROZEN_EVALUATOR'
