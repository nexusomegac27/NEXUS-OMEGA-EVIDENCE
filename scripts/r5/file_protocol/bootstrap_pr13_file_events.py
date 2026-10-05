#!/usr/bin/env python3
"""Bootstrap canonical file events for PR13 commits C1-C3 (backfill)."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
APPEND = ROOT / "scripts/r5/file_protocol/append_file_event.py"

ORDER_ID = (
    "NEXUS_OMEGA_CURSOR_QWEN_LAYER1_R1_FULL_MEASUREMENT_"
    "CHRONOLOGY_FILE_EVENT_GITHUB_ORDER_20260902_R0"
)
ORDER_SHA256 = "e00987e80a7eed8c135f8ba0b38b608b3a7d5638c6dda8bba2493063ba5b10fb"
REPO = "nexusomegac27/NEXUS-OMEGA-EVIDENCE"
PR_NUMBER = 13

COMMITS = [
    "8a985ad0e06ec33ca93502d930b7956d06ddcb76",
    "338547fdaf896de4625f6091e9fa5e78cef5e1d8",
    "ee537bcb60294126be67882ff384daa3326dc6f8",
]

ACTOR = {
    "actor_type": "AGENT",
    "role": "AXIOM_EPISTEMIC_AND_GITHUB_IMPLEMENTATION_AGENT",
    "provider": "OPENAI",
    "model": "GPT-5.6 Sol",
    "session_id": "CURRENT_AXIOM_GITHUB_IMPLEMENTATION_SESSION",
    "admission_id": "PRE_FORMAL_ADMISSION_BOOTSTRAP",
    "rank_profile": None,
    "capability_profile_sha256": None,
}


def git(*args: str, binary: bool = False) -> bytes | str:
    out = subprocess.check_output(["git", *args], cwd=ROOT, text=not binary)
    return out if not binary else out  # type: ignore[return-value]


def blob(ref: str, path: str | None) -> bytes | None:
    if path is None:
        return None
    try:
        return subprocess.check_output(["git", "show", f"{ref}:{path}"], cwd=ROOT)
    except subprocess.CalledProcessError:
        return None


def file_state(ref: str, path: str | None) -> dict:
    if path is None:
        return {"exists": False, "path": None, "bytes": None, "sha256": None}
    data = blob(ref, path)
    if data is None:
        return {"exists": False, "path": path, "bytes": None, "sha256": None}
    return {
        "exists": True,
        "path": path,
        "bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
    }


def changed(commit: str) -> list[tuple[str, str | None, str | None]]:
    out = git("diff-tree", "--no-commit-id", "--name-status", "-r", "-M", commit).strip()
    rows: list[tuple[str, str | None, str | None]] = []
    for line in out.splitlines():
        parts = line.split("\t")
        status = parts[0]
        if status.startswith("R") and len(parts) >= 3:
            rows.append(("MOVE", parts[1], parts[2]))
        elif status == "A":
            rows.append(("CREATE", None, parts[1]))
        elif status == "D":
            rows.append(("DELETE", parts[1], None))
        elif status == "M":
            rows.append(("MODIFY", parts[1], parts[1]))
    ledger = "communication/file-events/"
    return [r for r in rows if not ((r[1] or r[2] or "").startswith(ledger))]


def artifact_class(path: str) -> str:
    if path.startswith(".github/"):
        return "CI_WORKFLOW"
    if path.startswith("schema/"):
        return "SCHEMA"
    if path.startswith("scripts/"):
        return "SCRIPT"
    if path.startswith("tests/"):
        return "TEST"
    if path.startswith("validation/"):
        return "FIXTURE"
    if path.startswith("docs/"):
        return "DOCUMENTATION"
    if path.startswith("research/"):
        return "RESEARCH"
    if path == "AGENTS.md":
        return "GOVERNANCE"
    if path.startswith("communication/"):
        return "COMMUNICATION"
    return "OTHER"


def main() -> int:
    recorded_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    created: list[dict] = []
    seq = 0

    for commit in COMMITS:
        parent = git("rev-parse", f"{commit}^").strip()
        for op, before_path, after_path in changed(commit):
            seq += 1
            event_id = f"pr13-backfill-{commit[:8]}-{seq:03d}"
            before = file_state(parent, before_path)
            after = file_state(commit, after_path)
            event = {
                "schema_version": "1.0.0",
                "event_id": event_id,
                "recorded_at_utc": recorded_at,
                "actor": ACTOR,
                "task": {
                    "order_id": ORDER_ID,
                    "order_sha256": ORDER_SHA256,
                    "parent_event_id": None,
                },
                "operation": op,
                "artifact_class": artifact_class(after_path or before_path or "unknown"),
                "digest_domain": "SHA256_RAW_BYTES_V1",
                "before": before,
                "after": after,
                "reason": (
                    "BACKFILL=TRUE; BACKFILL_BASIS=EXACT_GIT_BYTES_AND_OPERATOR_AXIOM_SESSION_EVIDENCE; "
                    "CURSOR_BACKFILL_CAUSE=THIS_ORDER; CREATION_CAUSE=OPERATOR_CURRENT_REQUEST_VIA_AXIOM"
                ),
                "git": {
                    "repository": REPO,
                    "base_commit": parent,
                    "result_commit": commit,
                    "pr_number": PR_NUMBER,
                },
                "validation": {
                    "producer_self_report": None,
                    "independent_validation": "CURSOR_PRAXIS_BOOTSTRAP_20260902_R0",
                },
                "claim_ceiling": "C1",
            }
            tmp = ROOT / ".bootstrap_event.json"
            tmp.write_text(json.dumps(event, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
            out = subprocess.check_output(
                [sys.executable, str(APPEND), str(tmp), "--root", str(ROOT)],
                cwd=ROOT,
                text=True,
            )
            created.append({"commit": commit, "event_id": event_id, "append_result": json.loads(out)})

    summary = {
        "object": "PR13_FILE_EVENT_BOOTSTRAP_20260902_R0",
        "events_created": len(created),
        "commits": COMMITS,
        "details": created,
    }
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
