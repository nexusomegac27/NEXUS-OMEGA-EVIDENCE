#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Validate the NEXUS OMEGA repository-order contract."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT_FILES = {
    ".gitattributes", ".gitignore", "AGENTS.md", "CITATION.cff", "GOVERNANCE.md",
    "LICENSE", "README.md", "SECURITY.md", "_config.yml", "index.md",
    "requirements-a83-test.txt",
}
ROOT_DIRS = {
    ".github", "archive", "communication", "cross_forge", "docs", "examples", "index", "objects",
    "research", "schema", "scripts", "tests", "validation",
}
REQUIRED_READMES = {
    "archive/README.md", "communication/README.md", "cross_forge/README.md", "docs/README.md",
    "examples/README.md", "index/README.md", "objects/README.md", "research/README.md",
    "schema/README.md", "scripts/README.md", "tests/README.md", "validation/README.md",
    "docs/r5/README.md", "examples/r5/README.md", "research/r5/README.md",
    "schema/r5/README.md", "scripts/r5/README.md", "tests/r5/README.md",
    "validation/r5/README.md",
}
REQUIRED_CONTRACTS = {
    "docs/architecture/REPOSITORY_STRUCTURE.md",
    "docs/architecture/REPOSITORY_STRUCTURE.json",
    "docs/governance/REPOSITORY_ORDER_POLICY.md",
    "docs/governance/REPOSITORY_PATH_RULES.json",
}
HISTORICAL_PATHS = {
    "requirements-a83-test.txt",
    "docs/phase2/A83_FRAMEWORK_INVENTORY_AND_GAP_REPORT_v1.0.json",
    "docs/phase2/A83_FRAMEWORK_INVENTORY_AND_GAP_REPORT_v1.0.md",
    "docs/phase2/NEXUS_OMEGA_A84_INDEPENDENT_GITHUB_VALIDATION_RETURN_20260831_R0.md",
    "docs/phase2/NEXUS_OMEGA_A84_INDEPENDENT_GITHUB_VALIDATION_RETURN_20260831_R0_HANDSHAKE.json",
    "schema/A83_handoff_envelope_v1.schema.json",
    "scripts/a83_decision.py", "scripts/a83_sentinel.py", "scripts/reproduce_a83.py",
    "scripts/validate_a83_handoff.py", "scripts/verify_a83_artifact_binding.py",
    "tests/test_a83_handoff.py", "validation/A83_ARTIFACT_BINDING_v1.0.json",
    "validation/A83_WEAKNESS_AND_OPEN_QUESTIONS_AUDIT_v1.0.json",
    "validation/a83-handoff-negative-fixtures-v1.jsonl",
    "examples/a83/handoff-envelope-v1.example.json",
    ".github/workflows/validate-a83-framework-hardening.yml",
}


def validate_root_entries(names: set[str]) -> list[str]:
    errors = []
    allowed = ROOT_FILES | ROOT_DIRS
    for name in sorted(names - allowed):
        errors.append(f"UNEXPECTED_ROOT_ENTRY:{name}")
    for name in sorted(allowed - names):
        errors.append(f"REQUIRED_ROOT_ENTRY_MISSING:{name}")
    return errors


def validate_r5_lane_readmes(r5_root: Path) -> list[str]:
    """Require every direct R5 research lane to declare its purpose/status."""
    if not r5_root.is_dir():
        return ["R5_RESEARCH_ROOT_MISSING"]
    errors = []
    for lane in sorted((p for p in r5_root.iterdir() if p.is_dir()), key=lambda p: p.name):
        if not (lane / "README.md").is_file():
            errors.append(f"R5_LANE_README_MISSING:{lane.name}")
    return errors


def validate(root: Path) -> list[str]:
    root = root.resolve()
    errors: list[str] = []
    names = {p.name for p in root.iterdir() if p.name != ".git"}
    errors.extend(validate_root_entries(names))

    for rel in sorted(REQUIRED_READMES | REQUIRED_CONTRACTS | HISTORICAL_PATHS):
        if not (root / rel).is_file():
            errors.append(f"REQUIRED_PATH_MISSING:{rel}")

    contract_path = root / "docs/architecture/REPOSITORY_STRUCTURE.json"
    try:
        contract = json.loads(contract_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        errors.append("STRUCTURE_CONTRACT_UNREADABLE")
        return errors

    if set(contract.get("root_files", [])) != ROOT_FILES:
        errors.append("STRUCTURE_CONTRACT_ROOT_FILES_MISMATCH")
    if set(contract.get("root_directories", [])) != ROOT_DIRS:
        errors.append("STRUCTURE_CONTRACT_ROOT_DIRS_MISMATCH")
    if contract.get("order_law") != "REPOSITORY_ORDER_LAW_V1":
        errors.append("STRUCTURE_CONTRACT_ORDER_LAW_MISMATCH")

    errors.extend(validate_r5_lane_readmes(root / "research" / "r5"))

    # Prevent the common failure mode: agent/research outputs dumped at root.
    for p in root.iterdir():
        if p.is_file() and p.name not in ROOT_FILES:
            errors.append(f"ROOT_DUMP_PROHIBITED:{p.name}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    errors = validate(args.root)
    result = {
        "object": "NEXUS_OMEGA_REPOSITORY_STRUCTURE_VALIDATION_V1",
        "order_law": "REPOSITORY_ORDER_LAW_V1",
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
    }
    print(json.dumps(result, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
