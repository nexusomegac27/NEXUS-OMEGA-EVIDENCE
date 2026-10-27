#!/usr/bin/env python3
"""Independent, frozen C1 black-box evaluator for path display spoofing.

Fixture expectations are specified independently of the candidate. This is a
synthetic-only check, not a GitHub source authentication or OS portability proof.
"""
import importlib.util
import sys

ROOT = 'research/r16/axiom-alpha-node-c1-adaptation-20261012/'
SHA256 = 'a' * 64
BLOB = 'b' * 40

# Fixed before candidate implementation. Explicitly scoped Cc, Zl, Zp and bidi
# direction controls. Format chars not on the bidi denylist are not excluded.
CASES = [
    ('ascii', 'safe.py', 'COMPLETE_C1'),
    ('nested_ascii', 'dir/safe.py', 'COMPLETE_C1'),
    ('nfc_accent', 'caf\u00e9.py', 'COMPLETE_C1'),
    ('emoji', 'smile_\U0001f600.py', 'COMPLETE_C1'),
    ('arabic_letters', '\u0645\u0644\u0641.py', 'COMPLETE_C1'),
    ('joiner_not_banned', 'a\u200db.py', 'COMPLETE_C1'),
    ('nfd_existing_guard', 'cafe\u0301.py', 'FAIL_CLOSED'),
    ('surrogate_existing_guard', 'x\ud800.py', 'FAIL_CLOSED'),
    ('bidi_rlo', 'a\u202eb.py', 'FAIL_CLOSED'),
    ('bidi_lro', 'a\u202db.py', 'FAIL_CLOSED'),
    ('bidi_lri', 'a\u2066b.py', 'FAIL_CLOSED'),
    ('bidi_pdi', 'a\u2069b.py', 'FAIL_CLOSED'),
    ('bidi_lrm', 'a\u200eb.py', 'FAIL_CLOSED'),
    ('bidi_alm', 'a\u061cb.py', 'FAIL_CLOSED'),
    ('c0_newline', 'a\nb.py', 'FAIL_CLOSED'),
    ('c0_tab', 'a\tb.py', 'FAIL_CLOSED'),
    ('c0_escape', 'a\x1bb.py', 'FAIL_CLOSED'),
    ('del', 'a\x7fb.py', 'FAIL_CLOSED'),
    ('c1_next_line', 'a\x85b.py', 'FAIL_CLOSED'),
    ('line_separator', 'a\u2028b.py', 'FAIL_CLOSED'),
    ('paragraph_separator', 'a\u2029b.py', 'FAIL_CLOSED'),
]

def load(path):
    spec = importlib.util.spec_from_file_location('subject_under_test', path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def test(subject):
    results = []
    for name, suffix, expected in CASES:
        path = ROOT + suffix
        groups = [{'name': 'historical', 'files': [
            {'path': path, 'bytes': 1, 'sha256': SHA256, 'git_blob_sha1': BLOB}
        ]}]
        try:
            result = subject.audit_inventory(groups, [path])
            actual = result.get('status') if type(result) is dict else 'MALFORMED'
            caveats = (type(result) is dict and
                       result.get('source_authentication') == 'NOT_ESTABLISHED' and
                       result.get('project_automation_rate') == 'NOT_COMPUTABLE' and
                       result.get('claim_ceiling') == 'C1_DESCRIPTIVE_ONLY')
        except BaseException as exc:
            actual = 'UNCAUGHT_' + type(exc).__name__
            caveats = False
        results.append((name, expected, actual, actual == expected and caveats))
    for name, expected, actual, ok in results:
        print(f'{name}: expected={expected} actual={actual} pass={ok}')
    print('SUMMARY', sum(x[3] for x in results), '/', len(results))
    return all(x[3] for x in results)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('usage: frozen_evaluator.py SUBJECT.py')
    raise SystemExit(0 if test(load(sys.argv[1])) else 1)
