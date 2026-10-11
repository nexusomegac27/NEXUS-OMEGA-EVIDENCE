#!/usr/bin/env python3
"""Offline NEXUS TASK ANCHOR V1 structural & non-destructive drift validator.

This validates declared task semantics only. It does not grant any authority, fetch
private sources, reset nodes, write memory or execute a DRIFT_RESET operation.
Stdlib only; JSON Schema reference is in schema/task-anchor-norm-v1.schema.json.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from pathlib import Path, PurePosixPath

REPO = 'nexusomegac27/NEXUS-OMEGA-EVIDENCE'
INBOX = 'https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/issues/93'
HEX40 = re.compile(r'^[0-9a-f]{40}$')
HEX64 = re.compile(r'^[0-9a-f]{64}$')
OBJ = re.compile(r'^NEXUS_OMEGA_[A-Z0-9_]{5,200}$')
TOP = {'schema_version','object','norm_id','norm_class','din_status','claim_ceiling','origin',
       'delegation','mission','continuity','provenance','return_contract','quality_gates'}
FIELDS = {
 'origin': {'operator_authority','issuer_role','recipient_role','verified_github_actor',
            'predecessor_object','predecessor_repository','predecessor_commit','predecessor_path',
            'predecessor_bytes','predecessor_sha256'},
 'delegation': {'scope','allowed_actions','prohibited_actions','write_slot',
                'runtime_authorized','node_reset_authorized','claim_promotion_authorized'},
 'mission': {'question','deliverables','falsifiers','acceptance_tests','pause_conditions','not_executed'},
 'continuity': {'anchor_id','rebind_mode','node_reset_prohibited','history_preserved','source_bytes_preserved',
                'observations_preserved','checkpoints_preserved','runtime_state_preserved',
                'drift_triggers','rebind_procedure','correction_policy'},
 'provenance': {'sources','missing_source_policy','copyright_privacy','independent_rehash_required'},
 'return_contract': {'recipient','inbox_issue_url','transport_class','manifest_schema','receiver_ack',
                     'scientific_adjudication_separate'},
 'quality_gates': {'functionality_performance','robustness_stability','traceability_comprehensibility'},
}
SOURCE_KEYS = {'repository','commit','path','bytes','sha256','source_status'}
REQUIRED_DENY = {'NODE_RESET','MEMORY_DELETION','GITHUB_UNAUTHORIZED_WRITE','RUNTIME_EXECUTION','CLAIM_PROMOTION'}
REQUIRED_PRESERVE = {'history_preserved','source_bytes_preserved','observations_preserved',
                     'checkpoints_preserved','runtime_state_preserved'}

def pairs_no_duplicates(pairs):
    output = {}
    for k,v in pairs:
        if k in output:
            raise ValueError('DUPLICATE_JSON_KEY:'+k)
        output[k] = v
    return output

def strict_load(content:bytes) -> dict:
    if len(content) > 262144:
        raise ValueError('ANCHOR_TOO_LARGE')
    o=json.loads(content.decode('utf-8'), object_pairs_hook=pairs_no_duplicates)
    if not isinstance(o, dict):
        raise ValueError('OBJECT_REQUIRED')
    return o

def equal_keys(value,keys,path):
    if not isinstance(value,dict) or set(value)!=keys:
        raise ValueError('FIELDS_MISMATCH:'+path)

def safe_repo_path(s):
    if not isinstance(s,str) or not s or '\\' in s or ':' in s or '\x00' in s:
        raise ValueError('UNSAFE_SOURCE_PATH')
    if s.startswith('/') or any(p in {'', '.', '..'} for p in s.split('/')) or str(PurePosixPath(s))!=s:
        raise ValueError('UNSAFE_SOURCE_PATH')
    if not s.startswith(('docs/','schema/','scripts/','tests/','validation/','examples/','research/','objects/','index/','communication/')):
        raise ValueError('SOURCE_PATH_DOMAIN')

def strings(xs,key):
    if not isinstance(xs,list) or not xs or len(set(map(str,xs)))!=len(xs):
        raise ValueError('NONEMPTY_UNIQUE_LIST:'+key)
    if any(not isinstance(x,str) or len(x)<3 for x in xs):
        raise ValueError('INVALID_LIST_ITEMS:'+key)

def const(value,expected,key):
    if type(value)!=type(expected) or value != expected:
        raise ValueError('INVALID_'+key)

def validate(o:dict) -> dict:
    equal_keys(o, TOP, 'TOP')
    for key,ks in FIELDS.items(): equal_keys(o[key],ks,key)
    const(o['schema_version'],'1.0.0','VERSION')
    if not isinstance(o['object'],str) or not OBJ.fullmatch(o['object']):
        raise ValueError('INVALID_OBJECT_ID')
    const(o['norm_id'],'NEXUS_OMEGA_TASK_ANCHOR_NORM_V1','NORM')
    const(o['norm_class'],'NEXUS_INTERNAL_BINDING_TECHNICAL_SPECIFICATION','NORM_CLASS')
    const(o['din_status'],'DIN_SPEC_92001_1_INSPIRED_NOT_DIN_ISSUED_NOT_CERTIFIED','DIN_CLAIM')
    const(o['claim_ceiling'],'C1_DESCRIPTIVE_ONLY','CLAIM_CEILING')
    a=o['origin']; d=o['delegation']; m=o['mission']; c=o['continuity']; p=o['provenance']; r=o['return_contract']
    const(a['operator_authority'],'OPERATOR_GOVERNED_ONLY','OPERATOR_AUTHORITY')
    const(a['predecessor_repository'],REPO,'PREDECESSOR_REPO')
    for k in ('issuer_role','recipient_role','verified_github_actor','predecessor_object'):
        if not isinstance(a[k],str) or len(a[k])<2:raise ValueError('INVALID_'+k)
    if not isinstance(a['predecessor_bytes'],int) or isinstance(a['predecessor_bytes'],bool) or a['predecessor_bytes']<1: raise ValueError('INVALID_PARENT_BYTES')
    if not isinstance(a['predecessor_commit'],str) or not HEX40.fullmatch(a['predecessor_commit']): raise ValueError('INVALID_PARENT_COMMIT')
    if not isinstance(a['predecessor_sha256'],str) or not HEX64.fullmatch(a['predecessor_sha256']): raise ValueError('INVALID_PARENT_SHA256')
    safe_repo_path(a['predecessor_path'])
    if not isinstance(d['scope'],str) or not d['scope']: raise ValueError('MISSING_SCOPE')
    for k in ('allowed_actions','prohibited_actions'):
        strings(d[k],k)
    if not REQUIRED_DENY.issubset(set(d['prohibited_actions'])): raise ValueError('PROHIBITED_ACTIONS_INCOMPLETE')
    if set(d['allowed_actions']) & set(d['prohibited_actions']): raise ValueError('ACTION_SCOPE_CONFLICT')
    const(d['write_slot'],'NOT_ALLOCATED','WRITE_SLOT')
    for k in ('runtime_authorized','node_reset_authorized','claim_promotion_authorized'):const(d[k],False,k)
    if not isinstance(m['question'],str) or len(m['question'])<10: raise ValueError('QUESTION_REQUIRED')
    for k in ('deliverables','falsifiers','acceptance_tests','pause_conditions','not_executed'): strings(m[k],k)
    const(c['anchor_id'],o['object'],'ANCHOR_ID')
    const(c['rebind_mode'],'DRIFT_RESET_ONLY','REBOUND_MODE')
    const(c['node_reset_prohibited'],True,'NODE_RESET_BOUNDARY')
    for k in REQUIRED_PRESERVE: const(c[k],True,k)
    strings(c['drift_triggers'],'drift_triggers')
    const(c['rebind_procedure'],'RELOAD_VERIFIED_ANCHOR_APPEND_DIFFERENCE_WITNESS_NO_DELETION','REBOUND_PROCEDURE')
    const(c['correction_policy'],'APPEND_ONLY_SUCCESSOR','CORRECTION')
    const(p['missing_source_policy'],'HOLD_SCOPED_NOT_RECONSTRUCT','MISSING_SOURCE')
    const(p['independent_rehash_required'],True,'INDEPENDENT_REHASH')
    if not isinstance(p['copyright_privacy'],str) or len(p['copyright_privacy'])<8: raise ValueError('COPYRIGHT_PRIVACY_REQUIRED')
    if not isinstance(p['sources'],list) or not p['sources']: raise ValueError('SOURCE_INVENTORY_REQUIRED')
    for x in p['sources']:
        equal_keys(x,SOURCE_KEYS,'SOURCE')
        const(x['repository'],REPO,'SOURCE_REPO')
        if not isinstance(x['commit'],str) or not HEX40.fullmatch(x['commit']): raise ValueError('SOURCE_COMMIT')
        safe_repo_path(x['path'])
        if not isinstance(x['bytes'],int) or isinstance(x['bytes'],bool) or x['bytes']<1: raise ValueError('SOURCE_BYTES')
        if not isinstance(x['sha256'],str) or not HEX64.fullmatch(x['sha256']): raise ValueError('SOURCE_SHA')
        if x['source_status'] not in ('OPERATOR_REPORTED','GITHUB_SOURCE_VERIFIED','AXIOM_BYTES_MATCH'): raise ValueError('SOURCE_STATUS')
    if not any(x['commit']==a['predecessor_commit'] and x['path']==a['predecessor_path'] and x['sha256']==a['predecessor_sha256'] and x['bytes']==a['predecessor_bytes'] for x in p['sources']):
        raise ValueError('PREDECESSOR_NOT_IN_SOURCE_INVENTORY')
    const(r['recipient'],'NEXUS_OPERATOR_AXIOM','RECIPIENT')
    const(r['inbox_issue_url'],INBOX,'INBOX')
    const(r['transport_class'],'OPERATOR_TO_AXIOM_BRIDGE','BRIDGE_REQUIRED_EMPTY_ALLOWLIST')
    const(r['manifest_schema'],'schema/expert-hash-handshake-v1.schema.json','HANDSHAKE_SCHEMA')
    const(r['receiver_ack'],'PENDING_AXIOM_INDEPENDENT_REHASH','FORGED_ACK')
    const(r['scientific_adjudication_separate'],True,'SCIENCE_SEPARATION')
    for k,v in o['quality_gates'].items(): strings(v,k)
    return {'state':'ANCHOR_FORMAT_VALIDATED_ONLY','object':o['object'], 'reset_semantics':'DRIFT_RESET_ONLY',
            'node_reset':'PROHIBITED','actor_authorization':'NOT_ESTABLISHED_FROM_FORMAT',
            'source_bytes':'REQUIRES_INDEPENDENT_FETCH','scientific_claim':'C1_DESCRIPTIVE_ONLY'}

def classify_drift(anchor:dict, observed:dict) -> dict:
    """Pure decision helper: never mutates anchor, sources, node or checkpoints.

    observed: {source_present, source_hash_matches, requested_actions,
               claimed_role, claimed_ceiling, predecessor_sha256, scientific_successor}
    """
    validate(anchor)
    if not isinstance(observed,dict): raise ValueError('OBSERVATION_REQUIRED')
    if observed.get('source_present') is not True or observed.get('source_hash_matches') is not True:
        return {'decision':'HOLD_SOURCE_GAP','action':'FETCH_EXACT_ANCHOR_BYTES_AND_REHASH', 'node_reset':False,'history_preserved':True}
    acts=observed.get('requested_actions',[])
    if not isinstance(acts,list) or any(not isinstance(x,str) for x in acts): raise ValueError('INVALID_ACTIONS')
    if set(acts)&set(anchor['delegation']['prohibited_actions']):
        return {'decision':'AUTHORITY_HOLD','action':'NO_OPERATION_REQUIRE_OPERATOR_AUTHORIZATION','node_reset':False,'history_preserved':True}
    if set(acts)-set(anchor['delegation']['allowed_actions']):
        return {'decision':'AUTHORITY_HOLD','action':'NO_OPERATION_REQUIRE_OPERATOR_AUTHORIZATION','node_reset':False,'history_preserved':True}
    drift = []
    if observed.get('claimed_role')!=anchor['origin']['recipient_role']:drift.append('recipient_role')
    if observed.get('claimed_ceiling')!=anchor['claim_ceiling']:drift.append('claim_ceiling')
    if observed.get('predecessor_sha256')!=anchor['origin']['predecessor_sha256']:drift.append('predecessor_sha256')
    if drift:
        return {'decision':'DRIFT_RESET_REQUIRED','action':'RELOAD_VERIFIED_ANCHOR_APPEND_DIFFERENCE_WITNESS_NO_DELETION',
                'differing_fields':drift,'node_reset':False,'history_preserved':True}
    if observed.get('scientific_successor') is True:
        return {'decision':'SCIENTIFIC_SUCCESSOR_PROPOSED','action':'APPEND_ONLY_NEW_VERSION_WITH_OPERATOR_REVIEW','node_reset':False,'history_preserved':True}
    return {'decision':'NO_DRIFT','action':'CONTINUE_WITHIN_EXISTING_AUTHORITY','node_reset':False,'history_preserved':True}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--anchor',type=Path,required=True)
    parser.add_argument('--observed',type=Path)
    p=parser.parse_args()
    payload=p.anchor.read_bytes(); anchor=strict_load(payload); result=validate(anchor)
    result['anchor_bytes']=len(payload);result['anchor_sha256']=hashlib.sha256(payload).hexdigest()
    if p.observed: result['drift']=classify_drift(anchor,strict_load(p.observed.read_bytes()))
    print(json.dumps(result,sort_keys=True))
if __name__=='__main__':main()