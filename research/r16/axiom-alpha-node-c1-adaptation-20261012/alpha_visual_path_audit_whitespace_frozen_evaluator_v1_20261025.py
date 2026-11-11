#!/usr/bin/env python3
"""Independent frozen synthetic evaluator for whitespace-stable visual audit labels.

Scope: local string rendering contract only; no browser, source authentication,
path authorization, filesystem portability, or public release verification.
"""
from __future__ import annotations
import hashlib
import importlib.util
import re
import sys

# This reference is independently expressed as an allowlist, not as the
# candidate's codepoint escape decision tree.
ALLOWED_LITERAL = frozenset(chr(n) for n in range(33, 127)) - set('\\<>&"\'')


def oracle_label(s: str) -> str:
    return ''.join(c if c in ALLOWED_LITERAL else
                   ('\\\\' if c == '\\' else '\\u{' + f'{ord(c):X}' + '}')
                   for c in s)


VALID = [
    'src/file.py', 'src/a b.py', 'src/a  b.py', 'src/a   b.py',
    ' src/a.py', 'src/a.py ', 'src/ a .py ',
    'src/a\\u{20}.py', 'src/a \\u{20}.py',
    'src/a\u00a0b.py', 'src/a\u200bb.py', 'src/a\u202eb.py',
    'src/caf\u00e9.py', 'src/cafe\u0301.py', 'src/\u0430.py',
    'src/<x>&"\'.py', 'src/a\nb.py', 'src/a\tb.py',
    '.github/workflows/ci.yml', 'src/\U0001f600.py',
]
INVALID = ['', None, 123, 'src/\x00b', 'src/\ud800b', 'a' * 8193]
BAD_DECODES = ['raw space', '\\u{20} raw space', '\\u{0020}',
               '\\u{2f}', '\\u{2F}', '\\u{0}', '\\u{D800}',
               '\\u{110000}', '\\u{20', '\\u{20}\\', '<', '']
PAIRS = [('src/a b', 'src/a  b'), ('src/a', 'src/a '),
         ('src/a b', 'src/a\u00a0b'), ('src/a\\u{20}', 'src/a b')]


def collapse_html_whitespace(s: str) -> str:
    # Conservative proxy for ordinary CSS whitespace collapsing, NOT browser E2E.
    return re.sub(r'[\t\n\r\f ]+', ' ', s)


def check(mod):
    results = []
    labels = set()
    for i, original in enumerate(VALID):
        try:
            item = mod.audit_label(original)
            label = item['label']
            ok = (item['status'] == 'DISPLAY_ONLY_C1'
                  and label == oracle_label(original)
                  and label not in labels
                  and not any(ch.isspace() for ch in label)
                  and item['path_utf8_sha256'] == hashlib.sha256(original.encode()).hexdigest()
                  and item['source_authentication'] == 'NOT_ESTABLISHED'
                  and item['claim_ceiling'] == 'C1_DESCRIPTIVE_ONLY'
                  and item['has_escaped_codepoints'] == (label != original)
                  and mod.decode_audit_label(label) == original)
            labels.add(label)
        except Exception:
            ok = False
        results.append((f'valid_{i:02d}', ok))
    for i, invalid in enumerate(INVALID):
        try:
            item = mod.audit_label(invalid)
            ok = item['status'] == 'FAIL_CLOSED' and 'label' not in item
        except Exception:
            ok = False
        results.append((f'invalid_{i:02d}', ok))
    for i, invalid in enumerate(BAD_DECODES):
        try:
            mod.decode_audit_label(invalid)
            ok = False
        except ValueError:
            ok = True
        except Exception:
            ok = False
        results.append((f'decode_reject_{i:02d}', ok))
    for i, (a, b) in enumerate(PAIRS):
        try:
            aa, bb = mod.audit_label(a)['label'], mod.audit_label(b)['label']
            ok = aa != bb and collapse_html_whitespace(aa) != collapse_html_whitespace(bb)
        except Exception:
            ok = False
        results.append((f'whitespace_collision_{i:02d}', ok))
    for n, ok in results:
        print(n, 'PASS' if ok else 'FAIL')
    print('SUMMARY', sum(ok for _, ok in results), '/', len(results))
    return all(ok for _, ok in results)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('usage: EVALUATOR.py CANDIDATE.py')
    spec = importlib.util.spec_from_file_location('candidate', sys.argv[1])
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    raise SystemExit(0 if check(mod) else 1)
