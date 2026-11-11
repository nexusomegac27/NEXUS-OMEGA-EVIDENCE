#!/usr/bin/env python3
"""C1 research-only V3: reject scalar-type confusion in PR preflight.

Append-only successor to V2; V1/V2 remain immutable dependencies. This
syntactic check does not authenticate GitHub metadata, authorize publication,
or change an independent evaluator. The caller must pin dependency bytes,
source identity, branch head, privacy, license, CI and post-write readback.
"""
from alpha_pr_publication_preflight_guard_v2_20261023 import check_pr_publication_preflight as _v2


def check_pr_publication_preflight(snapshot, now_utc):
    """Fail closed when permission or PR identity scalars have wrong JSON types."""
    if not isinstance(snapshot, dict):
        return _v2(snapshot, now_utc)
    repo, pr, target = (snapshot.get(k) for k in ('repo', 'pr', 'target'))
    if not all(isinstance(x, dict) for x in (repo, pr, target)):
        return _v2(snapshot, now_utc)
    permissions = repo.get('permissions')
    if isinstance(permissions, dict) and 'push' in permissions:
        if permissions['push'] is not True:
            return {'status': 'ACTOR_SCOPE_HOLD'}
    if 'number' in pr and type(pr['number']) is not int:
        return {'status': 'PR_STATE_HOLD'}
    if 'pr_number' in target and type(target['pr_number']) is not int:
        return {'status': 'PR_STATE_HOLD'}
    return _v2(snapshot, now_utc)
