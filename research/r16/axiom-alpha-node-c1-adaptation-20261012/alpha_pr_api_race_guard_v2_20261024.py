#!/usr/bin/env python3
"""C1 isolated V2: reject reused before/after objects and non-scalar paths.

The immutable V1 remains the comparison baseline and semantic dependency.
This only enforces structural preconditions. Distinct Python dictionaries do
not establish two authenticated HTTP requests, page provenance or time order.
No network, mutation, deployment, merge or claim promotion.
"""
import hashlib
import importlib.util
from pathlib import Path

_V1_NAME = 'alpha_pr_api_race_guard_v1_20261023.py'
_V1_SHA256 = 'ec37870f94c187961cf684fa9a8bbce19668a87effaa11a5dd7141131a675d29'


def _incomplete(reason):
    return {'status':'INCOMPLETE','reasons':[reason],
            'source_authentication':'NOT_ESTABLISHED',
            'pagination_completeness':'COUNT_MATCH_ONLY_NOT_PROOF',
            'two_http_reads':'NOT_ESTABLISHED_BY_OBJECT_DISTINCTNESS'}


def _valid_unicode_scalar(value):
    return isinstance(value,str) and not any(0xD800 <= ord(ch) <= 0xDFFF for ch in value)


def _load_v1():
    path=Path(__file__).with_name(_V1_NAME)
    try: raw=path.read_bytes()
    except OSError: return None
    if hashlib.sha256(raw).hexdigest()!=_V1_SHA256: return None
    spec=importlib.util.spec_from_file_location('pinned_pr_api_race_v1',path)
    if spec is None or spec.loader is None: return None
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def check(snapshot):
    if not isinstance(snapshot,dict): return _incomplete('snapshot_type')
    before,after=snapshot.get('before'),snapshot.get('after')
    if not isinstance(before,dict) or not isinstance(after,dict):
        return _incomplete('two_metadata_reads_required')
    if before is after: return _incomplete('same_metadata_object_reused')
    paths=snapshot.get('filenames')
    if isinstance(paths,list) and any(not _valid_unicode_scalar(p) for p in paths):
        return _incomplete('non_scalar_or_non_string_filename')
    base=_load_v1()
    if base is None: return _incomplete('pinned_v1_dependency_missing_or_tampered')
    result=base.check(snapshot)
    result['two_http_reads']='NOT_ESTABLISHED_BY_OBJECT_DISTINCTNESS'
    result['unicode_scalar_guard']='NON_SCALAR_FILENAMES_REJECTED'
    return result
