#!/usr/bin/env python3
from __future__ import annotations

def decision_function(errors: list[str]) -> str:
    return "C1.2_CLOSED" if errors else "C1.1_ARTIFACT_VALIDATED_STRUCTURE_ONLY"
