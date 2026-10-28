#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Frozen black-box C1 oracle for post-publication mutation/swap detection.

Separate subprocesses load baseline/candidate by path. The oracle never imports
candidate functions, checks external outcomes, and injects mutations precisely
when the directory fsync completes. This is synthetic Linux/POSIX evidence.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

BASELINE_SHA256 = "847c3bd775b195f30617174904af6644ab1d13dd30725a9f44e40fe797423578"
PAYLOAD = b"NEXUS_POSTPUBLISH_READBACK_C1\n" * 73

CHILD = r'''
import errno, hashlib, importlib.util, json, os, stat, sys
from pathlib import Path
module_path, root_path, target_path, mode = sys.argv[1:]
spec = importlib.util.spec_from_file_location("isolated_module", module_path)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
original_fsync = os.fsync
payload = b"NEXUS_POSTPUBLISH_READBACK_C1\n" * 73
p = Path(target_path)
def fault(fd):
    is_dir = stat.S_ISDIR(os.fstat(fd).st_mode)
    if mode == "file-fsync-eio" and not is_dir:
        raise OSError(errno.EIO, "SYNTHETIC_FILE_FSYNC_EIO")
    if is_dir:
        if mode == "dir-fsync-eio":
            raise OSError(errno.EIO, "SYNTHETIC_DIR_FSYNC_EIO")
        result = original_fsync(fd)
        if mode == "tamper-after-link":
            p.write_bytes(b"SYNTHETIC_TAMPERED_CONTENT\n")
        elif mode == "swap-same-bytes":
            p.unlink()
            p.write_bytes(payload)
        return result
    return original_fsync(fd)
if mode in ("file-fsync-eio", "dir-fsync-eio", "tamper-after-link", "swap-same-bytes"):
    os.fsync = fault
exception = None
message = None
try:
    mod.guarded_write(Path(root_path), p, payload)
except Exception as exc:
    exception = type(exc).__name__
    message = str(exc)
finally:
    os.fsync = original_fsync
exists = p.is_file()
data = p.read_bytes() if exists else b""
print(json.dumps({"exception": exception, "message": message,
    "exists": exists, "bytes": len(data) if exists else None,
    "sha256": hashlib.sha256(data).hexdigest() if exists else None,
    "temps": sorted(x.name for x in p.parent.glob(".nexus-alpha-atomic-*.tmp"))},
    sort_keys=True))
'''


def run(module: Path, root: Path, target: Path, mode: str) -> dict:
    result = subprocess.run([sys.executable, "-c", CHILD, str(module), str(root), str(target), mode],
                            capture_output=True, text=True, timeout=20)
    if result.returncode != 0:
        return {"child_error": result.stderr[-600:], "returncode": result.returncode}
    return json.loads(result.stdout)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--baseline", type=Path, required=True)
    ap.add_argument("--candidate", type=Path)
    args = ap.parse_args()
    if hashlib.sha256(args.baseline.read_bytes()).hexdigest() != BASELINE_SHA256:
        raise SystemExit("BASELINE_BYTES_NOT_PINNED")
    checks = []
    def check(name: str, truth: bool):
        checks.append({"name": name, "pass": bool(truth)})
    expected = hashlib.sha256(PAYLOAD).hexdigest()
    tampered = hashlib.sha256(b"SYNTHETIC_TAMPERED_CONTENT\n").hexdigest()
    with tempfile.TemporaryDirectory(prefix="nexus-postpublish-readback-") as tmp:
        work = Path(tmp)
        root, out = work / "checkout", work / "external"
        root.mkdir()
        out.mkdir()
        baseline_tamper = run(args.baseline, root, out / "baseline-tamper.jsonl", "tamper-after-link")
        baseline_swap = run(args.baseline, root, out / "baseline-swap.jsonl", "swap-same-bytes")
        check("baseline_tamper_silent_success", baseline_tamper.get("exception") is None and baseline_tamper.get("sha256") == tampered)
        check("baseline_same_bytes_inode_swap_silent_success", baseline_swap.get("exception") is None and baseline_swap.get("sha256") == expected)
        baseline_good = run(args.baseline, root, out / "baseline-good.jsonl", "normal")
        check("baseline_positive_control", baseline_good.get("exception") is None and baseline_good.get("sha256") == expected)
        if args.candidate:
            tamper = run(args.candidate, root, out / "candidate-tamper.jsonl", "tamper-after-link")
            check("candidate_tamper_must_not_succeed", bool(tamper.get("exception")))
            check("candidate_tamper_explicit_mismatch", "PUBLISHED_READBACK_MISMATCH" in (tamper.get("message") or ""))
            check("candidate_tamper_fixture_effective", tamper.get("sha256") == tampered)
            check("candidate_tamper_no_temps", not tamper.get("temps"))
            swap = run(args.candidate, root, out / "candidate-swap.jsonl", "swap-same-bytes")
            check("candidate_swap_must_not_succeed", bool(swap.get("exception")))
            check("candidate_swap_explicit_inode_mismatch", "PUBLISHED_INODE_MISMATCH" in (swap.get("message") or ""))
            check("candidate_swap_fixture_preserves_content", swap.get("sha256") == expected)
            check("candidate_swap_no_temps", not swap.get("temps"))
            good = run(args.candidate, root, out / "candidate-good.jsonl", "normal")
            check("candidate_positive_control", good.get("exception") is None and good.get("sha256") == expected)
            dir_eio = run(args.candidate, root, out / "candidate-dir-eio.jsonl", "dir-fsync-eio")
            check("candidate_dir_eio_uncertain_not_success", dir_eio.get("exception") == "PublishedDurabilityUncertain" and "PUBLISHED_READBACK_MATCH_DURABILITY_UNKNOWN" in (dir_eio.get("message") or ""))
            check("candidate_dir_eio_bytes_complete", dir_eio.get("sha256") == expected and not dir_eio.get("temps"))
            file_eio = run(args.candidate, root, out / "candidate-file-eio.jsonl", "file-fsync-eio")
            check("candidate_file_eio_not_published", bool(file_eio.get("exception")) and not file_eio.get("exists") and not file_eio.get("temps"))
            existing = out / "existing.jsonl"
            existing.write_bytes(b"IMMUTABLE\n")
            no_replace = run(args.candidate, root, existing, "normal")
            check("candidate_no_replace", bool(no_replace.get("exception")) and existing.read_bytes() == b"IMMUTABLE\n")
            internal = root / "README.md"
            internal.write_bytes(b"IMMUTABLE_ROOT\n")
            blocked = run(args.candidate, root, internal, "normal")
            check("candidate_no_checkout_write", bool(blocked.get("exception")) and internal.read_bytes() == b"IMMUTABLE_ROOT\n")
            linked = work / "linked"
            linked.symlink_to(out, target_is_directory=True)
            symlink = run(args.candidate, root, linked / "blocked.jsonl", "normal")
            check("candidate_no_symlink_parent", bool(symlink.get("exception")) and not (out / "blocked.jsonl").exists())
    print(json.dumps({"baseline_sha256": BASELINE_SHA256, "candidate_executed": bool(args.candidate),
                      "passed": sum(x["pass"] for x in checks), "total": len(checks), "tests": checks}, sort_keys=True))
    return 0 if all(x["pass"] for x in checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
