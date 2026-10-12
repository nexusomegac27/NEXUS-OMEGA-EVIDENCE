#!/usr/bin/env python3
"""NEXUS GitHub Implant public-safe static mirror, offline from an existing Git checkout.
SPDX-License-Identifier: MIT. C1_DESCRIPTIVE_ONLY.
This program never pushes, deploys, creates credentials, or edits its source repository.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

FORBIDDEN_NAMES = {".env", ".env.local", ".npmrc", ".pypirc", "id_rsa", "id_ed25519", "credentials.json"}
SECRET_PATTERNS = (
    re.compile(rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(rb"(?i)\b(?:github_pat_|ghp_|gho_|ghu_|ghs_|ghr_)[A-Za-z0-9_]{12,}"),
    re.compile(rb"\bsk-(?:proj-)?[A-Za-z0-9_-]{18,}"),
)
# This filter is conservative: manual review can produce a new sanitized derivative.
PATH_PRIVATE_RE = re.compile(r"(?i)(?:^|/)(?:\.git|node_modules|__pycache__)(?:/|$)")
BYTES_LIMIT = 5 * 1024 * 1024
TOTAL_LIMIT = 120 * 1024 * 1024

def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def git(root: Path, *args: str) -> bytes:
    return subprocess.check_output(["git", "-C", str(root), *args], stderr=subprocess.DEVNULL)

def build(source: Path, output: Path) -> dict:
    source = source.resolve()
    output = output.resolve()
    if not (source / ".git").exists():
        # A normal checked-out worktree is required, not a guessed source directory.
        raise ValueError("source must be a normal Git checkout with .git")
    if output == source or source in output.parents or output in source.parents:
        raise ValueError("output must be entirely outside the source checkout")
    if git(source, "status", "--porcelain", "--untracked-files=no").strip():
        raise ValueError("refusing dirty tracked working tree")
    commit = git(source, "rev-parse", "HEAD").decode().strip()
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise ValueError("invalid Git commit ID")
    paths = sorted([p.decode("utf-8", "surrogateescape") for p in git(source, "ls-files", "-z").split(b"\0") if p])
    records, excluded = [], []
    count = 0
    with tempfile.TemporaryDirectory(prefix="nexus-implant-") as td:
        temp = Path(td)
        for name in paths:
            rel = Path(name)
            if rel.is_absolute() or ".." in rel.parts or PATH_PRIVATE_RE.search(name):
                excluded.append({"path": name, "reason": "UNSAFE_PATH"}); continue
            path = source / rel
            if any(part in FORBIDDEN_NAMES for part in rel.parts) or path.is_symlink() or not path.is_file():
                excluded.append({"path": name, "reason": "BLOCKED_FILE_CLASS"}); continue
            n = path.stat().st_size
            if n > BYTES_LIMIT or count + n > TOTAL_LIMIT:
                excluded.append({"path": name, "reason": "MIRROR_SIZE_LIMIT"}); continue
            data = path.read_bytes()
            if any(p.search(data) for p in SECRET_PATTERNS):
                excluded.append({"path": name, "reason": "SECRET_SCAN_HOLD"}); continue
            if b"\0" not in data[:1000] and re.search(rb"(?i)(?:C:\\\\Users\\\\|/home/[^/\s]+/\.ssh/)", data):
                excluded.append({"path": name, "reason": "PRIVATE_PATH_REVIEW"}); continue
            destination = temp / rel
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(data)
            if sha(destination.read_bytes()) != sha(data):
                raise ValueError("post-write hash mismatch: " + name)
            records.append({"path": rel.as_posix(), "bytes": len(data), "sha256": sha(data)})
            count += len(data)
        manifest = {
            "object": "NEXUS_OMEGA_FORUM_GITHUB_IMPLANT_PUBLIC_SAFE_MIRROR_V1",
            "claim_ceiling": "C1_DESCRIPTIVE_ONLY",
            "source_repository": "nexusomegac27/NEXUS-OMEGA-EVIDENCE",
            "source_commit": commit,
            "mirror_class": "PUBLIC_SAFE_FILTERED_NOT_ALL_GITHUB_BYTES",
            "file_count": len(records),
            "bytes_total": count,
            "files": records,
            "excluded": excluded,
            "source_git_tracked_count": len(paths),
            "complete_unfiltered_mirror": len(excluded) == 0,
        }
        blob = (json.dumps(manifest, indent=2, ensure_ascii=False, sort_keys=True) + "\n").encode("utf-8")
        (temp / "manifest.json").write_bytes(blob)
        if output.exists():
            raise FileExistsError("refusing overwrite: " + str(output))
        output.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(temp, output)
    return {"source_commit":commit,"files":len(records),"excluded":len(excluded),"manifest_sha256":sha(blob),"output":str(output)}

def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--source", type=Path, required=True, help="existing clean Git worktree")
    p.add_argument("--output", type=Path, required=True, help="new outside-tree staging location")
    args = p.parse_args()
    try:
        print(json.dumps(build(args.source, args.output), sort_keys=True))
        return 0
    except (ValueError, FileExistsError, OSError, subprocess.CalledProcessError) as exc:
        print("HOLD_SCOPED_MIRROR: " + str(exc), file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
