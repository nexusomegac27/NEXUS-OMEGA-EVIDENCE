#!/usr/bin/env python3
"""Run107 frozen external-to-candidate evaluator: inventory completeness.

This oracle is written/frozen BEFORE candidate V2 and tests only synthetic,
caller-asserted inputs. It does not authenticate any GitHub event or establish
project-wide automation attainment. No network or repository writes.
"""
import hashlib
import importlib.util
import json
import sys

H = 'a' * 64
C = 'b' * 40
B = 'c' * 40


def ev(i, **changes):
    row = dict(id=i, routine=True, public=True, authorized=True,
               accessible=True, automated=True, manual_trigger=False,
               verification='INDEPENDENT_READBACK_MATCH',
               source_sha256=H, readback_sha256=H,
               readback_commit=C, readback_blob=B, source_bytes=25)
    row.update(changes)
    return row


def inv(ids, **changes):
    data = dict(expected_ids=ids,
                inventory_sha256=hashlib.sha256(json.dumps(sorted(ids), ensure_ascii=False,
                   separators=(',', ':')).encode('utf-8')).hexdigest(),
                source_commit=C, source_blob=B, source_bytes=17,
                source_readback='INDEPENDENT_READBACK_MATCH')
    data.update(changes)
    return data


def cases():
    good = ev('a')
    return [
        ('unbound_inventory', [good], None, 'INCOMPLETE', 0, 0),
        ('one_complete', [good], inv(['a']), 'CALCULABLE', 1, 1),
        ('missing_event', [good], inv(['a', 'b']), 'INCOMPLETE', 0, 0),
        ('extra_event', [good, ev('b')], inv(['a']), 'INCOMPLETE', 0, 0),
        ('duplicate_inventory', [good], inv(['a', 'a']), 'INCOMPLETE', 0, 0),
        ('duplicate_events', [good, good], inv(['a']), 'INCOMPLETE', 0, 0),
        ('tampered_digest', [good], inv(['a'], inventory_sha256='f'*64), 'INCOMPLETE', 0, 0),
        ('bad_digest', [good], inv(['a'], inventory_sha256='not-a-hash'), 'INCOMPLETE', 0, 0),
        ('missing_commit', [good], inv(['a'], source_commit=None), 'INCOMPLETE', 0, 0),
        ('bad_blob', [good], inv(['a'], source_blob='z'*40), 'INCOMPLETE', 0, 0),
        ('boolean_inventory_bytes', [good], inv(['a'], source_bytes=True), 'INCOMPLETE', 0, 0),
        ('unread_inventory', [good], inv(['a'], source_readback='NOT_EXECUTED'), 'INCOMPLETE', 0, 0),
        ('empty_complete', [], inv([]), 'NO_ELIGIBLE_EVENTS', 0, 0),
        ('empty_unbound', [], None, 'INCOMPLETE', 0, 0),
        ('empty_extra', [good], inv([]), 'INCOMPLETE', 0, 0),
        ('one_manual', [good, ev('b', automated=False, manual_trigger=True)], inv(['a', 'b']), 'CALCULABLE', 2, 1),
        ('private_excluded', [good, ev('b', public=False)], inv(['a', 'b']), 'CALCULABLE', 1, 1),
        ('unknown_scope', [good, ev('b', routine=None)], inv(['a', 'b']), 'INCOMPLETE', 1, 1),
        ('source_hash_mismatch', [ev('a', readback_sha256='d'*64)], inv(['a']), 'CALCULABLE', 1, 0),
        ('source_hash_missing', [ev('a', source_sha256=None)], inv(['a']), 'CALCULABLE', 1, 0),
        ('nonlist_rows', {}, inv(['a']), 'INCOMPLETE', 0, 0),
        ('string_ids', [good], inv(['a'], expected_ids='a'), 'INCOMPLETE', 0, 0),
        ('negative_inventory_bytes', [good], inv(['a'], source_bytes=-1), 'INCOMPLETE', 0, 0),
        ('ids_modified_after_hash', [good, ev('b')], inv(['a'], expected_ids=['a', 'b']), 'INCOMPLETE', 0, 0),
        ('order_independent', [ev('b'), good], inv(['a', 'b']), 'CALCULABLE', 2, 2),
        ('unicode_id', [ev('ü')], inv(['ü']), 'CALCULABLE', 1, 1),
        ('null_event', [None], inv(['a']), 'INCOMPLETE', 0, 0),
        ('invalid_id', [ev('')], inv(['']), 'INCOMPLETE', 0, 0),
        ('provenance_not_promoted', [good], inv(['a']), 'CALCULABLE', 1, 1),
        ('unknown_trigger', [ev('a', manual_trigger=None)], inv(['a']), 'INCOMPLETE', 0, 0),
    ]


def load(path):
    spec = importlib.util.spec_from_file_location('target_module', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def evaluate(path, baseline=False):
    module = load(path)
    outcomes = []
    for name, rows, inventory, status, denominator, numerator in cases():
        try:
            actual = module.assess(rows) if baseline else module.assess(rows, inventory)
            ok = (actual['status'] == status and
                  actual['eligible_denominator'] == denominator and
                  actual['verified_automated_numerator'] == numerator and
                  (actual.get('rate_from_input_assertions') is None if status != 'CALCULABLE' else True) and
                  actual['target_90_adjudication'] == 'NOT_ESTABLISHED_INPUT_ASSERTIONS_ONLY')
            if name == 'provenance_not_promoted':
                ok = ok and actual['provenance'] == 'CALLER_ASSERTED_NOT_AUTHENTICATED_BY_THIS_GUARD'
            outcomes.append({'case': name, 'pass': bool(ok), 'actual_status': actual['status']})
        except Exception as ex:
            outcomes.append({'case': name, 'pass': False, 'exception': type(ex).__name__})
    print(json.dumps({'total': len(outcomes), 'passed': sum(x['pass'] for x in outcomes),
                      'outcomes': outcomes}, sort_keys=True, ensure_ascii=False))
    return 0 if all(x['pass'] for x in outcomes) else 1

if __name__ == '__main__':
    sys.exit(evaluate(sys.argv[1], '--baseline' in sys.argv[2:]))
