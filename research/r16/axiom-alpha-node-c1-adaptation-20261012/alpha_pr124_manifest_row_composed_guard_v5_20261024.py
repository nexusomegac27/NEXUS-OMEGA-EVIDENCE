"""C1 isolated V5: compose V4 cross-row checks with strict row fixity fields.

Research-only. Validates metadata shape, not referenced content, identity, or science.
The predecessor V3/V4 modules remain immutable; no runtime or network calls.
"""
import json
import re
import sys
from alpha_pr124_manifest_crossrow_path_guard_v3_20261024 import (
    _reject_duplicate_keys, _parse_finite_float, check_manifest_paths)
from alpha_pr124_manifest_crossrow_safe_integer_guard_v4_20261024 import _safe_int

ROW_FIELDS = frozenset(('path', 'bytes', 'sha256', 'git_blob_sha1'))
SHA256 = re.compile(r'[0-9a-f]{64}\Z', re.ASCII)
GIT_BLOB = re.compile(r'[0-9a-f]{40}\Z', re.ASCII)
SAFE = (1 << 53) - 1


def check_composed(payload):
    base = check_manifest_paths(payload)
    if base['status'] != 'PASS_C1':
        return base
    for row in payload['files']:
        if (type(row) is not dict or frozenset(row) != ROW_FIELDS
                or type(row['bytes']) is not int or not 1 <= row['bytes'] <= SAFE
                or type(row['sha256']) is not str or SHA256.fullmatch(row['sha256']) is None
                or type(row['git_blob_sha1']) is not str
                or GIT_BLOB.fullmatch(row['git_blob_sha1']) is None):
            return {'status': 'FAIL_CLOSED', 'reason_codes': ['INVALID_ROW_FIXITY'],
                    'row_count': base['row_count'],
                    'distinct_casefold_count': base['distinct_casefold_count']}
    return base


def main():
    try:
        payload = json.load(sys.stdin, object_pairs_hook=_reject_duplicate_keys,
                            parse_float=_parse_finite_float, parse_int=_safe_int,
                            parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))
        result = check_composed(payload)
    except (ValueError, TypeError, json.JSONDecodeError):
        result = {'status': 'FAIL_CLOSED', 'reason_codes': ['INVALID_JSON'],
                  'row_count': 0, 'distinct_casefold_count': 0}
    print(json.dumps(result, sort_keys=True, allow_nan=False))
    return 0 if result['status'] == 'PASS_C1' else 1


if __name__ == '__main__':
    sys.exit(main())
