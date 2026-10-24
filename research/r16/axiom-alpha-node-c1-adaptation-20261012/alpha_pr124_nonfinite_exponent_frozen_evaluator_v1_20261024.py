"""Frozen independent C1 subprocess evaluator for cross-row JSON numeric-domain handling.

Fixture oracle is fixed before candidate V3. The evaluator never imports or edits
candidate code and cannot authorize promotion, merging, or deployment.
Usage: python alpha_pr124_nonfinite_exponent_frozen_evaluator_v1_20261024.py TARGET.py [HISTORICAL_MANIFEST.json]
"""
import json
import subprocess
import sys

PREFIX = 'research/r16/axiom-alpha-node-c1-adaptation-20261012/'
A = PREFIX + 'Alpha.py'
B = PREFIX + 'Beta.py'


def make(rows=None, **extra):
    rows = rows if rows is not None else [{'path': A}]
    return json.dumps({'count': len(rows), 'files': rows, **extra}, separators=(',', ':'))


base = make()
needle = '"files":'


def insert_top_numeric(literal):
    return base.replace(needle, '"numeric_probe":' + literal + ',' + needle, 1)


cases = [
    ('valid_one_row', base, True),
    ('valid_two_rows', make([{'path': A}, {'path': B}]), True),
    ('valid_finite_fraction', insert_top_numeric('0.125'), True),
    ('valid_finite_exponent', insert_top_numeric('1e308'), True),
    ('valid_finite_negative_exponent', insert_top_numeric('-3.5e10'), True),
    ('valid_finite_underflow', insert_top_numeric('1e-999'), True),
    ('valid_nested_finite', make([{'path': A, 'measurement': 2.5}]), True),
    ('valid_nested_array', make([{'path': A, 'measurement': [0.125, 1000]}]), True),
    ('overflow_top_positive', insert_top_numeric('1e999'), False),
    ('overflow_top_negative', insert_top_numeric('-1e999'), False),
    ('overflow_uppercase', insert_top_numeric('1E+999'), False),
    ('overflow_fraction', insert_top_numeric('9.99e999'), False),
    ('overflow_nested_row', make([{'path': A}]).replace('"path":', '"measurement":1e999,"path":', 1), False),
    ('overflow_nested_list', make([{'path': A}]).replace('"path":', '"measurement":[0,1e999],"path":', 1), False),
    ('overflow_second_row', make([{'path': A}, {'path': B}]).replace('"path":"' + B + '"}', '"path":"' + B + '","measurement":-1e999}'), False),
    ('overflow_nested_object', make([{'path': A}]).replace('"path":', '"measurement":{"x":1e999},"path":', 1), False),
    ('duplicate_top_key', base.replace('"count":1', '"count":1,"count":1', 1), False),
    ('duplicate_nested_key', base.replace('"path":', '"path":"' + A + '","path":', 1), False),
    ('casefold_collision', make([{'path': A}, {'path': PREFIX + 'alpha.py'}]), False),
    ('exact_duplicate', make([{'path': A}, {'path': A}]), False),
    ('invalid_path', make([{'path': PREFIX + 'CON.txt'}]), False),
    ('count_mismatch', base.replace('"count":1', '"count":2', 1), False),
    ('literal_nan', insert_top_numeric('NaN'), False),
    ('literal_infinity', insert_top_numeric('Infinity'), False),
]


def run(target, payload):
    completed = subprocess.run([sys.executable, target], input=payload,
                               text=True, capture_output=True, timeout=5)
    try:
        result = json.loads(completed.stdout)
        observed = result.get('status') == 'PASS_C1' and completed.returncode == 0
    except (ValueError, TypeError, AttributeError):
        observed = False
    return observed, completed.returncode


def main():
    if len(sys.argv) not in (2, 3):
        raise SystemExit('Usage: evaluator.py TARGET.py [HISTORICAL_MANIFEST.json]')
    target = sys.argv[1]
    failures = []
    positives = negatives = 0
    for name, payload, expected in cases:
        observed, code = run(target, payload)
        positives += int(expected)
        negatives += int(not expected)
        if observed != expected:
            failures.append({'fixture': name, 'expected_pass': expected,
                             'observed_pass': observed, 'exit_code': code})
    historical = 'NOT_RUN'
    if len(sys.argv) == 3:
        with open(sys.argv[2], encoding='utf-8') as f:
            payload = f.read()
        observed, code = run(target, payload)
        historical = 'PASS' if observed and code == 0 else 'FAIL'
        if historical == 'FAIL':
            failures.append({'fixture': 'historical_original_manifest',
                             'expected_pass': True, 'observed_pass': observed, 'exit_code': code})
    print(json.dumps({'fixture_total': len(cases), 'positive_total': positives,
                      'negative_total': negatives, 'correct': len(cases) - len(failures),
                      'historical': historical, 'failures': failures}, sort_keys=True))
    return 0 if not failures else 1


if __name__ == '__main__':
    raise SystemExit(main())
