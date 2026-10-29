#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Isolated C1 wrapper: exclude Markdown fenced examples from receipt fields.

Loads the pinned predecessor V1 in the same research directory. Does not
fetch GitHub, authenticate users, write data, or modify the V1 source.
"""
import importlib.util
from pathlib import Path
import re
import sys

SOURCE = Path(__file__).with_name('alpha_issue93_exact_key_receipt_census_v1_20261029.py')
spec = importlib.util.spec_from_file_location('alpha_issue93_exact_key_v1', SOURCE)
if spec is None or spec.loader is None:
    raise SystemExit('FAIL_CLOSED: PREDECESSOR_NOT_PRESENT')
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)
OPEN = re.compile(r'^ {0,3}(`{3,}|~{3,})(.*)$')
BINDINGS = frozenset(('PR', 'ACTUAL_MAIN_READBACK', 'CLAIM_CEILING'))


def fenced_safe_fields(body):
    if type(body) is not str or len(body) > 250_000:
        base.fail('INVALID_COMMENT_BODY')
    out = {}
    fence = None
    for line in body.splitlines():
        if fence is not None:
            char, width = fence
            if re.fullmatch(r' {0,3}' + re.escape(char) + '{' + str(width) + r',}\s*', line):
                fence = None
            continue
        marker = OPEN.match(line)
        if marker:
            fence = (marker.group(1)[0], len(marker.group(1)))
            continue
        if '=' not in line:
            continue
        key, value = line.split('=', 1)
        if key in BINDINGS:
            if key in out:
                base.fail('DUPLICATE_RECEIPT_FIELD')
            out[key] = value.strip()
    if fence is not None:
        base.fail('UNCLOSED_MARKDOWN_FENCE')
    return out


base.fields = fenced_safe_fields
if __name__ == '__main__':
    sys.exit(base.main())
