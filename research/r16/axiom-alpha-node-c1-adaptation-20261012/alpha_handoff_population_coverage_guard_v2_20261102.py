"""C1-only, offline population-ID coverage guard; does not authenticate GitHub.

V2 wraps immutable V1 rather than rewriting a bound predecessor. Every
population identifier is caller-supplied; an exact set is NOT external proof.
"""
import hashlib
import importlib.util
import json
from pathlib import Path
import re

V1_NAME = 'alpha_handoff_denominator_guard_v1_20261102.py'
V1_SHA256 = '560ea49f753fa1a1118b12526e837bdfa3a055dfabe87894f553a7f3b1d04fb9'
HEX64 = re.compile(r'[0-9a-f]{64}\Z')
EVENT_ID = re.compile(r'[A-Za-z0-9_.:-]{1,128}\Z')
EVIDENCE = 'SUPPLIED_FIELDS_NOT_INDEPENDENTLY_AUTHENTICATED'


def _empty(status, coverage):
    return {'status': status, 'numerator': None, 'denominator': None,
            'cohort_rate': None, 'project_rate': 'NOT_COMPUTABLE',
            'evidence_class': EVIDENCE, 'coverage_status': coverage}


def _v1():
    path = Path(__file__).resolve().with_name(V1_NAME)
    try:
        source = path.read_bytes()
    except OSError:
        return None
    if hashlib.sha256(source).hexdigest() != V1_SHA256:
        return None
    spec = importlib.util.spec_from_file_location('_alpha_handoff_v1_pinned', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def ids_sha256(ids):
    """Deterministic declared-ID-list digest, not a GitHub source hash."""
    return hashlib.sha256(json.dumps(ids, ensure_ascii=True,
                                     separators=(',', ':')).encode('utf-8')).hexdigest()


def assess(events, population):
    prior = _v1()
    if prior is None:
        return _empty('HOLD_SCOPED', 'V1_ORIGINAL_BYTES_MISMATCH_OR_MISSING')
    base = prior.assess(events, population)
    if base['status'] != 'COHORT_DECLARED_ONLY':
        return {**base, 'coverage_status': 'NOT_ASSESSED_V1_GATE'}
    ids = population.get('enumerated_event_ids')
    if ids is None:
        return _empty('NOT_COMPUTABLE', 'ENUMERATED_IDS_MISSING')
    if (not isinstance(ids, list) or not 1 <= len(ids) <= 1000
            or any(not isinstance(i, str) or EVENT_ID.fullmatch(i) is None for i in ids)
            or ids != sorted(set(ids))):
        return _empty('INVALID_INPUT', 'MALFORMED_OR_DUPLICATE_ENUMERATION')
    count = population.get('enumerated_event_count')
    if not isinstance(count, int) or isinstance(count, bool) or count != len(ids):
        return _empty('INVALID_INPUT', 'ENUMERATION_COUNT_MISMATCH')
    digest = population.get('enumerated_event_ids_sha256')
    if not isinstance(digest, str) or HEX64.fullmatch(digest) is None or digest != ids_sha256(ids):
        return _empty('NOT_COMPUTABLE', 'ENUMERATED_ID_DIGEST_MISMATCH')
    if set(e['id'] for e in events) != set(ids):
        return _empty('NOT_COMPUTABLE', 'EVENT_ID_SET_MISMATCH')
    return {**base, 'coverage_status': 'EXACT_DECLARED_ID_SET'}
