#!/usr/bin/env python3
"""Frozen black-box oracle for Issue93 JSON Unicode scalar validity; synthetic only."""
import copy
import json
import subprocess
import sys

BASELINE, CANDIDATE = sys.argv[1:3]


def fixture():
    item = {'id': 1234, 'user': {'login': 'nexusomegac27'},
            'created_at': '2026-10-31T17:00:00Z',
            'updated_at': '2026-10-31T17:00:00Z', 'body': 'public receipt'}
    page = {'page': 1, 'per_page': 100, 'items': [item]}
    return {'schema_version': 'alpha_issue93_double_inventory_v1',
            'repository_full_name': 'nexusomegac27/NEXUS-OMEGA-EVIDENCE',
            'pre': {'issue_number': 93, 'comments': 1},
            'post': {'issue_number': 93, 'comments': 1},
            'passes': [[copy.deepcopy(page)], [copy.deepcopy(page)]]}


def classify(target, obj):
    raw = json.dumps(obj, ensure_ascii=True, separators=(',', ':'))
    proc = subprocess.run([sys.executable, target], input=raw, text=True,
                          capture_output=True, timeout=10)
    try:
        output = json.loads(proc.stdout)
    except ValueError:
        return 'UNSTRUCTURED'
    if proc.returncode == 0 and output.get('status') == 'DOUBLE_INVENTORY_STABLE_NOT_ATOMIC':
        return 'ACCEPT'
    if proc.returncode == 2 and output.get('status') == 'FAIL_CLOSED':
        return 'REJECT'
    return 'UNSTRUCTURED'


def check(name, obj, expected):
    actual = classify(CANDIDATE, obj)
    assert actual == expected, (name, expected, actual)
    print('PASS', name)


x = fixture()
check('valid_ascii', x, 'ACCEPT')
y = copy.deepcopy(x)
for p in y['passes']:
    p[0]['items'][0]['body'] = 'Grüße 😀'
check('valid_unicode_scalar', y, 'ACCEPT')
y = copy.deepcopy(x); y['note'] = '𝄞'
check('valid_extra_unicode_scalar', y, 'ACCEPT')
y = copy.deepcopy(x); y['extra'] = 1.25
check('valid_finite_float', y, 'ACCEPT')
y = copy.deepcopy(x); y['extra'] = 1e308
check('valid_large_finite_float', y, 'ACCEPT')

negative = []
for name, character in [('high_surrogate', '\ud800'), ('low_surrogate', '\udc00'),
                        ('last_surrogate', '\udfff')]:
    y = copy.deepcopy(x)
    for p in y['passes']:
        p[0]['items'][0]['body'] = 'x' + character
    negative.append(('body_'+name, y))
y = copy.deepcopy(x)
for p in y['passes']:
    p[0]['items'][0]['user']['login'] = 'agent\ud800'
negative.append(('actor_surrogate', y))
y = copy.deepcopy(x); y['note'] = 'surrogate\udc00'
negative.append(('extra_value_surrogate', y))
y = copy.deepcopy(x); y['bad\ud800key'] = 'safe'
negative.append(('extra_key_surrogate', y))
y = copy.deepcopy(x); y['passes'][0][0]['items'][0]['body'] = '\ud800'
negative.append(('single_pass_surrogate', y))
for name, obj in negative:
    check(name, obj, 'REJECT')

assert classify(BASELINE, negative[0][1]) == 'REJECT', 'V2 already rejects invalid surrogate in digest-bearing body'
assert classify(BASELINE, negative[4][1]) == 'ACCEPT', 'V2 must accept ignored surrogate extra field'
assert classify(BASELINE, negative[5][1]) == 'ACCEPT', 'V2 must accept ignored surrogate key'
print('CANDIDATE=12/12; NEGATIVES=7/7; BASELINE_FALSE_ACCEPT=2/2; BASELINE_BODY_REJECT=1/1')
