#!/usr/bin/env python3
"""C1-only Unicode portability preflight over the immutable Run142 set guard.

Synthetic research candidate, not an authoritative Git path policy. Rejects
non-UTF-8 Unicode scalar strings and non-NFC manifest paths. Does not mutate
sources, authenticate input, certify cross-platform checkout or authorize merge.
"""
import hashlib
import importlib.util
import unicodedata
from pathlib import Path

ORIGINAL = 'alpha_pr124_cross_snapshot_inventory_disjoint_guard_v1_20261025.py'
ORIGINAL_SHA256 = '110965af4788a7ac02df70af9be15a2f22be80b186a0fba9148b140a971179aa'

def fail(reason):
    return {'status': 'FAIL_CLOSED', 'reason': reason,
            'source_authentication': 'NOT_ESTABLISHED',
            'project_automation_rate': 'NOT_COMPUTABLE',
            'claim_ceiling': 'C1_DESCRIPTIVE_ONLY'}

def unicode_path_ok(path):
    if not isinstance(path, str):
        return False
    try:
        path.encode('utf-8', errors='strict')
    except UnicodeEncodeError:
        return False
    return unicodedata.normalize('NFC', path) == path

def audit_inventory(groups, current_paths):
    try:
        if isinstance(groups, list):
            for group in groups:
                if isinstance(group, dict) and isinstance(group.get('files'), list):
                    for row in group['files']:
                        if isinstance(row, dict) and 'path' in row and not unicode_path_ok(row['path']):
                            return fail('manifest_unicode_path_invalid')
        if isinstance(current_paths, list) and any(not unicode_path_ok(p) for p in current_paths):
            return fail('current_unicode_path_invalid')
        source = Path(__file__).with_name(ORIGINAL)
        original_bytes = source.read_bytes()
        if hashlib.sha256(original_bytes).hexdigest() != ORIGINAL_SHA256:
            return fail('original_guard_hash_mismatch')
        spec = importlib.util.spec_from_file_location('run142_pinned_guard', source)
        if spec is None or spec.loader is None:
            return fail('original_guard_not_loadable')
        guard = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(guard)
        return guard.audit_inventory(groups, current_paths)
    except (OSError, ValueError, TypeError, UnicodeError, ImportError, AttributeError):
        return fail('preflight_or_guard_exception')
