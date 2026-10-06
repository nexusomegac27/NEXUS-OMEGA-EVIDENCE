#!/usr/bin/env python3
"""
E0.2 GATE5 — Authority Capsule
Order: NEXUS_OMEGA_AXIOM_TO_GROK_E0_2_GATE4_TO_GATE7_ORDER_20261005_R5
C1_DESCRIPTIVE_ONLY · Fail-closed
"""

from typing import Any, Dict, List, Optional
from enum import Enum
import json
from datetime import datetime, timezone

class EpistemicState(Enum):
    VERIFIED = 1
    FALSIFIED = 0
    AIR_GAP = "Δ"

def check_authority(trace: Dict[str, Any], required_op: str = "execute") -> EpistemicState:
    """
    GATE5: Authority capsule must be present and scope must cover the operation.
    Missing capsule → FALSIFIED
    Scope does not contain operation → FALSIFIED
    Valid capsule + scope contains op → VERIFIED (for this gate)
    """
    if not isinstance(trace, dict):
        return EpistemicState.FALSIFIED

    capsule = trace.get("AUTHORITY_CAPSULE")
    if capsule is None:
        return EpistemicState.FALSIFIED

    if not isinstance(capsule, dict):
        return EpistemicState.FALSIFIED

    # Minimal required fields (hash-linked style, simplified)
    if "capsule_id" not in capsule or "scope" not in capsule:
        return EpistemicState.FALSIFIED

    scope = capsule.get("scope")
    if not isinstance(scope, (list, set, tuple)):
        return EpistemicState.FALSIFIED

    if required_op not in scope:
        return EpistemicState.FALSIFIED

    # Optional: parent hash presence (not strictly required for this minimal gate)
    return EpistemicState.VERIFIED

def run_tests() -> dict:
    cases = {}

    # B1: no capsule
    t1 = {"trace_id": "t1", "op": "execute"}
    r1 = check_authority(t1)
    cases["B1_missing_capsule"] = {
        "state": r1.value if isinstance(r1.value, (int, str)) else str(r1.value),
        "expected": "FALSIFIED",
        "pass": r1 == EpistemicState.FALSIFIED
    }

    # B2: valid capsule, scope covers
    t2 = {
        "trace_id": "t2",
        "AUTHORITY_CAPSULE": {
            "capsule_id": "cap-001",
            "scope": ["execute", "read"],
            "parent_capsule_hash": "abc"
        }
    }
    r2 = check_authority(t2, required_op="execute")
    cases["B2_valid_scope"] = {
        "state": r2.value if isinstance(r2.value, (int, str)) else str(r2.value),
        "expected": "VERIFIED",
        "pass": r2 == EpistemicState.VERIFIED
    }

    # B3: capsule present but scope does not cover
    t3 = {
        "trace_id": "t3",
        "AUTHORITY_CAPSULE": {
            "capsule_id": "cap-002",
            "scope": ["read", "list"],
            "parent_capsule_hash": "def"
        }
    }
    r3 = check_authority(t3, required_op="execute")
    cases["B3_scope_mismatch"] = {
        "state": r3.value if isinstance(r3.value, (int, str)) else str(r3.value),
        "expected": "FALSIFIED",
        "pass": r3 == EpistemicState.FALSIFIED
    }

    all_pass = all(c["pass"] for c in cases.values())
    return {
        "gate": "GATE5_AUTHORITY",
        "order": "NEXUS_OMEGA_AXIOM_TO_GROK_E0_2_GATE4_TO_GATE7_ORDER_20261005_R5",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "claim_ceiling": "C1_DESCRIPTIVE_ONLY",
        "cases": cases,
        "all_pass": all_pass,
        "terminal_state": "PASS_C1_GATE5" if all_pass else "FAIL_C1_GATE5",
        "note": "Authority attenuation only; no amplification. Minimal capsule check."
    }

if __name__ == "__main__":
    report = run_tests()
    print(json.dumps(report, indent=2, ensure_ascii=False))
