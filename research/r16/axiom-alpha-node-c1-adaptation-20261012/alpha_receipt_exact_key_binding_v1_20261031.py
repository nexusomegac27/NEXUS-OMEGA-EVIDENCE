#!/usr/bin/env python3
"""C1-only scoped receipt-key binder; never authenticates caller-supplied API data."""
import json
import re
import sys

REPO = 'nexusomegac27/NEXUS-OMEGA-EVIDENCE'
PR_URL = 'https://github.com/' + REPO + '/pull/'
HEX40 = re.compile(r'[0-9a-f]{40}\Z')
KEY_LINE = re.compile(r'([A-Z][A-Z0-9_]*)=(.*)\Z')
BINDING_KEYS = {'CLAIM_CEILING', 'PREDECESSOR_PR', 'PR', 'OWNER_PR',
                'ACTUAL_MAIN_READBACK', 'ACTUAL_MAIN', 'MAIN_AFTER'}


def require(ok, label):
    if not ok:
        raise ValueError(label)


def unique_pairs(pairs):
    d = {}
    for k, v in pairs:
        require(k not in d, 'duplicate_json_key')
        d[k] = v
    return d


def fields(body):
    require(isinstance(body, str) and 0 < len(body) <= 65536, 'receipt_body')
    out = {}
    for line in body.splitlines():
        match = KEY_LINE.fullmatch(line)
        if match:
            key, value = match.groups()
            if key in BINDING_KEYS:
                require(key not in out, 'duplicate_binding_field:' + key)
                out[key] = value
    return out


def verify(data):
    require(isinstance(data, dict) and data.get('schema_version') == 'alpha_receipt_exact_key_v1'
            and data.get('repository') == REPO, 'envelope')
    records = data.get('records')
    require(isinstance(records, list) and 0 < len(records) <= 100, 'record_count')
    seen_pr, seen_id = set(), set()
    for record in records:
        require(isinstance(record, dict), 'record')
        n, receipt_id, main = (record.get(k) for k in ('expected_pr', 'receipt_id', 'expected_main'))
        require(type(n) is int and n > 1 and n not in seen_pr, 'expected_pr')
        require(type(receipt_id) is int and receipt_id > 0 and receipt_id not in seen_id, 'receipt_id')
        require(isinstance(main, str) and HEX40.fullmatch(main), 'expected_main')
        require(record.get('actor_login') == 'nexusomegac27', 'actor_label')
        seen_pr.add(n)
        seen_id.add(receipt_id)
        f = fields(record.get('body'))
        require(f.get('CLAIM_CEILING') == 'C1_DESCRIPTIVE_ONLY', 'claim_ceiling')
        require(f.get('PREDECESSOR_PR') == str(n - 1), 'predecessor')
        pr_keys = [k for k in ('PR', 'OWNER_PR') if k in f]
        require(len(pr_keys) == 1, 'pr_key_cardinality')
        actual_pr = f['PR'] if pr_keys[0] == 'PR' else PR_URL + f['OWNER_PR']
        require(actual_pr == PR_URL + str(n), 'exact_pr_binding')
        main_keys = [k for k in ('ACTUAL_MAIN_READBACK', 'ACTUAL_MAIN', 'MAIN_AFTER') if k in f]
        require(len(main_keys) == 1, 'main_key_cardinality')
        require(f[main_keys[0]] == main, 'exact_main_binding')
    return {'status': 'SCOPED_RECEIPT_BINDINGS_MATCH_UNAUTHENTICATED_INPUT',
            'matched_receipts': len(records), 'actor_authenticated': False,
            'api_transport_authenticated': False, 'event_census_complete': False,
            'project_automation_rate': 'NOT_COMPUTABLE',
            'project_full_readback_rate': 'NOT_COMPUTABLE',
            'claim_ceiling': 'C1_DESCRIPTIVE_ONLY'}


def main():
    try:
        data = json.loads(sys.stdin.read(), object_pairs_hook=unique_pairs,
                          parse_constant=lambda _: (_ for _ in ()).throw(ValueError('nonfinite_json')))
        result = verify(data)
    except (ValueError, TypeError, KeyError, RecursionError, UnicodeError, OverflowError) as exc:
        result = {'status': 'FAIL_CLOSED', 'reason': str(exc)[:120]}
    print(json.dumps(result, sort_keys=True))
    return 2 if result['status'] == 'FAIL_CLOSED' else 0


if __name__ == '__main__':
    sys.exit(main())
