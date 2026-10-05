#!/usr/bin/env python3
"""AXIOM R1 independent fail-closed integration test for E0.2.
C1_DESCRIPTIVE_ONLY. Research/validation only; no production or claim promotion.
"""
from __future__ import annotations
from enum import Enum
from copy import deepcopy
from typing import Any, Mapping, Iterable
import json, hashlib

class S(str, Enum):
    VERIFIED='VERIFIED'; FALSIFIED='FALSIFIED'; AIR_GAP='AIR_GAP'

def parse_state(v: Any) -> S:
    if isinstance(v,S): return v
    if v is None: return S.AIR_GAP
    m={'1':S.VERIFIED,'VERIFIED':S.VERIFIED,'0':S.FALSIFIED,'FALSIFIED':S.FALSIFIED,'Δ':S.AIR_GAP,'AIR_GAP':S.AIR_GAP}
    return m.get(str(v).upper(), S.AIR_GAP)

def aggregate(xs: Iterable[S]) -> S:
    xs=list(xs)
    if not xs: return S.AIR_GAP
    if S.FALSIFIED in xs: return S.FALSIFIED
    if S.AIR_GAP in xs: return S.AIR_GAP
    return S.VERIFIED if all(x==S.VERIFIED for x in xs) else S.AIR_GAP

def g1(t: Mapping[str,Any]) -> S:
    return S.VERIFIED if isinstance(t.get('trace_id'),str) and t['trace_id'] else S.AIR_GAP

def g2(t): return parse_state(t.get('gate2_state'))
def g3(t): return parse_state(t.get('gate3_state'))

def g4(t: Mapping[str,Any]) -> S:
    if 'PARENT_TRACE' not in t or t.get('PARENT_TRACE') is None: return S.AIR_GAP
    seen=set(); cur=t
    for _ in range(33):
        tid=cur.get('trace_id') or cur.get('id')
        if not isinstance(tid,str) or not tid: return S.AIR_GAP
        if tid in seen: return S.FALSIFIED
        seen.add(tid)
        p=cur.get('PARENT_TRACE')
        if p=='ROOT': return S.VERIFIED
        if p is None: return S.AIR_GAP
        if not isinstance(p,Mapping): return S.FALSIFIED
        cur=p
    return S.FALSIFIED

def g5(t):
    c=t.get('AUTHORITY_CAPSULE')
    if not isinstance(c,Mapping): return S.FALSIFIED
    if not c.get('capsule_id') or not isinstance(c.get('scope'),(list,tuple,set)): return S.FALSIFIED
    op=t.get('op')
    if not isinstance(op,str) or not op: return S.AIR_GAP
    return S.VERIFIED if op in c['scope'] else S.FALSIFIED

def g6(t):
    m=t.get('memory')
    if not isinstance(m,Mapping): return S.FALSIFIED
    prov=m.get('provenance')
    if not isinstance(prov,Mapping) or not prov: return S.AIR_GAP
    if m.get('contradiction') is True: return S.FALSIFIED
    h=str(m.get('hygiene_status','')).upper()
    if h in {'FAIL','CONFLICT','QUARANTINE'}: return S.FALSIFIED
    if h not in {'PASS','OK','CLEAN'}: return S.AIR_GAP
    return S.VERIFIED

def g7(t):
    level=t.get('claim_level') or t.get('ceiling')
    if level not in {'C0','C1','C1_DESCRIPTIVE_ONLY'}: return S.FALSIFIED
    if not (t.get('provenance') or t.get('PARENT_TRACE')): return S.AIR_GAP
    d=t.get('DEFEAT_CONDITION')
    if not isinstance(d,str) or not d.strip(): return S.AIR_GAP
    return S.VERIFIED

def detail(t):
    states={'G1':g1(t),'G2':g2(t),'G3':g3(t),'G4':g4(t),'G5':g5(t),'G6':g6(t),'G7':g7(t)}
    return {k:v.value for k,v in states.items()}, aggregate(states.values()).value

def base():
    return {'trace_id':'t','gate2_state':'VERIFIED','gate3_state':'VERIFIED','PARENT_TRACE':{'trace_id':'root','PARENT_TRACE':'ROOT'},
            'AUTHORITY_CAPSULE':{'capsule_id':'cap','scope':['execute']},'memory':{'provenance':{'source':'trace'},'hygiene_status':'PASS'},
            'claim_level':'C1_DESCRIPTIVE_ONLY','provenance':{'source':'g4'},'DEFEAT_CONDITION':'independent reproduction fails','op':'execute'}

def run():
    cases=[]
    def add(name, mutate, exp):
        t=base(); mutate(t); gs,a=detail(t); cases.append({'name':name,'expected':exp.value,'actual':a,'passed':a==exp.value,'gate_states':gs})
    add('all_verified',lambda t:None,S.VERIFIED)
    add('authority_scope_mismatch',lambda t:t['AUTHORITY_CAPSULE'].__setitem__('scope',['read']),S.FALSIFIED)
    add('missing_provenance_parent',lambda t:t.__setitem__('PARENT_TRACE',None),S.AIR_GAP)
    add('missing_gate2_state',lambda t:t.pop('gate2_state'),S.AIR_GAP)
    add('missing_gate3_state',lambda t:t.pop('gate3_state'),S.AIR_GAP)
    add('missing_authority_capsule',lambda t:t.pop('AUTHORITY_CAPSULE'),S.FALSIFIED)
    add('missing_defeat_condition',lambda t:t.pop('DEFEAT_CONDITION'),S.AIR_GAP)
    add('claim_above_ceiling_even_with_release',lambda t:(t.__setitem__('claim_level','C2'),t.__setitem__('operator_release',True)),S.FALSIFIED)
    def cycle(t):
        x={'trace_id':'x'}; x['PARENT_TRACE']=x; t['PARENT_TRACE']=x
    add('provenance_cycle',cycle,S.FALSIFIED)
    add('broken_parent_without_root_marker',lambda t:t.__setitem__('PARENT_TRACE',{'trace_id':'orphan'}),S.AIR_GAP)
    ok=all(c['passed'] for c in cases)
    return {'object':'E0_2_FULL_INTEGRATION_AXIOM_R1','claim_ceiling':'C1_DESCRIPTIVE_ONLY','scope':'SYNTHETIC_FAIL_CLOSED_REGRESSION_ONLY',
            'terminal_state':'PASS_C1_AXIOM_R1_FAIL_CLOSED_REGRESSION' if ok else 'FAIL_C1_AXIOM_R1_FAIL_CLOSED_REGRESSION',
            'cases':cases,'passed':sum(c['passed'] for c in cases),'total':len(cases),
            'caveat':'Passing synthetic fixtures does not establish production readiness, semantic truth, external validity, cryptographic authority, or empirical Soft-Lineage validation.'}

if __name__=='__main__':
    out=run(); print(json.dumps(out,ensure_ascii=False,indent=2))
