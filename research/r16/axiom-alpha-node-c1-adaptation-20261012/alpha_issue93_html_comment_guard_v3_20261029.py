#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Isolated C1 wrapper: ignore HTML comments as well as Markdown fences.

Reads V2 and V1 from the same pinned research directory. No GitHub fetch,
identity authentication, writes, or change to predecessor/evaluator bytes.
"""
import importlib.util
from pathlib import Path
import re
import sys

SOURCE = Path(__file__).with_name('alpha_issue93_fenced_receipt_guard_v2_20261029.py')
spec = importlib.util.spec_from_file_location('alpha_issue93_fence_v2', SOURCE)
if spec is None or spec.loader is None:
    raise SystemExit('FAIL_CLOSED: PREDECESSOR_NOT_PRESENT')
parent = importlib.util.module_from_spec(spec)
spec.loader.exec_module(parent)


def html_safe_fields(body):
    if type(body) is not str or len(body) > 250_000:
        parent.base.fail('INVALID_COMMENT_BODY')
    out = {}
    fence = None
    in_html = False
    for line in body.splitlines():
        if fence is not None:
            char, width = fence
            if re.fullmatch(r' {0,3}' + re.escape(char) + '{' + str(width) + r',}\s*', line):
                fence = None
            continue
        if not in_html:
            marker = parent.OPEN.match(line)
            if marker:
                fence = (marker.group(1)[0], len(marker.group(1)))
                continue
        pos = 0
        has_html = in_html
        while pos < len(line):
            if in_html:
                end = line.find('-->', pos)
                if end == -1:
                    break
                in_html = False
                pos = end + 3
            else:
                start = line.find('<!--', pos)
                if start == -1:
                    break
                in_html = True
                has_html = True
                pos = start + 4
        if has_html or in_html:
            continue  # Never stitch a receipt binding across HTML boundaries.
        if '=' not in line:
            continue
        key, value = line.split('=', 1)
        if key in parent.BINDINGS:
            if key in out:
                parent.base.fail('DUPLICATE_RECEIPT_FIELD')
            out[key] = value.strip()
    if fence is not None:
        parent.base.fail('UNCLOSED_MARKDOWN_FENCE')
    if in_html:
        parent.base.fail('UNCLOSED_HTML_COMMENT')
    return out


parent.base.fields = html_safe_fields
if __name__ == '__main__':
    sys.exit(parent.base.main())
