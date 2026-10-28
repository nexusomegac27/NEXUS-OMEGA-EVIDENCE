#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Research-only constructor for a POSIX executable-mode full-CLI patch.

Source-exact additive candidate. Never changes the productive Steward or Git
checkout. Does not fix symlink-parent aliasing, races or Windows portability.
"""
from __future__ import annotations
import hashlib

PINNED_SOURCE_SHA256 = '94051a46bc8968e05579410fb607393d07907fd499c4e397d11c611be52d7998'
ANCHOR = '''            if computed_oid != oid:
                faults.append("WORKTREE_GIT_BLOB_MISMATCH")'''
REPLACEMENT = '''            if computed_oid != oid:
                faults.append("WORKTREE_GIT_BLOB_MISMATCH")
            if mode in ("100644", "100755"):
                expected_exec = mode == "100755"
                observed_exec = bool(actual.stat().st_mode & 0o111)
                if observed_exec != expected_exec:
                    faults.append("GIT_WORKTREE_EXEC_MODE_MISMATCH")'''


def patch_steward_source(source: str) -> str:
    if hashlib.sha256(source.encode('utf-8')).hexdigest() != PINNED_SOURCE_SHA256:
        raise ValueError('PINNED_SOURCE_DRIFT')
    if source.count(ANCHOR) != 1:
        raise ValueError('ANCHOR_AMBIGUOUS')
    return source.replace(ANCHOR, REPLACEMENT, 1)
