#!/usr/bin/env python3
"""C1-only whitespace-stable reversible ASCII audit labels for provenance paths.

ASCII spaces are escaped to avoid ordinary HTML whitespace collapse.
This is a pure display transform; not an authentication, path validator, URL
sanitizer, browser test, claim promotion, or permission decision. Original
path bytes and their provenance must remain separately bound by the caller.
"""
from __future__ import annotations
import hashlib
import re

MAX_SCALARS = 8192
_ESCAPE = re.compile(r'\\u\{([0-9A-F]{1,6})\}')


def _fail(reason: str) -> dict:
    return {'status': 'FAIL_CLOSED', 'reason': reason,
            'source_authentication': 'NOT_ESTABLISHED',
            'claim_ceiling': 'C1_DESCRIPTIVE_ONLY'}


def audit_label(path: str) -> dict:
    if not isinstance(path, str) or not path or len(path) > MAX_SCALARS:
        return _fail('invalid_path_or_resource_limit')
    if '\x00' in path or any(0xD800 <= ord(ch) <= 0xDFFF for ch in path):
        return _fail('invalid_unicode_scalar_or_nul')
    try:
        original = path.encode('utf-8', 'strict')
    except UnicodeError:
        return _fail('non_utf8_path')
    pieces = []
    escaped = False
    for ch in path:
        cp = ord(ch)
        if ch == '\\':
            pieces.append('\\\\')
            escaped = True
        elif cp < 0x20 or cp > 0x7e or ch in '<>&"\' ':
            pieces.append('\\u{' + format(cp, 'X') + '}')
            escaped = True
        else:
            pieces.append(ch)
    return {'status': 'DISPLAY_ONLY_C1', 'label': ''.join(pieces),
            'has_escaped_codepoints': escaped,
            'path_utf8_sha256': hashlib.sha256(original).hexdigest(),
            'source_authentication': 'NOT_ESTABLISHED',
            'claim_ceiling': 'C1_DESCRIPTIVE_ONLY'}


def decode_audit_label(label: str) -> str:
    """Strict inverse for the ASCII audit label, not a path trust operation."""
    if not isinstance(label, str) or len(label) > MAX_SCALARS * 10:
        raise ValueError('invalid label')
    out = []
    i = 0
    while i < len(label):
        ch = label[i]
        if ch != '\\':
            if ord(ch) < 0x20 or ord(ch) > 0x7e or ch in '<>&"\' ':
                raise ValueError('noncanonical literal')
            out.append(ch)
            i += 1
            continue
        if label.startswith('\\\\', i):
            out.append('\\')
            i += 2
            continue
        m = _ESCAPE.match(label, i)
        if not m:
            raise ValueError('invalid escape')
        cp = int(m.group(1), 16)
        if cp == 0 or cp > 0x10ffff or 0xd800 <= cp <= 0xdfff:
            raise ValueError('invalid scalar')
        char = chr(cp)
        if cp >= 0x20 and cp <= 0x7e and char not in '<>&"\' ':
            raise ValueError('noncanonical escape')
        if format(cp, 'X') != m.group(1):
            raise ValueError('noncanonical hex')
        out.append(char)
        i = m.end()
    result = ''.join(out)
    if not result or len(result) > MAX_SCALARS:
        raise ValueError('resource limit')
    return result
