#!/usr/bin/env python3
"""C1 isolated V3: bind handoff events to physically supplied source bytes.

Rejects metadata-only 'readback' claims when actual source bytes are absent.
Checks exact length, SHA-256, Git blob SHA-1, strict JSON and event equality.
A matching Git blob digest is NOT proof of GitHub commit membership, actor
identity, completeness of the original source, or independent verification.
No network, repository writes, runtime change, or claim promotion.
"""
import hashlib
import importlib.util
import json
from pathlib import Path
import re

_V2_NAME = 'alpha_handoff_inventory_completeness_guard_v2_20261023.py'
_V2_SHA256 = '2b3d33497df837267ac3d0a3f2a3080097ec784604b4940e2a217de34500ef72'
_SHA256 = re.compile(r'[0-9a-f]{64}\Z')
_MAX_BYTES = 4 * 1024 * 1024


def _incomplete(reason):
    return {'status': 'INCOMPLETE', 'eligible_denominator': 0,
            'verified_automated_numerator': 0, 'excluded_events': 0,
            'unknown_scope_events': 0, 'rate_from_input_assertions': None,
            'target_90_adjudication': 'NOT_ESTABLISHED_INPUT_ASSERTIONS_ONLY',
            'provenance': 'SOURCE_BYTES_LOCALLY_BOUND_GITHUB_ORIGIN_NOT_AUTHENTICATED',
            'reasons': [reason]}


def _strict_pairs(pairs):
    obj = {}
    for key, value in pairs:
        if key in obj:
            raise ValueError('duplicate_json_key')
        obj[key] = value
    return obj


def _reject_constant(value):
    raise ValueError('nonfinite_json_constant:' + value)


def _load_v2():
    path = Path(__file__).with_name(_V2_NAME)
    try:
        raw = path.read_bytes()
    except OSError:
        return None
    if hashlib.sha256(raw).hexdigest() != _V2_SHA256:
        return None
    spec = importlib.util.spec_from_file_location('pinned_alpha_handoff_v2', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def assess(events, inventory=None, source_payload=None):
    if not isinstance(inventory, dict):
        return _incomplete('inventory_not_bound')
    if type(source_payload) is not bytes:
        return _incomplete('source_original_bytes_not_supplied')
    if not 0 < len(source_payload) <= _MAX_BYTES:
        return _incomplete('source_byte_size_out_of_bounds')
    if type(inventory.get('source_bytes')) is not int or inventory['source_bytes'] != len(source_payload):
        return _incomplete('source_byte_count_mismatch')
    digest = inventory.get('source_sha256')
    if not isinstance(digest, str) or _SHA256.fullmatch(digest) is None:
        return _incomplete('source_sha256_missing_or_invalid')
    if hashlib.sha256(source_payload).hexdigest() != digest:
        return _incomplete('source_sha256_mismatch')
    blob = hashlib.sha1(b'blob ' + str(len(source_payload)).encode('ascii')
                        + b'\0' + source_payload).hexdigest()
    if inventory.get('source_blob') != blob:
        return _incomplete('source_git_blob_mismatch')
    try:
        decoded = json.loads(source_payload.decode('utf-8'),
                             object_pairs_hook=_strict_pairs,
                             parse_constant=_reject_constant)
        if not isinstance(decoded, list) or not isinstance(events, list):
            return _incomplete('event_payload_not_list')
        left = json.dumps(decoded, sort_keys=True, ensure_ascii=False,
                          allow_nan=False, separators=(',', ':'))
        right = json.dumps(events, sort_keys=True, ensure_ascii=False,
                           allow_nan=False, separators=(',', ':'))
    except (ValueError, TypeError, UnicodeError, RecursionError, OverflowError):
        return _incomplete('event_payload_invalid_json')
    if left != right:
        return _incomplete('event_payload_does_not_match_supplied_rows')
    base = _load_v2()
    if base is None:
        return _incomplete('pinned_v2_dependency_missing_or_tampered')
    result = base.assess(events, inventory)
    result['source_byte_binding'] = 'LOCAL_BYTES_LENGTH_SHA256_GIT_BLOB_AND_JSON_MATCH'
    result['source_authentication'] = 'NOT_ESTABLISHED_BY_OFFLINE_GUARD'
    return result
