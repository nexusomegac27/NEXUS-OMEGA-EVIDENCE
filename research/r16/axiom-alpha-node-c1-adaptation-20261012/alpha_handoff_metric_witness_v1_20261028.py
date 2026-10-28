#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Offline C1 scoped public-handoff numerator/denominator witness.

Caller-supplied records only: no GitHub authentication, completeness proof, or
scientific validation. NEVER interpret its scoped rates as project-wide rates.
"""
import json
import re
import sys

OBJECT = 'NEXUS_OMEGA_ALPHA_HANDOFF_METRIC_WITNESS_V1'
REPO = 'nexusomegac27/NEXUS-OMEGA-EVIDENCE'
MAX_INPUT = 1_048_576
MAX_EVENTS = 5000
SHA40 = re.compile(r'[0-9a-f]{40}\Z')
SHA64 = re.compile(r'[0-9a-f]{64}\Z')
EVENT_ID = re.compile(r'[A-Za-z0-9][A-Za-z0-9._:-]{0,95}\Z')
EVENT_FIELDS = {'id', 'channel', 'routine', 'authorized', 'accessible',
                'published', 'automatic', 'commit_readback', 'source_readback',
                'test_readback', 'receipt_readback', 'unauthorized_write',
                'hidden_source_gap', 'source_overwrite', 'claim_promotion'}
BOOLEAN_FIELDS = EVENT_FIELDS - {'id', 'channel', 'routine', 'authorized', 'accessible'}


def fail(code):
    raise ValueError(code)


def unique_pairs(pairs):
    obj = {}
    for k, v in pairs:
        if k in obj:
            fail('DUPLICATE_JSON_KEY')
        obj[k] = v
    return obj


def nonfinite(_):
    fail('NONFINITE_JSON')


def check_event(e):
    if type(e) is not dict or set(e) != EVENT_FIELDS:
        fail('INVALID_EVENT_FIELD')
    if type(e['id']) is not str or not EVENT_ID.fullmatch(e['id']):
        fail('INVALID_EVENT_FIELD')
    if e['channel'] not in ('PUBLIC_GITHUB', 'PRIVATE_LOCAL', 'PRIVATE_CONNECTED', 'UNKNOWN'):
        fail('INVALID_EVENT_FIELD')
    for k in ('routine', 'authorized', 'accessible'):
        if e[k] is not None and type(e[k]) is not bool:
            fail('INVALID_EVENT_FIELD')
    for k in BOOLEAN_FIELDS:
        if type(e[k]) is not bool:
            fail('INVALID_EVENT_FIELD')


def ratio(n, d):
    return f'{n}/{d}' if d else 'NOT_COMPUTABLE'


def audit(obj):
    if type(obj) is not dict or set(obj) != {'object', 'repository', 'scope', 'events'}:
        fail('INVALID_ENVELOPE')
    if obj['object'] != OBJECT or obj['repository'] != REPO:
        fail('INVALID_SCOPE')
    s = obj['scope']
    if type(s) is not dict or set(s) != {'scope_id', 'coverage', 'source_commit_sha', 'source_manifest_sha256'}:
        fail('INVALID_SCOPE')
    if type(s['scope_id']) is not str or not EVENT_ID.fullmatch(s['scope_id']):
        fail('INVALID_SCOPE')
    if s['coverage'] not in ('PARTIAL', 'DECLARED_COMPLETE'):
        fail('INVALID_SCOPE')
    if type(s['source_commit_sha']) is not str or not SHA40.fullmatch(s['source_commit_sha']):
        fail('INVALID_SCOPE')
    if type(s['source_manifest_sha256']) is not str or not SHA64.fullmatch(s['source_manifest_sha256']):
        fail('INVALID_SCOPE')
    es = obj['events']
    if type(es) is not list or not 1 <= len(es) <= MAX_EVENTS:
        fail('INVALID_EVENT_COUNT')
    ids = set()
    eligible_ids, excluded_ids, uncertain_ids = [], [], []
    automated = publications = complete_readbacks = unauthorized_publications = 0
    unknown_publications = 0
    safety_ids = set()
    for e in es:
        check_event(e)
        i = e['id']
        if i in ids:
            fail('DUPLICATE_EVENT_ID')
        ids.add(i)
        channel = e['channel']
        if channel in ('PRIVATE_LOCAL', 'PRIVATE_CONNECTED'):
            excluded_ids.append(i)
        elif channel == 'UNKNOWN':
            uncertain_ids.append(i)
        elif False in (e['routine'], e['authorized'], e['accessible']):
            excluded_ids.append(i)
        elif None in (e['routine'], e['authorized'], e['accessible']):
            uncertain_ids.append(i)
        else:
            eligible_ids.append(i)
            if e['published'] and e['automatic']:
                automated += 1
        if channel == 'PUBLIC_GITHUB' and e['published']:
            publications += 1
            if all(e[k] for k in ('commit_readback', 'source_readback', 'test_readback', 'receipt_readback')):
                complete_readbacks += 1
            if e['authorized'] is False:
                unauthorized_publications += 1
                safety_ids.add(i)
        elif channel == 'UNKNOWN' and e['published']:
            unknown_publications += 1
        if any(e[k] for k in ('unauthorized_write', 'hidden_source_gap', 'source_overwrite', 'claim_promotion')):
            safety_ids.add(i)
    n = len(eligible_ids)
    unknown = len(uncertain_ids)
    sample = ratio(automated, n) if not unknown else 'NOT_COMPUTABLE'
    scoped = sample if s['coverage'] == 'DECLARED_COMPLETE' else 'NOT_COMPUTABLE'
    readback = ratio(complete_readbacks, publications) if not unknown_publications else 'NOT_COMPUTABLE'
    return {
        'state': 'C1_CALLER_SUPPLIED_SCOPE_ARITHMETIC_ONLY',
        'scope_id': s['scope_id'], 'coverage': s['coverage'],
        'events_observed': len(es), 'eligible': n, 'automated': automated,
        'excluded': len(excluded_ids), 'unknown_eligibility': unknown,
        'eligible_ids': sorted(eligible_ids), 'excluded_ids': sorted(excluded_ids),
        'uncertain_ids': sorted(uncertain_ids),
        'observed_sample_rate': sample,
        'scope_automation_rate': scoped,
        'scope_automation_percent': round(100 * automated / n, 4) if scoped != 'NOT_COMPUTABLE' else None,
        'project_automation_rate': 'NOT_COMPUTABLE',
        'publications': publications, 'complete_readbacks': complete_readbacks,
        'readback_rate': readback,
        'unknown_publications': unknown_publications,
        'unauthorized_publications': unauthorized_publications,
        'safety_event_count': len(safety_ids), 'safety_event_ids': sorted(safety_ids),
        'global_zero_violations_established': False,
        'api_origin_authenticated': False,
        'source_completeness_authenticated': False,
        'claim_ceiling': 'C1_DESCRIPTIVE_ONLY'
    }


def main():
    try:
        raw = sys.stdin.buffer.read(MAX_INPUT + 1)
        if len(raw) > MAX_INPUT:
            fail('INPUT_TOO_LARGE')
        obj = json.loads(raw.decode('utf-8'), object_pairs_hook=unique_pairs,
                         parse_constant=nonfinite)
        print(json.dumps(audit(obj), sort_keys=True, separators=(',', ':')))
        return 0
    except (ValueError, TypeError, UnicodeError, RecursionError) as e:
        print('FAIL_CLOSED: ' + str(e), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
