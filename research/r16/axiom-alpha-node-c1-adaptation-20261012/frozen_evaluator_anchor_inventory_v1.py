#!/usr/bin/env python3
"""Independent fixed test oracle: unique source identities (repo, commit, path).
Synthetic only; no GitHub/network writes. This evaluator is not the candidate.
"""
import copy, importlib.util, json, sys
from pathlib import Path

REPO='nexusomegac27/NEXUS-OMEGA-EVIDENCE'
COMMIT='206381c880770954865c67d9075c401efd2295f0'
PATH='research/r26/collective-expert-handoffs-20261011/NEXUS_OMEGA_AXIOM_COLLECTIVE_EXPERT_MAXI_ORDER_20261011_R0.md'
SHA='4a4a2770622ee46dc394d84f32d693a05531896efb4213e7d01c8fc3873d82c5'

def fixture():
    src={'repository':REPO,'commit':COMMIT,'path':PATH,'bytes':13150,'sha256':SHA,'source_status':'GITHUB_SOURCE_VERIFIED'}
    return {'schema_version':'1.0.0','object':'NEXUS_OMEGA_EXAMPLE_TASK_ANCHOR_V1_20261011_R0',
    'norm_id':'NEXUS_OMEGA_TASK_ANCHOR_NORM_V1','norm_class':'NEXUS_INTERNAL_BINDING_TECHNICAL_SPECIFICATION',
    'din_status':'DIN_SPEC_92001_1_INSPIRED_NOT_DIN_ISSUED_NOT_CERTIFIED','claim_ceiling':'C1_DESCRIPTIVE_ONLY',
    'origin':{'operator_authority':'OPERATOR_GOVERNED_ONLY','issuer_role':'AXIOM','recipient_role':'EXTERNAL_RESEARCH_CANDIDATE','verified_github_actor':'NOT_ESTABLISHED','predecessor_object':'NEXUS_OMEGA_AXIOM_COLLECTIVE_EXPERT_MAXI_ORDER_20261011_R0','predecessor_repository':REPO,'predecessor_commit':COMMIT,'predecessor_path':PATH,'predecessor_bytes':13150,'predecessor_sha256':SHA},
    'delegation':{'scope':'EXTERNAL_RESEARCH_ONLY','allowed_actions':['READ_PUBLIC_SOURCES','INDEPENDENT_FALSIFICATION','OPERATOR_BRIDGE_RETURN'],'prohibited_actions':['NODE_RESET','MEMORY_DELETION','GITHUB_UNAUTHORIZED_WRITE','RUNTIME_EXECUTION','CLAIM_PROMOTION','HOSTINGER_DEPLOY'],'write_slot':'NOT_ALLOCATED','runtime_authorized':False,'node_reset_authorized':False,'claim_promotion_authorized':False},
    'mission':{'question':'Independently test the scoped R26 mathematical and provenance results without elevating claims.','deliverables':['FALSIFICATION_REPORT','SOURCE_HASH_INVENTORY','REPRODUCTION_METHOD'],'falsifiers':['NUMERIC_COUNTEREXAMPLE','FALSE_PROVENANCE_LINK','HISTORICAL_RETRACTION_MISSING'],'acceptance_tests':['ALL_SOURCE_IDS_DECLARED','NEGATIVE_RESULTS_PRESERVED','NO_C1_PROMOTION'],'pause_conditions':['MISSING_SOURCE_OR_AUTHORITY','IRREVERSIBLE_ACTION','OUT_OF_SCOPE_REQUEST'],'not_executed':['NF05_NF06','RUNTIME_DEPLOYMENT','NODE_RESET']},
    'continuity':{'anchor_id':'NEXUS_OMEGA_EXAMPLE_TASK_ANCHOR_V1_20261011_R0','rebind_mode':'DRIFT_RESET_ONLY','node_reset_prohibited':True,'history_preserved':True,'source_bytes_preserved':True,'observations_preserved':True,'checkpoints_preserved':True,'runtime_state_preserved':True,'drift_triggers':['PROVENANCE_MISMATCH','AUTHORITY_ESCALATION','REPOSITORY_PATH_DRIFT','CLAIM_PROMOTION'],'rebind_procedure':'RELOAD_VERIFIED_ANCHOR_APPEND_DIFFERENCE_WITNESS_NO_DELETION','correction_policy':'APPEND_ONLY_SUCCESSOR'},
    'provenance':{'sources':[src],'missing_source_policy':'HOLD_SCOPED_NOT_RECONSTRUCT','copyright_privacy':'PUBLIC_SAFE_REFERENCES_ONLY_NO_RAW_PRIVATE_DATA','independent_rehash_required':True},
    'return_contract':{'recipient':'NEXUS_OPERATOR_AXIOM','inbox_issue_url':'https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/issues/93','transport_class':'OPERATOR_TO_AXIOM_BRIDGE','manifest_schema':'schema/expert-hash-handshake-v1.schema.json','receiver_ack':'PENDING_AXIOM_INDEPENDENT_REHASH','scientific_adjudication_separate':True},
    'quality_gates':{'functionality_performance':['OFFLINE_VALIDATOR_RUNS_WITHOUT_NETWORK'],'robustness_stability':['NODE_RESET_DENIED','HISTORY_CANNOT_BE_CLEARED_BY_REBIND'],'traceability_comprehensibility':['PINNED_FULL_PARENT_SHA','APPEND_ONLY_NEGATIVE_FINDINGS']}}

