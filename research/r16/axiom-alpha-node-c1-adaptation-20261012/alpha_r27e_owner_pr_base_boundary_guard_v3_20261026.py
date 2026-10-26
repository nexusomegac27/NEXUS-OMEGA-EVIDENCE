#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Isolated C1 research: bind both PR base and head at pagination boundaries.

This read-only adapter is NOT the trusted R27-E CI validator. A stable base/head
pair at two boundaries is NOT an atomic GitHub diff snapshot. The caller remains
responsible for API provenance, authenticated actor, changed_files metadata,
structure checks, return slots, content bytes, and GitHub branch protections.
"""
import hashlib
import importlib.util
import re
from pathlib import Path

V2_NAME = 'alpha_r27e_owner_pr_head_boundary_guard_v2_20261026.py'
V2_SHA256 = 'f9c424f633fdecf3a5ec0e4a818049f350ba3e6929b8bd548f2325ef337c29f1'
SHA = re.compile(r'^[0-9a-f]{40}$')


def enumerate_pr_files_with_base_head_recheck(*, fetch_page, fetch_head,
        fetch_base, actor, owner, external_allowlist, expected_count,
        expected_head_sha, expected_base_sha, max_external_files=7):
    if not callable(fetch_base):
        raise ValueError('BASE_READBACK_REQUIRED')
    if not isinstance(expected_base_sha, str) or not SHA.fullmatch(expected_base_sha):
        raise ValueError('INVALID_PINNED_BASE_SHA')
    base_before = fetch_base()
    if not isinstance(base_before, str) or base_before != expected_base_sha:
        raise ValueError('BASE_DRIFT_BEFORE_PAGINATION')
    path = Path(__file__).with_name(V2_NAME)
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise ValueError('PINNED_V2_SOURCE_NOT_PRESENT') from exc
    if hashlib.sha256(raw).hexdigest() != V2_SHA256:
        raise ValueError('PINNED_V2_SOURCE_MISMATCH')
    spec = importlib.util.spec_from_file_location('r27e_pinned_v2', path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    result = mod.enumerate_pr_files_with_boundary_recheck(
        fetch_page=fetch_page, fetch_head=fetch_head, actor=actor, owner=owner,
        external_allowlist=external_allowlist, expected_count=expected_count,
        expected_head_sha=expected_head_sha, max_external_files=max_external_files)
    base_after = fetch_base()
    if not isinstance(base_after, str) or base_after != expected_base_sha:
        raise ValueError('BASE_DRIFT_AFTER_PAGINATION')
    return {**result, 'status': 'BASE_HEAD_BOUNDARIES_CONSISTENT_NOT_ATOMIC',
            'base_before': base_before, 'base_after': base_after,
            'atomic_snapshot': 'NOT_ESTABLISHED',
            'base_authentication': 'CALLER_RESPONSIBILITY'}
