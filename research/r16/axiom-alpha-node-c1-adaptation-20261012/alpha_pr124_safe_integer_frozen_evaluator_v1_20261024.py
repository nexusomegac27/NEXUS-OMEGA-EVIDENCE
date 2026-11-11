"""Frozen independent subprocess oracle for V3->V4 integer-domain test.

Run: python EVALUATOR.py V3.py V4.py [HISTORICAL_MANIFEST.json]
The evaluator never imports the candidate or modifies the expected labels.
"""
import json
from concurrent.futures import ThreadPoolExecutor
import subprocess
import sys

P = 'research/r16/axiom-alpha-node-c1-adaptation-20261012/'
A = P + 'Alpha.py'
B = P + 'Beta.py'
BASE = '{"count":1,"files":[{"path":"' + A + '"}]}'


def add_top(literal):
    return BASE.replace('"files":', '"probe":' + literal + ',"files":', 1)


cases = [
    ('one_row', BASE, True),
    ('two_rows', json.dumps({'count': 2, 'files': [{'path': A}, {'path': B}]}), True),
    ('max_safe', add_top('9007199254740991'), True),
    ('min_safe', add_top('-9007199254740991'), True),
    ('zero', add_top('0'), True),
    ('nested_safe', BASE.replace('"path":', '"probe":9007199254740991,"path":', 1), True),
    ('float_finite', add_top('1e308'), True),
    ('overflow_plus', add_top('9007199254740992'), False),
    ('overflow_plus_one', add_top('9007199254740993'), False),
    ('overflow_minus', add_top('-9007199254740992'), False),
    ('huge_integer', add_top('123456789012345678901234567890'), False),
    ('nested_overflow', BASE.replace('"path":', '"probe":9007199254740993,"path":', 1), False),
    ('array_overflow', BASE.replace('"path":', '"probe":[0,9007199254740993],"path":', 1), False),
    ('deep_overflow', BASE.replace('"path":', '"probe":{"x":-9007199254740993},"path":', 1), False),
    ('casefold', json.dumps({'count': 2, 'files': [{'path': A}, {'path': P + 'alpha.py'}]}), False),
    ('duplicate_key', BASE.replace('"count":1', '"count":1,"count":1', 1), False),
    ('nonfinite', add_top('1e999'), False),
    ('count_mismatch', BASE.replace('"count":1', '"count":2', 1), False),
]


def run(target, data):
    p = subprocess.run([sys.executable, target], input=data, text=True,
                       capture_output=True, timeout=5)
    try:
        obj = json.loads(p.stdout)
        return p.returncode == 0 and obj['status'] == 'PASS_C1'
    except (ValueError, KeyError, TypeError):
        return False


def evaluate(target):
    with ThreadPoolExecutor(max_workers=12) as pool:
        actuals = list(pool.map(lambda case: run(target, case[1]), cases))
    return [{'name': name, 'expected': expected, 'actual': actual}
            for (name, data, expected), actual in zip(cases, actuals)]


def main():
    if len(sys.argv) not in (3, 4):
        raise SystemExit('Usage: evaluator.py V3.py V4.py [manifest.json]')
    before = evaluate(sys.argv[1])
    after = evaluate(sys.argv[2])
    correct = lambda rows: sum(row['expected'] == row['actual'] for row in rows)
    historical = 'NOT_RUN'
    if len(sys.argv) == 4:
        with open(sys.argv[3], encoding='utf-8') as f:
            original = f.read()
        historical = 'PASS' if run(sys.argv[2], original) else 'FAIL'
    result = {'total': len(cases), 'negative': sum(not x[2] for x in cases),
              'baseline_correct': correct(before), 'candidate_correct': correct(after),
              'baseline_errors': [r['name'] for r in before if r['expected'] != r['actual']],
              'candidate_errors': [r['name'] for r in after if r['expected'] != r['actual']],
              'historical': historical}
    print(json.dumps(result, sort_keys=True))
    return 0 if correct(after) == len(cases) and historical != 'FAIL' else 1


if __name__ == '__main__':
    sys.exit(main())
