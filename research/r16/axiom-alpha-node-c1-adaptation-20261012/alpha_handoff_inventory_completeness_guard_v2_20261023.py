#!/usr/bin/env python3
"""C1 isolated inventory-completeness gate for handoff denominator V1.

The V1 guard can compute a plausible 1/1 from a truncated event stream.
V2 requires a complete caller-provided, SHA256-bound expected-ID inventory
before allowing V1 to compute any rate. Inventory provenance fields remain
CALLER ASSERTIONS; this module cannot independently authenticate GitHub
coverage, ownership, permissions, source bytes or 90-percent attainment.
No network, runtime changes, repository writes or oracle modification.
"""
import hashlib
import importlib.util
import json
from pathlib import Path
import re

_V1_NAME = 'alpha_handoff_denominator_guard_v1_20261023.py'
_V1_SHA256 = '38ad809c61c86346b3b63bdea4fbad3f13c60dab08311cf155b5674632d54d95'
_SHA256 = re.compile(r'[0-9a-f]{64}\Z')
_SHA40 = re.compile(r'[0-9a-f]{40}\Z')


def _incomplete(reason, expected=0, observed=0, missing=None, unexpected=None):
    return {
        'status': 'INCOMPLETE',
        'eligible_denominator': 0,
        'verified_automated_numerator': 0,
        'excluded_events': 0,
        'unknown_scope_events': 0,
        'rate_from_input_assertions': None,
        'target_90_adjudication': 'NOT_ESTABLISHED_INPUT_ASSERTIONS_ONLY',
        'provenance': 'CALLER_ASSERTED_NOT_AUTHENTICATED_BY_THIS_GUARD',
        'inventory_expected_count': expected,
        'inventory_observed_count': observed,
        'missing_ids': sorted(missing or []),
        'unexpected_ids': sorted(unexpected or []),
        'reasons': [reason],
    }


def _hash_match(value, regex):
    return isinstance(value, str) and regex.fullmatch(value) is not None


def _load_v1():
    path = Path(__file__).with_name(_V1_NAME)
    try:
        raw = path.read_bytes()
    except OSError:
        return None
    if hashlib.sha256(raw).hexdigest() != _V1_SHA256:
        return None
    spec = importlib.util.spec_from_file_location('pinned_alpha_handoff_v1', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def assess(events, inventory=None):
    if not isinstance(inventory, dict):
        return _incomplete('inventory_not_bound')
    expected = inventory.get('expected_ids')
    if (not isinstance(expected, list)
            or any(not isinstance(i, str) or not i for i in expected)
            or len(expected) != len(set(expected))):
        return _incomplete('inventory_ids_invalid')
    expected_count = len(expected)
    canonical = json.dumps(sorted(expected), ensure_ascii=False,
                           separators=(',', ':')).encode('utf-8')
    if (not _hash_match(inventory.get('inventory_sha256'), _SHA256)
            or hashlib.sha256(canonical).hexdigest() != inventory['inventory_sha256']):
        return _incomplete('inventory_digest_mismatch', expected_count)
    if (not _hash_match(inventory.get('source_commit'), _SHA40)
            or not _hash_match(inventory.get('source_blob'), _SHA40)
            or type(inventory.get('source_bytes')) is not int
            or inventory['source_bytes'] <= 0
            or inventory.get('source_readback') != 'INDEPENDENT_READBACK_MATCH'):
        return _incomplete('inventory_provenance_unbound', expected_count)
    if not isinstance(events, list):
        return _incomplete('events_not_list', expected_count)
    seen = set()
    for row in events:
        if not isinstance(row, dict):
            return _incomplete('event_not_object', expected_count, len(events))
        ident = row.get('id')
        if not isinstance(ident, str) or not ident or ident in seen:
            return _incomplete('event_id_invalid_or_duplicate', expected_count, len(events))
        seen.add(ident)
    expected_set = set(expected)
    if seen != expected_set:
        return _incomplete('inventory_coverage_mismatch', expected_count, len(events),
                           expected_set - seen, seen - expected_set)
    base = _load_v1()
    if base is None:
        return _incomplete('pinned_v1_dependency_missing_or_tampered', expected_count, len(events))
    result = base.assess(events)
    result['inventory_expected_count'] = expected_count
    result['inventory_observed_count'] = len(events)
    result['inventory_binding'] = 'CALLER_ASSERTED_DIGEST_MATCH_NOT_SOURCE_AUTHENTICATION'
    return result
