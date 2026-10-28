#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Research-only source-exact, non-destructive steward patch constructor.

The production script is never changed. The returned source is executable only
in a disposable synthetic Git checkout, under the frozen independent evaluator.
Linux/POSIX dirfd O_NOFOLLOW semantics only; no Windows portability claim.
"""
from __future__ import annotations
import hashlib

PINNED_SOURCE_SHA256 = '94051a46bc8968e05579410fb607393d07907fd499c4e397d11c611be52d7998'
IMPORT_ANCHOR = 'ROOT_SPECIAL = frozenset('
READ_ANCHOR = '''            content = actual.read_bytes()
            if len(content) != declared_bytes:
                faults.append("GIT_TREE_BYTE_COUNT_MISMATCH")
            computed_oid = hashlib.sha1(b"blob " + str(len(content)).encode("ascii") + b"\\0" + content).hexdigest()
            if computed_oid != oid:
                faults.append("WORKTREE_GIT_BLOB_MISMATCH")'''

SAFE_READ = '''import os
import stat


def _read_confined_regular_file(root, parts):
    """No-follow every directory and leaf; reject unsupported platforms closed."""
    if not hasattr(os, "O_NOFOLLOW") or not hasattr(os, "O_DIRECTORY"):
        raise OSError("NOFOLLOW_NOT_SUPPORTED")
    fd = os.open(root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        for component in parts[:-1]:
            next_fd = os.open(component, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                              dir_fd=fd)
            os.close(fd)
            fd = next_fd
        leaf_fd = os.open(parts[-1], os.O_RDONLY | os.O_NOFOLLOW, dir_fd=fd)
        try:
            if not stat.S_ISREG(os.fstat(leaf_fd).st_mode):
                raise OSError("NOT_REGULAR_FILE")
            with os.fdopen(leaf_fd, "rb", closefd=False) as stream:
                return stream.read()
        finally:
            os.close(leaf_fd)
    finally:
        os.close(fd)


'''

REPLACEMENT = '''            try:
                content = _read_confined_regular_file(root, parts)
            except (OSError, ValueError):
                faults.append("UNSAFE_PATH_COMPONENT")
            if content is not None:
                if len(content) != declared_bytes:
                    faults.append("GIT_TREE_BYTE_COUNT_MISMATCH")
                computed_oid = hashlib.sha1(b"blob " + str(len(content)).encode("ascii") + b"\\0" + content).hexdigest()
                if computed_oid != oid:
                    faults.append("WORKTREE_GIT_BLOB_MISMATCH")'''


def patch_steward_source(source: str) -> str:
    """Refuse any source drift; patch only the original leaf read block."""
    if hashlib.sha256(source.encode('utf-8')).hexdigest() != PINNED_SOURCE_SHA256:
        raise ValueError('PINNED_STEWARD_SOURCE_DRIFT')
    if source.count(IMPORT_ANCHOR) != 1 or source.count(READ_ANCHOR) != 1:
        raise ValueError('SOURCE_ANCHOR_AMBIGUOUS')
    return source.replace(IMPORT_ANCHOR, SAFE_READ + IMPORT_ANCHOR, 1).replace(
        READ_ANCHOR, REPLACEMENT, 1)
