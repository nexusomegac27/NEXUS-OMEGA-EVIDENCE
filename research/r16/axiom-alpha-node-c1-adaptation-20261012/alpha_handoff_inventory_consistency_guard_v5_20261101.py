"""C1 isolated V5: fail-closed consistency with a separately declared census inventory.
Does not authenticate inventory, discover omitted events, or prove project-wide coverage.
Preserves immutable V4 eligibility arithmetic and source semantics.
"""
import json
import sys
import unicodedata
import alpha_handoff_evidence_ref_canonical_guard_v4_20261101 as prior


def canonical_id(value):
    return (type(value) is str and bool(value.strip()) and
            value == unicodedata.normalize('NFC', value.strip()) and
            not any(unicodedata.category(c) in ('Cc', 'Cf') for c in value))


def inventory_ok(data):
    if type(data) is not dict or type(data.get('attempts')) is not list:
        return False
    inventory = data.get('inventory')
    if type(inventory) is not dict:
        return False
    expected = inventory.get('expected_attempt_ids')
    if type(expected) is not list or not expected or not all(canonical_id(x) for x in expected):
        return False
    if type(inventory.get('expected_count')) is not int or inventory['expected_count'] != len(expected):
        return False
    if len(set(expected)) != len(expected):
        return False
    if inventory.get('source_commit') != data.get('pinned_commit'):
        return False
    if type(inventory.get('source_ref')) is not str or not inventory['source_ref'].strip():
        return False
    attempts = data['attempts']
    if len(attempts) != len(expected):
        return False
    observed = [r.get('attempt_id') for r in attempts if type(r) is dict]
    return len(observed) == len(expected) and all(canonical_id(x) for x in observed) and set(observed) == set(expected)


def fail():
    result = prior.not_computable()
    result['inventory_consistency_structural'] = False
    result['scope'] = 'STRUCTURAL_INVENTORY_UNAUTHENTICATED'
    return result


def evaluate(data):
    if not inventory_ok(data):
        return fail()
    result = prior.evaluate(data)
    result['inventory_consistency_structural'] = result['status'] != 'NOT_COMPUTABLE'
    result['scope'] = 'STRUCTURAL_INVENTORY_UNAUTHENTICATED'
    return result


def main():
    try:
        raw = sys.stdin.buffer.read(prior.MAX_BYTES + 1)
        if len(raw) > prior.MAX_BYTES:
            raise ValueError('INPUT_TOO_LARGE')
        data = json.loads(raw.decode('utf-8'), object_pairs_hook=prior.unique_keys,
                          parse_constant=prior.reject_constant, parse_float=prior.finite_float)
        result = evaluate(data)
    except (ValueError, TypeError, UnicodeError, OverflowError, RecursionError):
        result = fail()
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
