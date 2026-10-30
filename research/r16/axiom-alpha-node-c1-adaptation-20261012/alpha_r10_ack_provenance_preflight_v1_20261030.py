#!/usr/bin/env python3
"""C1-only offline R10 ACK provenance classifier; not a GitHub authenticator."""
import json
import re
import sys

FIELDS = {
    'source_commit', 'source_sha256', 'source_bytes', 'source_git_blob',
    'source_bytes_rehashed', 'source_blob_rehashed', 'owner_login',
    'actor_login', 'actor_origin', 'external_actor_allowlist',
    'receipt_origin', 'claims_independent_receiver_ack',
    'claims_expert_research_executed',
}
HEX40 = re.compile(r'^[0-9a-f]{40}$')
HEX64 = re.compile(r'^[0-9a-f]{64}$')


def pairs_unique(pairs):
    obj = {}
    for key, value in pairs:
        if key in obj:
            raise ValueError('DUPLICATE_JSON_KEY')
        obj[key] = value
    return obj


def check(doc):
    if type(doc) is not dict or set(doc) != FIELDS:
        raise ValueError('INVALID_FIELDS')
    for key, pattern in [('source_commit', HEX40), ('source_sha256', HEX64), ('source_git_blob', HEX40)]:
        if type(doc[key]) is not str or not pattern.fullmatch(doc[key]):
            raise ValueError('INVALID_DIGEST_OR_COMMIT')
    if type(doc['source_bytes']) is not int or doc['source_bytes'] <= 0:
        raise ValueError('INVALID_BYTE_COUNT')
    for key in ('source_bytes_rehashed', 'source_blob_rehashed',
                'claims_independent_receiver_ack', 'claims_expert_research_executed'):
        if type(doc[key]) is not bool:
            raise ValueError('INVALID_BOOLEAN')
    for key in ('owner_login', 'actor_login'):
        if type(doc[key]) is not str or not re.fullmatch(r'[A-Za-z0-9-]{1,39}', doc[key]):
            raise ValueError('INVALID_ACTOR')
    allowlist = doc['external_actor_allowlist']
    if type(allowlist) is not list or any(type(x) is not str or not re.fullmatch(r'[A-Za-z0-9-]{1,39}', x) for x in allowlist):
        raise ValueError('INVALID_ALLOWLIST')
    if len({x.lower() for x in allowlist}) != len(allowlist):
        raise ValueError('DUPLICATE_ALLOWLIST')
    if doc['actor_origin'] not in ('GITHUB_API', 'SELF_DECLARED', 'UNKNOWN'):
        raise ValueError('INVALID_ACTOR_ORIGIN')
    if doc['receipt_origin'] not in ('EXTERNAL_GITHUB_ASSET', 'OWNER_MEDIATED_FILE', 'OWNER_ISSUE_COMMENT'):
        raise ValueError('INVALID_RECEIPT_ORIGIN')
    bytes_ok = doc['source_bytes_rehashed'] and doc['source_blob_rehashed']
    actor_ok = (doc['actor_origin'] == 'GITHUB_API'
                and doc['actor_login'].lower() != doc['owner_login'].lower()
                and doc['actor_login'].lower() in {x.lower() for x in allowlist})
    origin_ok = doc['receipt_origin'] == 'EXTERNAL_GITHUB_ASSET'
    eligible = bool(bytes_ok and actor_ok and origin_ok and doc['claims_independent_receiver_ack'])
    return {
        'source_byte_integrity': 'MATCH_REPORTED_FROM_INDEPENDENT_INPUT' if bytes_ok else 'NOT_ESTABLISHED',
        'receiver_ack': 'ELIGIBLE_FOR_SEPARATE_AUTHENTICATION_AND_ADJUDICATION' if eligible else 'NOT_ESTABLISHED',
        'expert_research_execution': 'SOURCE_ASSERTED_NOT_INDEPENDENTLY_ADJUDICATED' if doc['claims_expert_research_executed'] else 'NOT_ESTABLISHED',
        'axiom_scientific_adjudication': 'NOT_PERFORMED',
        'claim_ceiling': 'C1_DESCRIPTIVE_ONLY',
    }


def main():
    try:
        raw = sys.stdin.buffer.read(65537)
        if len(raw) > 65536:
            raise ValueError('INPUT_TOO_LARGE')
        doc = json.loads(raw.decode('utf-8'), object_pairs_hook=pairs_unique,
                         parse_constant=lambda _: (_ for _ in ()).throw(ValueError('NONFINITE')))
        out = check(doc)
        print(json.dumps({'ok': True, 'result': out}, sort_keys=True))
    except (ValueError, UnicodeDecodeError, TypeError) as exc:
        print(json.dumps({'ok': False, 'error': str(exc)}, sort_keys=True))
        sys.exit(2)


if __name__ == '__main__':
    main()
