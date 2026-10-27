#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""C1 isolated guard for a pinned unittest evaluator using exit=False.

A Python unittest.main(exit=False) can return process status 0 after test
failures. This adapter checks the actual unittest summary and fails closed.
It does NOT change any existing evaluator, assert scientific validity, or
execute untrusted code: only run a previously audited, hash-pinned script.
"""
import argparse
import ast
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

SUMMARY = re.compile(r"^Ran ([0-9]+) tests? in [0-9]+(?:\.[0-9]+)?s$")
HEX = re.compile(r"^[0-9a-f]{64}$")


def assess(script: Path, expected_sha256: str, expected_tests: int,
           evaluator_args: list[str], timeout: int = 20) -> dict:
    out = {"object": "NEXUS_ALPHA_UNITTEST_PROCESS_RESULT_GUARD_V1",
           "status": "FAIL_CLOSED", "reason": "NOT_EXECUTED",
           "expected_tests": expected_tests, "observed_tests": None}
    if not HEX.fullmatch(expected_sha256):
        out["reason"] = "INVALID_EXPECTED_SHA256"
        return out
    if type(expected_tests) is not int or not 1 <= expected_tests <= 10000:
        out["reason"] = "INVALID_EXPECTED_TEST_COUNT"
        return out
    if type(timeout) is not int or not 1 <= timeout <= 60:
        out["reason"] = "INVALID_TIMEOUT"
        return out
    try:
        raw = script.read_bytes()
    except OSError:
        out["reason"] = "PINNED_EVALUATOR_NOT_READABLE"
        return out
    if hashlib.sha256(raw).hexdigest() != expected_sha256:
        out["reason"] = "PINNED_EVALUATOR_HASH_MISMATCH"
        return out
    args = evaluator_args[1:] if evaluator_args[:1] == ["--"] else evaluator_args
    try:
        result = subprocess.run([sys.executable, "-I", str(script.resolve()), *args],
                                cwd=str(script.resolve().parent), capture_output=True,
                                text=True, timeout=timeout, errors="replace")
    except subprocess.TimeoutExpired:
        out["reason"] = "EVALUATOR_TIMEOUT"
        return out
    except OSError:
        out["reason"] = "EVALUATOR_EXECUTION_FAILED"
        return out
    try:
        after = hashlib.sha256(script.read_bytes()).hexdigest()
    except OSError:
        out["reason"] = "EVALUATOR_DISAPPEARED"
        return out
    if after != expected_sha256:
        out["reason"] = "EVALUATOR_CHANGED_DURING_EXECUTION"
        return out
    transcript = result.stderr + "\n" + result.stdout
    if len(transcript) > 1_000_000:
        out["reason"] = "EVALUATOR_OUTPUT_TOO_LARGE"
        return out
    lines = transcript.splitlines()
    summaries = [(i, int(m.group(1))) for i, line in enumerate(lines)
                 if (m := SUMMARY.fullmatch(line.strip()))]
    if len(summaries) != 1:
        out["reason"] = "MISSING_OR_AMBIGUOUS_UNITTEST_SUMMARY"
        return out
    # Reject transcripts fabricated by scripts that never call unittest.main.
    # This is a narrow structural preflight, NOT a proof of nonmalicious code.
    try:
        tree = ast.parse(raw.decode("utf-8"))
    except (SyntaxError, UnicodeError):
        out["reason"] = "INVALID_EVALUATOR_SOURCE"
        return out
    mains = [n for n in ast.walk(tree) if isinstance(n, ast.Call)
             and isinstance(n.func, ast.Attribute) and n.func.attr == "main"
             and isinstance(n.func.value, ast.Name) and n.func.value.id == "unittest"]
    if len(mains) != 1:
        out["reason"] = "UNITTEST_ENTRYPOINT_NOT_ESTABLISHED"
        return out
    idx, observed = summaries[0]
    out["observed_tests"] = observed
    verdict = [line.strip() for line in lines[idx + 1:] if line.strip()]
    if result.returncode != 0:
        out["reason"] = "NONZERO_EVALUATOR_EXIT"
    elif observed != expected_tests:
        out["reason"] = "UNITTEST_COUNT_MISMATCH"
    elif verdict != ["OK"] or any("FAILED" in line for line in lines):
        out["reason"] = "UNITTEST_FAILURE_OR_AMBIGUOUS_VERDICT"
    else:
        out["status"] = "PASS_ISOLATED"
        out["reason"] = "UNITTEST_SUMMARY_AND_EXIT_MATCH"
    return out


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--script", type=Path, required=True)
    p.add_argument("--sha256", required=True)
    p.add_argument("--expected-tests", type=int, required=True)
    p.add_argument("--timeout", type=int, default=20)
    p.add_argument("evaluator_args", nargs=argparse.REMAINDER)
    args = p.parse_args()
    result = assess(args.script, args.sha256, args.expected_tests,
                    args.evaluator_args, args.timeout)
    print(json.dumps(result, sort_keys=True))
    return 0 if result["status"] == "PASS_ISOLATED" else 1


if __name__ == "__main__":
    sys.exit(main())
