"""C1 isolated V4: prevent one declared handoff receipt counting two events.

This does not dereference GitHub URLs or authenticate provider events. Shared
trigger/evaluator receipts may be legitimate; only eligible structurally
counted events require distinct handoff receipt URLs. V1-V3 stay immutable.
"""
import hashlib
import importlib.util
from pathlib import Path

V3_NAME = 'alpha_handoff_receipt_role_guard_v3_20261102.py'
V3_SHA256 = '40485983568c9c0722abdf4817fb3ef4061d30de44235b7378358772860c85df'
EVIDENCE = 'SUPPLIED_FIELDS_NOT_INDEPENDENTLY_AUTHENTICATED'


def _empty(status, reason):
    return {'status': status, 'numerator': None, 'denominator': None,
            'cohort_rate': None, 'project_rate': 'NOT_COMPUTABLE',
            'evidence_class': EVIDENCE, 'coverage_status': 'NOT_ASSESSED_V4_REUSE',
            'receipt_status': reason}


def _v3():
    path = Path(__file__).resolve().with_name(V3_NAME)
    try:
        data = path.read_bytes()
    except OSError:
        return None
    if hashlib.sha256(data).hexdigest() != V3_SHA256:
        return None
    spec = importlib.util.spec_from_file_location('_alpha_handoff_v3_pinned', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def assess(events, population):
    prior = _v3()
    if prior is None:
        return _empty('HOLD_SCOPED', 'V3_ORIGINAL_BYTES_MISMATCH_OR_MISSING')
    base = prior.assess(events, population)
    if base['status'] != 'COHORT_DECLARED_ONLY':
        return {**base, 'receipt_status': 'NOT_ASSESSED_V3_GATE'}
    v2 = prior._v2()
    if v2 is None:
        return _empty('HOLD_SCOPED', 'V2_ORIGINAL_BYTES_MISMATCH_OR_MISSING')
    v1 = v2._v1()
    if v1 is None:
        return _empty('HOLD_SCOPED', 'V1_ORIGINAL_BYTES_MISMATCH_OR_MISSING')
    seen = set()
    for event in events:
        if v1.eligible(event) != 'YES' or not v1.structurally_supported_unattended(event):
            continue
        receipt = event['handoff_receipt']
        if receipt in seen:
            return {**_empty('NOT_COMPUTABLE', 'CROSS_EVENT_HANDOFF_RECEIPT_REUSED'),
                    'coverage_status': base['coverage_status']}
        seen.add(receipt)
    return {**base, 'receipt_status': 'DISTINCT_ELIGIBLE_HANDOFF_URLS_DECLARED_ONLY'}
