#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""C1 research-only POSIX postpublication byte+inode readback witness.

The final path is checked after directory fsync, including the inode identity
captured before link publication. Synthetic tampering is detected, not prevented.
No race-freedom, crash durability, Windows support or production fix is claimed.
"""
from __future__ import annotations
import hashlib
import importlib.util
import os
from pathlib import Path
import secrets
import stat

BASE_NAME = "steward_output_postpublish_status_candidate_v3_20261028.py"
BASE_SHA256 = "847c3bd775b195f30617174904af6644ab1d13dd30725a9f44e40fe797423578"


class PublishedDurabilityUncertain(OSError):
    """Published bytes and inode read back; directory durability is unknown."""


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
    hold_fd = None
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
            hold_fd = os.dup(stream.fileno())  # prevent inode reuse after unlink/swap
            published_stat = os.fstat(hold_fd)
        os.link(temp_name, destination.name, src_dir_fd=fd, dst_dir_fd=fd,
                follow_symlinks=False)
        os.unlink(temp_name, dir_fd=fd)
        temp_name = None
        dir_error = None
        try:
            os.fsync(fd)
        except OSError as exc:
            dir_error = exc
        suffix = "DURABILITY_UNKNOWN" if dir_error else "NO_SUCCESS"
        try:
            verify_fd = os.open(destination.name, os.O_RDONLY | os.O_NOFOLLOW,
                                dir_fd=fd)
            with os.fdopen(verify_fd, "rb") as stream:
                observed_stat = os.fstat(stream.fileno())
                observed = stream.read()
                final_stat = os.fstat(stream.fileno())
        except OSError as exc:
            raise OSError(f"PUBLISHED_READBACK_GAP_{suffix}") from exc
        if (not stat.S_ISREG(observed_stat.st_mode) or
            (observed_stat.st_dev, observed_stat.st_ino) !=
            (published_stat.st_dev, published_stat.st_ino) or
            (final_stat.st_dev, final_stat.st_ino) !=
            (published_stat.st_dev, published_stat.st_ino)):
            raise OSError(f"PUBLISHED_INODE_MISMATCH_{suffix}")
        if observed != content:
            raise OSError(f"PUBLISHED_READBACK_MISMATCH_{suffix}")
        if dir_error is not None:
            raise PublishedDurabilityUncertain(
                "PUBLISHED_READBACK_MATCH_DURABILITY_UNKNOWN "
                f"bytes={len(observed)} sha256={hashlib.sha256(observed).hexdigest()}"
            ) from dir_error
    finally:
        if temp_name is not None:
            try:
                os.unlink(temp_name, dir_fd=fd)
            except FileNotFoundError:
                pass
        if hold_fd is not None:
            os.close(hold_fd)
        os.close(fd)


def main() -> int:
    base_path = Path(__file__).with_name(BASE_NAME)
    if hashlib.sha256(base_path.read_bytes()).hexdigest() != BASE_SHA256:
        raise ValueError("PINNED_POSTPUBLISH_BASE_MISMATCH")
    spec = importlib.util.spec_from_file_location("pinned_postpublish_guard_v3", base_path)
    if spec is None or spec.loader is None:
        raise ValueError("BASE_GUARD_LOAD_FAILED")
    base = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(base)
    base.guarded_write = guarded_write
    return base.main()


if __name__ == "__main__":
    raise SystemExit(main())
