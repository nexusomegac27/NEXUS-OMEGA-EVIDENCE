#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""C1 isolated V7: require canonical raw HTML closing tags in receipts.

Append-only successor to V6, retaining its multiline scanner. A close tag
with attributes or a distinct tag-name suffix cannot terminate a raw block.
No GitHub authentication, network, writes, or runtime integration.
"""
import importlib.util
from pathlib import Path
import re
import sys

SOURCE = Path(__file__).with_name('alpha_issue93_quoted_attribute_guard_v5_20261029.py')
spec = importlib.util.spec_from_file_location('alpha_issue93_quoted_v5', SOURCE)
if spec is None or spec.loader is None:
    raise SystemExit('FAIL_CLOSED: PREDECESSOR_NOT_PRESENT')
parent = importlib.util.module_from_spec(spec)
spec.loader.exec_module(parent)

BASE = parent.parent.parent.parent.base
RAW_OPEN = re.compile(r'<(pre|script|style|textarea)\b[\s\S]*>\Z', re.I)
MAX_TAG = 8192
STRICT_CLOSE = re.compile(r'</(pre|script|style|textarea)\s*>\Z', re.I)


def multiline_safe_fields(body):
    if type(body) is not str or len(body) > 250_000:
        BASE.fail('INVALID_COMMENT_BODY')
    output = []
    fence = None
    comment = False
    raw = None
    pending = None
    quote = None
    for line in body.splitlines():
        if fence is not None:
            output.append(line)
            char, width = fence
            if re.fullmatch(r' {0,3}' + re.escape(char) + '{' + str(width) + r',}\s*', line):
                fence = None
            continue
        if raw is None and pending is None and not comment:
            marker = parent.parent.parent.parent.OPEN.match(line)
            if marker:
                fence = (marker.group(1)[0], len(marker.group(1)))
                output.append(line)
                continue
        touched = raw is not None or pending is not None
        i = 0
        while i < len(line):
            if pending is not None:
                char = line[i]
                pending += char
                if len(pending) > MAX_TAG:
                    BASE.fail('HTML_TAG_TOO_LONG')
                if quote is not None:
                    if char == quote:
                        quote = None
                elif char in ('"', "'"):
                    quote = char
                elif char == '>':
                    token = pending
                    pending = None
                    if raw is not None:
                        close = STRICT_CLOSE.fullmatch(token)
                        if close and close.group(1).lower() == raw:
                            raw = None
                    else:
                        opened = RAW_OPEN.fullmatch(token)
                        if opened:
                            raw = opened.group(1).lower()
                            touched = True
                i += 1
                continue
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
            match = parent.TAG_START.match(line, i) if line[i] == '<' else None
            if match is None:
                i += 1
                continue
            pending = ''
            quote = None
            touched = True  # Fail-safe: suppress lines containing partial tags.
            # Process the complete tag, including the initial '<', through the
            # same cross-line state machine; quoted '>' never closes a tag.
        if pending is not None:
            pending += '\n'
            if len(pending) > MAX_TAG:
                BASE.fail('HTML_TAG_TOO_LONG')
        output.append('' if touched else line)
    if pending is not None:
        BASE.fail('UNCLOSED_HTML_TAG')
    if raw is not None:
        BASE.fail('UNCLOSED_RAW_HTML_BLOCK')
    return parent.quoted_attribute_safe_fields('\n'.join(output))


BASE.fields = multiline_safe_fields
if __name__ == '__main__':
    sys.exit(BASE.main())
