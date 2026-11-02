"""C1 isolated V5: canonical GitHub issue-comment ID collision guard.

A URL string is not a GitHub-authenticated receipt. This guard only catches
aliases of the same declared issue-comment ID across receipt roles/events.
The pinned V1-V4 files remain unchanged; no network or production writes.
"""
import hashlib
import importlib.util
from pathlib import Path
import re

V4_NAME = 'alpha_handoff_cross_event_receipt_guard_v4_20261102.py'
V4_SHA256 = '16e797b4e60d5854c7aa3cd25a22511f0cd6e4e8273eb13dca097a7f62ed8b2a'
COMMENT_ANCHOR = re.compile(r'#issuecomment-([0-9]+)\Z')
ROLES = ('trigger_receipt', 'handoff_receipt', 'independent_evaluator_receipt')
EVIDENCE = 'SUPPLIED_FIELDS_NOT_INDEPENDENTLY_AUTHENTICATED'


def _empty(status, reason):
    return {'status': status, 'numerator': None, 'denominator': None,
            'cohort_rate': None, 'project_rate': 'NOT_COMPUTABLE',
            'evidence_class': EVIDENCE, 'coverage_status': 'NOT_ASSESSED_V5_IDENTITY',
            'receipt_status': reason}


def _v4():
    path = Path(__file__).resolve().with_name(V4_NAME)
    try:
        data = path.read_bytes()
    except OSError:
        return None
    if hashlib.sha256(data).hexdigest() != V4_SHA256:
        return None
    spec = importlib.util.spec_from_file_location('_alpha_handoff_v4_pinned', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _identity(url):
    match = COMMENT_ANCHOR.search(url)
    if match:
        return ('github_issue_comment', match.group(1).lstrip('0') or '0')
    return ('exact_url', url)


def assess(events, population):
    prior = _v4()
    if prior is None:
        return _empty('HOLD_SCOPED', 'V4_ORIGINAL_BYTES_MISMATCH_OR_MISSING')
    base = prior.assess(events, population)
    if base['status'] != 'COHORT_DECLARED_ONLY':
        return {**base, 'receipt_status': 'NOT_ASSESSED_V4_GATE'}
    v3 = prior._v3()
    v2 = v3._v2() if v3 is not None else None
    v1 = v2._v1() if v2 is not None else None
    if v1 is None:
        return _empty('HOLD_SCOPED', 'PINNED_V1_V3_SOURCE_UNAVAILABLE')
    seen_handoffs = set()
    for event in events:
        if v1.eligible(event) != 'YES' or not v1.structurally_supported_unattended(event):
            continue
        keys = [_identity(event[role]) for role in ROLES]
        if len(set(keys)) != len(ROLES):
            return {**_empty('NOT_COMPUTABLE', 'CANONICAL_RECEIPT_ROLE_ID_COLLISION'),
                    'coverage_status': base['coverage_status']}
        if keys[1] in seen_handoffs:
            return {**_empty('NOT_COMPUTABLE', 'CANONICAL_HANDOFF_COMMENT_ID_REUSED'),
                    'coverage_status': base['coverage_status']}
        seen_handoffs.add(keys[1])
    return {**base, 'receipt_status': 'DISTINCT_CANONICAL_HANDOFF_IDENTITIES_DECLARED_ONLY'}
