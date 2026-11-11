#!/usr/bin/env python3
"""Frozen independent C1 evaluator: handoff event source-byte binding.

Oracle fixed before V3 candidate implementation. Synthetic fixtures only.
This oracle tests local bytes/metadata consistency, NOT GitHub actor identity,
source completeness, Git commit ancestry, scientific validity or 90% attainment.
"""
import copy
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

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


def encoded(rows, **kwargs):
    return json.dumps(rows, ensure_ascii=False, separators=(',', ':'),
                      allow_nan=False, **kwargs).encode('utf-8')


def inventory(rows, payload):
    ids = sorted(r['id'] for r in rows)
    digest = hashlib.sha256(json.dumps(ids, ensure_ascii=False,
                       separators=(',', ':')).encode('utf-8')).hexdigest()
    return {'expected_ids': ids, 'inventory_sha256': digest,
            'source_commit': C, 'source_blob': hashlib.sha1(
                b'blob ' + str(len(payload)).encode('ascii') + b'\0' + payload).hexdigest(),
            'source_bytes': len(payload), 'source_sha256': hashlib.sha256(payload).hexdigest(),
            'source_readback': 'INDEPENDENT_READBACK_MATCH'}


def cases():
    out = []
    def add(name, rows, status, denominator=0, numerator=0,
            transform=None, raw=None, rebuild=True):
        original = encoded(rows) if raw is None else raw
        inv = inventory(rows, original)
        supplied = copy.deepcopy(rows)
        payload = original
        if transform:
            supplied, inv, payload = transform(supplied, inv, payload)
        out.append((name, supplied, inv, payload, status, denominator, numerator))

    add('valid_one_success', [event()], 'CALCULABLE', 1, 1)
    add('valid_one_manual', [event(manual_trigger=True)], 'CALCULABLE', 1, 0)
    add('valid_two_mixed', [event(), event('evt-2', automated=False)], 'CALCULABLE', 2, 1)
    add('valid_one_excluded', [event(public=False)], 'NO_ELIGIBLE_EVENTS')
    add('valid_mixed_excluded', [event(), event('evt-2', routine=False)], 'CALCULABLE', 1, 1)
    add('valid_unicode_id', [event('übergabe-π')], 'CALCULABLE', 1, 1)
    add('valid_json_ascii_escape', [event('übergabe-π')], 'CALCULABLE', 1, 1,
        raw=json.dumps([event('übergabe-π')], ensure_ascii=True).encode())
    add('valid_empty_inventory', [], 'NO_ELIGIBLE_EVENTS')
    add('valid_no_verification', [event(verification='REPORTED_ONLY')], 'CALCULABLE', 1, 0)
    add('valid_missing_hash', [event(source_sha256=None)], 'CALCULABLE', 1, 0)
    add('valid_no_automation', [event(automated=False)], 'CALCULABLE', 1, 0)
    add('valid_pretty_json', [event()], 'CALCULABLE', 1, 1,
        raw=json.dumps([event()], indent=2).encode())

    add('missing_payload', [event()], 'INCOMPLETE', transform=lambda r,i,p:(r,i,None))
    add('payload_is_string', [event()], 'INCOMPLETE', transform=lambda r,i,p:(r,i,p.decode()))
    add('changed_payload_same_id', [event()], 'INCOMPLETE',
        transform=lambda r,i,p:(r,i,p.replace(b'"automated":true', b'"automated":false')))
    add('changed_input_same_id', [event()], 'INCOMPLETE',
        transform=lambda r,i,p:([event(automated=False)],i,p))
    add('wrong_byte_count', [event()], 'INCOMPLETE',
        transform=lambda r,i,p:(r,{**i,'source_bytes':i['source_bytes']+1},p))
    add('wrong_git_blob', [event()], 'INCOMPLETE',
        transform=lambda r,i,p:(r,{**i,'source_blob':'f'*40},p))
    add('wrong_sha256', [event()], 'INCOMPLETE',
        transform=lambda r,i,p:(r,{**i,'source_sha256':'f'*64},p))
    add('missing_sha256', [event()], 'INCOMPLETE',
        transform=lambda r,i,p:(r,{k:v for k,v in i.items() if k!='source_sha256'},p))
    duplicate = b'[{"id":"evt-1","id":"evt-1","routine":true}]'
    add('duplicate_json_key', [event()], 'INCOMPLETE', raw=duplicate)
    add('nonfinite_json_nan', [event()], 'INCOMPLETE', raw=b'[{"id":"evt-1","value":NaN}]')
    add('malformed_json', [event()], 'INCOMPLETE', raw=b'[{"id":"evt-1",}]')
    add('json_object_not_list', [event()], 'INCOMPLETE', raw=b'{"id":"evt-1"}')
    add('payload_reordered_events', [event(), event('evt-2')], 'INCOMPLETE',
        transform=lambda r,i,p:(r,i,encoded(list(reversed(r)))))
    add('payload_invalid_utf8', [event()], 'INCOMPLETE', raw=b'\xff\xfe')
    add('bool_int_semantic_alias', [event()], 'INCOMPLETE',
        transform=lambda r,i,p:([event(automated=1)],i,p))
    add('source_sha256_uppercase', [event()], 'INCOMPLETE',
        transform=lambda r,i,p:(r,{**i,'source_sha256':i['source_sha256'].upper()},p))
    return out


def run(module_path, baseline=False):
    spec = importlib.util.spec_from_file_location('candidate_under_test', module_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    failures = []
    records = []
    for name, rows, inv, payload, status, den, num in cases():
        try:
            result = mod.assess(rows, inv) if baseline else mod.assess(rows, inv, payload)
            actual = (result.get('status'), result.get('eligible_denominator'),
                      result.get('verified_automated_numerator'))
        except Exception as exc:
            actual = ('EXCEPTION:' + type(exc).__name__, None, None)
        expected = (status, den, num)
        passed = actual == expected
        records.append({'fixture':name, 'expected':expected, 'actual':actual, 'pass':passed})
        if not passed:
            failures.append(name)
    return {'total':len(records), 'passed':len(records)-len(failures),
            'failed':failures, 'records':records}


if __name__ == '__main__':
    report = run(Path(sys.argv[1]), baseline='--baseline' in sys.argv[2:])
    print(json.dumps(report, indent=2))
    sys.exit(0 if report['passed'] == report['total'] else 1)
