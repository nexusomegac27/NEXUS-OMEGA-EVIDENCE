#!/usr/bin/env python3
"""R41 P4 — fail-closed 14-gate engine. PASS only with source-exact evidence."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

WORKER = Path(__file__).resolve().parents[1]
ANNOTATED = Path(__file__).resolve().parent / "R40_14_HARD_GATES_ANNOTATED.json"
OUT = Path(__file__).resolve().parent / "GATE_ENGINE_RECEIPT.json"

# Physical / device / public — always HOLD under R41 offline order
ALWAYS_HOLD = {
    "OWNER_ONE_SHOT_APPROVAL",
    "PRIVATE_ORIGINAL_RECEIVER",
    "INDEPENDENT_SECOND_SOURCE",
    "R38_T21_TO_T28_EXECUTION_SOURCE",
}

# Offline-implementable gates that may become PASS only with local evidence
EVIDENCE_MAP = {
    "STOP_DEADLINE_REPAIR": WORKER
    / "05_STOP_DEADLINE"
    / "STOP_DEADLINE_HARNESS_RECEIPT.json",
    "INDEPENDENT_ANGLE_REFERENCE": WORKER
    / "06_METROLOGY"
    / "METROLOGY_OFFLINE_RECEIPT.json",
    "SENSOR_FRAME_AND_UNITS": WORKER
    / "06_METROLOGY"
    / "METROLOGY_OFFLINE_RECEIPT.json",
    "MONOTONIC_EVENT_CLOCK": WORKER
    / "05_STOP_DEADLINE"
    / "STOP_DEADLINE_HARNESS_RECEIPT.json",
}


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def evaluate_gate(gate_id: str) -> dict:
    if gate_id in ALWAYS_HOLD:
        return {
            "id": gate_id,
            "status": "HOLD",
            "passed": False,
            "reason": "PHYSICAL_OR_OPERATOR_OR_EXTERNAL_REQUIRED",
        }
    evidence = EVIDENCE_MAP.get(gate_id)
    if evidence is None:
        return {
            "id": gate_id,
            "status": "OPEN_OR_HOLD",
            "passed": False,
            "reason": "NO_OFFLINE_EVIDENCE_BOUND",
        }
    if not evidence.is_file():
        return {
            "id": gate_id,
            "status": "OPEN_OR_HOLD",
            "passed": False,
            "reason": "EVIDENCE_ABSENT",
            "expected_path": str(evidence),
        }
    try:
        data = json.loads(evidence.read_text(encoding="utf-8"))
    except Exception as e:
        return {
            "id": gate_id,
            "status": "OPEN_OR_HOLD",
            "passed": False,
            "reason": f"EVIDENCE_UNREADABLE:{e}",
        }
    verdict = str(data.get("verdict", "")).upper()
    if verdict != "PASS":
        return {
            "id": gate_id,
            "status": "OPEN_OR_HOLD",
            "passed": False,
            "reason": f"EVIDENCE_VERDICT_NOT_PASS:{verdict or 'MISSING'}",
            "evidence_sha256": sha256_file(evidence),
        }
    return {
        "id": gate_id,
        "status": "PASS_OFFLINE_C1",
        "passed": True,
        "reason": "SOURCE_EXACT_OFFLINE_EVIDENCE",
        "evidence_path": str(evidence),
        "evidence_sha256": sha256_file(evidence),
    }


def main() -> int:
    annotated = json.loads(ANNOTATED.read_text(encoding="utf-8"))
    gate_ids = [g["id"] for g in annotated["gates"]]
    assert len(gate_ids) == 14, f"expected 14 gates, got {len(gate_ids)}"

    results = [evaluate_gate(gid) for gid in gate_ids]
    passed = sum(1 for r in results if r["passed"])
    hold = sum(1 for r in results if r["status"] == "HOLD")
    open_or_hold = sum(1 for r in results if not r["passed"])

    # Fail-closed: never auto-lift physical; never claim full 14 PASS
    physical_auto_clear = False
    full_pass_claim = passed == 14

    receipt = {
        "object": "R41_14_GATE_ENGINE_RECEIPT",
        "recorded_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "claim_ceiling": "C1_DESCRIPTIVE_ONLY",
        "bodytwin_validated": False,
        "physical": "ALT_D_DO_NOT_RUN_ACTIVE",
        "device_capture": False,
        "total": 14,
        "passed_offline_c1": passed,
        "hold_physical_or_operator": hold,
        "open_or_hold_remaining": open_or_hold,
        "physical_auto_clear": physical_auto_clear,
        "full_14_pass_claim": full_pass_claim,
        "fail_closed": True,
        "gates": results,
        "verdict": "PASS_ENGINE_FAIL_CLOSED"
        if (not physical_auto_clear and not full_pass_claim)
        else "FAIL_ENGINE_OVERCLAIM",
    }
    OUT.write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "verdict": receipt["verdict"],
                "passed_offline_c1": passed,
                "open_or_hold_remaining": open_or_hold,
                "receipt": str(OUT),
                "sha256": sha256_file(OUT),
            }
        )
    )
    return 0 if receipt["verdict"] == "PASS_ENGINE_FAIL_CLOSED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
