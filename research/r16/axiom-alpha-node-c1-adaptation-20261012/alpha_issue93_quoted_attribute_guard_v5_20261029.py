#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Isolated C1 Issue93 receipt guard V5: quote-aware HTML tag tokenization.

V4 can treat </pre> inside a quoted HTML attribute as a real closing tag.
V5 masks raw blocks until a syntactically complete, quote-aware closing tag.
This wrapper does not authenticate GitHub data or modify the predecessors.
"""
import importlib.util
from pathlib import Path
import re
import sys

SOURCE = Path(__file__).with_name('alpha_issue93_raw_html_block_guard_v4_20261029.py')
spec = importlib.util.spec_from_file_location('alpha_issue93_raw_v4', SOURCE)
if spec is None or spec.loader is None:
    raise SystemExit('FAIL_CLOSED: PREDECESSOR_NOT_PRESENT')
parent = importlib.util.module_from_spec(spec)
spec.loader.exec_module(parent)

# Match only a complete HTML tag. Quote-aware scanning below determines the
# true end delimiter, so apparent closing tags inside attributes stay inert.
TAG_START = re.compile(r'</?[A-Za-z][A-Za-z0-9:-]*')
RAW_OPEN = re.compile(r'<(pre|script|style|textarea)\b.*>\Z', re.I)


def quoted_attribute_safe_fields(body):
    if type(body) is not str or len(body) > 250_000:
        parent.parent.parent.base.fail('INVALID_COMMENT_BODY')
    out = []
    fence = None
    comment = False
    raw_tag = None
    for line in body.splitlines():
        if fence is not None:
            out.append(line)
            char, width = fence
            if re.fullmatch(r' {0,3}' + re.escape(char) + '{' + str(width) + r',}\s*', line):
                fence = None
            continue
        if raw_tag is None and not comment:
            marker = parent.parent.parent.OPEN.match(line)
            if marker:
                fence = (marker.group(1)[0], len(marker.group(1)))
                out.append(line)
                continue
        touched_raw = raw_tag is not None
        i = 0
        while i < len(line):
            if comment:
                end = line.find('-->', i)
                if end < 0:
                    break
                comment = False
                i = end + 3
                continue
            if line.startswith('<!--', i):
                comment = True
                i += 4
                continue
            if line[i] != '<' or TAG_START.match(line, i) is None:
                i += 1
                continue
            # Consume one complete tag, respecting both kinds of quoted attrs.
            quote = None
            j = i + 1
            while j < len(line):
                char = line[j]
                if quote is not None:
                    if char == quote:
                        quote = None
                elif char in ('"', "'"):
                    quote = char
                elif char == '>':
                    break
                j += 1
            if j == len(line):
                # Never reclassify later lines as operative receipts after an
                # unterminated tag in a raw block.
                if raw_tag is not None:
                    parent.parent.parent.base.fail('UNCLOSED_HTML_TAG')
                break
            token = line[i:j + 1]
            if raw_tag is not None:
                close = parent.CLOSE.fullmatch(token)
                if close and close.group(1).lower() == raw_tag:
                    raw_tag = None
            else:
                opened = RAW_OPEN.fullmatch(token)
                if opened:
                    raw_tag = opened.group(1).lower()
                    touched_raw = True
            i = j + 1
        out.append('' if touched_raw else line)
    if raw_tag is not None:
        parent.parent.parent.base.fail('UNCLOSED_RAW_HTML_BLOCK')
    # V3 still checks Markdown fences, HTML comments and exact receipt fields.
    return parent.parent.html_safe_fields('\n'.join(out))


parent.parent.parent.base.fields = quoted_attribute_safe_fields
if __name__ == '__main__':
    sys.exit(parent.parent.parent.base.main())
