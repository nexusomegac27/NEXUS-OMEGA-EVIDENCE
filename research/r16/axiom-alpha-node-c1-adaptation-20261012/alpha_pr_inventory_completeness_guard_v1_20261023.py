#!/usr/bin/env python3
"""C1-only PR file-inventory completeness gate; never grants publication.

A caller must provide an authenticated, complete GitHub PR metadata projection.
This module only checks internal consistency of that *untrusted* projection.
It does not fetch GitHub, prove authenticity, approve CI, or authorize a merge.
The historical V3 description oracle is imported unchanged after SHA256 pinning.
"""
import hashlib
import importlib.util
from pathlib import Path

EXPECTED_REPO = 'nexusomegac27/NEXUS-OMEGA-EVIDENCE'
PARENT_NAME = 'alpha_pr_description_drift_guard_v3_20261023.py'
PARENT_SHA256 = 'f1f4cede41576c64c44792f27a8caa8b2e38c28047d3225ef3cd9e35f9c94cfa'
MAX_FILES = 3000


def incomplete(reason):
    return {'status':'INCOMPLETE','reasons':[reason],
            'inventory_complete':'NOT_ESTABLISHED',
            'source_authentication':'NOT_ESTABLISHED'}


def audit_pr_description(snapshot):
    """Fail closed on missing/partial API file pagination, then run pinned V3."""
    if not isinstance(snapshot,dict):
        return incomplete('snapshot_type')
    total=snapshot.get('changed_files')
    files=snapshot.get('files')
    number=snapshot.get('number')
    if snapshot.get('repository')!=EXPECTED_REPO:
        return incomplete('repository_unbound')
    if type(number) is not int or number<1:
        return incomplete('pr_number_invalid')
    if type(total) is not int or not (0<=total<=MAX_FILES):
        return incomplete('changed_files_total_invalid')
    if not isinstance(files,list) or len(files)>MAX_FILES:
        return incomplete('files_array_invalid')
    if len(files)!=total:
        return incomplete('pr_file_inventory_incomplete')
    parent=Path(__file__).with_name(PARENT_NAME)
    try:
        raw=parent.read_bytes()
    except OSError:
        return incomplete('pinned_parent_source_missing')
    if hashlib.sha256(raw).hexdigest()!=PARENT_SHA256:
        return incomplete('pinned_parent_source_mismatch')
    spec=importlib.util.spec_from_file_location('pinned_pr_description_v3',str(parent))
    if spec is None or spec.loader is None:
        return incomplete('pinned_parent_unloadable')
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    verdict=module.audit_pr_description(snapshot)
    # Never turn a parent INCOMPLETE or DRIFT into success.
    if verdict.get('status') not in ('CONSISTENT','DRIFT','INCOMPLETE'):
        return incomplete('parent_verdict_invalid')
    return {**verdict,'inventory_complete':'COUNT_MATCH_ONLY',
            'source_authentication':'NOT_ESTABLISHED'}
