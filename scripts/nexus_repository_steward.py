#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""NEXUS repository steward: read-only, source-exact Git tree inventory.

This is an existing-CI/local deterministic tool, NOT evidence of a live Node-Bus agent.
No file moves, network, LLM inference, renames, or canonical-event writes.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT_SPECIAL = frozenset({"AGENTS.md", "GOVERNANCE.md", "SECURITY.md", "README.md",
                          "CITATION.cff", "LICENSE", "index.md", "_config.yml"})
WINDOWS_FORBIDDEN = set('<>:"\\|?*')
RESERVED = re.compile(r"^(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(?:\..*)?$", re.I)
SAFE_NEW_DIR = re.compile(r"^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$")
ID_ARTIFACT = re.compile(r"^NEXUS_[A-Z0-9_]+")
NAME_POLICY = "NEXUS_REPOSITORY_STEWARD_CONVENTION_V1"


def policy(path: str, allowed_roots: set[str]) -> tuple[str, list[str], list[str]]:
    """Return owning domain, non-destructive review advisories, integrity faults."""
    parts = path.split("/")
    reviews, faults = [], []
    if not path or any(not p or p in (".", "..") for p in parts):
        faults.append("INVALID_PATH_COMPONENT")
    for part in parts:
        if any(ord(c) < 32 or c in WINDOWS_FORBIDDEN for c in part):
            faults.append("WINDOWS_INCOMPATIBLE_CHARACTER")
        if part.rstrip(" .") != part or RESERVED.fullmatch(part):
            faults.append("WINDOWS_RESERVED_NAME")
    root = parts[0]
    if root not in allowed_roots:
        faults.append("ROOT_NOT_ALLOWLISTED")
    if len(parts) > 1:
        for directory in parts[:-1]:
            if directory.startswith(".") and directory == ".github":
                continue
            if not SAFE_NEW_DIR.fullmatch(directory) and directory not in ("sha256",):
                reviews.append("LEGACY_DIRECTORY_NAMING_REVIEW")
                break
    file_name = parts[-1]
    if (file_name not in ROOT_SPECIAL and file_name != "README.md" and
        not ID_ARTIFACT.match(file_name) and
        ((" " in file_name) or any(c.isupper() for c in file_name))):
        reviews.append("LEGACY_FILE_NAMING_REVIEW")
    if len(path.encode("utf-8", errors="surrogateescape")) > 240:
        reviews.append("PORTABLE_PATH_LENGTH_REVIEW")
    owner = root if len(parts) > 1 else "root-control"
    return owner, sorted(set(reviews)), sorted(set(faults))


def parse_ls_tree(raw: bytes):
    """Parse NUL-delimited git ls-tree -r -l HEAD, excluding tree objects."""
    rows = []
    for item in raw.split(b"\0"):
        if not item:
            continue
        header, name = item.split(b"\t", 1)
        mode, typ, oid, size = header.decode("ascii").split()
        if typ != "blob":
            rows.append((name.decode("utf-8", "surrogateescape"), mode, typ, oid, None))
            continue
        rows.append((name.decode("utf-8", "surrogateescape"), mode, typ, oid,
                     int(size) if size != "-" else None))
    return rows


