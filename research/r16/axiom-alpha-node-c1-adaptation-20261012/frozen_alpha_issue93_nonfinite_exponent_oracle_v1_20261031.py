#!/usr/bin/env python3
"""Frozen independent subprocess oracle: reject overflow exponent JSON anywhere."""
import json
import subprocess
import sys

BASELINE, CANDIDATE = sys.argv[1:3]

base = ('{"schema_version":"alpha_issue93_double_inventory_v1",'
        '"repository_full_name":"nexusomegac27/NEXUS-OMEGA-EVIDENCE",'
        '"pre":{"issue_number":93,"comments":0},'
        '"post":{"issue_number":93,"comments":0},"passes":[[],[]]')


def payload(extra):
    return base + extra + '}'


def run(target, raw):
    p = subprocess.run([sys.executable, target], input=raw,
                       capture_output=True, text=True, timeout=10)
    try:
        data = json.loads(p.stdout)
    except ValueError:
        return 'UNSTRUCTURED'
    if p.returncode == 0 and data.get('status') == 'DOUBLE_INVENTORY_STABLE_NOT_ATOMIC':
        return 'ACCEPT'
    if p.returncode == 2 and data.get('status') == 'FAIL_CLOSED':
        return 'REJECT'
    return 'UNSTRUCTURED'


positive = [('', 'valid_empty'), (',"extra":1.25', 'finite_float'),
            (',"extra":1e308', 'finite_large'),
            (',"extra":"😀"', 'unicode_scalar')]
negative = [(',"extra":1e999', 'positive_overflow'),
            (',"extra":-1e999', 'negative_overflow'),
            (',"extra":NaN', 'nan'),
            (',"extra":Infinity', 'infinity'),
            (',"extra":1e999,"extra":2', 'duplicate_key')]
for suffix, name in positive:
    assert run(CANDIDATE, payload(suffix)) == 'ACCEPT', name
    print('PASS_POSITIVE', name)
for suffix, name in negative:
    assert run(CANDIDATE, payload(suffix)) == 'REJECT', name
    print('PASS_NEGATIVE', name)
for suffix, name in negative[:2]:
    assert run(BASELINE, payload(suffix)) == 'ACCEPT', ('baseline_counterexample', name)
    print('BASELINE_FALSE_ACCEPT', name)
assert run(BASELINE, payload('')) == 'ACCEPT'
print('ORACLE_CANDIDATE=9/9;BASELINE_OVERFLOW_FALSE_ACCEPT=2/2')
