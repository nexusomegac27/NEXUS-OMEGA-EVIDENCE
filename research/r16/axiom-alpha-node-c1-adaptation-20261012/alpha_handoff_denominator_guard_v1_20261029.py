#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Isolated C1 declared-input handoff accounting; not a GitHub authenticator.
No network, no filesystem writes, no API actor authority, no project-wide claims.
"""
import json
import sys

FIELDS = {'id', 'accessible', 'routine', 'public', 'authorized', 'automated',
          'delivered', 'published', 'commit_readback', 'source_readback',
          'test_readback', 'receipt_readback'}
BOOLS = FIELDS - {'id'}
MAX_INPUT = 262144
MAX_ROWS = 1000


def unique_pairs(pairs):
    out = {}
    for k, v in pairs:
        if k in out:
            raise ValueError('DUPLICATE_JSON_KEY')
        out[k] = v
    return out


def reject_constant(value):
    raise ValueError('NONFINITE_NUMBER')


def audit(doc):
    if not isinstance(doc, dict) or set(doc) != {'handoffs'}:
        raise ValueError('INVALID_DOCUMENT')
    rows = doc['handoffs']
    if not isinstance(rows, list) or len(rows) > MAX_ROWS:
        raise ValueError('INVALID_HANDOFFS')
    ids = set()
    eligible = excluded = auto = published = full = unauthorized_publications = 0
    for r in rows:
        if not isinstance(r, dict) or set(r) != FIELDS:
            raise ValueError('INVALID_HANDOFF_ROW')
        if not isinstance(r['id'], str) or not (1 <= len(r['id']) <= 128):
            raise ValueError('INVALID_ID')
        if r['id'] in ids:
            raise ValueError('DUPLICATE_HANDOFF_ID')
        ids.add(r['id'])
        if any(type(r[k]) is not bool for k in BOOLS):
            raise ValueError('NONBOOLEAN_FLAG')
        if r['published']:
            published += 1
            full += int(all(r[k] for k in ('commit_readback', 'source_readback',
                                           'test_readback', 'receipt_readback')))
            unauthorized_publications += int(not r['authorized'])
        if not all(r[k] for k in ('accessible', 'routine', 'public', 'authorized')):
            excluded += 1
            continue
        eligible += 1
        auto += int(r['automated'] and r['delivered'])
    return dict(scope='DECLARED_INPUT_ONLY_NOT_AUTHENTICATED',
                claim_ceiling='C1_DESCRIPTIVE_ONLY', input_rows=len(rows),
                eligible=eligible, excluded=excluded, automated_success=auto,
                sample_automation_ratio=f'{auto}/{eligible}' if eligible else 'NOT_COMPUTABLE',
                published=published, full_readback=full,
                declared_unauthorized_publications=unauthorized_publications,
                sample_readback_ratio=f'{full}/{published}' if published else 'NOT_COMPUTABLE',
                project_automation_rate='NOT_COMPUTABLE',
                project_readback_rate='NOT_COMPUTABLE',
                independent_github_authentication=False)


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
