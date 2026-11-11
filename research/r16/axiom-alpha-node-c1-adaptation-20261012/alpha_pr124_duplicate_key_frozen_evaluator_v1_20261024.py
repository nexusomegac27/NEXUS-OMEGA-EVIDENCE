"""Frozen independent CLI evaluator: reject duplicate JSON object keys at every depth.

Evaluator contract: pass raw JSON bytes to a separate candidate process. The oracle
is a fixed table of expected exit statuses and descriptive codes, not candidate logic.
No repository or network writes. Usage: python this_file.py candidate.py
"""
import json
import subprocess
import sys

P = 'research/r16/axiom-alpha-node-c1-adaptation-20261012/'
GOOD = '{"files":[{"path":"'+P+'Alpha.py"}]}'
GOOD_TWO = '{"files":[{"path":"'+P+'Alpha.py"},{"path":"'+P+'Beta.py"}],"count":2}'
BAD_CASE = '{"files":[{"path":"'+P+'Alpha.py"},{"path":"'+P+'alpha.py"}]}'
FIXTURES = [
    ('positive_single', GOOD, 0, 'PASS_C1'),
    ('positive_two_count', GOOD_TWO, 0, 'PASS_C1'),
    ('positive_nested_distinct', '{"files":[{"path":"'+P+'Alpha.py","note":{"a":1,"b":2}}]}', 0, 'PASS_C1'),
    ('positive_same_key_different_objects', '{"files":[{"path":"'+P+'A.py"},{"path":"'+P+'B.py"}]}', 0, 'PASS_C1'),
    ('negative_duplicate_files', '{"files":[],"files":[{"path":"'+P+'A.py"}]}', 1, 'FAIL_CLOSED'),
    ('negative_duplicate_count', '{"count":999,"count":1,"files":[{"path":"'+P+'A.py"}]}', 1, 'FAIL_CLOSED'),
    ('negative_duplicate_row_path', '{"files":[{"path":"'+P+'CON.txt","path":"'+P+'A.py"}]}', 1, 'FAIL_CLOSED'),
    ('negative_duplicate_nested_metadata', '{"files":[{"path":"'+P+'A.py","meta":{"x":1,"x":2}}]}', 1, 'FAIL_CLOSED'),
    ('negative_duplicate_same_value', '{"files":[{"path":"'+P+'A.py","path":"'+P+'A.py"}]}', 1, 'FAIL_CLOSED'),
    ('negative_casefold', BAD_CASE, 1, 'FAIL_CLOSED'),
    ('negative_bad_path', '{"files":[{"path":"'+P+'CON.txt"}]}', 1, 'FAIL_CLOSED'),
    ('negative_nonfinite', '{"files":[{"path":"'+P+'A.py"}],"count":NaN}', 1, 'FAIL_CLOSED'),
    ('negative_truncated', '{"files":[', 1, 'FAIL_CLOSED'),
]

def evaluate(path):
    bad = []
    for name, raw, exit_expected, status_expected in FIXTURES:
        run = subprocess.run([sys.executable, path], input=raw.encode('utf-8'), capture_output=True, timeout=5)
        try:
            payload = json.loads(run.stdout.decode('utf-8'))
            status = payload.get('status')
            reasons = payload.get('reason_codes', [])
        except (ValueError, UnicodeDecodeError, AttributeError):
            status = None
            reasons = []
        need_invalid_json = name.startswith('negative_duplicate') or name in ('negative_nonfinite', 'negative_truncated')
        if run.returncode != exit_expected or status != status_expected or (need_invalid_json and 'INVALID_JSON' not in reasons):
            bad.append({'fixture':name,'returncode':run.returncode,'status':status})
    return {'total':len(FIXTURES),'passed':len(FIXTURES)-len(bad),'negative':sum(n.startswith('negative') for n,_,_,_ in FIXTURES),'failures':bad}

if __name__ == '__main__':
    print(json.dumps(evaluate(sys.argv[1]), sort_keys=True))
