#!/usr/bin/env python3
"""Frozen black-box oracle: two-phase GitHub Issue #93 census (synthetic fixtures)."""
import copy
import json
import subprocess
import sys

TARGET = sys.argv[1]

def fixture(n=101):
    items = [{"id": 1000+i, "user": {"login": "nexusomegac27"},
              "created_at": "2026-10-31T17:00:00Z", "updated_at": "2026-10-31T17:00:00Z",
              "body": "public receipt " + str(i)} for i in range(n)]
    return {"schema_version": "alpha_issue93_two_phase_snapshot_v1",
            "repository_full_name": "nexusomegac27/NEXUS-OMEGA-EVIDENCE",
            "pre": {"issue_number": 93, "comments": n},
            "post": {"issue_number": 93, "comments": n},
            "pages": [{"page": j+1, "per_page": 100, "items": items[j*100:(j+1)*100]}
                      for j in range((n+99)//100)]}

def run(obj, expect, name, raw=None, edited=None):
    payload = raw if raw is not None else json.dumps(obj, ensure_ascii=False)
    p = subprocess.run([sys.executable, TARGET], input=payload, text=True,
                       capture_output=True, timeout=12)
    try:
        result = json.loads(p.stdout)
    except Exception:
        raise AssertionError(name + ': no valid JSON output: ' + p.stdout[:100])
    accepted = p.returncode == 0 and result.get('status') == 'CENSUS_CONSISTENT_NOT_AUTHENTICATED'
    assert accepted == expect, (name, p.returncode, result)
    if edited is not None:
        assert result.get('edited_count') == edited, (name, result)
    print('PASS', name)

x = fixture()
run(x, True, 'valid_101', edited=0)
y = copy.deepcopy(x); y['post']['comments'] = 102; run(y, False, 'post_growth')
y = copy.deepcopy(x); y['pre']['comments'] = 102; run(y, False, 'pre_mismatch')
y = copy.deepcopy(x); del y['post']; run(y, False, 'missing_post')
y = copy.deepcopy(x); y['pages'].pop(); run(y, False, 'missing_last_page')
y = copy.deepcopy(x); y['pages'][1]['items'][0]['id'] = 1099; run(y, False, 'duplicate_id')
y = copy.deepcopy(x); y['pages'][0]['items'][2]['id'] = 1000; run(y, False, 'out_of_order')
y = copy.deepcopy(x); del y['pages'][0]['items'][0]['user']; run(y, False, 'missing_actor')
y = copy.deepcopy(x); del y['pages'][0]['items'][0]['body']; run(y, False, 'missing_body')
y = copy.deepcopy(x); y['pages'][0]['items'][0]['created_at'] = 'yesterday'; run(y, False, 'invalid_timestamp')
y = copy.deepcopy(x); y['pages'][0]['items'][0]['updated_at'] = '2026-10-30T00:00:00Z'; run(y, False, 'reversed_timestamp')
y = copy.deepcopy(x); y['repository_full_name'] = 'other/repo'; run(y, False, 'wrong_repo')
run(None, False, 'duplicate_json_key', raw='{"schema_version":"a","schema_version":"b"}')
run(None, False, 'nonfinite_json', raw='{"x":NaN}')
y = copy.deepcopy(x); y['pages'][0]['items'][0]['updated_at'] = '2026-10-31T17:01:00Z'; run(y, True, 'edited_observation', edited=1)
run(None, False, 'malformed_json', raw='{')
run(fixture(0), True, 'empty_issue', edited=0)
y = copy.deepcopy(x); y['pages'].append({"page":3,"per_page":100,"items":[]}); run(y, False, 'extra_page')
print('ORACLE_EXPECTED_OUTCOMES=18/18')
