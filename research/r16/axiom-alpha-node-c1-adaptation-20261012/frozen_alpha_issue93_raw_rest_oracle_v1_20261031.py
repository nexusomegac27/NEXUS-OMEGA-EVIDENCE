#!/usr/bin/env python3
"""Independent black-box subprocess oracle; no import or mutation of candidate."""
import copy
import json
import subprocess
import sys

BASE = {'id': 1, 'user': {'login': 'nexusomegac27'}, 'created_at': '2026-10-31T10:00:00Z',
        'updated_at': '2026-10-31T10:00:00Z', 'body': 'C1_DESCRIPTIVE_ONLY'}

def packet(items, count=None):
    return {'schema_version': 'alpha_issue93_raw_rest_census_v1',
            'issue': {'number': 93, 'comments': len(items) if count is None else count},
            'pages': [{'page': 1, 'per_page': 100, 'items': items}]}

def run(script, obj=None, raw=None):
    p = subprocess.run([sys.executable, script], input=json.dumps(obj) if raw is None else raw,
                       text=True, capture_output=True, timeout=10)
    return p.returncode, json.loads(p.stdout)

def main(script):
    total = 0
    def check(ok, name):
        nonlocal total
        total += 1
        if not ok:
            raise AssertionError(name)
    rc, r = run(script, packet([BASE]))
    check(rc == 0 and r['observed'] == 1 and r['owner_comments'] == 1, 'positive')
    check(r['edited_timestamps'] == 0 and not r['historical_immutability_proven'], 'limited_claim')
    check(r['project_rate'] == 'NOT_COMPUTABLE' and not r['authenticated_external_expert'], 'no_promotion')
    edited = dict(BASE, updated_at='2026-10-31T11:00:00Z')
    rc, r = run(script, packet([edited]))
    check(rc == 2 and r['status'] == 'EDITED_COMMENT_OBSERVED', 'edited_timestamp')
    rc, r = run(script, packet([BASE], count=2))
    check(rc == 2 and r['status'] == 'FAIL_CLOSED', 'missing_page_count')
    rc, r = run(script, packet([BASE, BASE]))
    check(rc == 2 and r['status'] == 'FAIL_CLOSED', 'duplicate_id')
    rc, r = run(script, packet([dict(BASE, updated_at=None)]))
    check(rc == 2 and r['status'] == 'FAIL_CLOSED', 'missing_timestamp')
    rc, r = run(script, packet([dict(BASE, updated_at='2026-10-30T11:00:00Z')]))
    check(rc == 2 and r['status'] == 'FAIL_CLOSED', 'time_reversal')
    rc, r = run(script, packet([dict(BASE, user={})]))
    check(rc == 2 and r['status'] == 'FAIL_CLOSED', 'missing_actor')
    rc, r = run(script, packet([dict(BASE, user={'login':'external'})]))
    check(rc == 0 and r['nonowner_comments'] == 1 and not r['authenticated_external_expert'], 'external_not_ack')
    rc, r = run(script, packet([dict(BASE, body='tampered')]))
    check(rc == 0 and r['body_inventory_sha256'] != run(script, packet([BASE]))[1]['body_inventory_sha256'], 'body_drift')
    rc, r = run(script, raw='{"schema_version":"alpha_issue93_raw_rest_census_v1","issue":{},"issue":{},"pages":[]}')
    check(rc == 2 and r['status'] == 'FAIL_CLOSED', 'duplicate_json_key')
    rc, r = run(script, raw='{"schema_version":"alpha_issue93_raw_rest_census_v1","issue":{},"pages":[],"x":NaN}')
    check(rc == 2 and r['status'] == 'FAIL_CLOSED', 'nonfinite')
    rc, r = run(script, packet([dict(BASE, body=None)]))
    check(rc == 2 and r['status'] == 'FAIL_CLOSED', 'missing_body')
    print(json.dumps({'oracle': 'FROZEN_RAW_REST_V1', 'passed': total, 'total': total}))

if __name__ == '__main__':
    main(sys.argv[1])
