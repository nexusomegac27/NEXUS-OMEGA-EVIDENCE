#!/usr/bin/env python3
"""Frozen external oracle for C1 Alpha handoff denominator accounting.

FIXED BEFORE candidate code. Synthetic fixtures; no GitHub or operator
metrics are inferred from this test. Compare against a naive reported-only
baseline that counts every 'automated' event as a success.
"""
import copy
import importlib.util
import json
import sys

H='a'*64
C='b'*40
B='c'*40

def ev(i, **kw):
    x=dict(id=i, routine=True, public=True, authorized=True,
           accessible=True, automated=True, manual_trigger=False,
           verification='INDEPENDENT_READBACK_MATCH',
           source_sha256=H, readback_commit=C, readback_blob=B,
           readback_sha256=H, source_bytes=100)
    x.update(kw)
    return x

# Expected: (status, eligible denominator, independently readback-backed numerator)
FIXTURES=[
 ('one_verified',[ev('1')],('CALCULABLE',1,1)),
 ('one_manual',[ev('1',automated=False,manual_trigger=True)],('CALCULABLE',1,0)),
 ('manual_trigger_invalid_success',[ev('1',manual_trigger=True)],('CALCULABLE',1,0)),
 ('private_excluded',[ev('1',public=False)],('NO_ELIGIBLE_EVENTS',0,0)),
 ('local_inaccessible_excluded',[ev('1',accessible=False)],('NO_ELIGIBLE_EVENTS',0,0)),
 ('unauthorized_excluded',[ev('1',authorized=False)],('NO_ELIGIBLE_EVENTS',0,0)),
 ('nonroutine_excluded',[ev('1',routine=False)],('NO_ELIGIBLE_EVENTS',0,0)),
 ('mixed',[ev('1'),ev('2',public=False),ev('3',automated=False)],('CALCULABLE',2,1)),
 ('unverified_not_success',[ev('1',verification='REPORTED_ONLY')],('CALCULABLE',1,0)),
 ('source_hash_absent',[ev('1',source_sha256=None)],('CALCULABLE',1,0)),
 ('blob_absent',[ev('1',readback_blob=None)],('CALCULABLE',1,0)),
 ('commit_absent',[ev('1',readback_commit=None)],('CALCULABLE',1,0)),
 ('readback_sha_absent',[ev('1',readback_sha256=None)],('CALCULABLE',1,0)),
 ('readback_mismatch',[ev('1',readback_sha256='d'*64)],('CALCULABLE',1,0)),
 ('bytes_zero',[ev('1',source_bytes=0)],('CALCULABLE',1,0)),
 ('unknown_accessibility',[ev('1',accessible=None)],('INCOMPLETE',0,0)),
 ('unknown_authorization',[ev('1',authorized=None)],('INCOMPLETE',0,0)),
 ('unknown_plus_valid',[ev('1'),ev('2',public=None)],('INCOMPLETE',1,1)),
 ('duplicate_ids',[ev('1'),ev('1')],('INCOMPLETE',0,0)),
 ('string_boolean',[ev('1',authorized='false')],('INCOMPLETE',0,0)),
 ('missing_id',[ev('1',id='')],('INCOMPLETE',0,0)),
 ('empty',[],('NO_ELIGIBLE_EVENTS',0,0)),
 ('unverified_two',[ev('1'),ev('2',verification='SOURCE_GAP')],('CALCULABLE',2,1)),
 ('wrong_sha_format',[ev('1',source_sha256='abc')],('CALCULABLE',1,0)),
 ('false_automated_type',[ev('1',automated='true')],('INCOMPLETE',0,0)),
 ('source_bytes_bool',[ev('1',source_bytes=True)],('CALCULABLE',1,0)),
]

def baseline(events):
    return sum(bool(x.get('automated')) for x in events)

def run(module_path):
    spec=importlib.util.spec_from_file_location('candidate',module_path)
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    good=0
    details=[]
    for name,events,expected in FIXTURES:
        try:
            out=mod.assess(copy.deepcopy(events))
            got=(out.get('status'),out.get('eligible_denominator'),out.get('verified_automated_numerator'))
        except Exception as exc:
            got=('EXCEPTION:'+type(exc).__name__,None,None)
        passed=(got==expected)
        good+=passed
        details.append(dict(case=name,pass_=passed,expected=expected,actual=got,naive_numerator=baseline(events)))
    print(json.dumps(dict(total=len(FIXTURES),pass_count=good,details=details),sort_keys=True))
    return 0 if good==len(FIXTURES) else 1

if __name__=='__main__':
    sys.exit(run(sys.argv[1]))
