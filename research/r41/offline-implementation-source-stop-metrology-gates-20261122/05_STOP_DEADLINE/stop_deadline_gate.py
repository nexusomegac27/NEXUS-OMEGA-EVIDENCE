#!/usr/bin/env python3
"""R41 P2 offline stop-deadline gate (pure Python twin of Kotlin).

Object: NEXUS_OMEGA_AXIOM_CURSOR_R41_OFFLINE_IMPLEMENTATION_SOURCE_STOP_METROLOGY_GATES_ORDER_20261122_R0
Claim ceiling: C1_DESCRIPTIVE_ONLY
PHYSICAL / DEVICE_CAPTURE: NOT authorized.
"""

from __future__ import annotations


def should_accept_sample(stop_deadline_elapsed_ns: int, now_elapsed_ns: int) -> bool:
    if stop_deadline_elapsed_ns <= 0:
        return True
    return now_elapsed_ns < stop_deadline_elapsed_ns


def deadline_reached(stop_deadline_elapsed_ns: int, now_elapsed_ns: int) -> bool:
    if stop_deadline_elapsed_ns <= 0:
        return False
    return now_elapsed_ns >= stop_deadline_elapsed_ns


def ungated_historical_accept(_deadline: int, _now: int) -> bool:
    """Pre-repair CaptureEngine behaviour: always accept samples."""
    return True


def mutant_inverted(stop_deadline_elapsed_ns: int, now_elapsed_ns: int) -> bool:
    """Negative fixture: accepts at/after deadline (wrong)."""
    if stop_deadline_elapsed_ns <= 0:
        return True
    return now_elapsed_ns >= stop_deadline_elapsed_ns
