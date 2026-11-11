#!/usr/bin/env python3
"""Frozen C1 adversarial evaluator for handoff Unicode scalar validity.

This oracle is pinned before V4 implementation. It is deliberately separate
from the candidate, uses only Python stdlib, and is synthetic (not a GitHub
actor/source-authentication test). Exact expectation: reject all lone UTF-16
surrogates, including escaped JSON keys and nested values; accept valid
Unicode scalar strings. Original V3 is the comparison baseline.
"""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

H = 'a' * 64
C = 'b' * 40
B = 'c' * 40


def event(ident='evt-1', **changes):
    row = {'id': ident, 'routine': True, 'public': True,
           'authorized': True, 'accessible': True, 'automated': True,
           'manual_trigger': False, 'verification': 'INDEPENDENT_READBACK_MATCH',
           'source_sha256': H, 'readback_sha256': H,
           'readback_commit': C, 'readback_blob': B, 'source_bytes': 9}
    row.update(changes)
    return row


def inventory(rows, raw):
    ids = sorted(r['id'] for r in rows)
    try:
        ids_bytes = json.dumps(ids, ensure_ascii=False,
                               separators=(',', ':')).encode('utf-8')
        digest = hashlib.sha256(ids_bytes).hexdigest()
    except UnicodeEncodeError:
        # A syntactically valid 64-hex placeholder makes the V2 encode fault
        # independently observable, rather than preemptively rejecting it.
        digest = H
    blob = hashlib.sha1(b'blob ' + str(len(raw)).encode('ascii')
                        + b'\0' + raw).hexdigest()
    return {'expected_ids': ids, 'inventory_sha256': digest,
            'source_commit': C, 'source_blob': blob,
            'source_bytes': len(raw), 'source_sha256': hashlib.sha256(raw).hexdigest(),
            'source_readback': 'INDEPENDENT_READBACK_MATCH'}


def cases():
    out = []
    def add(name, rows, status, den=0, num=0, inv_edit=None, raw_edit=None, row_edit=None):
        raw = json.dumps(rows, ensure_ascii=True, allow_nan=False,
                         separators=(',', ':')).encode('utf-8')
        inv = inventory(rows, raw)
        if inv_edit: inv_edit(inv)
        supplied = copy.deepcopy(rows)
        if row_edit: row_edit(supplied)
        if raw_edit: raw = raw_edit(raw)
        out.append((name, supplied, inv, raw, status, den, num))

    add('ascii_one_success', [event()], 'CALCULABLE', 1, 1)
    add('ascii_manual', [event(manual_trigger=True)], 'CALCULABLE', 1, 0)
    add('valid_unicode_accent_id', [event('übergabe-π')], 'CALCULABLE', 1, 1)
    add('valid_unicode_emoji_id', [event('ok-😀')], 'CALCULABLE', 1, 1)
    add('valid_emoji_note', [event(note='😀')], 'CALCULABLE', 1, 1)
    add('valid_replacement_char', [event(note='\ufffd')], 'CALCULABLE', 1, 1)
    add('valid_line_separator', [event(note='\u2028')], 'CALCULABLE', 1, 1)
    add('valid_empty_list', [], 'NO_ELIGIBLE_EVENTS', 0, 0)
    add('valid_two_rows', [event(), event('evt-2', automated=False)], 'CALCULABLE', 2, 1)
    add('valid_nested_unicode', [event(meta={'x':['你好','🚀']})], 'CALCULABLE', 1, 1)

    add('invalid_lone_high_surrogate_id', [event('id-\ud800')], 'INCOMPLETE')
    add('invalid_lone_low_surrogate_id', [event('id-\udfff')], 'INCOMPLETE')
    add('invalid_lone_high_surrogate_note', [event(note='\ud800')], 'INCOMPLETE')
    add('invalid_lone_low_surrogate_note', [event(note='\udfff')], 'INCOMPLETE')
    add('invalid_surrogate_in_key', [{**event(), '\ud800':'x'}], 'INCOMPLETE')
    add('invalid_surrogate_nested_dict', [event(meta={'k':['ok', {'inner':'\ud800'}]})], 'INCOMPLETE')
    add('invalid_surrogate_nested_key', [event(meta={'\udfff':'value'})], 'INCOMPLETE')
    add('invalid_surrogate_second_event', [event(), event('evt-2', note='\ud800')], 'INCOMPLETE')
    add('invalid_inventory_only_surrogate', [event()], 'INCOMPLETE',
        inv_edit=lambda i:i.update(expected_ids=['\ud800'], inventory_sha256=H))
    add('invalid_supplied_only_surrogate', [event()], 'INCOMPLETE',
        row_edit=lambda r:r[0].update(note='\ud800'))
    add('invalid_source_only_surrogate', [event()], 'INCOMPLETE',
        raw_edit=lambda raw:raw.replace(b'"id":"evt-1"', b'"id":"\\ud800"'))
    add('invalid_wrong_source_sha256', [event()], 'INCOMPLETE',
        inv_edit=lambda i:i.update(source_sha256=H))
    add('invalid_missing_source_blob', [event()], 'INCOMPLETE',
        inv_edit=lambda i:i.pop('source_blob'))
    add('invalid_wrong_event_ids', [event()], 'INCOMPLETE',
        inv_edit=lambda i:i.update(expected_ids=['other']))
    return out


def run(path):
    spec = importlib.util.spec_from_file_location('isolated_candidate_under_test', path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    records = []
    for name, rows, inv, raw, status, den, num in cases():
        try:
            got = mod.assess(rows, inv, raw)
            actual = [got.get('status'), got.get('eligible_denominator'),
                      got.get('verified_automated_numerator')]
        except Exception as exc:
            actual = ['EXCEPTION:'+type(exc).__name__, None, None]
        expected = [status, den, num]
        records.append({'name':name, 'expected':expected,
                        'actual':actual, 'pass':actual==expected})
    return {'total':len(records), 'passed':sum(r['pass'] for r in records),
            'records':records}

if __name__ == '__main__':
    result = run(Path(sys.argv[1]))
    print(json.dumps(result, ensure_ascii=True, indent=2))
    sys.exit(0 if result['passed']==result['total'] else 1)
