#!/usr/bin/env python3
"""Frozen, independent evaluator for C1 PR-file-inventory completeness.

Oracle and expected statuses are specified independently of the candidate.
The real PR #124 case is a manually captured projection of public GitHub API
metadata at pinned head 09ff7100...; it is NOT raw API-response byte evidence.
No network, writes, secrets, approvals or runtime mutation.
"""
import copy
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

MAIN = 'd355400dabed3c280e1fce5030cab69ea099428b'
HEAD = '09ff7100f92c6fcd291de132a4039b9f7b6a9cf7'
ROOT = 'research/r16/axiom-alpha-node-c1-adaptation-20261012/'
REPO = 'nexusomegac27/NEXUS-OMEGA-EVIDENCE'
PREDECESSOR_SHA256 = 'f1f4cede41576c64c44792f27a8caa8b2e38c28047d3225ef3cd9e35f9c94cfa'

# GitHub PR #124 /pulls/124/files?per_page=100 projection; observed 40/40.
ACTUAL_BASENAMES = '''ALPHA_BYTE_CAPTURE_CONSISTENCY_GUARD_V1_20261021.py
ALPHA_BYTE_CAPTURE_FROZEN_EVALUATOR_V1_20261021.py
ALPHA_CAPTURE_JSON_NUMERIC_DOMAIN_GUARD_V2_20261021.py
ALPHA_CI_EVIDENCE_COVERAGE_FROZEN_EVALUATOR_V1_20261021.py
ALPHA_CI_EVIDENCE_COVERAGE_GUARD_V1_20261021.py
ALPHA_CI_EVIDENCE_COVERAGE_REPLAY_RECEIPT_20261021_R1.md
ALPHA_CI_EVIDENCE_COVERAGE_REPLAY_RESULT_20261021_R1.json
ALPHA_PINNED_FIXTURE_HYDRATION_REPLAY_C1_20261021_R0.md
ALPHA_PUBLICATION_PROOF_AND_DENOMINATOR_GUARD_20261021_R0.md
ALPHA_SAFE_INTEGER_PUBLIC_REPLAY_EVIDENCE_20261021_R0.json
alpha-json-safe-integer-frozen-evaluator-v1-20261021.py
alpha-json-safe-integer-guard-v3-20261021.py
alpha_manifest_pin_guard_v1_20261023.py
alpha_manifest_pin_guard_v2_20261023.py
alpha_manifest_pin_guard_v3_20261023.py
alpha_pr_description_drift_guard_v1_20261023.py
alpha_pr_description_drift_guard_v2_20261023.py
alpha_pr_description_drift_guard_v3_20261023.py
alpha_pr_publication_preflight_guard_v1_20261023.py
alpha_pr_publication_preflight_guard_v2_20261023.py
alpha_pr_publication_preflight_guard_v3_20261023.py
alpha_pr_publication_preflight_guard_v4_20261023.py
alpha_pr_scope_drift_frozen_evaluator_v2_20261022.py
alpha_pr_scope_drift_guard_v3_20261022.py
alpha_pr_scope_drift_guard_v4_20261022.py
alpha_pr_scope_drift_guard_v5_20261022.py
alpha_pr_scope_drift_guard_v6_20261022.py
alpha_source_exactness_guard_v1_20261023.py
frozen_claim_cardinality_evaluator_v1_20261022.py
frozen_dependency_integrity_evaluator_v1_20261023.py
frozen_file_change_kind_evaluator_v1_20261022.py
frozen_pr_description_drift_evaluator_v1_20261023.py
frozen_pr_description_json_kind_evaluator_v1_20261023.py
frozen_pr_numeric_claim_evaluator_v1_20261023.py
frozen_scalar_type_preflight_evaluator_v1_20261023.py
frozen_source_exactness_evaluator_v1_20261023.py
frozen_timezone_preflight_evaluator_v1_20261023.py
frozen_unicode_path_evaluator_v1_20261022.py
frozen_v3_source_gap_evaluator_20261023.py
heldout_path_scope_evaluator_v1_20261022.py'''.splitlines()
ACTUAL_BODY = ('Research-only, append-only C1 candidate from pinned main '+MAIN+
    ' to pinned head 5fb35be25870e3a8785f0b41a82bcba652b43088. '
    'GitHub compare: 2 commits ahead, 0 behind; two added Markdown files only '
    'under the existing '+ROOT+' lane. Original bytes independently checked '
    'through the existing GitHub read API: publication proof report 2070 B '
    'SHA256 5e626c47ce63042c5156aacfe345784a78e719acd0a4f05cf4abe1ae736e21c7 '
    'blob edc5248e954472379bd63e06ae401857d10baa43; fixture hydration report '
    '2418 B SHA256 e59da6e3c1bf6af8f3cecd808967bb0fa6a515325da415ac82cd7613962d2a47 '
    'blob 5dae97c9a2f2211e05fdcde1d14f9d7a19e96c63. '
    'An isolated frozen adversarial PR-readiness evaluator (SHA256 '
    '8d6d81267d14f5c1cc97b1fb0593d9f97fb72b6fab191327590a7b58a60c4814) '
    'passed 18/18 local fixtures; naive baseline 1/18. This is NOT an independent '
    'scientific validation, production integration, WWW parity or main merge. '
    'No source overwrites, no new directories, no external actor registrations, '
    'no secrets. CLAIM_CEILING=C1_DESCRIPTIVE_ONLY. Keep DRAFT pending required '
    'CI and independent readback. Issue #93 remains passive receiver.')

