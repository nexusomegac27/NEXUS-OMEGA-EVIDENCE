#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Frozen independent black-box oracle for a POSIX post-publication fsync error.

Loads baseline/candidate as independent subprocesses; asserts externally visible
exception class/status, final bytes, cleanup, and safety controls. Does not
import candidate code or rely on its implementation-specific exception class.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

BASELINE_SHA256 = "441bffe0285183605b8d76d9f4d542ebf06f8e63e4f8cc92112550bc4df93841"
PAYLOAD = b"NEXUS_POSTPUBLISH_FSYNC_C1_FIXTURE\n" * 101

CHILD = r'''
import errno, hashlib, importlib.util, json, os, stat, sys
from pathlib import Path
module_path, root_path, target_path, mode = sys.argv[1:]
spec = importlib.util.spec_from_file_location("isolated_module", module_path)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
original_fsync = os.fsync
def fault(fd):
    is_dir = stat.S_ISDIR(os.fstat(fd).st_mode)
    if (mode == "dir-fsync" and is_dir) or (mode == "file-fsync" and not is_dir):
        raise OSError(errno.EIO, "SYNTHETIC_FSYNC_EIO")
    return original_fsync(fd)
if mode in ("dir-fsync", "file-fsync"):
    os.fsync = fault
payload = b"NEXUS_POSTPUBLISH_FSYNC_C1_FIXTURE\n" * 101
exc_type = None
exc_text = None
try:
    mod.guarded_write(Path(root_path), Path(target_path), payload)
except Exception as exc:
    exc_type = type(exc).__name__
    exc_text = str(exc)
finally:
    os.fsync = original_fsync
p = Path(target_path)
exists = p.is_file()
data = p.read_bytes() if exists else b""
print(json.dumps({
    "exception": exc_type,
    "message": exc_text,
    "exists": exists,
    "bytes": len(data) if exists else None,
    "sha256": hashlib.sha256(data).hexdigest() if exists else None,
    "temps": sorted(x.name for x in p.parent.glob(".nexus-alpha-atomic-*.tmp"))
}, sort_keys=True))
'''


def run(module: Path, root: Path, target: Path, mode: str) -> dict:
    p = subprocess.run([sys.executable, "-c", CHILD, str(module), str(root), str(target), mode],
                       capture_output=True, text=True, timeout=20)
    if p.returncode != 0:
        return {"child_failure": p.stderr[-400:], "returncode": p.returncode}
    return json.loads(p.stdout)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseline", type=Path, required=True)
    parser.add_argument("--candidate", type=Path)
    args = parser.parse_args()
    if hashlib.sha256(args.baseline.read_bytes()).hexdigest() != BASELINE_SHA256:
        raise SystemExit("BASELINE_SHA256_MISMATCH_FAIL_CLOSED")
    tests = []
    def check(name: str, condition: bool):
        tests.append({"name": name, "pass": bool(condition)})
    expected_hash = hashlib.sha256(PAYLOAD).hexdigest()
    with tempfile.TemporaryDirectory(prefix="nexus-postpublish-eval-") as tmp:
        work = Path(tmp)
        root = work / "checkout"
        root.mkdir()
        out = work / "external"
        out.mkdir()
        old = run(args.baseline, root, out / "baseline-dir.jsonl", "dir-fsync")
        check("baseline_dir_fsync_reports_exception", old.get("exception") == "OSError")
        check("baseline_dir_fsync_final_exists_complete", old.get("exists") and old.get("sha256") == expected_hash)
        check("baseline_dir_fsync_no_explicit_published_uncertain_marker", "PUBLISHED_READBACK_MATCH_DURABILITY_UNKNOWN" not in (old.get("message") or ""))
        if args.candidate:
            new = run(args.candidate, root, out / "candidate-dir.jsonl", "dir-fsync")
            check("candidate_dir_fsync_never_silent_success", bool(new.get("exception")))
            check("candidate_dir_fsync_explicit_distinct_exception", new.get("exception") == "PublishedDurabilityUncertain")
            check("candidate_dir_fsync_explicit_uncertain_marker", "PUBLISHED_READBACK_MATCH_DURABILITY_UNKNOWN" in (new.get("message") or ""))
            check("candidate_dir_fsync_preserves_complete_final_bytes", new.get("exists") and new.get("sha256") == expected_hash and new.get("bytes") == len(PAYLOAD))
            check("candidate_dir_fsync_message_binds_sha_and_size", expected_hash in (new.get("message") or "") and str(len(PAYLOAD)) in (new.get("message") or ""))
            check("candidate_dir_fsync_cleans_temp", not new.get("temps"))
            good = run(args.candidate, root, out / "candidate-success.jsonl", "normal")
            check("candidate_positive_control", good.get("exception") is None and good.get("sha256") == expected_hash)
            file_fail = run(args.candidate, root, out / "candidate-file.jsonl", "file-fsync")
            check("candidate_prepublication_fsync_failure_not_published", file_fail.get("exception") and not file_fail.get("exists"))
            check("candidate_prepublication_failure_no_published_marker", "PUBLISHED_READBACK_MATCH_DURABILITY_UNKNOWN" not in (file_fail.get("message") or ""))
            check("candidate_prepublication_temp_cleanup", not file_fail.get("temps"))
            existing = out / "existing.jsonl"
            existing.write_bytes(b"IMMUTABLE_ORIGINAL\n")
            no_replace = run(args.candidate, root, existing, "normal")
            check("candidate_refuses_existing_destination", no_replace.get("exception") and existing.read_bytes() == b"IMMUTABLE_ORIGINAL\n")
            internal = root / "README.md"
            internal.write_bytes(b"IMMUTABLE_ROOT\n")
            blocked = run(args.candidate, root, internal, "normal")
            check("candidate_refuses_checkout_write", blocked.get("exception") and internal.read_bytes() == b"IMMUTABLE_ROOT\n")
            linked = work / "linked"
            linked.symlink_to(out, target_is_directory=True)
            symlink = run(args.candidate, root, linked / "blocked.jsonl", "normal")
            check("candidate_refuses_symlink_parent", symlink.get("exception") and not (out / "blocked.jsonl").exists())
    print(json.dumps({"baseline_sha256": BASELINE_SHA256, "candidate_executed": bool(args.candidate),
                      "passed": sum(t["pass"] for t in tests), "total": len(tests), "tests": tests}, sort_keys=True))
    return 0 if all(t["pass"] for t in tests) else 1


if __name__ == "__main__":
    raise SystemExit(main())
