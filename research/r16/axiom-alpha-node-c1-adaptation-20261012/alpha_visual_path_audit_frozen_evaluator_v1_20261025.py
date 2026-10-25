#!/usr/bin/env python3
"""Frozen, independent black-box oracle for C1 visual path audit labels.

Only synthetic fixtures. This does not authenticate repository bytes or
certify actual browser rendering, accessibility, source correctness or OS safety.
"""
from __future__ import annotations
import importlib.util
import hashlib
import sys

CASES = (
    ('ascii', 'src/file.py', 'src/file.py', False),
    ('spaces', 'src/a b.py', 'src/a b.py', False),
    ('literal_backslash', 'src/a\\u{200B}.py', 'src/a\\\\u{200B}.py', True),
    ('zero_width_space', 'src/a\u200bb.py', 'src/a\\u{200B}b.py', True),
    ('zero_width_joiner', 'src/a\u200db.py', 'src/a\\u{200D}b.py', True),
    ('bidi_override', 'src/a\u202eb.py', 'src/a\\u{202E}b.py', True),
    ('bidi_isolate', 'src/a\u2066b.py', 'src/a\\u{2066}b.py', True),
    ('arabic', 'src/\u0645\u0644\u0641.py', 'src/\\u{645}\\u{644}\\u{641}.py', True),
    ('cyrillic_confusable', 'src/\u0430.py', 'src/\\u{430}.py', True),
    ('latin', 'src/a.py', 'src/a.py', False),
    ('nfc', 'src/caf\u00e9.py', 'src/caf\\u{E9}.py', True),
    ('nfd', 'src/cafe\u0301.py', 'src/cafe\\u{301}.py', True),
    ('emoji', 'src/\U0001f600.py', 'src/\\u{1F600}.py', True),
    ('markup', 'src/<a&"\'>.py', 'src/\\u{3C}a\\u{26}\\u{22}\\u{27}\\u{3E}.py', True),
    ('new_line', 'src/a\nb.py', 'src/a\\u{A}b.py', True),
    ('tab', 'src/a\tb.py', 'src/a\\u{9}b.py', True),
    ('del', 'src/a\x7fb.py', 'src/a\\u{7F}b.py', True),
    ('no_break_space', 'src/a\u00a0b.py', 'src/a\\u{A0}b.py', True),
    ('paragraph_sep', 'src/a\u2029b.py', 'src/a\\u{2029}b.py', True),
    ('leading_period', '.github/file.yml', '.github/file.yml', False),
)
REJECT = (('surrogate', 'src/a\ud800.py'), ('nul', 'src/a\x00b.py'),
          ('too_long', 'src/' + 'a' * 8200), ('non_string', 23))


def test(mod):
    results = []
    labels = set()
    for name, path, expected, warned in CASES:
        try:
            r = mod.audit_label(path)
            label = r['label']
            ok = (r['status'] == 'DISPLAY_ONLY_C1' and label == expected
                  and r['has_escaped_codepoints'] is warned
                  and r['path_utf8_sha256'] == hashlib.sha256(path.encode('utf-8')).hexdigest()
                  and r['source_authentication'] == 'NOT_ESTABLISHED'
                  and r['claim_ceiling'] == 'C1_DESCRIPTIVE_ONLY'
                  and mod.decode_audit_label(label) == path
                  and label.isascii() and '\n' not in label and '<' not in label
                  and label not in labels)
            labels.add(label)
        except BaseException:
            ok = False
        results.append((name, ok))
    for name, path in REJECT:
        try:
            r = mod.audit_label(path)
            ok = r['status'] == 'FAIL_CLOSED' and 'label' not in r
        except BaseException:
            ok = False
        results.append((name, ok))
    # Negative mutation: an audit label must be injective even when the original
    # contains the literal escape syntax or visually confusable characters.
    pairs = [('src/a\u200bb.py', 'src/a\\u{200B}b.py'),
             ('src/caf\u00e9.py', 'src/cafe\u0301.py'),
             ('src/a.py', 'src/\u0430.py')]
    for i, (a, b) in enumerate(pairs):
        try:
            ok = mod.audit_label(a)['label'] != mod.audit_label(b)['label']
        except BaseException:
            ok = False
        results.append(('collision_'+str(i), ok))
    for n, ok in results:
        print(n, 'PASS' if ok else 'FAIL')
    print('SUMMARY', sum(x[1] for x in results), '/', len(results))
    return all(x[1] for x in results)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('usage: FROZEN_EVALUATOR.py CANDIDATE.py')
    spec = importlib.util.spec_from_file_location('candidate', sys.argv[1])
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    raise SystemExit(0 if test(m) else 1)
