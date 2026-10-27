#!/usr/bin/env python3
"""Isolated C1 research candidate: no-follow, descriptor-relative Git worktree read.

Linux/POSIX-only prototype; does not modify the live repository steward.
A missing O_NOFOLLOW or dir_fd implementation fails closed. Not a GitHub
identity/authentication check or a guarantee against arbitrary local races.
"""
import os
import stat
from pathlib import Path

MAX_READ = 4 * 1024 * 1024


def read_tracked(root, relative, max_bytes=MAX_READ):
    if (type(relative) is not str or not relative or relative.startswith("/") or
            "\\" in relative or any(p in ("", ".", "..") for p in relative.split("/"))):
        raise ValueError("INVALID_RELATIVE_PATH")
    if type(max_bytes) is not int or max_bytes < 0:
        raise ValueError("INVALID_MAX_BYTES")
    if (not hasattr(os, "O_NOFOLLOW") or not hasattr(os, "O_DIRECTORY") or
            os.open not in os.supports_dir_fd):
        raise OSError("NOFOLLOW_DIRFD_UNAVAILABLE")
    directory_flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
    file_flags = os.O_RDONLY | os.O_NOFOLLOW
    root_fd = os.open(Path(root), directory_flags)
    fd = root_fd
    try:
        parts = relative.split("/")
        for part in parts[:-1]:
            next_fd = os.open(part, directory_flags, dir_fd=fd)
            if fd != root_fd:
                os.close(fd)
            fd = next_fd
        file_fd = os.open(parts[-1], file_flags, dir_fd=fd)
        try:
            info = os.fstat(file_fd)
            if not stat.S_ISREG(info.st_mode):
                raise ValueError("NOT_REGULAR_FILE")
            if info.st_size > max_bytes:
                raise ValueError("FILE_TOO_LARGE")
            with os.fdopen(os.dup(file_fd), "rb") as f:
                data = f.read(max_bytes + 1)
            if len(data) > max_bytes:
                raise ValueError("FILE_TOO_LARGE")
            return data
        finally:
            os.close(file_fd)
    finally:
        if fd != root_fd:
            os.close(fd)
        os.close(root_fd)
