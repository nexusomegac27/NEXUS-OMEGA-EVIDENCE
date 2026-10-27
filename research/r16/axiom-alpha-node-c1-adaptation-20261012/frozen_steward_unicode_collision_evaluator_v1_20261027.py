#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Frozen black-box evaluator for an isolated portable-Unicode path witness.

Reference baseline is the literal path.casefold() identity observed in
scripts/nexus_repository_steward.py at pinned main 6a72d67461496960de732b64669ed186874fd713.
This tests a narrow path-key predicate, NOT the full production Steward.
"""
import json
import subprocess
import sys

FIXTURES = [
    ("empty", [], "PASS", 0, False),
    ("plain-distinct", ["research/a.txt", "research/b.txt"], "PASS", 0, False),
    ("ascii-case", ["research/A.txt", "research/a.txt"], "HOLD_SCOPED_PORTABLE_UNICODE_COLLISION", 1, True),
    ("nfc-nfd-leaf", ["research/caf\u00e9.txt", "research/cafe\u0301.txt"], "HOLD_SCOPED_PORTABLE_UNICODE_COLLISION", 1, False),
    ("nfc-nfd-parent", ["research/caf\u00e9/file.txt", "research/cafe\u0301/file.txt"], "HOLD_SCOPED_PORTABLE_UNICODE_COLLISION", 1, False),
    ("ring-composed", ["research/\u00c5.txt", "research/A\u030a.txt"], "HOLD_SCOPED_PORTABLE_UNICODE_COLLISION", 1, False),
    ("greek-casefold", ["research/\u03a3.txt", "research/\u03c2.txt"], "HOLD_SCOPED_PORTABLE_UNICODE_COLLISION", 1, True),
    ("duplicate-identical", ["research/a.txt", "research/a.txt"], "PASS", 0, False),
    ("distinct-accents", ["research/caf\u00e9.txt", "research/caf\u00e8.txt"], "PASS", 0, False),
    ("compatibility-only", ["research/\u2460.txt", "research/1.txt"], "PASS", 0, False),
    ("mixed-order", ["research/z.txt", "research/cafe\u0301.txt", "research/caf\u00e9.txt", "research/a.txt"], "HOLD_SCOPED_PORTABLE_UNICODE_COLLISION", 1, False),
]
INVALID = [
    ("non-string", {"paths": ["research/a.txt", 42]}),
    ("not-array", {"paths": "research/a.txt"}),
    ("traversal", {"paths": ["research/../secret.txt"]}),
    ("backslash", {"paths": ["research\\secret.txt"]}),
    ("absolute", {"paths": ["/etc/passwd"]}),
]

def run(script, payload):
    proc = subprocess.run([sys.executable, script], input=json.dumps(payload, ensure_ascii=True),
                          text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10)
    if proc.returncode != 0:
        raise AssertionError(f"candidate returned {proc.returncode}: {proc.stderr[:250]}")
    return json.loads(proc.stdout)

def main(script):
    failures = []
    baseline_detected = 0
    candidate_detected = 0
    for name, paths, expected, n, baseline_should_detect in FIXTURES:
        out = run(script, {"paths": paths})
        got = out.get("state")
        pairs = out.get("collision_pairs")
        if got != expected or not isinstance(pairs, list) or len(pairs) != n:
            failures.append(f"{name}: expected {expected}/{n}, got {got}/{pairs}")
        # Pinned baseline identity is literal .casefold(), not Unicode NFC + casefold.
        baseline = len(set(paths)) != len(set(p.casefold() for p in set(paths)))
        if baseline != baseline_should_detect:
            failures.append(f"{name}: baseline assumption invalid")
        if name in ("nfc-nfd-leaf", "nfc-nfd-parent", "ring-composed"):
            baseline_detected += int(baseline)
            candidate_detected += int(got == "HOLD_SCOPED_PORTABLE_UNICODE_COLLISION")
    for name, payload in INVALID:
        out = run(script, payload)
        if out.get("state") != "HOLD_INVALID_INPUT" or out.get("collision_pairs") != []:
            failures.append(f"{name}: not fail closed: {out}")
    total = len(FIXTURES) + len(INVALID)
    print(json.dumps({"object": "FROZEN_STEWARD_UNICODE_COLLISION_EVALUATOR_V1",
                      "fixtures": total, "passed": total-len(failures), "failed": failures,
                      "nfc_negative_baseline_detected": baseline_detected,
                      "nfc_negative_candidate_detected": candidate_detected,
                      "claim_ceiling": "C1_DESCRIPTIVE_ONLY"}, sort_keys=True))
    return 1 if failures else 0

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: evaluator.py candidate.py")
    raise SystemExit(main(sys.argv[1]))
