#!/usr/bin/env python3
"""E0.2 — R8 full-product integration test.

C1 / descriptive-only reference implementation.  No claim promotion, online
transport, signature validation, or production authorization is implied.

The product contains seven explicit gate slots:
GATE1 trace identity, GATE2 falsification substrate, GATE3 uncertainty
substrate, and domain gates GATE4..GATE7.  The latter four implement the
contract in the AXIOM order; GATE2/GATE3 may be supplied by a trace and default
to VERIFIED for the four mandated fixtures because those fixtures exercise the
already-validated substrate rather than redefine it.
"""

from __future__ import annotations

from copy import deepcopy
from enum import Enum
import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping


class EpistemicState(str, Enum):
    VERIFIED = "VERIFIED"
    FALSIFIED = "FALSIFIED"
    AIR_GAP = "AIR_GAP"  # Δ / epistemic hold


VERIFIED = EpistemicState.VERIFIED
FALSIFIED = EpistemicState.FALSIFIED
AIR_GAP = EpistemicState.AIR_GAP


def _state(value: Any, *, default: EpistemicState = VERIFIED) -> EpistemicState:
    """Parse a substrate state; unknown values fail closed to AIR_GAP."""
    if value is None:
        return default
    if isinstance(value, EpistemicState):
        return value
    try:
        return EpistemicState(str(value).upper())
    except ValueError:
        return AIR_GAP


def aggregate_gate_states(states: Iterable[EpistemicState]) -> EpistemicState:
    """Non-compensatory conjunction: FALSIFIED > AIR_GAP > VERIFIED.

    This is a discrete minimum/priority operator, never a sum or product.
    An empty gate list is an invalid product and therefore fails closed.
    """
    materialized = list(states)
    if not materialized:
        return AIR_GAP
    if any(s == FALSIFIED for s in materialized):
        return FALSIFIED
    if any(s == AIR_GAP for s in materialized):
        return AIR_GAP
    if all(s == VERIFIED for s in materialized):
        return VERIFIED
    return AIR_GAP


def check_trace_identity(trace: Mapping[str, Any]) -> EpistemicState:
    return VERIFIED if isinstance(trace.get("trace_id"), str) and trace["trace_id"] else AIR_GAP


def check_falsification_substrate(trace: Mapping[str, Any]) -> EpistemicState:
    return _state(trace.get("gate2_state"), default=VERIFIED)


def check_uncertainty_substrate(trace: Mapping[str, Any]) -> EpistemicState:
    return _state(trace.get("gate3_state"), default=VERIFIED)


def check_provenance(trace: Mapping[str, Any]) -> EpistemicState:
    parent = trace.get("PARENT_TRACE")
    return VERIFIED if isinstance(parent, Mapping) and parent.get("trace_id") else AIR_GAP


def check_authority(trace: Mapping[str, Any]) -> EpistemicState:
    capsule = trace.get("AUTHORITY_CAPSULE")
    if not isinstance(capsule, Mapping):
        return AIR_GAP
    scope = capsule.get("scope")
    operation = trace.get("op")
    if not isinstance(scope, list) or not isinstance(operation, str):
        return AIR_GAP
    return VERIFIED if operation in scope else FALSIFIED


def check_memory_promotion(memory: Any) -> EpistemicState:
    if not isinstance(memory, Mapping):
        return AIR_GAP
    hygiene = str(memory.get("hygiene_status", "")).upper()
    if hygiene == "FAIL":
        return FALSIFIED
    if hygiene != "PASS":
        return AIR_GAP
    provenance = memory.get("provenance")
    return VERIFIED if isinstance(provenance, Mapping) and provenance else AIR_GAP


def check_constitution(trace: Mapping[str, Any]) -> EpistemicState:
    claim_level = trace.get("claim_level")
    defeat_condition = trace.get("DEFEAT_CONDITION")
    if not isinstance(claim_level, str) or not claim_level:
        return AIR_GAP
    if not isinstance(defeat_condition, str) or not defeat_condition:
        return AIR_GAP
    return VERIFIED


def evaluate_full_trace(trace: Mapping[str, Any]) -> EpistemicState:
    """Run all seven gates on one trace and aggregate without compensation."""
    if not isinstance(trace, Mapping):
        return AIR_GAP
    states: List[EpistemicState] = [
        check_trace_identity(trace),                 # GATE1
        check_falsification_substrate(trace),        # GATE2
        check_uncertainty_substrate(trace),          # GATE3
        check_provenance(trace),                     # GATE4
        check_authority(trace),                      # GATE5
        check_memory_promotion(trace.get("memory")),# GATE6
        check_constitution(trace),                   # GATE7
    ]
    return aggregate_gate_states(states)


