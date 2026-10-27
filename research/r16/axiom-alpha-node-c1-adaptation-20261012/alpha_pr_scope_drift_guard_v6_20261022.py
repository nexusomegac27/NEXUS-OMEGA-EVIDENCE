#!/usr/bin/env python3
"""C1 isolated V6: check PR file change kind and snapshot completeness.

The immutable V5 source remains the narrative/path oracle. V6 adds only the
missing 'added only' file-status requirement. A supplied completeness boolean
is a *precondition*, not cryptographic proof of GitHub API pagination; callers
must separately verify full pages and immutable PR-head consistency.
No merge, authorization, deployment or scientific validity is conferred.
"""
import hashlib
import importlib.util
from pathlib import Path

V5_SHA256 = '5cc92f933dfabfc80a8ac97c3901bcd81de70ec25b425a2bae5eb2112ad5ad3f'
V5_NAME = 'alpha_pr_scope_drift_guard_v5_20261022.py'


def _v5(snapshot):
    path = Path(__file__).with_name(V5_NAME)
    try:
        raw = path.read_bytes()
        if hashlib.sha256(raw).hexdigest() != V5_SHA256:
            raise ValueError('V5_SHA256_MISMATCH')
        spec = importlib.util.spec_from_file_location('pinned_v5_guard', path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module.check_scope(snapshot)
    except (OSError, ValueError, ImportError, SyntaxError):
        return {'status': 'INCOMPLETE', 'reasons': ['V5_DEPENDENCY_UNAVAILABLE_OR_CHANGED']}


def check_scope(snapshot):
    base = _v5(snapshot)
    if base.get('status') != 'MATCH':
        return base
    changes = snapshot.get('file_changes')
    if snapshot.get('file_pages_complete') is not True or type(snapshot.get('file_pages_complete')) is not bool:
        return {'status': 'INCOMPLETE', 'reasons': ['FILE_LIST_PAGINATION_NOT_CONFIRMED']}
    if (not isinstance(changes, list) or len(changes) != snapshot['changed_files']
        or not all(isinstance(row, dict) and isinstance(row.get('filename'), str)
                       and isinstance(row.get('status'), str) for row in changes)):
        return {'status': 'INCOMPLETE', 'reasons': ['FILE_CHANGE_RECORDS_MISSING_OR_INVALID']}
    names = [row['filename'] for row in changes]
    if len(set(names)) != len(names) or set(names) != set(snapshot['filenames']):
        return {'status': 'INCOMPLETE', 'reasons': ['FILE_CHANGE_RECORDS_NOT_SAME_PATH_SET']}
    allowed_statuses = {'added', 'modified', 'removed', 'renamed', 'copied', 'changed', 'unchanged'}
    if any(row['status'] not in allowed_statuses for row in changes):
        return {'status': 'INCOMPLETE', 'reasons': ['UNRECOGNIZED_FILE_CHANGE_STATUS']}
    if any(row['status'] != 'added' for row in changes):
        return {'status': 'DRIFT', 'reasons': ['FILE_CHANGE_KIND_NOT_ADDED']}
    return base
