"""Research-only handoff denominator guard V2: unique attempt-level evidence refs (C1).
This does not authenticate GitHub events, prove source completeness, or collect data.
"""
import json
import math
import re
import sys

MAX_BYTES = 4 * 1024 * 1024
HEX40 = re.compile(r'[0-9a-f]{40}\Z')
FIELDS = ('routine', 'public', 'authorized', 'accessible', 'completed',
          'operator_nudge', 'receipt_verified')


def unique_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('DUPLICATE_KEY')
        result[key] = value
    return result


def finite_float(token):
    value = float(token)
    if not math.isfinite(value):
        raise ValueError('NONFINITE_NUMBER')
    return value


def reject_constant(token):
    raise ValueError('NONFINITE_CONSTANT')


def evaluate(data):
    empty = {'status': 'NOT_COMPUTABLE', 'eligible_denominator': None,
             'automated_numerator': None, 'automation_pct': None,
             'scope': 'STRUCTURAL_ONLY_NOT_AUTHENTICATED'}
    if not isinstance(data, dict) or data.get('coverage_complete') is not True:
        return empty
    if not isinstance(data.get('coverage_source'), str) or not data['coverage_source'].strip():
        return empty
    commit = data.get('pinned_commit')
    if not isinstance(commit, str) or HEX40.fullmatch(commit) is None:
        return empty
    attempts = data.get('attempts')
    if not isinstance(attempts, list) or not attempts:
        return empty
    ids = set()
    refs = set()
    eligible = numerator = 0
    for row in attempts:
        if not isinstance(row, dict):
            return empty
        rid = row.get('attempt_id')
        ref = row.get('evidence_ref')
        if not isinstance(rid, str) or not rid.strip() or rid in ids:
            return empty
        if not isinstance(ref, str) or not ref.strip():
            return empty
        # Fail closed on reused attempt-level evidence, including whitespace aliases.
        canonical_ref = ref.strip()
        if canonical_ref in refs:
            return empty
        refs.add(canonical_ref)
        ids.add(rid)
        if any(type(row.get(field)) is not bool for field in FIELDS):
            return empty
        is_eligible = all(row[k] for k in ('routine', 'public', 'authorized', 'accessible'))
        if is_eligible:
            eligible += 1
            if row['completed'] and not row['operator_nudge'] and row['receipt_verified']:
                numerator += 1
    if eligible == 0:
        return empty
    return {'status': 'METRIC_READY_STRUCTURAL_ONLY',
            'eligible_denominator': eligible, 'automated_numerator': numerator,
            'automation_pct': round(100 * numerator / eligible, 6),
            'scope': 'STRUCTURAL_ONLY_NOT_AUTHENTICATED'}


def main():
    try:
        raw = sys.stdin.buffer.read(MAX_BYTES + 1)
        if len(raw) > MAX_BYTES:
            raise ValueError('INPUT_TOO_LARGE')
        data = json.loads(raw.decode('utf-8'), object_pairs_hook=unique_keys,
                          parse_constant=reject_constant, parse_float=finite_float)
        result = evaluate(data)
    except (ValueError, TypeError, UnicodeError, OverflowError, RecursionError):
        result = {'status': 'NOT_COMPUTABLE', 'eligible_denominator': None,
                  'automated_numerator': None, 'automation_pct': None,
                  'scope': 'STRUCTURAL_ONLY_NOT_AUTHENTICATED'}
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
