#!/usr/bin/env python3
"""Frozen independent black-box evaluator for a C1-only Steward output guard.

Evaluator is versioned before the candidate. It does not import candidate code.
Only synthetic temporary Git repositories are modified.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

PINNED_STEWARD_SHA256 = "94051a46bc8968e05579410fb607393d07907fd499c4e397d11c611be52d7998"


def run(*argv, cwd=None):
    return subprocess.run([str(x) for x in argv], cwd=cwd, capture_output=True, text=True)


def fixture(source: bytes, location: Path):
    root = location / "repo"
    (root / "docs" / "architecture").mkdir(parents=True)
    (root / "scripts").mkdir()
    (root / "README.md").write_text("CANONICAL_SOURCE_DO_NOT_OVERWRITE\n", encoding="utf-8")
    (root / "scripts" / "nexus_repository_steward.py").write_bytes(source)
    contract = {"version": "fixture", "root_files": ["README.md"],
                "root_directories": ["docs", "scripts"], "active_research_lanes": {}}
    (root / "docs" / "architecture" / "REPOSITORY_STRUCTURE.json").write_text(
        json.dumps(contract), encoding="utf-8")
    assert run("git", "init", "-q", root).returncode == 0
    assert run("git", "-C", root, "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
               "add", ".").returncode == 0
    assert run("git", "-C", root, "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
               "commit", "-qm", "fixture").returncode == 0
    return root


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--steward", required=True, type=Path)
    ap.add_argument("--candidate", type=Path)
    args = ap.parse_args()
    source = args.steward.read_bytes()
    if hashlib.sha256(source).hexdigest() != PINNED_STEWARD_SHA256:
        raise SystemExit("FAIL_CLOSED: source steward SHA-256 differs from frozen pin")
    checks = []
    def check(name, condition):
        checks.append({"name": name, "pass": bool(condition)})
    with tempfile.TemporaryDirectory(prefix="alpha-output-guard-") as td:
        tmp = Path(td)
        root = fixture(source, tmp)
        steward = root / "scripts" / "nexus_repository_steward.py"
        protected = root / "README.md"
        original = protected.read_bytes()
        # Baseline: real unmodified Steward CLI overwrites an existing tracked source.
        baseline = run(sys.executable, steward, "--root", root, "--output", protected)
        check("baseline_tracked_source_overwritten", baseline.returncode == 0 and protected.read_bytes() != original)
        check("baseline_reports_no_source_mutation", baseline.returncode == 0 and
              json.loads(baseline.stdout).get("source_mutation") is False)
        assert run("git", "-C", root, "checkout", "--", "README.md").returncode == 0
        control = tmp / "baseline.jsonl"
        base_ok = run(sys.executable, steward, "--root", root, "--output", control)
        check("baseline_external_new_output_positive", base_ok.returncode == 0 and control.is_file())
        if args.candidate:
            c = args.candidate
            def invoke(out):
                return run(sys.executable, c, "--root", root, "--output", out)
            denied = invoke(protected)
            check("candidate_rejects_tracked_source_overwrite", denied.returncode != 0 and protected.read_bytes() == original)
            in_root = root / "new.jsonl"
            check("candidate_rejects_new_in_checkout", invoke(in_root).returncode != 0 and not in_root.exists())
            existing = tmp / "existing.txt"
            existing.write_text("KEEP", encoding="utf-8")
            check("candidate_rejects_existing_external", invoke(existing).returncode != 0 and existing.read_text() == "KEEP")
            outside = tmp / "outside"
            outside.mkdir()
            link_dir = tmp / "linked"
            link_dir.symlink_to(outside, target_is_directory=True)
            check("candidate_rejects_symlink_parent", invoke(link_dir / "alias.jsonl").returncode != 0 and
                  not (outside / "alias.jsonl").exists())
            link_file = tmp / "file-link"
            link_file.symlink_to(protected)
            check("candidate_rejects_symlink_leaf", invoke(link_file).returncode != 0 and protected.read_bytes() == original)
            check("candidate_rejects_relative_output", invoke(Path("relative.jsonl")).returncode != 0)
            traversal = tmp / "outside" / ".." / "traversal.jsonl"
            check("candidate_rejects_parent_traversal", invoke(traversal).returncode != 0 and
                  not (tmp / "traversal.jsonl").exists())
            new = tmp / "candidate.jsonl"
            positive = invoke(new)
            check("candidate_new_external_output_positive", positive.returncode == 0 and new.is_file())
            check("candidate_matches_baseline_positive_bytes", new.is_file() and new.read_bytes() == control.read_bytes())
            check("candidate_preserves_source_after_positive", protected.read_bytes() == original)
            # Source drift is rejected rather than silently executing a different Steward.
            steward.write_bytes(source + b"\n# mutated fixture\n")
            drift = tmp / "drift.jsonl"
            check("candidate_rejects_steward_source_drift", invoke(drift).returncode != 0 and not drift.exists())
    print(json.dumps({"source_sha256": PINNED_STEWARD_SHA256,
                      "candidate_executed": args.candidate is not None,
                      "tests": checks, "passed": sum(c["pass"] for c in checks),
                      "total": len(checks)}, sort_keys=True))
    return 0 if all(c["pass"] for c in checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
