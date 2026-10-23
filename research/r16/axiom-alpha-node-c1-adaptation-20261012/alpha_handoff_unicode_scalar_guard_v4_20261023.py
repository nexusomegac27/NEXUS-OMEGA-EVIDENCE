#!/usr/bin/env python3
"""C1 isolated V4: fail closed on unpaired Unicode surrogate code points.

Extends the immutable V3 source-byte validator without changing its oracle.
The V3->V2 path can raise UnicodeEncodeError for escaped lone surrogates in
inventory IDs, or count surrogate-containing event values as valid. V4
rejects those non-scalar strings before invoking the hash-pinned V3.

Only local input consistency is tested. GitHub provenance, actor identity,
complete project denominator, CI, main merge and WWW parity remain separate.
"""
import hashlib
import importlib.util
from pathlib import Path

_V3_NAME = 'alpha_handoff_source_bytes_guard_v3_20261023.py'
_V3_SHA256 = '1a11635fc49c9787885fc55c220c91d5dd97fe82e24147238bba052501a8e728'
_MAX_NODES = 250000


def _incomplete(reason):
    return {'status': 'INCOMPLETE', 'eligible_denominator': 0,
            'verified_automated_numerator': 0, 'excluded_events': 0,
            'unknown_scope_events': 0, 'rate_from_input_assertions': None,
            'target_90_adjudication': 'NOT_ESTABLISHED_INPUT_ASSERTIONS_ONLY',
            'provenance': 'SOURCE_BYTES_LOCALLY_BOUND_GITHUB_ORIGIN_NOT_AUTHENTICATED',
            'reasons': [reason]}


def _contains_non_scalar(root):
    stack = [root]
    seen = set()
    inspected = 0
    while stack:
        inspected += 1
        if inspected > _MAX_NODES:
            return True
        item = stack.pop()
        if isinstance(item, str):
            if any(0xD800 <= ord(ch) <= 0xDFFF for ch in item):
                return True
        elif isinstance(item, dict):
            if id(item) in seen:
                continue
            seen.add(id(item))
            for key, value in item.items():
                stack.append(key)
                stack.append(value)
        elif isinstance(item, (list, tuple)):
            if id(item) in seen:
                continue
            seen.add(id(item))
            stack.extend(item)
    return False


def _load_v3():
    path = Path(__file__).with_name(_V3_NAME)
    try:
        raw = path.read_bytes()
    except OSError:
        return None
    if hashlib.sha256(raw).hexdigest() != _V3_SHA256:
        return None
    spec = importlib.util.spec_from_file_location('pinned_alpha_handoff_v3', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def assess(events, inventory=None, source_payload=None):
    if _contains_non_scalar(events):
        return _incomplete('event_non_scalar_unicode_or_traversal_limit')
    if isinstance(inventory, dict) and _contains_non_scalar(inventory.get('expected_ids')):
        return _incomplete('inventory_id_non_scalar_unicode_or_traversal_limit')
    base = _load_v3()
    if base is None:
        return _incomplete('pinned_v3_dependency_missing_or_tampered')
    try:
        result = base.assess(events, inventory, source_payload)
    except (UnicodeError, RecursionError):
        return _incomplete('pinned_dependency_unicode_or_recursion_exception')
    result['unicode_scalar_guard'] = 'UNPAIRED_SURROGATES_REJECTED'
    return result
