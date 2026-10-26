#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Isolated R27-E read-only pagination research candidate, NOT a CI validator.
Caller must independently authenticate GitHub actor, pin head SHA and obtain
changed_files from GitHub metadata. Existing validate_paths/manifest checks remain mandatory.
No write capability or owner authorization is granted by this function.
"""
import re

SHA = re.compile(r'^[0-9a-f]{40}$')
VALID_STATUS = frozenset(('added', 'modified', 'removed', 'renamed', 'copied', 'changed'))


def enumerate_pr_files(*, fetch_page, actor, owner, external_allowlist,
                       expected_count, expected_head_sha, observed_head_sha,
                       max_external_files=7):
    if type(expected_count) is not int or not (1 <= expected_count < 3000):
        raise ValueError('INVALID_OR_UNVERIFIABLE_EXPECTED_COUNT')
    if (not isinstance(expected_head_sha, str) or not SHA.fullmatch(expected_head_sha)
            or observed_head_sha != expected_head_sha):
        raise ValueError('UNPINNED_OR_DRIFTED_PR_HEAD')
    if not isinstance(actor, str) or not actor or not isinstance(owner, str) or not owner:
        raise ValueError('INVALID_ACTOR_METADATA')
    if actor != owner:
        if actor not in external_allowlist:
            raise ValueError('UNREGISTERED_EXTERNAL_GITHUB_ACTOR')
        if expected_count > max_external_files:
            raise ValueError('EXTERNAL_FILE_COUNT_CAP_EXCEEDED')
    out, seen = [], set()
    for page in range(1, 32):
        batch = fetch_page(page)
        if not isinstance(batch, list) or len(batch) > 100:
            raise ValueError('INVALID_PR_FILE_RESPONSE')
        for item in batch:
            if not isinstance(item, dict):
                raise ValueError('INVALID_PR_FILE_RECORD')
            name, status = item.get('filename'), item.get('status')
            if not isinstance(name, str) or not name or status not in VALID_STATUS:
                raise ValueError('INVALID_PR_FILE_RECORD')
            if name in seen:
                raise ValueError('DUPLICATE_PR_FILE_PATH')
            seen.add(name)
            out.append(item)
        if len(out) > expected_count:
            raise ValueError('PR_FILE_COUNT_EXCEEDS_PINNED_METADATA')
        if len(batch) < 100:
            if len(out) != expected_count:
                raise ValueError('INCOMPLETE_PR_FILE_CENSUS')
            return out
    raise ValueError('PR_FILE_PAGINATION_LIMIT_UNVERIFIABLE')