def audit(root: Path, entries: list[tuple], structure: dict, commit: str) -> dict:
    roots = set(structure["root_files"]) | set(structure["root_directories"])
    registry = structure["active_research_lanes"]
    lanes = {entry["path"]: key for key, entry in registry.items()}
    directory_names = set()
    rows, findings = [], []
    case_map = {}
    for path, mode, typ, oid, declared_bytes in sorted(entries):
        parts = path.split("/")
        directory_names.update("/".join(parts[:i]) for i in range(1, len(parts)))
        owner, reviews, faults = policy(path, roots)
        identity = path.casefold()
        if identity in case_map and case_map[identity] != path:
            faults.append("PORTABLE_CASE_COLLISION")
        case_map[identity] = path
        if typ != "blob" or mode == "120000":
            reviews.append("NON_REGULAR_GIT_ENTRY_REVIEW")
        actual = root.joinpath(*parts)
        content = None
        if not faults and typ == "blob" and mode != "120000" and actual.is_file() and not actual.is_symlink():
            content = actual.read_bytes()
            if len(content) != declared_bytes:
                faults.append("GIT_TREE_BYTE_COUNT_MISMATCH")
            computed_oid = hashlib.sha1(b"blob " + str(len(content)).encode("ascii") + b"\0" + content).hexdigest()
            if computed_oid != oid:
                faults.append("WORKTREE_GIT_BLOB_MISMATCH")
        elif not faults and typ == "blob" and mode != "120000":
            faults.append("TRACKED_FILE_NOT_PRESENT")
        lane = next((k for p, k in lanes.items() if path.startswith(p + "/")), None)
        if owner == "research" and lane is None and path != "research/README.md":
            reviews.append("RESEARCH_NOT_IN_REGISTERED_LANE_REVIEW")
        rows.append({"path": path, "domain": owner, "registered_lane": lane,
                     "git_blob_sha1": oid if typ == "blob" else None,
                     "mode": mode, "declared_bytes": declared_bytes,
                     "observed_bytes": len(content) if content is not None else None,
                     "observed_sha256": hashlib.sha256(content).hexdigest() if content is not None else None,
                     "advisories": sorted(set(reviews)), "integrity_errors": sorted(set(faults))})
        for f in sorted(set(faults)):
            findings.append({"severity": "INTEGRITY", "code": f, "path": path})
    for path, lane_id in sorted(lanes.items()):
        if path + "/README.md" not in {r["path"] for r in rows}:
            findings.append({"severity": "INTEGRITY", "code": "REGISTERED_LANE_README_MISSING",
                             "path": path, "lane": lane_id})
    findings.sort(key=lambda v: (v["code"], v["path"]))
    review_counter = Counter(code for row in rows for code in row["advisories"])
    return {"object": "NEXUS_OMEGA_REPOSITORY_STEWARD_V1", "claim_ceiling": "C1_DESCRIPTIVE_ONLY",
            "source_commit": commit, "registry_version": structure.get("version"),
            "tracked_file_count": len(rows), "directory_count": len(directory_names),
            "registered_lane_count": len(lanes),
            "integrity_error_count": len(findings), "review_counts": dict(sorted(review_counter.items())),
            "findings": findings, "files": rows,
            "scope": "PUBLIC_GIT_CHECKOUT_ONLY", "node_bus_runtime": "NOT_ASSESSED",
            "autonomous_moves": False, "source_mutation": False}


def git(root: Path, *args) -> bytes:
    return subprocess.check_output(["git", *args], cwd=root, stderr=subprocess.DEVNULL)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, default=Path("."))
    ap.add_argument("--output", type=Path, help="Write complete machine-readable JSONL inventory")
    ap.add_argument("--fail-on-integrity", action="store_true")
    args = ap.parse_args()
    try:
        root = args.root.resolve()
        contract = json.loads((root / "docs/architecture/REPOSITORY_STRUCTURE.json").read_text("utf-8"))
        commit = git(root, "rev-parse", "HEAD").decode("ascii").strip()
        entries = parse_ls_tree(git(root, "ls-tree", "-r", "-l", "-z", "HEAD"))
        report = audit(root, entries, contract, commit)
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text("".join(json.dumps(row, sort_keys=True, ensure_ascii=True) + "\n"
                                           for row in report["files"]), encoding="utf-8")
        summary = {k: v for k, v in report.items() if k != "files"}
        print(json.dumps(summary, sort_keys=True, ensure_ascii=True))
        return 1 if args.fail_on_integrity and report["integrity_error_count"] else 0
    except (OSError, ValueError, KeyError, subprocess.CalledProcessError) as exc:
        print(json.dumps({"state": "HOLD_SOURCE", "reason": str(exc)}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
