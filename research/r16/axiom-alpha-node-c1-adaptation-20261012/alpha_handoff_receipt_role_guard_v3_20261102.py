"""C1-only offline V3 receipt-role collision guard; no GitHub authentication.

The three declared receipt roles must use different URLs before a cohort can
be called structurally countable. Different URLs do NOT prove different actors,
executed evaluations, or unattended handoffs. V1 and V2 remain immutable.
"""
import hashlib
import importlib.util
from pathlib import Path

V2_NAME = 'alpha_handoff_population_coverage_guard_v2_20261102.py'
V2_SHA256 = '04ad66f90be63f173709627f14f5bd87f7577b2d810323ce6156f8829befc98e'
EVIDENCE = 'SUPPLIED_FIELDS_NOT_INDEPENDENTLY_AUTHENTICATED'
ROLES = ('trigger_receipt', 'handoff_receipt', 'independent_evaluator_receipt')


def _empty(status, receipt_status):
    return {'status': status, 'numerator': None, 'denominator': None,
            'cohort_rate': None, 'project_rate': 'NOT_COMPUTABLE',
            'evidence_class': EVIDENCE, 'coverage_status': 'NOT_ASSESSED_V3_COLLISION',
            'receipt_status': receipt_status}


def _v2():
    path = Path(__file__).resolve().with_name(V2_NAME)
    try:
        source = path.read_bytes()
    except OSError:
        return None
    if hashlib.sha256(source).hexdigest() != V2_SHA256:
        return None
    spec = importlib.util.spec_from_file_location('_alpha_handoff_v2_pinned', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def assess(events, population):
    v2 = _v2()
    if v2 is None:
        return _empty('HOLD_SCOPED', 'V2_ORIGINAL_BYTES_MISMATCH_OR_MISSING')
    base = v2.assess(events, population)
    if base['status'] != 'COHORT_DECLARED_ONLY':
        return {**base, 'receipt_status': 'NOT_ASSESSED_V2_GATE'}
    v1 = v2._v1()
    if v1 is None:
        return _empty('HOLD_SCOPED', 'V1_ORIGINAL_BYTES_MISMATCH_OR_MISSING')
    for event in events:
        if v1.eligible(event) != 'YES' or not v1.structurally_supported_unattended(event):
            continue
        urls = [event[role] for role in ROLES]
        if len(set(urls)) != len(ROLES):
            return {**_empty('NOT_COMPUTABLE', 'RECEIPT_ROLE_URL_COLLISION'),
                    'coverage_status': base['coverage_status']}
    return {**base, 'receipt_status': 'DISTINCT_DECLARED_URLS_NOT_AUTHENTICATED'}
