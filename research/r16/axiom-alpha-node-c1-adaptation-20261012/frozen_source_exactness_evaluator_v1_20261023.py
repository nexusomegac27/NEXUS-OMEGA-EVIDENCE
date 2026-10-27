#!/usr/bin/env python3
"""Independent frozen oracle for byte-exact GitHub publication intake; C1 only."""
import hashlib
import importlib.util
import json
import sys


def identity(raw):
    return len(raw), hashlib.sha256(raw).hexdigest(), hashlib.sha1(
        b'blob ' + str(len(raw)).encode('ascii') + b'\0' + raw).hexdigest()


def fixtures():
    a = b'line with trailing space \n'
    n, h, b = identity(a)
    yield 'positive_original', (a, n, h, b), 'MATCH'
    yield 'negative_trailing_space_lost', (a.replace(b' \n', b'\n'), n, h, b), 'SOURCE_MISMATCH'
    yield 'negative_newline_added', (a+b'\n', n, h, b), 'SOURCE_MISMATCH'
    yield 'negative_same_length_substitution', (a.replace(b'line', b'LINE'), n, h, b), 'SOURCE_MISMATCH'
    yield 'negative_sha_mismatch', (a, n, '0'*64, b), 'SOURCE_MISMATCH'
    yield 'negative_size_mismatch', (a, n+1, h, b), 'SOURCE_MISMATCH'
    yield 'negative_blob_mismatch', (a, n, h, '0'*40), 'BLOB_MISMATCH'
    yield 'negative_bool_size', (a, True, h, b), 'INCOMPLETE'
    yield 'negative_sha_uppercase', (a, n, h.upper(), b), 'INCOMPLETE'
    yield 'negative_blob_invalid', (a, n, h, 'bad'), 'INCOMPLETE'
    yield 'negative_text_instead_bytes', (a.decode(), n, h, b), 'INCOMPLETE'
    yield 'negative_none_bytes', (None, n, h, b), 'INCOMPLETE'
    yield 'negative_size_negative', (a, -1, h, b), 'INCOMPLETE'
    e = b''
    en, eh, eb = identity(e)
    yield 'positive_empty_bytes', (e, en, eh, eb), 'MATCH'
    u = 'Änderung\n'.encode('utf-8')
    un, uh, ub = identity(u)
    yield 'positive_utf8_bytes', (u, un, uh, ub), 'MATCH'


def evaluate(candidate_path):
    spec = importlib.util.spec_from_file_location('candidate', candidate_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rows = []
    for name, args, expected in fixtures():
        try:
            output = module.check_source_exactness(*args)
            actual = output.get('status') if type(output) is dict else 'INVALID_RETURN'
        except Exception as exc:
            actual = 'EXCEPTION_' + type(exc).__name__
        rows.append({'name': name, 'expected': expected, 'actual': actual,
                     'pass': actual == expected})
    return {'evaluator': 'FROZEN_SOURCE_EXACTNESS_V1', 'total': len(rows),
            'passed': sum(r['pass'] for r in rows), 'rows': rows}


if __name__ == '__main__':
    report = evaluate(sys.argv[1])
    print(json.dumps(report, indent=2, ensure_ascii=False))
    sys.exit(0 if report['passed'] == report['total'] else 1)