def test_cases():
    cases=[]
    def add(name,expect,mutate):
        a=fixture(); mutate(a); cases.append((name,expect,a))
    add('single_valid',True,lambda a:None)
    add('two_distinct_paths',True,lambda a:a['provenance']['sources'].append({**a['provenance']['sources'][0],'path':'research/r26/second-source.md'}))
    add('same_path_different_commit',True,lambda a:a['provenance']['sources'].append({**a['provenance']['sources'][0],'commit':'1'*40}))
    add('same_commit_path_conflicting_sha',False,lambda a:a['provenance']['sources'].append({**a['provenance']['sources'][0],'sha256':'f'*64}))
    add('same_commit_path_identical_duplicate',False,lambda a:a['provenance']['sources'].append(copy.deepcopy(a['provenance']['sources'][0])))
    add('same_commit_path_status_conflict',False,lambda a:a['provenance']['sources'].append({**a['provenance']['sources'][0],'source_status':'OPERATOR_REPORTED'}))
    add('non_parent_duplicate',False,lambda a:a['provenance']['sources'].extend([{**a['provenance']['sources'][0],'path':'research/r26/other.md'}]*2))
    add('missing_predecessor',False,lambda a:a['provenance']['sources'].__setitem__(0,{**a['provenance']['sources'][0],'path':'research/r26/other.md'}))
    add('invalid_sha',False,lambda a:a['provenance']['sources'].__setitem__(0,{**a['provenance']['sources'][0],'sha256':'INVALID'}))
    add('foreign_repository',False,lambda a:a['provenance']['sources'].__setitem__(0,{**a['provenance']['sources'][0],'repository':'other/repo'}))
    return cases

def run(module_path):
    spec=importlib.util.spec_from_file_location('subject',module_path); mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    rows=[]
    for name,expect,a in test_cases():
        try: mod.validate(mod.strict_load(json.dumps(a).encode()));accepted=True;error=None
        except Exception as e:accepted=False;error=type(e).__name__+':'+str(e)
        rows.append({'name':name,'expected_accept':expect,'actual_accept':accepted,'pass':accepted==expect,'error':error})
    return rows

if __name__=='__main__':
    rows=run(Path(sys.argv[1]));print(json.dumps({'total':len(rows),'passed':sum(x['pass'] for x in rows),'rows':rows},indent=2));sys.exit(0 if all(x['pass'] for x in rows) else 1)
