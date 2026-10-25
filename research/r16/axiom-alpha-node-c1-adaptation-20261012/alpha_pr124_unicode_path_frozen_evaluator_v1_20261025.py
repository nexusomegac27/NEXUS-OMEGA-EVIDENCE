#!/usr/bin/env python3
"""Independent, frozen C1 black-box oracle for Unicode path preflight.

Only isolated synthetic fixtures. Does not authenticate GitHub paths, certify
production portability, authorize a merge or change the original Run142 oracle.
"""
import importlib.util
import sys

ROOT = 'research/r16/axiom-alpha-node-c1-adaptation-20261012/'
SHA = 'a' * 64
BLOB = 'b' * 40

def row(s):
    return {'path': ROOT + s, 'bytes': 1, 'sha256': SHA, 'git_blob_sha1': BLOB}

def fixture(names):
    rows = [row(s) for s in names]
    return ([{'name': 'historical', 'files': rows}], [r['path'] for r in rows])

# Explicitly defined independently of candidate implementation.
CASES = [
    ('ascii', ['alpha.py'], 'COMPLETE_C1'),
    ('ascii_nested', ['one/a.py', 'two/b.py'], 'COMPLETE_C1'),
    ('nfc_accent', ['caf\u00e9.py'], 'COMPLETE_C1'),
    ('emoji_nfc', ['emoji_\U0001f600.py'], 'COMPLETE_C1'),
    ('two_nfc_distinct', ['caf\u00e9.py', 'caf\u00e8.py'], 'COMPLETE_C1'),
    ('lone_high_surrogate', ['bad_\ud800.py'], 'FAIL_CLOSED'),
    ('lone_low_surrogate', ['bad_\udfff.py'], 'FAIL_CLOSED'),
    ('nfd_decomposed', ['cafe\u0301.py'], 'FAIL_CLOSED'),
    ('nfd_combining_ring', ['a\u030a.py'], 'FAIL_CLOSED'),
    ('nfc_nfd_collision', ['caf\u00e9.py', 'cafe\u0301.py'], 'FAIL_CLOSED'),
    ('mixed_nfc_nfd', ['valid.py', 'cafe\u0301.py'], 'FAIL_CLOSED'),
    ('high_surrogate_nested', ['nested/bad_\ud800.py'], 'FAIL_CLOSED'),
]

def run(module_path):
    spec = importlib.util.spec_from_file_location('subject_under_test', module_path)
    subject = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(subject)
    result = []
    for name, names, expected in CASES:
        groups, current = fixture(names)
        try:
            actual = subject.audit_inventory(groups, current)
            status = actual.get('status') if isinstance(actual, dict) else 'MALFORMED'
            caveats = isinstance(actual, dict) and actual.get('source_authentication') == 'NOT_ESTABLISHED' and actual.get('project_automation_rate') == 'NOT_COMPUTABLE' and actual.get('claim_ceiling') == 'C1_DESCRIPTIVE_ONLY'
        except BaseException as exc:
            status = 'UNCAUGHT_' + type(exc).__name__
            caveats = False
        result.append((name, expected, status, expected == status and caveats))
    for name, expected, actual, ok in result:
        print(f'{name}: {actual} expected={expected} pass={ok}')
    print('SUMMARY', sum(r[3] for r in result), '/', len(result))
    return 0 if all(r[3] for r in result) else 1

if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('Usage: evaluator.py CANDIDATE.py')
    raise SystemExit(run(sys.argv[1]))
