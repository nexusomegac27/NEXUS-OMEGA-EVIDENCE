#!/usr/bin/env python3
"""Frozen independent evaluator for timezone-explicit PR preflight; no GitHub writes.

Fixture contract fixed before candidate implementation. These are synthetic
metadata snapshots, not independently authenticated GitHub event timestamps.
"""
import copy
import importlib
import json
import sys

MODULE = sys.argv[1] if len(sys.argv)>1 else 'alpha_pr_publication_preflight_guard_v2_20261023'
fn = importlib.import_module(MODULE).check_pr_publication_preflight

BASE = {
 'repo': {'repository_full_name':'nexusomegac27/NEXUS-OMEGA-EVIDENCE', 'owner':{'login':'nexusomegac27'},'permissions':{'push':True},'default_branch':'main'},
 'pr': {'number':124,'state':'open','merged':False,'draft':True,'base':'main','base_sha':'d355400dabed3c280e1fce5030cab69ea099428b','head':'axiom/alpha-export-surface-closure-c1-20261021','head_sha':'0327becd1fa8a0ff3ed468847de13f36f00f8f2b','head_repo_full_name':'nexusomegac27/NEXUS-OMEGA-EVIDENCE','user':{'login':'nexusomegac27'}},
 'main': {'name':'main','sha':'d355400dabed3c280e1fce5030cab69ea099428b'},
 'branch': {'name':'axiom/alpha-export-surface-closure-c1-20261021','sha':'0327becd1fa8a0ff3ed468847de13f36f00f8f2b'},
 'target': {'pinned_main':'d355400dabed3c280e1fce5030cab69ea099428b','pinned_head':'0327becd1fa8a0ff3ed468847de13f36f00f8f2b','repository_full_name':'nexusomegac27/NEXUS-OMEGA-EVIDENCE','pr_number':124,'branch':'axiom/alpha-export-surface-closure-c1-20261021','path':'research/r16/axiom-alpha-node-c1-adaptation-20261012/alpha_pr_publication_preflight_guard_v2_20261023.py','path_absent_confirmed':True,'observed_at':'2026-10-23T08:09:30Z'}
}
NOW='2026-10-23T08:10:00Z'
CASES = [
 ('aware_z_valid',{},NOW,'READY_FOR_CONTENT_CHECK'),
 ('aware_offset_valid',{'target.observed_at':'2026-10-23T10:09:30+02:00'},NOW,'READY_FOR_CONTENT_CHECK'),
 ('both_naive',{'target.observed_at':'2026-10-23T08:09:30'},'2026-10-23T08:10:00','TIMEZONE_REQUIRED'),
 ('observed_naive',{'target.observed_at':'2026-10-23T08:09:30'},NOW,'TIMEZONE_REQUIRED'),
 ('now_naive',{},'2026-10-23T08:10:00','TIMEZONE_REQUIRED'),
 ('date_only',{'target.observed_at':'2026-10-23'},NOW,'TIMEZONE_REQUIRED'),
 ('offset_no_colon',{'target.observed_at':'2026-10-23T10:09:30+0200'},NOW,'TIMEZONE_REQUIRED'),
 ('offset_out_of_range',{'target.observed_at':'2026-10-23T22:09:30+14:30'},NOW,'TIMEZONE_REQUIRED'),
 ('lowercase_z',{'target.observed_at':'2026-10-23T08:09:30z'},NOW,'TIMEZONE_REQUIRED'),
 ('timestamp_non_string',{'target.observed_at':True},NOW,'TIMEZONE_REQUIRED'),
 ('stale_aware',{'target.observed_at':'2026-10-23T08:07:59Z'},NOW,'STALE_SNAPSHOT'),
 ('future_aware',{'target.observed_at':'2026-10-23T08:10:01Z'},NOW,'STALE_SNAPSHOT'),
 ('wrong_branch',{'target.branch':'codex/alpha-node-publication-proof-20261021'},NOW,'WRONG_BRANCH'),
 ('head_drift',{'pr.head_sha':'0'*40},NOW,'HEAD_DRIFT'),
 ('path_unverified',{'target.path_absent_confirmed':False},NOW,'PATH_EXISTS_OR_UNVERIFIED'),
 ('repo_mismatch',{'repo.repository_full_name':'example/other'},NOW,'REPO_SCOPE_MISMATCH'),
 ('offset_zero',{'target.observed_at':'2026-10-23T08:09:30+00:00'},NOW,'READY_FOR_CONTENT_CHECK'),
 ('fractional',{'target.observed_at':'2026-10-23T08:09:30.123456Z'},NOW,'READY_FOR_CONTENT_CHECK'),
 ('invalid_calendar',{'target.observed_at':'2026-02-30T08:09:30Z'},NOW,'INCOMPLETE'),
 ('invalid_path',{'target.path':'research/r16/../unsafe.py'},NOW,'PATH_SCOPE_HOLD'),
 ('missing_target',{'target':None},NOW,'INCOMPLETE'),
 ('empty_snapshot',None,NOW,'INCOMPLETE'),
]
results=[]
for name,changes,now,expected in CASES:
    snap=copy.deepcopy(BASE) if changes is not None else {}
    if changes:
        for path,value in changes.items():
            keys=path.split('.')
            at=snap
            for key in keys[:-1]: at=at[key]
            at[keys[-1]]=value
    try: actual=fn(snap,now)['status']
    except Exception as e: actual='EXCEPTION:'+type(e).__name__
    results.append({'name':name,'expected':expected,'actual':actual,'pass':actual==expected})
print(json.dumps({'module':MODULE,'total':len(results),'passed':sum(x['pass'] for x in results),'results':results},indent=2))
if not all(x['pass'] for x in results): sys.exit(1)
