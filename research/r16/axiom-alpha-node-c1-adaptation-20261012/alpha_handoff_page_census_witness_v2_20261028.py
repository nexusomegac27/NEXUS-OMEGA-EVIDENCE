#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""C1 offline paginated handoff census: caller-supplied pages, no API auth.

Checks continuity, reported totals, source pins and cross-page event uniqueness.
This is not an independent GitHub inventory or a project-wide 90% claim.
"""
import json
import re
import sys

OBJECT = 'NEXUS_OMEGA_ALPHA_HANDOFF_PAGE_CENSUS_V2'
REPO = 'nexusomegac27/NEXUS-OMEGA-EVIDENCE'
MAX_INPUT = 1_048_576
MAX_PAGES = 100
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
    d = {}
    for k, v in pairs:
        if k in d:
            fail('DUPLICATE_JSON_KEY')
        d[k] = v
    return d


def nonfinite(_):
    fail('NONFINITE_JSON')


def ratio(n, d):
    return f'{n}/{d}' if d else 'NOT_COMPUTABLE'


def check_event(e):
    if type(e) is not dict or set(e) != EVENT_FIELDS:
        fail('INVALID_EVENT_FIELD')
    if type(e['id']) is not str or not EVENT_ID.fullmatch(e['id']):
        fail('INVALID_EVENT_FIELD')
    if type(e['channel']) is not str or e['channel'] not in (
            'PUBLIC_GITHUB', 'PRIVATE_LOCAL', 'PRIVATE_CONNECTED', 'UNKNOWN'):
        fail('INVALID_EVENT_FIELD')
    for k in ('routine', 'authorized', 'accessible'):
        if e[k] is not None and type(e[k]) is not bool:
            fail('INVALID_EVENT_FIELD')
    for k in BOOLEAN_FIELDS:
        if type(e[k]) is not bool:
            fail('INVALID_EVENT_FIELD')


def audit(obj):
    if type(obj) is not dict or set(obj) != {'object', 'repository', 'scope', 'pages'}:
        fail('INVALID_ENVELOPE')
    if obj['object'] != OBJECT or obj['repository'] != REPO:
        fail('INVALID_SCOPE')
    scope = obj['scope']
    if type(scope) is not dict or set(scope) != {
            'scope_id', 'coverage', 'source_commit_sha', 'source_manifest_sha256'}:
        fail('INVALID_SCOPE')
    if type(scope['scope_id']) is not str or not EVENT_ID.fullmatch(scope['scope_id']):
        fail('INVALID_SCOPE')
    if scope['coverage'] not in ('PARTIAL', 'DECLARED_COMPLETE'):
        fail('INVALID_SCOPE')
    if type(scope['source_commit_sha']) is not str or not SHA40.fullmatch(scope['source_commit_sha']):
        fail('INVALID_SCOPE')
    if type(scope['source_manifest_sha256']) is not str or not SHA64.fullmatch(scope['source_manifest_sha256']):
        fail('INVALID_SCOPE')
    pages = obj['pages']
    if type(pages) is not list or not 1 <= len(pages) <= MAX_PAGES:
        fail('INVALID_PAGE_COUNT')
    events = []
    declared_total = None
    for idx, page in enumerate(pages, 1):
        if type(page) is not dict or set(page) != {
                'page', 'source_commit_sha', 'reported_total', 'next_page', 'events'}:
            fail('INVALID_PAGE')
        if type(page['page']) is not int or page['page'] != idx:
            fail('PAGE_ORDER_INVALID')
        if page['source_commit_sha'] != scope['source_commit_sha']:
            fail('PAGE_SOURCE_MISMATCH')
        total = page['reported_total']
        if type(total) is not int or not 1 <= total <= MAX_EVENTS:
            fail('INVALID_PAGE')
        if declared_total is None:
            declared_total = total
        elif declared_total != total:
            fail('PAGE_TOTAL_MISMATCH')
        items = page['events']
        if type(items) is not list or not items:
            fail('INVALID_EVENT_COUNT')
        if len(events) + len(items) > MAX_EVENTS:
            fail('INVALID_EVENT_COUNT')
        events.extend(items)
        nxt = page['next_page']
        if idx < len(pages):
            if type(nxt) is not int or nxt != idx + 1:
                fail('PAGE_CHAIN_INVALID')
        elif nxt is not None:
            if type(nxt) is not int or nxt != idx + 1:
                fail('PAGE_CHAIN_INVALID')
            if scope['coverage'] == 'DECLARED_COMPLETE':
                fail('MISSING_PAGE')
    terminal = pages[-1]['next_page'] is None
    if terminal and len(events) != declared_total and scope['coverage'] == 'DECLARED_COMPLETE':
        fail('PAGE_TOTAL_MISMATCH')
    if not terminal and len(events) >= declared_total:
        fail('PAGE_TOTAL_MISMATCH')
    ids = set()
    eligible, excluded, uncertain, safety = [], [], [], set()
    automated = publications = complete_readbacks = unknown_publications = 0
    unauthorized_publications = 0
    for e in events:
        check_event(e)
        key = e['id']
        if key in ids:
            fail('DUPLICATE_EVENT_ID')
        ids.add(key)
        channel = e['channel']
        if channel in ('PRIVATE_LOCAL', 'PRIVATE_CONNECTED'):
            excluded.append(key)
        elif channel == 'UNKNOWN':
            uncertain.append(key)
        elif False in (e['routine'], e['authorized'], e['accessible']):
            excluded.append(key)
        elif None in (e['routine'], e['authorized'], e['accessible']):
            uncertain.append(key)
        else:
            eligible.append(key)
            if e['published'] and e['automatic']:
                automated += 1
        if channel == 'PUBLIC_GITHUB' and e['published']:
            publications += 1
            if all(e[k] for k in ('commit_readback', 'source_readback',
                                  'test_readback', 'receipt_readback')):
                complete_readbacks += 1
            if e['authorized'] is False:
                unauthorized_publications += 1
                safety.add(key)
        elif channel == 'UNKNOWN' and e['published']:
            unknown_publications += 1
        if any(e[k] for k in ('unauthorized_write', 'hidden_source_gap',
                              'source_overwrite', 'claim_promotion')):
            safety.add(key)
    pagination_complete = terminal and len(events) == declared_total
    sample = ratio(automated, len(eligible)) if not uncertain else 'NOT_COMPUTABLE'
    scoped = (sample if scope['coverage'] == 'DECLARED_COMPLETE'
              and pagination_complete else 'NOT_COMPUTABLE')
    sample_readback = ratio(complete_readbacks, publications)
    readback = (sample_readback if pagination_complete and not unknown_publications
                else 'NOT_COMPUTABLE')
    return {
        'state': 'C1_CALLER_SUPPLIED_PAGE_CENSUS_ONLY',
        'claim_ceiling': 'C1_DESCRIPTIVE_ONLY',
        'scope_id': scope['scope_id'], 'coverage': scope['coverage'],
        'pagination_state': 'COMPLETE_DECLARED' if pagination_complete else 'INCOMPLETE',
        'pages_observed': len(pages), 'reported_total': declared_total,
        'events_observed': len(events), 'eligible': len(eligible),
        'automated': automated, 'excluded': len(excluded),
        'unknown_eligibility': len(uncertain),
        'observed_sample_rate': sample, 'scope_automation_rate': scoped,
        'scope_automation_percent': (round(100 * automated / len(eligible), 4)
                                     if scoped != 'NOT_COMPUTABLE' else None),
        'project_automation_rate': 'NOT_COMPUTABLE',
        'publications': publications, 'complete_readbacks': complete_readbacks,
        'observed_readback_sample_rate': sample_readback, 'readback_rate': readback,
        'unknown_publications': unknown_publications,
        'unauthorized_publications': unauthorized_publications,
        'safety_event_count': len(safety), 'safety_event_ids': sorted(safety),
        'global_zero_violations_established': False,
        'api_origin_authenticated': False,
        'source_completeness_authenticated': False,
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
    except (ValueError, TypeError, UnicodeError, RecursionError) as exc:
        print('FAIL_CLOSED: ' + str(exc), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
