#!/usr/bin/env python3
"""Isolated C1 guard composing the prior PR census with caller-supplied original bytes.

This does not authenticate the API, caller, completeness of the source set, or a PR actor.
"""
import base64
import binascii
import hashlib
import json
import re
import sys

from alpha_pr_dual_endpoint_census_guard_v1_20261031 import verify as verify_dual

HEX40 = re.compile(r'[0-9a-f]{40}\Z')
HEX64 = re.compile(r'[0-9a-f]{64}\Z')


def require(ok, label):
    if not ok:
        raise ValueError(label)


def unique_pairs(pairs):
    obj = {}
    for k, v in pairs:
        require(k not in obj, 'duplicate_json_key')
        obj[k] = v
    return obj


def verify(payload):
    require(isinstance(payload, dict), 'envelope')
    dual = payload.get('dual_endpoint')
    dual_result = verify_dual(dual)
    source = payload.get('source_bytes')
    require(isinstance(source, dict), 'source_section')
    pr = dual['pr']
    require(type(source.get('pr_number')) is int and source['pr_number'] == pr['number']
            and source.get('head_sha') == pr['head_sha'], 'source_pr_binding')
    files = source.get('files')
    require(isinstance(files, list) and len(files) == pr['changed_files'], 'source_count')
    api_files = {item['filename']: item['sha'] for item in dual['api_file_listing']['pages'][0]['items']}
    seen = set()
    for item in files:
        require(isinstance(item, dict), 'source_entry')
        path = item.get('path')
        require(isinstance(path, str) and path in api_files and path not in seen, 'source_path')
        seen.add(path)
        require(type(item.get('bytes')) is int and 0 <= item['bytes'] <= 1048576
                and isinstance(item.get('sha256'), str) and HEX64.fullmatch(item['sha256'])
                and isinstance(item.get('git_blob'), str) and HEX40.fullmatch(item['git_blob'])
                and isinstance(item.get('content_b64'), str), 'source_metadata')
        try:
            raw = base64.b64decode(item['content_b64'], validate=True)
        except (ValueError, binascii.Error) as exc:
            raise ValueError('invalid_base64') from exc
        require(base64.b64encode(raw).decode('ascii') == item['content_b64'], 'noncanonical_base64')
        require(len(raw) == item['bytes'], 'source_length')
        require(hashlib.sha256(raw).hexdigest() == item['sha256'], 'source_sha256')
        blob = hashlib.sha1(b'blob ' + str(len(raw)).encode('ascii') + b'\0' + raw).hexdigest()
        require(blob == item['git_blob'] == api_files[path], 'source_blob_cross_binding')
    require(seen == set(api_files), 'source_file_set')
    return {'status': 'DUAL_ENDPOINT_AND_SOURCE_BLOB_MATCH_UNAUTHENTICATED_INPUT',
            'matched_files': len(seen), 'pr_number': pr['number'],
            'api_transport_authenticated': False, 'actor_authenticated': False,
            'source_set_completeness_authenticated': False,
            'project_automation_rate': 'NOT_COMPUTABLE',
            'project_full_readback_rate': 'NOT_COMPUTABLE',
            'claim_ceiling': 'C1_DESCRIPTIVE_ONLY',
            'prior_dual_status': dual_result['status']}


def main():
    try:
        obj = json.loads(sys.stdin.read(), object_pairs_hook=unique_pairs,
                         parse_constant=lambda _: (_ for _ in ()).throw(ValueError('nonfinite_json')))
        result = verify(obj)
    except (ValueError, TypeError, KeyError, RecursionError, UnicodeError, OverflowError) as exc:
        result = {'status': 'FAIL_CLOSED', 'reason': str(exc)[:120]}
    print(json.dumps(result, sort_keys=True))
    return 2 if result['status'] == 'FAIL_CLOSED' else 0


if __name__ == '__main__':
    sys.exit(main())