def small():
    return {'repository':REPO,'number':124,'body':(
        f'Research-only C1 candidate from pinned main {MAIN} to pinned head {HEAD}. '
        f'GitHub compare: 2 commits ahead, 0 behind; two added Python files only '
        f'under the existing {ROOT} lane. CLAIM_CEILING=C1_DESCRIPTIVE_ONLY.'),
        'base_sha':MAIN,'head_sha':HEAD,'commits':2,'changed_files':2,
        'files':[{'filename':ROOT+'a.py','status':'added'},
                 {'filename':ROOT+'b.py','status':'added'}]}

def actual():
    assert len(ACTUAL_BASENAMES)==40
    return {'repository':REPO,'number':124,'body':ACTUAL_BODY,'base_sha':MAIN,
            'head_sha':HEAD,'commits':37,'changed_files':40,
            'files':[{'filename':ROOT+x,'status':'added'} for x in ACTUAL_BASENAMES]}

# Every expected outcome is predeclared; no candidate-derived oracle.
CASES = [
    ('small_complete','CONSISTENT',lambda s:s),
    ('declared_extra_file','INCOMPLETE',lambda s:s.update(changed_files=3)),
    ('declared_missing_file','INCOMPLETE',lambda s:s.update(changed_files=1)),
    ('absent_total','INCOMPLETE',lambda s:s.pop('changed_files')),
    ('string_total','INCOMPLETE',lambda s:s.update(changed_files='2')),
    ('bool_total','INCOMPLETE',lambda s:s.update(changed_files=True)),
    ('float_total','INCOMPLETE',lambda s:s.update(changed_files=2.0)),
    ('negative_total','INCOMPLETE',lambda s:s.update(changed_files=-1)),
    ('oversized_total','INCOMPLETE',lambda s:s.update(changed_files=3001)),
    ('partial_first_page','INCOMPLETE',lambda s:s['files'].pop()),
    ('duplicate_file','INCOMPLETE',lambda s:s['files'].__setitem__(1,copy.deepcopy(s['files'][0]))),
    ('missing_repository','INCOMPLETE',lambda s:s.pop('repository')),
    ('wrong_repository','INCOMPLETE',lambda s:s.update(repository='other/repo')),
    ('missing_pr_number','INCOMPLETE',lambda s:s.pop('number')),
    ('bool_pr_number','INCOMPLETE',lambda s:s.update(number=True)),
    ('bad_pr_number','INCOMPLETE',lambda s:s.update(number=0)),
    ('malformed_sha','INCOMPLETE',lambda s:s.update(head_sha='not-a-sha')),
    ('changed_description','DRIFT',lambda s:s.update(body=s['body'].replace('two added','three added'))),
]

def load(path):
    spec=importlib.util.spec_from_file_location('guard_under_test',str(path))
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def evaluate(path):
    mod=load(path)
    rows=[]
    for name,expected,mutate in CASES:
        snap=small()
        mutate(snap)
        try: actual_status=mod.audit_pr_description(snap)['status']
        except Exception as e: actual_status='EXCEPTION:'+type(e).__name__
        rows.append({'case':name,'expected':expected,'actual':actual_status,
                     'pass':actual_status==expected})
    # Real API projection (not immutable raw response) plus a negative missing entry.
    for name,expected,mutate in [
        ('real_pr124_40_of_40','DRIFT',lambda s:s),
        ('real_pr124_39_of_40','INCOMPLETE',lambda s:s['files'].pop()),
        ('real_pr124_declared_41','INCOMPLETE',lambda s:s.update(changed_files=41))]:
        snap=actual(); mutate(snap)
        try: actual_status=mod.audit_pr_description(snap)['status']
        except Exception as e: actual_status='EXCEPTION:'+type(e).__name__
        rows.append({'case':name,'expected':expected,'actual':actual_status,
                     'pass':actual_status==expected})
    return {'total':len(rows),'correct':sum(x['pass'] for x in rows),'rows':rows}

if __name__=='__main__':
    result=evaluate(Path(sys.argv[1]))
    print(json.dumps(result,indent=2))
    sys.exit(0 if result['correct']==result['total'] else 1)
