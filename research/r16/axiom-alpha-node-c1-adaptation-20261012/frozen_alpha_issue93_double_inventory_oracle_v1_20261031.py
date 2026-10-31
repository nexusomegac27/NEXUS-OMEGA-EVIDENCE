#!/usr/bin/env python3
"""Frozen black-box oracle: two full paginated Issue93 inventories; synthetic only."""
import copy
import json
import subprocess
import sys

TARGET = sys.argv[1]


def fixture(n=101):
    items = [{'id': 1000+i, 'user': {'login': 'nexusomegac27'},
              'created_at': '2026-10-31T17:00:00Z',
              'updated_at': '2026-10-31T17:00:00Z',
              'body': 'public receipt ' + str(i)} for i in range(n)]
    pages = [{'page': j+1, 'per_page': 100,
              'items': items[j*100:(j+1)*100]} for j in range((n+99)//100)]
    return {'schema_version': 'alpha_issue93_double_inventory_v1',
            'repository_full_name': 'nexusomegac27/NEXUS-OMEGA-EVIDENCE',
            'pre': {'issue_number': 93, 'comments': n},
            'post': {'issue_number': 93, 'comments': n},
            'passes': [copy.deepcopy(pages), copy.deepcopy(pages)]}


def run(obj, accept, name, raw=None, edited=None):
    payload = raw if raw is not None else json.dumps(obj, ensure_ascii=False)
    p = subprocess.run([sys.executable, TARGET], input=payload,
                       text=True, capture_output=True, timeout=12)
    try:
        result = json.loads(p.stdout)
    except Exception:
        raise AssertionError((name, 'bad_output', p.stdout[:100]))
    actual = p.returncode == 0 and result.get('status') == 'DOUBLE_INVENTORY_STABLE_NOT_ATOMIC'
    assert actual == accept, (name, p.returncode, result)
    if edited is not None:
        assert result.get('edited_count') == edited, (name, result)
    print('PASS', name)

x = fixture()
run(x, True, 'valid_101', edited=0)
run(fixture(0), True, 'empty_issue', edited=0)
y = copy.deepcopy(x); y['passes'][0][0]['items'][0]['updated_at'] = '2026-10-31T17:01:00Z'; y['passes'][1][0]['items'][0]['updated_at'] = '2026-10-31T17:01:00Z'; run(y, True, 'stable_edited', edited=1)
y = copy.deepcopy(x); y['passes'][1][0]['items'][0]['body'] = 'modified'; run(y, False, 'same_count_body_edit')
y = copy.deepcopy(x); y['passes'][1][0]['items'][0]['user']['login'] = 'other'; run(y, False, 'same_count_actor_change')
y = copy.deepcopy(x); y['passes'][1][0]['items'][0]['updated_at'] = '2026-10-31T17:01:00Z'; run(y, False, 'same_count_timestamp_change')
y = copy.deepcopy(x); y['passes'][1][0]['items'][0]['id'] = 999; run(y, False, 'same_count_id_change')
y = copy.deepcopy(x); y['post']['comments'] = 102; run(y, False, 'count_drift')
y = copy.deepcopy(x); del y['post']; run(y, False, 'missing_post')
y = copy.deepcopy(x); del y['passes'][1]; run(y, False, 'missing_second_pass')
y = copy.deepcopy(x); y['passes'][1].pop(); run(y, False, 'second_pass_missing_page')
y = copy.deepcopy(x); y['passes'][1][0]['items'].pop(); run(y, False, 'second_pass_missing_item')
y = copy.deepcopy(x); y['passes'][0][1]['items'][0]['id'] = 1099; run(y, False, 'duplicate_id')
y = copy.deepcopy(x); y['passes'][1][0]['items'][2]['id'] = 1000; run(y, False, 'out_of_order')
y = copy.deepcopy(x); del y['passes'][1][0]['items'][0]['body']; run(y, False, 'missing_body')
y = copy.deepcopy(x); del y['passes'][0][0]['items'][0]['user']; run(y, False, 'missing_actor')
y = copy.deepcopy(x); y['passes'][0][0]['items'][0]['created_at'] = 'yesterday'; run(y, False, 'invalid_timestamp')
y = copy.deepcopy(x); y['passes'][1][0]['items'][0]['updated_at'] = '2026-10-30T00:00:00Z'; run(y, False, 'reversed_timestamp')
y = copy.deepcopy(x); y['repository_full_name'] = 'other/repo'; run(y, False, 'wrong_repo')
run(None, False, 'duplicate_json_key', raw='{"schema_version":"a","schema_version":"b"}')
run(None, False, 'nonfinite_json', raw='{"x":NaN}')
run(None, False, 'malformed_json', raw='{')
y = copy.deepcopy(x); y['passes'][1].append({'page': 3, 'per_page': 100, 'items': []}); run(y, False, 'extra_page')
y = copy.deepcopy(x); y['passes'][1][0]['page'] = 2; run(y, False, 'wrong_page_number')
y = copy.deepcopy(x); y['passes'][1][0]['items'][0]['body'] = '😀'; run(y, False, 'unicode_body_change')
print('ORACLE_EXPECTED_OUTCOMES=25/25')
