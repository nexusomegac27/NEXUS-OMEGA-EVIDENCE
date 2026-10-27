"""C1 isolated cross-row path guard V3 (nonfinite exponent fail-closed); not a replacement for row-schema or byte verification.

Checks a single manifest's file-path namespace for exact and ASCII-casefold aliases.
No filesystem writes, no network, no claims of content/authentication validity.
"""
import json
import math
import re
import sys

PREFIX = 'research/r16/axiom-alpha-node-c1-adaptation-20261012/'
BASENAME = re.compile(r'[A-Za-z0-9][A-Za-z0-9_.-]*\Z', re.ASCII)
DEVICE = re.compile(r'(?:CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(?:\..*)?\Z', re.IGNORECASE | re.ASCII)
MAX_ROWS = 10000


def _portable(path):
    if not isinstance(path, str) or not path.startswith(PREFIX):
        return False
    name = path[len(PREFIX):]
    return (bool(BASENAME.fullmatch(name)) and len(name.encode('ascii')) <= 255
            and not name.endswith('.') and DEVICE.fullmatch(name) is None)


def _reject_duplicate_keys(pairs):
    obj = {}
    for key, value in pairs:
        if key in obj:
            raise ValueError('duplicate JSON object key')
        obj[key] = value
    return obj


def _parse_finite_float(token):
    """Reject exponent-overflow floats instead of silently accepting Infinity."""
    value = float(token)
    if not math.isfinite(value):
        raise ValueError('nonfinite JSON float')
    return value


def check_manifest_paths(manifest):
    """Return descriptive PASS_C1 or FAIL_CLOSED; never promote science or runtime."""
    errors = set()
    rows = manifest.get('files') if isinstance(manifest, dict) else None
    if not isinstance(rows, list) or not rows or len(rows) > MAX_ROWS:
        return {'status': 'FAIL_CLOSED', 'reason_codes': ['INVALID_CONTAINER'],
                'row_count': 0, 'distinct_casefold_count': 0}
    declared = manifest.get('count')
    if declared is not None and (type(declared) is not int or declared != len(rows)):
        errors.add('COUNT_MISMATCH')
    exact = set()
    folded = {}
    for row in rows:
        path = row.get('path') if isinstance(row, dict) else None
        if not _portable(path):
            errors.add('INVALID_PATH')
            continue
        if path in exact:
            errors.add('DUPLICATE_EXACT')
        exact.add(path)
        key = path.casefold()
        if key in folded and folded[key] != path:
            errors.add('CASEFOLD_COLLISION')
        else:
            folded[key] = path
    return {'status': 'FAIL_CLOSED' if errors else 'PASS_C1',
            'reason_codes': sorted(errors), 'row_count': len(rows),
            'distinct_casefold_count': len(folded)}


if __name__ == '__main__':
    try:
        payload = json.load(sys.stdin, object_pairs_hook=_reject_duplicate_keys,
                            parse_constant=lambda v: (_ for _ in ()).throw(ValueError(v)),
                            parse_float=_parse_finite_float)
        outcome = check_manifest_paths(payload)
    except (ValueError, TypeError, json.JSONDecodeError):
        outcome = {'status': 'FAIL_CLOSED', 'reason_codes': ['INVALID_JSON'],
                   'row_count': 0, 'distinct_casefold_count': 0}
    print(json.dumps(outcome, sort_keys=True, allow_nan=False))
    sys.exit(0 if outcome['status'] == 'PASS_C1' else 1)
