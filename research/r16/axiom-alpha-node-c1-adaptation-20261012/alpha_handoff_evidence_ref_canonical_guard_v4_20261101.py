"""Research-only V4 evidence-reference canonicalization guard (C1).
Requires the immutable V3 guard in the same research directory. Synthetic only.
No event authentication, census completeness proof, or production integration.
"""
import json
import sys
import unicodedata

from alpha_handoff_attempt_id_canonical_guard_v3_20261101 import (
    MAX_BYTES, evaluate as evaluate_v3, finite_float, reject_constant,
    unique_keys,
)


def not_computable():
    return {'status': 'NOT_COMPUTABLE', 'eligible_denominator': None,
            'automated_numerator': None, 'automation_pct': None,
            'scope': 'STRUCTURAL_ONLY_NOT_AUTHENTICATED'}


def evaluate(data):
    if not isinstance(data, dict) or not isinstance(data.get('attempts'), list):
        return not_computable()
    seen = set()
    for row in data['attempts']:
        if not isinstance(row, dict):
            return not_computable()
        ref = row.get('evidence_ref')
        if not isinstance(ref, str) or not ref.strip():
            return not_computable()
        canonical = unicodedata.normalize('NFC', ref.strip())
        if (ref != canonical or canonical in seen or
                any(unicodedata.category(ch) in ('Cc', 'Cf') for ch in ref)):
            return not_computable()
        seen.add(canonical)
    return evaluate_v3(data)


def main():
    try:
        raw = sys.stdin.buffer.read(MAX_BYTES + 1)
        if len(raw) > MAX_BYTES:
            raise ValueError('INPUT_TOO_LARGE')
        data = json.loads(raw.decode('utf-8'), object_pairs_hook=unique_keys,
                          parse_constant=reject_constant, parse_float=finite_float)
        result = evaluate(data)
    except (ValueError, TypeError, UnicodeError, OverflowError, RecursionError):
        result = not_computable()
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
