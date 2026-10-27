#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Isolated read-only R27-E V2: detect head drift across PR file pagination.
Two head reads are NOT an atomic GitHub snapshot or authenticated actor proof.
Trusted CI validator, branch protections and external slots remain unchanged.
"""
import hashlib
import importlib.util
from pathlib import Path

V1_NAME = 'alpha_r27e_owner_pr_pagination_candidate_v1_20261026.py'
V1_SHA256 = '3d44ca5d228b205995f9ba05dae9073dc97db3ecc496a90da8b72253fbe3f586'


def enumerate_pr_files_with_boundary_recheck(*, fetch_page, fetch_head, actor,
        owner, external_allowlist, expected_count, expected_head_sha,
        max_external_files=7):
    if not callable(fetch_head):
        raise ValueError('HEAD_READBACK_REQUIRED')
    before = fetch_head()
    if not isinstance(before, str) or before != expected_head_sha:
        raise ValueError('HEAD_DRIFT_BEFORE_PAGINATION')
    path = Path(__file__).with_name(V1_NAME)
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise ValueError('PINNED_V1_SOURCE_NOT_PRESENT') from exc
    if hashlib.sha256(raw).hexdigest() != V1_SHA256:
        raise ValueError('PINNED_V1_SOURCE_MISMATCH')
    spec = importlib.util.spec_from_file_location('r27e_pinned_v1', path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    files = mod.enumerate_pr_files(fetch_page=fetch_page, actor=actor, owner=owner,
        external_allowlist=external_allowlist, expected_count=expected_count,
        expected_head_sha=expected_head_sha, observed_head_sha=before,
        max_external_files=max_external_files)
    after = fetch_head()
    if not isinstance(after, str) or after != expected_head_sha:
        raise ValueError('HEAD_DRIFT_AFTER_PAGINATION')
    return {'status': 'BOUNDARY_CONSISTENT_NOT_ATOMIC', 'files': files,
            'head_before': before, 'head_after': after,
            'atomic_snapshot': 'NOT_ESTABLISHED',
            'github_authentication': 'CALLER_RESPONSIBILITY'}
