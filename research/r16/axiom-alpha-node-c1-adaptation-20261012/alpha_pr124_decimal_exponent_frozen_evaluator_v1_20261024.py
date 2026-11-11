"""Frozen independent subprocess oracle for structured JSON fail-closed behavior.

Checks CLI status, valid JSON stdout, return code, and positive/negative outcomes.
Never imports the candidate; old V6 and candidate are separate processes.
"""
import json
import subprocess
import sys

PREFIX = 'research/r16/axiom-alpha-node-c1-adaptation-20261012/'
ROW = {'path': PREFIX + 'Alpha.py', 'bytes': 42,
       'sha256': 'a' * 64, 'git_blob_sha1': 'b' * 40}

FLOAT_CASES = [
    ('ordinary_decimal', '0.1', True),
    ('fraction_exact', '1.25', True),
    ('small_scientific', '1e-7', True),
    ('large_scientific', '1e300', True),
    ('explicit_zero', '0.0', True),
    ('negative_zero', '-0.0', True),
    ('integer_float', '42.0', True),
    ('small_subnormal', '1e-320', True),
    ('underflow_positive', '1e-999', False),
    ('underflow_negative', '-1e-999', False),
    ('rounded_unit', '1.0000000000000001', False),
    ('rounded_fraction', '0.10000000000000001', False),
    ('unsafe_float_integer', '9007199254740993.0', False),
    ('unsafe_float_negative', '-9007199254740993.0', False),
    ('overflow_exponent', '1e999', False),
    ('decimal_exponent_too_large_negative', '1e-999999999999999999999', False),
    ('decimal_exponent_too_large_negative_signed', '-1e-999999999999999999999', False),
    ('decimal_exponent_too_large_positive', '1e999999999999999999999', False),
    ('decimal_exponent_too_large_nested', '1e-999999999999999999999', False),
]


def evaluate(script):
    failures = []
    for name, token, expected in FLOAT_CASES:
        prefix = '{"count":1,"files":' + json.dumps([ROW])
        if name.endswith('_nested'):
            raw = prefix + ',"metadata_probe":{"nested":' + token + '}}'
        else:
            raw = prefix + ',"metadata_probe":' + token + '}'
        proc = subprocess.run([sys.executable, script], input=raw,
                              text=True, capture_output=True, timeout=5)
        try:
            data = json.loads(proc.stdout)
            actual = data['status'] == 'PASS_C1'
            structured = (data['status'] in ('PASS_C1', 'FAIL_CLOSED')
                          and (proc.returncode == 0) == actual
                          and isinstance(data['reason_codes'], list))
        except (ValueError, TypeError, KeyError):
            actual, structured = False, False
        if actual != expected or not structured:
            failures.append(name)
    # Independent row-fixity regression; malformed source must be rejected.
    bad = dict(ROW)
    bad.pop('sha256')
    proc = subprocess.run([sys.executable, script], input=json.dumps(
        {'count': 1, 'files': [bad]}), text=True, capture_output=True, timeout=5)
    try:
        data = json.loads(proc.stdout)
        if data['status'] != 'FAIL_CLOSED' or proc.returncode != 1:
            failures.append('missing_sha256')
    except (ValueError, KeyError):
        failures.append('missing_sha256')
    return {'correct': 20 - len(failures), 'total': 20, 'failures': failures}


if __name__ == '__main__':
    print(json.dumps(evaluate(sys.argv[1]), sort_keys=True))
