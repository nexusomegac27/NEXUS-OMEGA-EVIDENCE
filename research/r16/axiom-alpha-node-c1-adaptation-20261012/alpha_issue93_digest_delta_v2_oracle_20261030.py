#!/usr/bin/env python3
"""Independent structural oracle for append-only Issue #93 digest delta V2.

Does not fetch GitHub, authenticate actors, or verify original comment-body bytes.
"""
import copy
import json
import re
from pathlib import Path

PREVIOUS_COUNT = 201
PREVIOUS_LAST_ID = 6516343927
PREVIOUS_SHA256 = '69787c3cf2e59401eb9ea52048f8c0f0ba4cf928040f1095a8b4c99986e0f4fb'
PREVIOUS_BLOB = 'a7e8314a9742c2eeb04e98f8ba02deddbd16e92c'
MAIN = 'e726697213b2d637d42f2929c98a8c0f5f63a477'
SHA64 = re.compile(r'[0-9a-f]{64}\Z')
SHA40 = re.compile(r'[0-9a-f]{40}\Z')

def no_dupes(pairs):
    d = {}
    for k, v in pairs:
        if k in d:
            raise ValueError('duplicate key')
        d[k] = v
    return d

def reject_constant(_):
    raise ValueError('nonfinite JSON')

def validate(x):
    if type(x) is not dict or set(x) != {'schema_version','source','pinned_main_before','predecessor','old_count','old_last_comment_id','delta_count','total_count','last_comment_id','pins'}:
        raise ValueError('unexpected fields')
    if x['schema_version'] != 'alpha_issue93_body_digest_delta_v2' or x['source'] != 'nexusomegac27/NEXUS-OMEGA-EVIDENCE/issues/93' or x['pinned_main_before'] != MAIN:
        raise ValueError('source/commit mismatch')
    p=x['predecessor']
    if type(p) is not dict or set(p) != {'sha256','git_blob','path'} or p['sha256'] != PREVIOUS_SHA256 or p['git_blob'] != PREVIOUS_BLOB or p['path'] != 'research/r16/axiom-alpha-node-c1-adaptation-20261012/alpha_issue93_real_body_digest_inventory_v1_20261030.json':
        raise ValueError('predecessor mismatch')
    if type(x['old_count']) is not int or x['old_count'] != PREVIOUS_COUNT or type(x['old_last_comment_id']) is not int or x['old_last_comment_id'] != PREVIOUS_LAST_ID:
        raise ValueError('old cutoff mismatch')
    if type(x['pins']) is not list or not x['pins'] or type(x['delta_count']) is not int or x['delta_count'] != len(x['pins']) or type(x['total_count']) is not int or x['total_count'] != PREVIOUS_COUNT + len(x['pins']):
        raise ValueError('census mismatch')
    last=PREVIOUS_LAST_ID
    for p in x['pins']:
        if type(p) is not dict or set(p) != {'id','bytes','sha256'} or type(p['id']) is not int or p['id'] <= last or type(p['bytes']) is not int or p['bytes'] < 0 or type(p['sha256']) is not str or not SHA64.fullmatch(p['sha256']):
            raise ValueError('invalid, duplicate or unordered pin')
        last=p['id']
    if type(x['last_comment_id']) is not int or x['last_comment_id'] != last:
        raise ValueError('last ID mismatch')
    return True

def run_tests(obj):
    assert validate(obj)
    negatives=[]
    def mutate(name, fn):
        x=copy.deepcopy(obj); fn(x); negatives.append((name,x))
    mutate('wrong_repo', lambda x:x.update(source='other/repo/issues/93'))
    mutate('wrong_main', lambda x:x.update(pinned_main_before='0'*40))
    mutate('wrong_prev_hash', lambda x:x['predecessor'].update(sha256='0'*64))
    mutate('wrong_prev_blob', lambda x:x['predecessor'].update(git_blob='0'*40))
    mutate('wrong_prev_path', lambda x:x['predecessor'].update(path='other.json'))
    mutate('missing_pin', lambda x:x['pins'].pop())
    mutate('duplicate_id', lambda x:x['pins'][1].update(id=x['pins'][0]['id']))
    mutate('out_of_order', lambda x:x['pins'][0].update(id=x['pins'][1]['id']+1))
    mutate('bad_digest', lambda x:x['pins'][0].update(sha256='zz'))
    mutate('bad_bytes', lambda x:x['pins'][0].update(bytes=-1))
    mutate('bool_bytes', lambda x:x['pins'][0].update(bytes=True))
    mutate('wrong_total', lambda x:x.update(total_count=999))
    mutate('wrong_last', lambda x:x.update(last_comment_id=999))
    mutate('extra_field', lambda x:x.update(authentication='PASS'))
    mutate('wrong_old_cutoff', lambda x:x.update(old_last_comment_id=1))
    for name, bad in negatives:
        try: validate(bad)
        except (ValueError,TypeError): continue
        raise AssertionError('accepted negative '+name)
    for name, payload in [('duplicate_json_key','{"a":1,"a":2}'),('nonfinite_json','{"a":NaN}')]:
        try: json.loads(payload,object_pairs_hook=no_dupes,parse_constant=reject_constant)
        except ValueError: continue
        raise AssertionError('accepted negative '+name)
    print('PASS: 1 positive + 17 negative/malformed = 18/18')

if __name__=='__main__':
    import sys
    if len(sys.argv)!=2: raise SystemExit('usage: oracle.py DELTA_JSON')
    obj=json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'),object_pairs_hook=no_dupes,parse_constant=reject_constant)
    run_tests(obj)
