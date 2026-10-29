#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Isolated C1 receipt guard V4: exclude raw HTML example blocks.

Adds CommonMark raw HTML block types pre/script/style/textarea to V3's
HTML-comment and fenced-Markdown exclusions. Caller-supplied input only;
no GitHub authentication, network, filesystem mutation or project-rate claim.
"""
import importlib.util
from pathlib import Path
import re
import sys

SOURCE = Path(__file__).with_name('alpha_issue93_html_comment_guard_v3_20261029.py')
spec = importlib.util.spec_from_file_location('alpha_issue93_html_v3', SOURCE)
if spec is None or spec.loader is None:
    raise SystemExit('FAIL_CLOSED: PREDECESSOR_NOT_PRESENT')
parent = importlib.util.module_from_spec(spec)
spec.loader.exec_module(parent)

TOKEN = re.compile(r'<!--|-->|</?(?:pre|script|style|textarea)\b[^>]*>', re.I)
CLOSE = re.compile(r'</(pre|script|style|textarea)\b[^>]*>', re.I)
OPEN = re.compile(r'<(pre|script|style|textarea)\b[^>]*>', re.I)


def raw_html_safe_fields(body):
    if type(body) is not str or len(body) > 250_000:
        parent.parent.base.fail('INVALID_COMMENT_BODY')
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
            marker = parent.parent.OPEN.match(line)
            if marker:
                fence = (marker.group(1)[0], len(marker.group(1)))
                out.append(line)
                continue
        touched_raw = raw_tag is not None
        for match in TOKEN.finditer(line):
            token = match.group()
            if comment:
                if token == '-->':
                    comment = False
                continue
            if raw_tag is not None:
                close = CLOSE.fullmatch(token)
                if close and close.group(1).lower() == raw_tag:
                    raw_tag = None
                continue
            if token == '<!--':
                comment = True
                continue
            opened = OPEN.fullmatch(token)
            if opened:
                raw_tag = opened.group(1).lower()
                touched_raw = True
        out.append('' if touched_raw else line)
    if raw_tag is not None:
        parent.parent.base.fail('UNCLOSED_RAW_HTML_BLOCK')
    # Parent V3 independently enforces HTML-comment and Markdown-fence rules.
    return parent.html_safe_fields('\n'.join(out))


parent.parent.base.fields = raw_html_safe_fields
if __name__ == '__main__':
    sys.exit(parent.parent.base.main())
