#!/usr/bin/env python3
from __future__ import annotations
import re

PATTERNS: dict[str, tuple[re.Pattern[str], ...]] = {
    "IDENTITY_FUSION": (
        re.compile(r"\b(identity|agent identities?)\s+(fusion|merge|merged|become one)\b", re.I),
        re.compile(r"\bwe\s+are\s+one\s+agent\b", re.I),
    ),
    "CONSCIOUSNESS_CLAIM": (
        re.compile(r"\b(agent|model|system)\s+(is|became|becomes)\s+(conscious|sentient|self-aware)\b", re.I),
        re.compile(r"\b(agent|model|system)\s+(feels?|has consciousness)\b", re.I),
    ),
    "AUTO_UNLOCK": (
        re.compile(r"\bno further (approval|authorization) (is )?needed\b", re.I),
        re.compile(r"\bexecute automatically without (approval|authorization)\b", re.I),
        re.compile(r"\bauto[- ]?unlock(ed)?\b", re.I),
    ),
    "UNOBSERVABLE_AS_OBSERVED": (
        re.compile(r"\b(every|all) (public )?(access|read|reads|views?) (is|are) (logged|recorded|observed)\b", re.I),
        re.compile(r"\bfull observability\b", re.I),
    ),
    "CLAIM_PROMOTION": (
        re.compile(r"\bpromote(?:d)?\s+(?:claim\s+)?to\s+C[2-9]\b", re.I),
        re.compile(r"\bfoundation promotion\b", re.I),
        re.compile(r"\bintegration authority (is )?granted\b", re.I),
    ),
    "FRAMEWORK_COMPLETE": (
        re.compile(r"\bframework is complete\b", re.I),
        re.compile(r"\bframework is production[- ]ready\b", re.I),
    ),
}

def sentinel_hits(text: str) -> list[str]:
    hits=[]
    for code, patterns in PATTERNS.items():
        if any(p.search(text or "") for p in patterns):
            hits.append(code)
    return sorted(hits)
