#!/usr/bin/env python3
"""C1-only path-display spoofing preflight, composed over frozen Run146.

Rejects Unicode control/line-separator characters and bidi direction controls
in manifest and current-snapshot paths. Does not certify Git portability,
authenticate source bytes, authorize merge, or alter the Run146 predecessor.
"""
import hashlib
import importlib.util
import unicodedata
from pathlib import Path

PREDECESSOR = 'alpha_pr124_unicode_path_preflight_adapter_v1_20261025.py'
PREDECESSOR_SHA256 = '0742097b6d88013921d9074a1114b6382d5b0bce9a300115fd98a0ec8be67823'
BIDI_CONTROLS = frozenset('\u061c\u200e\u200f\u202a\u202b\u202c\u202d\u202e\u2066\u2067\u2068\u2069')
DENIED_CATEGORIES = frozenset(('Cc', 'Zl', 'Zp'))

def fail(reason):
    return {'status': 'FAIL_CLOSED', 'reason': reason,
            'source_authentication': 'NOT_ESTABLISHED',
            'project_automation_rate': 'NOT_COMPUTABLE',
            'claim_ceiling': 'C1_DESCRIPTIVE_ONLY'}

def display_path_ok(path):
    if not isinstance(path, str):
        return False
    return all(c not in BIDI_CONTROLS and
               unicodedata.category(c) not in DENIED_CATEGORIES for c in path)

def audit_inventory(groups, current_paths):
    try:
        if isinstance(groups, list):
            for group in groups:
                if isinstance(group, dict) and isinstance(group.get('files'), list):
                    for row in group['files']:
                        if isinstance(row, dict) and 'path' in row and not display_path_ok(row['path']):
                            return fail('manifest_display_control_path_invalid')
        if isinstance(current_paths, list) and any(not display_path_ok(p) for p in current_paths):
            return fail('current_display_control_path_invalid')
        source = Path(__file__).with_name(PREDECESSOR)
        if hashlib.sha256(source.read_bytes()).hexdigest() != PREDECESSOR_SHA256:
            return fail('predecessor_hash_mismatch')
        spec = importlib.util.spec_from_file_location('run146_pinned_adapter', source)
        if spec is None or spec.loader is None:
            return fail('predecessor_not_loadable')
        predecessor = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(predecessor)
        return predecessor.audit_inventory(groups, current_paths)
    except (OSError, ValueError, TypeError, UnicodeError, ImportError, AttributeError):
        return fail('preflight_or_predecessor_exception')
