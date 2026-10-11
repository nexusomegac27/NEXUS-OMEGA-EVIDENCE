#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""R28: trusted-base, read-only PR pre-entry laboratory.

The existing R27-E GitHub-API structural validator is the sole path/identity
authority. This module only runs fixed offline conformance suites and emits
a bounded, falsifiable descriptive receipt. Not a WWW or Node runtime gate.
"""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
SOURCE_FILES = (
    "scripts/nexus_preentry_lab.py",
    "scripts/validate_external_agent_pr.py",
    "docs/governance/EXTERNAL_AGENT_WRITE_SLOTS_V1.json",
    "tests/test_preentry_lab.py",
    "tests/r19/orbis-satellite-directory.test.mjs",
    "tests/r19/orbis-sgp4-public-contract-bridge.test.mjs",
)
COMMANDS = (
    (sys.executable, "-m", "unittest", "tests.test_preentry_lab", "-v"),
    ("node", "--test",
     "tests/r19/orbis-satellite-directory.test.mjs",
     "tests/r19/orbis-sgp4-public-contract-bridge.test.mjs"),
)
MAX_LOG = 12000


def compute_bindings(root: Path = ROOT) -> list[dict]:
    output = []
    for path in SOURCE_FILES:
        resolved = (root / path).resolve()
        if not resolved.is_file() or not resolved.is_relative_to(root.resolve()):
            raise ValueError("MISSING_OR_UNSAFE_TRUSTED_SOURCE:" + path)
        data = resolved.read_bytes()
        output.append({"path": path, "bytes": len(data),
                       "sha256": hashlib.sha256(data).hexdigest()})
    return output


def execute(root: Path = ROOT) -> dict:
    """Run fixed commands only; never interpret PR text as shell, code, or args."""
    results = []
    for argv in COMMANDS:
        try:
            p = subprocess.run(argv, cwd=root, stdin=subprocess.DEVNULL,
                               capture_output=True, text=True, timeout=120,
                               check=False)
            results.append({"command": argv[1:] if argv[0] == sys.executable else argv,
                            "exit_code": p.returncode, "passed": p.returncode == 0,
                            "output_tail": (p.stdout + "\n" + p.stderr)[-MAX_LOG:]})
        except (OSError, subprocess.TimeoutExpired) as exc:
            results.append({"command": argv, "exit_code": None, "passed": False,
                            "error": type(exc).__name__})
            break
    ok = len(results) == len(COMMANDS) and all(x["passed"] for x in results)
    return {"status": "PASS_OFFLINE_FIXTURES_C1" if ok else "FAIL_CLOSED",
            "all_passed": ok, "results": results}


def receipt(run_result: dict, bindings: list[dict], *,
            run_id: str | None = None, source_sha: str | None = None) -> dict:
    return {
        "object": "NEXUS_R28_TRUSTED_BASE_PREENTRY_LAB_RECEIPT_V1",
        "status": run_result["status"],
        "github_run_id": run_id,
        "trusted_base_sha": source_sha,
        "tests": [{"command": v["command"], "passed": v["passed"],
                   "exit_code": v["exit_code"]} for v in run_result["results"]],
        "inputs": bindings,
        "git_pr_actor_and_paths": "R27E_UPSTREAM_CHECK_REQUIRED",
        "untrusted_pr_code_executed": False,
        "github_token_permissions": "CONTENTS_READ",
        "artifact_attestation": "NOT_GENERATED",
        "egress_default_deny": "NOT_ENFORCED",
        "independent_provider_signature": "NOT_ESTABLISHED",
        "runtime_auth001_002_003": "HOLD_SECURITY_NOT_TESTED_HERE",
        "external_actor_registration": "NOT_MODIFIED",
        "www_or_internal_entry_guard": "NOT_INSTALLED",
        "production_release": "NOT_AUTHORIZED",
        "claim_ceiling": "C1_DESCRIPTIVE_ONLY",
    }


def main() -> int:
    # This is deliberately not an API client or any form of daemon.
    try:
        bindings = compute_bindings()
        result = execute()
        r = receipt(result, bindings, run_id=os.getenv("GITHUB_RUN_ID"),
                    source_sha=os.getenv("GITHUB_SHA"))
        print("NEXUS_ENTRY_LAB_RECEIPT_JSON=" + json.dumps(r, sort_keys=True,
                                                         separators=(",", ":")))
        return 0 if result["all_passed"] else 1
    except (OSError, ValueError) as exc:
        print(json.dumps({"object": "NEXUS_R28_TRUSTED_BASE_PREENTRY_LAB_RECEIPT_V1",
                          "status": "FAIL_CLOSED", "error_type": type(exc).__name__,
                          "claim_ceiling": "C1_DESCRIPTIVE_ONLY"}))
        return 1


if __name__ == "__main__":
    sys.exit(main())
