#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""C1 research-only Git tree/worktree executable-bit consistency witness.

No production steward modification, no writes, no source read, no platform
portability assertion. POSIX only; caller supplies Git-tree entries.
"""
from __future__ import annotations
import os
import stat
from pathlib import Path


def check(root: Path, entries: list[tuple]) -> list[dict]:
    if os.name != 'posix':
        raise RuntimeError('POSIX_EXEC_MODE_ONLY')
    findings = []
    for path, mode, kind, oid, size in entries:
        if kind != 'blob' or mode not in ('100644', '100755'):
            continue
        parts = path.split('/')
        if any(not p or p in ('.', '..') for p in parts):
            findings.append({'path': path, 'code': 'UNSAFE_COMPONENT_NOT_ASSESSED'})
            continue
        current = Path(root)
        unsafe = False
        try:
            for component in parts[:-1]:
                current = current / component
                info = current.lstat()
                if not stat.S_ISDIR(info.st_mode):
                    unsafe = True
                    break
            if not unsafe:
                current = current / parts[-1]
                info = current.lstat()
                if not stat.S_ISREG(info.st_mode):
                    unsafe = True
        except OSError:
            unsafe = True
        if unsafe:
            findings.append({'path': path, 'code': 'UNSAFE_COMPONENT_NOT_ASSESSED'})
            continue
        observed_exec = bool(info.st_mode & 0o111)
        expected_exec = mode == '100755'
        if observed_exec != expected_exec:
            findings.append({'path': path, 'code': 'GIT_WORKTREE_EXEC_MODE_MISMATCH',
                             'git_mode': mode, 'worktree_executable': observed_exec})
    return findings
