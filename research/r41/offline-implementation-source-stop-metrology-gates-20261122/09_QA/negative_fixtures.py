#!/usr/bin/env python3
"""R41 P6 — negative fixtures for stop-deadline + gate fail-closed."""
from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

WORKER = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(WORKER / "05_STOP_DEADLINE"))
from stop_deadline_gate import should_accept_sample  # noqa: E402

OUT = Path(__file__).resolve().parent / "NEGATIVE_FIXTURES_RECEIPT.json"


def run_fixture(name: str, fn) -> dict:
    try:
        fn()
        return {"name": name, "status": "PASS_EXPECTED_REJECT", "detail": "rejected_as_designed"}
    except AssertionError as e:
        return {"name": name, "status": "FAIL_UNEXPECTED_ACCEPT", "detail": str(e)}
    except Exception as e:
        return {"name": name, "status": "ERROR", "detail": str(e)}


def fx_exact_deadline_must_reject():
    # Exact equality must reject (deadline exclusive)
    assert should_accept_sample(1_000_000_000, 1_000_000_000) is False


def fx_after_deadline_must_reject():
    assert should_accept_sample(1_000_000_000, 1_000_000_001) is False


def fx_tail_363_all_reject():
    deadline = 59_990_077_000
    # ~363 samples at 10ms after deadline — all must reject
    for i in range(363):
        t = deadline + (i + 1) * 10_000_000
        assert should_accept_sample(deadline, t) is False, f"accepted post-deadline i={i}"


def fx_mutant_leq_would_accept_exact():
    # Document that a <= mutant would falsely accept exact deadline
    deadline = 1_000_000_000
    now = 1_000_000_000
    mutant_accept = now <= deadline  # WRONG semantics
    correct = should_accept_sample(deadline, now)
    assert mutant_accept is True and correct is False


def fx_zero_deadline_accepts():
    assert should_accept_sample(0, 999_999_999_999) is True


def fx_gate_engine_never_claims_14_pass():
    receipt = WORKER / "07_GATES_14" / "GATE_ENGINE_RECEIPT.json"
    assert receipt.is_file(), "gate engine receipt missing — run gate_engine.py first"
    data = json.loads(receipt.read_text(encoding="utf-8"))
    assert data.get("full_14_pass_claim") is False
    assert data.get("physical_auto_clear") is False
    assert data.get("fail_closed") is True
    assert data.get("verdict") == "PASS_ENGINE_FAIL_CLOSED"


def main() -> int:
    fixtures = [
        ("exact_deadline_reject", fx_exact_deadline_must_reject),
        ("after_deadline_reject", fx_after_deadline_must_reject),
        ("tail_363_all_reject", fx_tail_363_all_reject),
        ("mutant_leq_documented", fx_mutant_leq_would_accept_exact),
        ("zero_deadline_accepts", fx_zero_deadline_accepts),
        ("gate_engine_fail_closed", fx_gate_engine_never_claims_14_pass),
    ]
    results = [run_fixture(n, f) for n, f in fixtures]
    fails = [r for r in results if r["status"] != "PASS_EXPECTED_REJECT"]
    receipt = {
        "object": "R41_NEGATIVE_FIXTURES_RECEIPT",
        "recorded_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "claim_ceiling": "C1_DESCRIPTIVE_ONLY",
        "total": len(results),
        "pass": len(results) - len(fails),
        "fail": len(fails),
        "fixtures": results,
        "verdict": "PASS" if not fails else "FAIL",
    }
    text = json.dumps(receipt, indent=2, ensure_ascii=False) + "\n"
    OUT.write_text(text, encoding="utf-8")
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    print(json.dumps({"verdict": receipt["verdict"], "sha256": digest, "path": str(OUT)}))
    return 0 if not fails else 1


if __name__ == "__main__":
    raise SystemExit(main())
