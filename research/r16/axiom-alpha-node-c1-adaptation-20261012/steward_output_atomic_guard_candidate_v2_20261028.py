#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""C1 research-only atomic/no-replace output guard; POSIX, not production.

Builds on the immutable v1 output guard, with an exclusive temporary file and
atomic hard-link publication. A failed write leaves no *final* inventory path;
crashes can leave orphan temporary files. No protection from privileged mount
replacement or cross-platform claims is made.
"""
from __future__ import annotations
import hashlib
import importlib.util
import os
from pathlib import Path
import secrets

BASE_NAME = "steward_output_guard_candidate_v1_20261028.py"
BASE_SHA256 = "0640f1c23c236880fed6400319bfacf523442fd103b4f1ebafeeb85daa2dfd74"


def guarded_write(root: Path, destination: Path, content: bytes) -> None:
    if not (hasattr(os, "O_NOFOLLOW") and hasattr(os, "O_DIRECTORY")):
        raise ValueError("UNSUPPORTED_PLATFORM_FAIL_CLOSED")
    if not destination.is_absolute() or any(p in (".", "..") for p in destination.parts):
        raise ValueError("OUTPUT_MUST_BE_ABSOLUTE_WITHOUT_TRAVERSAL")
    if destination.name in ("", ".", ".."):
        raise ValueError("INVALID_OUTPUT_NAME")
    root_real = root.resolve(strict=True)
    parent_real = destination.parent.resolve(strict=True)
    if os.path.commonpath([str(root_real), str(parent_real)]) == str(root_real):
        raise ValueError("OUTPUT_INSIDE_CHECKOUT_DENIED")
    fd = os.open(os.sep, os.O_RDONLY | os.O_DIRECTORY)
    temp_name = None
    try:
        for component in destination.parent.parts[1:]:
            if component in ("", os.sep):
                continue
            next_fd = os.open(component, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                              dir_fd=fd)
            os.close(fd)
            fd = next_fd
        temp_name = ".nexus-alpha-atomic-" + secrets.token_hex(16) + ".tmp"
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW
        temp_fd = os.open(temp_name, flags, 0o600, dir_fd=fd)
        with os.fdopen(temp_fd, "wb") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        # link() fails with EEXIST, including a symlink leaf; no rename overwrite.
        os.link(temp_name, destination.name, src_dir_fd=fd, dst_dir_fd=fd,
                follow_symlinks=False)
        os.unlink(temp_name, dir_fd=fd)
        temp_name = None
        os.fsync(fd)
    finally:
        if temp_name is not None:
            try:
                os.unlink(temp_name, dir_fd=fd)
            except FileNotFoundError:
                pass
        os.close(fd)


def main() -> int:
    base_path = Path(__file__).with_name(BASE_NAME)
    if hashlib.sha256(base_path.read_bytes()).hexdigest() != BASE_SHA256:
        raise ValueError("PINNED_BASE_GUARD_MISMATCH")
    spec = importlib.util.spec_from_file_location("pinned_output_guard_v1", base_path)
    if spec is None or spec.loader is None:
        raise ValueError("BASE_GUARD_LOAD_FAILED")
    base = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(base)
    base.guarded_write = guarded_write
    return base.main()


if __name__ == "__main__":
    raise SystemExit(main())
