#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Isolated POSIX C1 Steward inventory output guard; NOT production integration.

Reuses pinned original Steward audit, but writes a new JSONL only outside the
checkout via O_EXCL and directory-fd O_NOFOLLOW traversal. No mkdir/overwrite.
Unsupported platforms fail closed. Does not establish safety against bind mounts,
concurrent privileged directory replacement, or unrelated callers.
"""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys

SOURCE_SHA256 = "94051a46bc8968e05579410fb607393d07907fd499c4e397d11c611be52d7998"


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
    # Walk each parent with O_NOFOLLOW: a symlink parent cannot redirect writes.
    fd = os.open(os.sep, os.O_RDONLY | os.O_DIRECTORY)
    try:
        for component in destination.parent.parts[1:]:
            if component in ("", os.sep):
                continue
            next_fd = os.open(component, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                              dir_fd=fd)
            os.close(fd)
            fd = next_fd
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW
        file_fd = os.open(destination.name, flags, 0o600, dir_fd=fd)
        with os.fdopen(file_fd, "wb") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
    finally:
        os.close(fd)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True, type=Path)
    ap.add_argument("--output", required=True, type=Path)
    args = ap.parse_args()
    try:
        root = args.root.resolve(strict=True)
        source_path = root / "scripts" / "nexus_repository_steward.py"
        source = source_path.read_bytes()
        if hashlib.sha256(source).hexdigest() != SOURCE_SHA256:
            raise ValueError("PINNED_STEWARD_SOURCE_MISMATCH")
        spec = importlib.util.spec_from_file_location("pinned_steward", source_path)
        if spec is None or spec.loader is None:
            raise ValueError("PINNED_STEWARD_LOAD_FAILED")
        steward = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(steward)
        contract = json.loads((root / "docs/architecture/REPOSITORY_STRUCTURE.json").read_text("utf-8"))
        commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root).decode("ascii").strip()
        entries = steward.parse_ls_tree(subprocess.check_output(
            ["git", "ls-tree", "-r", "-l", "-z", "HEAD"], cwd=root))
        report = steward.audit(root, entries, contract, commit)
        payload = "".join(json.dumps(row, sort_keys=True, ensure_ascii=True) + "\n"
                          for row in report["files"]).encode("utf-8")
        guarded_write(root, args.output, payload)
        print(json.dumps({k: v for k, v in report.items() if k != "files"}, sort_keys=True))
        return 0
    except (OSError, ValueError, KeyError, subprocess.CalledProcessError) as exc:
        print("HOLD_SCOPED_OUTPUT: " + str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