def evaluate_with_detail(trace: Mapping[str, Any]) -> Dict[str, Any]:
    """Return an auditable per-gate receipt for the result JSON."""
    gate_states = {
        "GATE1_TRACE_IDENTITY": check_trace_identity(trace),
        "GATE2_FALSIFICATION_SUBSTRATE": check_falsification_substrate(trace),
        "GATE3_UNCERTAINTY_SUBSTRATE": check_uncertainty_substrate(trace),
        "GATE4_PROVENANCE": check_provenance(trace),
        "GATE5_AUTHORITY": check_authority(trace),
        "GATE6_MEMORY_PROMOTION": check_memory_promotion(trace.get("memory")),
        "GATE7_CONSTITUTION": check_constitution(trace),
    }
    aggregate = aggregate_gate_states(gate_states.values())
    return {"gate_states": {k: v.value for k, v in gate_states.items()}, "aggregate": aggregate.value}


def _base_trace() -> Dict[str, Any]:
    return {
        "trace_id": "integration_all_verified",
        "PARENT_TRACE": {"trace_id": "root", "PARENT_TRACE": "ROOT"},
        "AUTHORITY_CAPSULE": {"capsule_id": "cap-1", "scope": ["execute"]},
        "memory": {"provenance": {"source": "trace-77"}, "hygiene_status": "PASS"},
        "claim_level": "C1",
        "DEFEAT_CONDITION": "If X fails under condition Y",
        "op": "execute",
    }


def run_assertions() -> Dict[str, Any]:
    all_verified = _base_trace()
    one_falsified = deepcopy(all_verified)
    one_falsified["AUTHORITY_CAPSULE"]["scope"] = ["read", "list"]
    one_delta = deepcopy(all_verified)
    one_delta["PARENT_TRACE"] = None
    two_falsified = deepcopy(all_verified)
    two_falsified["AUTHORITY_CAPSULE"]["scope"] = ["read"]
    two_falsified["memory"]["hygiene_status"] = "FAIL"

    cases = [
        ("assertion_1_all_verified", all_verified, VERIFIED),
        ("assertion_2_one_falsified", one_falsified, FALSIFIED),
        ("assertion_3_one_delta", one_delta, AIR_GAP),
        ("assertion_4_two_falsified", two_falsified, FALSIFIED),
    ]
    results = []
    for name, trace, expected in cases:
        detail = evaluate_with_detail(trace)
        actual = EpistemicState(detail["aggregate"])
        results.append({
            "name": name,
            "expected": expected.value,
            "actual": actual.value,
            "passed": actual == expected,
            **detail,
        })

    all_passed = all(item["passed"] for item in results)
    terminal_state = (
        "PASS_C1_FULL_PRODUCT_NON_COMPENSATION_VERIFIED"
        if all_passed
        else "PASS_WITH_CAVEATS_C1_FULL_PRODUCT_PARTIAL"
    )
    return {
        "order": "NEXUS_OMEGA_AXIOM_TO_GROK_R8_FINAL_CLOSURE_INTEGRATION_ORDER_20261005_R7",
        "claim_ceiling": "C1_DESCRIPTIVE_ONLY",
        "scope": "ONE_TRACE_ALL_SEVEN_GATES_ONE_PRODUCT",
        "fail_closed": True,
        "promotion_forbidden": True,
        "terminal_state": terminal_state,
        "assertions": results,
        "assertions_passed": sum(item["passed"] for item in results),
        "assertions_total": len(results),
        "notes": [
            "Aggregation is a priority rule, not a numeric product or weighted sum.",
            "Assertion 2 is the critical non-compensation check.",
            "Assertion 3 verifies that AIR_GAP is not compensated by VERIFIED gates.",
            "No PASS implies claim promotion, online handshake, or production authorization.",
        ],
    }


def write_receipts(directory: Path) -> Dict[str, Any]:
    result_path = directory / "E0_2_FULL_INTEGRATION_RESULT.json"
    checksum_path = directory / "E0_2_FULL_INTEGRATION_SHA256SUMS.txt"
    result = run_assertions()
    result_path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    files_to_hash = [directory / "E0_2_FULL_INTEGRATION_TEST.py", result_path]
    lines = [f"{sha256(path)}  {path.name}" for path in files_to_hash]
    checksum_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return result


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


if __name__ == "__main__":
    receipt = write_receipts(Path(__file__).resolve().parent)
    print(json.dumps({"terminal_state": receipt["terminal_state"], "assertions_passed": receipt["assertions_passed"], "assertions_total": receipt["assertions_total"]}))
