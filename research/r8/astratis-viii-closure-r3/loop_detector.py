# NEXUS deterministic loop detector C1. Repetition != new evidence.
from __future__ import annotations

from typing import Any, Dict, List, Tuple


def evidence_key(run: Dict[str, Any]) -> Tuple[str, Tuple[str, ...]]:
    method = str(run.get("method_id") or "")
    hashes = tuple(sorted(str(x) for x in (run.get("evidence_hashes") or [])))
    return method, hashes


def detect_loop(runs: List[Dict[str, Any]]) -> Dict[str, Any]:
    """First independent reproduction of the same method+evidence is allowed.
    A later run with the same key and no new_method is LOOP_RISK.
    """
    seen_first = None
    independent_repro = None
    loop_from = None
    for i, run in enumerate(runs):
        key = evidence_key(run)
        if seen_first is None:
            seen_first = (i, key)
            continue
        if key != seen_first[1]:
            continue
        if independent_repro is None and run.get("independent") is True:
            independent_repro = i
            continue
        if run.get("new_method") is True:
            continue
        loop_from = i
        break
    if loop_from is not None:
        return {
            "loop_risk": "DETECTED",
            "new_evidence": "NO_NEW_EVIDENCE",
            "next": "NEW_METHOD_OR_HOLD",
            "first_index": seen_first[0] if seen_first else None,
            "independent_reproduction_index": independent_repro,
            "loop_index": loop_from,
        }
    if independent_repro is not None:
        return {
            "loop_risk": "NOT_DETECTED_AFTER_FIRST_INDEPENDENT_REPRODUCTION_ONLY",
            "new_evidence": "INDEPENDENT_REPRODUCTION_COMPLETE",
            "next": "NEW_METHOD_OR_HOLD_FOR_FURTHER_REPEATS",
            "first_index": seen_first[0] if seen_first else None,
            "independent_reproduction_index": independent_repro,
            "loop_index": None,
        }
    return {
        "loop_risk": "NOT_DETECTED",
        "new_evidence": "INSUFFICIENT_RUNS_FOR_REPRODUCTION",
        "next": "AWAIT_INDEPENDENT_REPRODUCTION",
        "first_index": seen_first[0] if seen_first else None,
        "independent_reproduction_index": None,
        "loop_index": None,
    }
