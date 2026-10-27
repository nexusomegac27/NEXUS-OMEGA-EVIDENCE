#!/usr/bin/env python3
"""C1 research-only handoff denominator accounting guard.

Input rows are caller assertions, NOT independently authenticated GitHub facts.
The caller must verify each source, commit and blob separately. The guard
prevents private/inaccessible/unauthorized/nonroutine events from inflating
an eligible denominator or an automated success numerator. Unknown scope
makes the rate NOT_COMPUTABLE; no claim that 90% was attained follows.
No network, repository write, runtime update or model modification.
"""
import re

_SHA256 = re.compile(r'[0-9a-f]{64}\Z')
_SHA40 = re.compile(r'[0-9a-f]{40}\Z')
_SCOPE = ('routine', 'public', 'authorized', 'accessible')

def _valid_hash(value, pattern):
    return isinstance(value, str) and pattern.fullmatch(value) is not None

def _success(event):
    return (type(event.get('automated')) is bool and event['automated']
            and type(event.get('manual_trigger')) is bool
            and not event['manual_trigger']
            and event.get('verification') == 'INDEPENDENT_READBACK_MATCH'
            and _valid_hash(event.get('source_sha256'), _SHA256)
            and _valid_hash(event.get('readback_sha256'), _SHA256)
            and event['source_sha256'] == event['readback_sha256']
            and _valid_hash(event.get('readback_commit'), _SHA40)
            and _valid_hash(event.get('readback_blob'), _SHA40)
            and type(event.get('source_bytes')) is int
            and event['source_bytes'] > 0)

def _result(status, denominator, numerator, excluded, unknown, reasons):
    calculable = status == 'CALCULABLE'
    return {
        'status': status,
        'eligible_denominator': denominator,
        'verified_automated_numerator': numerator,
        'excluded_events': excluded,
        'unknown_scope_events': unknown,
        'rate_from_input_assertions': numerator / denominator if calculable else None,
        'target_90_adjudication': 'NOT_ESTABLISHED_INPUT_ASSERTIONS_ONLY',
        'provenance': 'CALLER_ASSERTED_NOT_AUTHENTICATED_BY_THIS_GUARD',
        'reasons': reasons,
    }

def assess(events):
    if not isinstance(events, list):
        return _result('INCOMPLETE', 0, 0, 0, 0, ['not_a_list'])
    ids = set()
    for row in events:
        if not isinstance(row, dict):
            return _result('INCOMPLETE', 0, 0, 0, 0, ['row_not_object'])
        ident = row.get('id')
        if not isinstance(ident, str) or not ident or ident in ids:
            return _result('INCOMPLETE', 0, 0, 0, 0, ['missing_or_duplicate_event_id'])
        ids.add(ident)
    denominator = numerator = excluded = unknown = 0
    reasons = []
    for row in events:
        if (any(type(row.get(k)) is not bool for k in _SCOPE)
                or type(row.get('automated')) is not bool
                or type(row.get('manual_trigger')) is not bool):
            unknown += 1
            reasons.append('unbound_scope_or_trigger:' + row['id'])
            continue
        if not all(row[k] for k in _SCOPE):
            excluded += 1
            continue
        denominator += 1
        if _success(row):
            numerator += 1
    status = ('INCOMPLETE' if unknown else
              'CALCULABLE' if denominator else 'NO_ELIGIBLE_EVENTS')
    return _result(status, denominator, numerator, excluded, unknown, reasons)
