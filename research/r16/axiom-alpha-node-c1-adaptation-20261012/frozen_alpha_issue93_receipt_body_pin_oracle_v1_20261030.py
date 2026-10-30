#!/usr/bin/env python3
"""C1 fixed-sample oracle, frozen before the new supplement; no network/authentication."""
import copy
import json
import re
import sys
from pathlib import Path

MAIN = '97838201eb9e435e3d2690752133b96d02368953'
DELTA = 'e83aa5f19d1882e56291ab21bb4685710d57fd5809f7b90fc6d2079f7d44079f'
AUDIT = 'a16f417851d6af8d3a95c4b15a6eb3b2028874776cba4f45b3dec4e1e5fd0c22'
EXPECTED = (221, 6527434004, 2699, 'fd602eda80fc9f505dedd146aa3beec28815eb7e96fc528a85df2a53497b037a')
ROOT = {'schema','repository','pinned_main','predecessor_delta_sha256','pr_audit_sha256','previous_pins','new_pins','scope','provenance','claim_ceiling'}
PIN = {'pr','id','bytes','sha256','actor'}

def pairs_unique(pairs):
    d = {}
    for k,v in pairs:
        if k in d: raise ValueError('duplicate JSON key')
        d[k] = v
    return d

def nonfinite(x): raise ValueError('nonfinite JSON')

def validate(d):
    if type(d) is not dict or set(d) != ROOT: raise ValueError('root fields')
    expected = {
        'schema':'alpha_issue93_receipt_body_pin_supplement_v1',
        'repository':'nexusomegac27/NEXUS-OMEGA-EVIDENCE',
        'pinned_main':MAIN,'predecessor_delta_sha256':DELTA,
        'pr_audit_sha256':AUDIT,'previous_pins':9,
        'scope':'PR212_TO_PR221_TEN_OWNER_RECEIPTS_FIXED_SAMPLE',
        'provenance':'API_BODY_SHA256_C1_NOT_TRANSPORT_AUTHENTICATION',
        'claim_ceiling':'C1_DESCRIPTIVE_ONLY'}
    for k,v in expected.items():
        if type(d[k]) is not type(v) or d[k] != v: raise ValueError('mismatch '+k)
    a = d['new_pins']
    if type(a) is not list or len(a) != 1: raise ValueError('new pin cardinality')
    p = a[0]
    if type(p) is not dict or set(p) != PIN: raise ValueError('pin fields')
    for k,v in zip(('pr','id','bytes','sha256'),EXPECTED):
        if type(p[k]) is not type(v) or p[k] != v: raise ValueError('pin mismatch '+k)
    if p['actor'] != 'nexusomegac27': raise ValueError('actor')
    if not re.fullmatch('[0-9a-f]{64}',p['sha256']): raise ValueError('hash syntax')
    return {'previous_digest_coverage':'9/10','new_digest_coverage':'10/10',
            'project_automation_rate':None,'project_readback_rate':None,
            'claim_ceiling':'C1_DESCRIPTIVE_ONLY'}

def main(path):
    raw = Path(path).read_bytes()
    if len(raw) > 8192: raise ValueError('oversize')
    d = json.loads(raw.decode('utf-8','strict'),object_pairs_hook=pairs_unique,parse_constant=nonfinite)
    result = validate(d)
    tests = 1
    cases = [
      ('repository','attacker/repo'),('pinned_main','0'*40),
      ('predecessor_delta_sha256','0'*64),('pr_audit_sha256','0'*64),
      ('previous_pins',8),('previous_pins',True),('scope','COMPLETE_PROJECT'),
      ('provenance','AUTHENTICATED'),('claim_ceiling','C2')]
    for key,value in cases:
        x = copy.deepcopy(d);x[key] = value
        try: validate(x)
        except (ValueError,TypeError,KeyError): tests += 1
        else: raise AssertionError('accepted bad '+key)
    for key,value in [('pr',220),('id',6526826821),('bytes',2698),
                      ('sha256','0'*64),('actor','expert-bot'),('extra',True)]:
        x = copy.deepcopy(d);x['new_pins'][0][key] = value
        try: validate(x)
        except (ValueError,TypeError,KeyError): tests += 1
        else: raise AssertionError('accepted bad pin '+key)
    for val in ([],[d['new_pins'][0]]*2):
        x = copy.deepcopy(d);x['new_pins'] = val
        try: validate(x)
        except ValueError: tests += 1
        else: raise AssertionError('accepted pin cardinality')
    for invalid in ('{"x":1,"x":2}','{"x":NaN}'):
        try: json.loads(invalid,object_pairs_hook=pairs_unique,parse_constant=nonfinite)
        except ValueError: tests += 1
        else: raise AssertionError('accepted invalid JSON')
    print(json.dumps({'state':'PASS_C1_FIXED_SAMPLE','checks':tests,'negatives_rejected':tests-1,**result},sort_keys=True))

if __name__ == '__main__':
    if len(sys.argv)!=2: sys.exit('usage: oracle.py supplement.json')
    main(sys.argv[1])
