"""Frozen independent subprocess evaluator: JSON recursion must fail closed with a structured response.

No candidate imports, no network, no repository mutations. Tests identical inputs for V7 and successor.
"""
import json
import subprocess
import sys

PREFIX = 'research/r16/axiom-alpha-node-c1-adaptation-20261012/'
ROW = {'path': PREFIX + 'Alpha.py', 'bytes': 42,
       'sha256': 'a' * 64, 'git_blob_sha1': 'b' * 40}
BASE = json.dumps({'count': 1, 'files': [ROW]}, separators=(',', ':'))


def nested(depth):
    return BASE[:-1] + ',"metadata_probe":' + '[' * depth + '0' + ']' * depth + '}'


CASES = [
    ('positive_depth_1', nested(1), True),
    ('positive_depth_16', nested(16), True),
    ('positive_depth_64', nested(64), True),
    ('positive_depth_128', nested(128), True),
    ('negative_depth_10000', nested(10000), False),
    ('negative_depth_15000', nested(15000), False),
    ('negative_depth_20000', nested(20000), False),
    ('negative_missing_sha', json.dumps({'count': 1, 'files': [{k:v for k,v in ROW.items() if k!='sha256'}]}), False),
    ('negative_duplicate_key', BASE[:-1] + ',"count":1}', False),
]


def evaluate(script):
    errors = []
    outcomes = []
    for name, raw, expected_pass in CASES:
        proc = subprocess.run([sys.executable, script], input=raw,
                              text=True, capture_output=True, timeout=6)
        try:
            result = json.loads(proc.stdout)
            actual_pass = result.get('status') == 'PASS_C1'
            structured = (result.get('status') in ('PASS_C1', 'FAIL_CLOSED')
                          and isinstance(result.get('reason_codes'), list)
                          and (proc.returncode == 0) == actual_pass)
        except (ValueError, TypeError, KeyError):
            actual_pass, structured = False, False
        correct = actual_pass == expected_pass and structured
        outcomes.append({'name': name, 'correct': correct,
                         'structured': structured, 'returncode': proc.returncode})
        if not correct:
            errors.append(name)
    return {'correct': len(CASES)-len(errors), 'total': len(CASES),
            'negative_total': sum(not c[2] for c in CASES),
            'positive_total': sum(c[2] for c in CASES),
            'errors': errors, 'outcomes': outcomes}


if __name__ == '__main__':
    print(json.dumps(evaluate(sys.argv[1]), sort_keys=True))
