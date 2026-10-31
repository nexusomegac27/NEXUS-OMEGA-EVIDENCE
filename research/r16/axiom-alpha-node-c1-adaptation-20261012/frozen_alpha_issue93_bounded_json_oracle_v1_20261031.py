#!/usr/bin/env python3
"""Frozen black-box C1 oracle: bounded stdin, recursion, and V3 preservation.

No import of candidate. Independent expected classifications. Synthetic only.
"""
import copy
import json
import subprocess
import sys

BASELINE, CANDIDATE = sys.argv[1:3]
LIMIT = 4 * 1024 * 1024


def fixture():
    item = {'id': 100, 'user': {'login': 'nexusomegac27'},
            'created_at': '2026-10-31T17:00:00Z',
            'updated_at': '2026-10-31T17:00:00Z', 'body': 'public receipt'}
    page = {'page': 1, 'per_page': 100, 'items': [item]}
    return {'schema_version': 'alpha_issue93_double_inventory_v1',
            'repository_full_name': 'nexusomegac27/NEXUS-OMEGA-EVIDENCE',
            'pre': {'issue_number': 93, 'comments': 1},
            'post': {'issue_number': 93, 'comments': 1},
            'passes': [[copy.deepcopy(page)], [copy.deepcopy(page)]]}


def encode(obj):
    return json.dumps(obj, ensure_ascii=True, separators=(',', ':')).encode('utf-8')


def padded(length):
    obj = fixture()
    obj['padding'] = ''
    base = encode(obj)
    assert length >= len(base)
    obj['padding'] = 'x' * (length - len(base))
    raw = encode(obj)
    assert len(raw) == length
    return raw


def classify(path, raw):
    proc = subprocess.run([sys.executable, path], input=raw,
                          capture_output=True, timeout=25)
    try:
        data = json.loads(proc.stdout.decode('utf-8'))
    except (UnicodeError, ValueError):
        return 'UNSTRUCTURED'
    if proc.returncode == 0 and data.get('status') == 'DOUBLE_INVENTORY_STABLE_NOT_ATOMIC':
        return 'ACCEPT'
    if proc.returncode == 2 and data.get('status') == 'FAIL_CLOSED':
        return 'REJECT'
    return 'UNSTRUCTURED'


def check(label, raw, expected):
    got = classify(CANDIDATE, raw)
    assert got == expected, (label, expected, got)
    print('PASS', label)


valid = fixture()
check('one_owner_receipt', encode(valid), 'ACCEPT')
empty = fixture()
empty['pre']['comments'] = empty['post']['comments'] = 0
empty['passes'] = [[], []]
check('empty_inventory', encode(empty), 'ACCEPT')
nonowner = fixture()
for p in nonowner['passes']:
    p[0]['items'][0]['user']['login'] = 'third-party-label'
check('nonowner_observed_not_authenticated', encode(nonowner), 'ACCEPT')
unicode_ok = fixture()
for p in unicode_ok['passes']:
    p[0]['items'][0]['body'] = 'Grüße 😀'
check('valid_unicode', encode(unicode_ok), 'ACCEPT')
finite = fixture()
finite['extra'] = 1e308
check('finite_float', encode(finite), 'ACCEPT')
check('exact_4mib_boundary', padded(LIMIT), 'ACCEPT')

check('oversized_plus_one', padded(LIMIT + 1), 'REJECT')
check('oversized_plus_100', padded(LIMIT + 100), 'REJECT')
deep = b'{"extra":' + b'[' * 1200 + b'0' + b']' * 1200 + b'}'
check('deep_json_parser_recursion', deep, 'REJECT')
check('deep_json_string_subtree', b'{"note":' + b'[' * 1100 + b'"x"' + b']' * 1100 + b'}', 'REJECT')
check('invalid_utf8', b'\xff', 'REJECT')
check('nonfinite_exponent', encode(valid)[:-1] + b',"extra":1e999}', 'REJECT')
check('unpaired_surrogate_extra', encode(valid)[:-1] + b',"extra":"\\ud800"}', 'REJECT')
check('duplicate_key', encode(valid)[:-1] + b',"pre":{}}', 'REJECT')
drift = fixture()
drift['post']['comments'] = 2
check('count_drift', encode(drift), 'REJECT')

assert classify(BASELINE, padded(LIMIT + 1)) == 'ACCEPT', 'baseline must accept oversize'
assert classify(BASELINE, deep) == 'UNSTRUCTURED', 'baseline recursion must be unstructured'
assert classify(BASELINE, encode(valid)) == 'ACCEPT', 'baseline positive must remain valid'
print('CANDIDATE=15/15; POSITIVE=6/6; NEGATIVE=9/9; BASELINE_OVERSIZE_FALSE_ACCEPT=1/1; BASELINE_RECURSION_UNSTRUCTURED=1/1')
