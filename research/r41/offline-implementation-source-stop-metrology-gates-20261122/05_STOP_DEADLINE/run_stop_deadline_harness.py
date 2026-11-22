#!/usr/bin/env python3
"""R41 P2 offline harness: reproduce R37 tail defect class, prove repaired gate.

Produces JSON receipt under this directory. No device I/O.
"""

from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from stop_deadline_gate import (
    deadline_reached,
    mutant_inverted,
    should_accept_sample,
    ungated_historical_accept,
)

HERE = Path(__file__).resolve().parent
PERIOD_NS = 10_000_000  # 100 Hz
DEADLINE_NS = 60_000_000_000  # 60 s
TAIL_SAMPLES = 363
TAIL_SPAN_NS = 3_622_217_000  # R37 reported ~3.622217 s


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def count_accepts(fn, deadline: int, samples: list[int]) -> int:
    return sum(1 for t in samples if fn(deadline, t))


def main() -> int:
    pre = [i * PERIOD_NS for i in range(5990)]  # 59.90 s
    post = [DEADLINE_NS + i * PERIOD_NS for i in range(TAIL_SAMPLES)]
    # ensure span covers reported tail
    assert post[-1] - DEADLINE_NS >= TAIL_SPAN_NS - PERIOD_NS

    repaired_pre = count_accepts(should_accept_sample, DEADLINE_NS, pre)
    repaired_post = count_accepts(should_accept_sample, DEADLINE_NS, post)
    historical_post = count_accepts(ungated_historical_accept, DEADLINE_NS, post)
    mutant_post = count_accepts(mutant_inverted, DEADLINE_NS, post)

    exact = should_accept_sample(DEADLINE_NS, DEADLINE_NS)
    reached = deadline_reached(DEADLINE_NS, DEADLINE_NS)

    checks = {
        "repaired_pre_all_accepted": repaired_pre == len(pre),
        "repaired_post_all_rejected": repaired_post == 0,
        "historical_post_all_accepted_defect": historical_post == len(post),
        "mutant_post_accepts_defect": mutant_post == len(post),
        "exact_deadline_rejected": exact is False,
        "deadline_reached_at_exact": reached is True,
        "negative_mutant_diverges": mutant_post != repaired_post,
    }
    hard_fails = [k for k, v in checks.items() if not v]

    receipt = {
        "object": "NEXUS_OMEGA_CURSOR_R41_STOP_DEADLINE_OFFLINE_HARNESS_20261122_R0",
        "claim_ceiling": "C1_DESCRIPTIVE_ONLY",
        "physical": "ALT_D_DO_NOT_RUN_ACTIVE",
        "device_capture": False,
        "utc": datetime.now(timezone.utc).isoformat(),
        "parameters": {
            "deadline_ns": DEADLINE_NS,
            "period_ns": PERIOD_NS,
            "pre_samples": len(pre),
            "post_samples": len(post),
            "r37_tail_span_ns_reference": TAIL_SPAN_NS,
        },
        "counts": {
            "repaired_pre_accepted": repaired_pre,
            "repaired_post_accepted": repaired_post,
            "historical_post_accepted": historical_post,
            "mutant_post_accepted": mutant_post,
        },
        "checks": checks,
        "hard_fails": hard_fails,
        "verdict": "PASS" if not hard_fails else "FAIL",
        "epistemic_walls": [
            "OFFLINE_HARNESS_PASS != PHYSICAL_OPPO_PASS",
            "REPAIRED_GATE != BODYTWIN_VALIDATED",
            "SYNTHETIC_363_TAIL != DEVICE_CAPTURE",
        ],
    }

    out = HERE / "STOP_DEADLINE_HARNESS_RECEIPT.json"
    out.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"verdict": receipt["verdict"], "receipt": str(out), "sha256": sha256_file(out)}))
    return 0 if not hard_fails else 1


if __name__ == "__main__":
    sys.exit(main())
