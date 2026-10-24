#!/usr/bin/env python3
"""C1 isolated preflight V2: reject timezone-ambiguous snapshot timestamps.

This is a syntax guard, NOT independent evidence that a GitHub snapshot is
fresh, authentic, or sufficient to authorize a write. All V1 checks remain.
"""
import re
from alpha_pr_publication_preflight_guard_v1_20261023 import check_pr_publication_preflight as _v1

_AWARE = re.compile(
    r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?'
    r'(?:Z|[+-](?:0\d|1[0-4]):[0-5]\d)$', re.ASCII
)


def _explicit_offset(value):
    if not isinstance(value, str) or not _AWARE.fullmatch(value):
        return False
    if value[-6] in '+-' and value[-5:-3] == '14' and value[-2:] != '00':
        return False
    return True


def check_pr_publication_preflight(snapshot, now_utc):
    """Fail closed on missing timezone; otherwise preserve pinned V1 behavior."""
    if not isinstance(snapshot, dict) or not isinstance(snapshot.get('target'), dict):
        return _v1(snapshot, now_utc)
    if not (_explicit_offset(now_utc) and
            _explicit_offset(snapshot['target'].get('observed_at'))):
        return {'status': 'TIMEZONE_REQUIRED'}
    return _v1(snapshot, now_utc)
