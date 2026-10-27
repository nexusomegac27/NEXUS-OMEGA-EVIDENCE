"""Frozen independent C1 evaluator for cross-row portable path identity.

The evaluator is separate from the candidate. No network or repository mutation.
Usage: python alpha_pr124_crossrow_frozen_evaluator_v1_20261024.py candidate.py
"""
import copy
import importlib.util
import json
import sys
from pathlib import Path

PREFIX = 'research/r16/axiom-alpha-node-c1-adaptation-20261012/'

def rows(*names, count=None):
    doc = {'files': [{'path': PREFIX + name} for name in names]}
    if count is not None:
        doc['count'] = count
    return doc

# Frozen expectations, deliberately independent of the implementation.
FIXTURES = [
    ('positive_single', rows('Alpha.py'), 'PASS_C1', None),
    ('positive_distinct', rows('Alpha.py', 'Beta.py'), 'PASS_C1', None),
    ('positive_extensions', rows('Alpha.py', 'Alpha.md'), 'PASS_C1', None),
    ('positive_distinct_case', rows('A_1.py', 'a_2.py'), 'PASS_C1', None),
    ('positive_count', rows('A.py', 'B.py', count=2), 'PASS_C1', None),
    ('negative_casefold_simple', rows('Alpha.py', 'alpha.py'), 'FAIL_CLOSED', 'CASEFOLD_COLLISION'),
    ('negative_casefold_extension', rows('A.py', 'a.PY'), 'FAIL_CLOSED', 'CASEFOLD_COLLISION'),
    ('negative_casefold_readme', rows('Readme.MD', 'README.md'), 'FAIL_CLOSED', 'CASEFOLD_COLLISION'),
    ('negative_casefold_three', rows('ABC', 'abc', 'Abc'), 'FAIL_CLOSED', 'CASEFOLD_COLLISION'),
    ('negative_exact_duplicate', rows('A.py', 'A.py'), 'FAIL_CLOSED', 'DUPLICATE_EXACT'),
    ('negative_traversal', rows('../evil.py'), 'FAIL_CLOSED', 'INVALID_PATH'),
    ('negative_windows_reserved', rows('CON.txt'), 'FAIL_CLOSED', 'INVALID_PATH'),
    ('negative_trailing_dot', rows('foo.'), 'FAIL_CLOSED', 'INVALID_PATH'),
    ('negative_nonstring', {'files': [{'path': 7}]}, 'FAIL_CLOSED', 'INVALID_PATH'),
    ('negative_count', rows('A.py', count=2), 'FAIL_CLOSED', 'COUNT_MISMATCH'),
    ('negative_missing_files', {'count': 1}, 'FAIL_CLOSED', 'INVALID_CONTAINER'),
    ('negative_unicode', rows('straße.py'), 'FAIL_CLOSED', 'INVALID_PATH'),
    ('negative_long_basename', rows('A'*256+'.py'), 'FAIL_CLOSED', 'INVALID_PATH'),
    ('negative_nested_path', rows('subdir/A.py'), 'FAIL_CLOSED', 'INVALID_PATH'),
]

def evaluate(module):
    failures=[]
    for name, doc, status, reason in FIXTURES:
        before=copy.deepcopy(doc)
        a=module.check_manifest_paths(doc)
        b=module.check_manifest_paths(doc)
        if not isinstance(a, dict) or a.get('status') != status or (reason is not None and reason not in a.get('reason_codes', [])) or a != b or doc != before:
            failures.append({'fixture': name, 'expected_status': status, 'expected_reason': reason, 'observed': a})
    return {'passed': len(FIXTURES)-len(failures), 'total': len(FIXTURES), 'negative': sum(f[0].startswith('negative') for f in FIXTURES), 'casefold_negatives': 4, 'failures': failures}

if __name__ == '__main__':
    spec=importlib.util.spec_from_file_location('candidate_under_test',sys.argv[1])
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    result=evaluate(module)
    print(json.dumps(result,sort_keys=True))
    sys.exit(0 if result['passed']==result['total'] else 1)
