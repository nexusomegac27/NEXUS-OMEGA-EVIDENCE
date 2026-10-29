#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Read-only C1 cohort-census guard; input declarations are NOT GitHub authentication.

This is an isolated successor to the declared-input V1. No network, writes,
worker activation, runtime integration or project-wide success claims.
"""
import json
import sys

FIELDS = {'id', 'accessible', 'routine', 'public', 'authorized', 'automated',
          'delivered', 'manual_nudge', 'published', 'commit_readback',
          'source_readback', 'test_readback', 'receipt_readback',
          'unauthorized_write', 'concealed_source_gap', 'overwrite', 'claim_promotion'}
BOOLS = FIELDS - {'id'}
MAX_INPUT = 262144
MAX_ROWS = 1000


def unique_pairs(pairs):
    out = {}
    for key, value in pairs:
        if key in out:
            raise ValueError('DUPLICATE_JSON_KEY')
        out[key] = value
    return out


def reject_constant(value):
    raise ValueError('NONFINITE_NUMBER')


def audit(doc):
    if not isinstance(doc, dict) or set(doc) != {'cohort', 'scope_complete',
                                                 'declared_attempt_ids', 'handoffs'}:
        raise ValueError('INVALID_DOCUMENT')
    if not isinstance(doc['cohort'], str) or not doc['cohort'] or len(doc['cohort']) > 128:
        raise ValueError('INVALID_COHORT')
    if doc['scope_complete'] is not True:
        raise ValueError('SCOPE_NOT_DECLARED_COMPLETE')
    rows, declared = doc['handoffs'], doc['declared_attempt_ids']
    if not isinstance(rows, list) or not isinstance(declared, list):
        raise ValueError('INVALID_POPULATION')
    if len(rows) > MAX_ROWS or not declared or len(declared) > MAX_ROWS:
        raise ValueError('INVALID_POPULATION_SIZE')
    if any(not isinstance(x, str) or not 1 <= len(x) <= 128 for x in declared):
        raise ValueError('INVALID_DECLARED_ID')
    if len(set(declared)) != len(declared):
        raise ValueError('DUPLICATE_DECLARED_ID')
    ids = set()
    eligible = excluded = auto = published = full = violations = 0
    for row in rows:
        if not isinstance(row, dict) or set(row) != FIELDS:
            raise ValueError('INVALID_HANDOFF_ROW')
        if not isinstance(row['id'], str) or not 1 <= len(row['id']) <= 128:
            raise ValueError('INVALID_ID')
        if row['id'] in ids:
            raise ValueError('DUPLICATE_HANDOFF_ID')
        ids.add(row['id'])
        if any(type(row[key]) is not bool for key in BOOLS):
            raise ValueError('NONBOOLEAN_FLAG')
        if row['published']:
            published += 1
            full += int(all(row[key] for key in ('commit_readback', 'source_readback',
                                                'test_readback', 'receipt_readback')))
        violations += int(any(row[key] for key in ('unauthorized_write',
                          'concealed_source_gap', 'overwrite', 'claim_promotion'))
                          or (row['published'] and not row['authorized']))
        if not all(row[key] for key in ('accessible', 'routine', 'public', 'authorized')):
            excluded += 1
            continue
        eligible += 1
        auto += int(row['automated'] and row['delivered'] and not row['manual_nudge'])
    if ids != set(declared):
        raise ValueError('ATTEMPT_CENSUS_MISMATCH')
    return dict(scope='DECLARED_COMPLETE_COHORT_ONLY_NOT_AUTHENTICATED',
                cohort=doc['cohort'], claim_ceiling='C1_DESCRIPTIVE_ONLY',
                declared=len(declared), observed=len(rows), eligible=eligible,
                excluded=excluded, automated_success=auto,
                sample_automation_ratio=f'{auto}/{eligible}' if eligible else 'NOT_COMPUTABLE',
                published=published, full_readback=full,
                sample_readback_ratio=f'{full}/{published}' if published else 'NOT_COMPUTABLE',
                reported_violations=violations,
                safety_status='VIOLATION_REPORTED' if violations else 'NO_VIOLATION_REPORTED_NOT_VERIFIED',
                project_automation_rate='NOT_COMPUTABLE',
                project_readback_rate='NOT_COMPUTABLE',
                independent_github_authentication=False,
                runtime_integration=False)


def main():
    try:
        raw = sys.stdin.buffer.read(MAX_INPUT + 1)
        if len(raw) > MAX_INPUT:
            raise ValueError('INPUT_TOO_LARGE')
        doc = json.loads(raw.decode('utf-8'), object_pairs_hook=unique_pairs,
                         parse_constant=reject_constant)
        print(json.dumps(audit(doc), sort_keys=True, separators=(',', ':')))
        return 0
    except (ValueError, TypeError, UnicodeError, RecursionError) as exc:
        print('FAIL_CLOSED: ' + str(exc), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
