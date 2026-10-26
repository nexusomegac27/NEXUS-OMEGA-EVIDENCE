#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""C1 isolated successor to v1: require an observed unittest.TestResult.

This adapter runs only separately audited, SHA256-pinned evaluator scripts.
It preserves their bytes, does not change their assertions, and instruments
unittest.main in a child Python process. The resulting structured telemetry
is evidence of that child process's test runner, not hostile-code attestation.
"""
import argparse
import hashlib
import json
import re
import secrets
import subprocess
import sys
from pathlib import Path

HEX = re.compile(r'^[0-9a-f]{64}$')
# The nonce separates harness telemetry from accidental evaluator output.
# It is NOT a cryptographic attestation of a malicious evaluator process.
CHILD_BOOTSTRAP = r'''
import json, runpy, sys, unittest
script, nonce = sys.argv[1], sys.argv[2]
script_args = sys.argv[3:]
original = unittest.main
records = []
def instrumented_main(*args, **kwargs):
    kwargs['exit'] = False
    program = original(*args, **kwargs)
    result = getattr(program, 'result', None)
    records.append({'tests_run': getattr(result, 'testsRun', None),
                    'successful': bool(result.wasSuccessful()) if result is not None else False})
    return program
unittest.main = instrumented_main
sys.argv = [script] + script_args
try:
    runpy.run_path(script, run_name='__main__')
finally:
    sys.stderr.write('\nNEXUS_RUN_RESULT_' + nonce + '=' + json.dumps(records, separators=(',', ':')) + '\n')
'''


def assess(script: Path, expected_sha256: str, expected_tests: int,
           evaluator_args: list[str], timeout: int = 20) -> dict:
    out = {'object': 'NEXUS_ALPHA_UNITTEST_EXECUTION_PROVENANCE_GUARD_V2',
           'status': 'FAIL_CLOSED', 'reason': 'NOT_EXECUTED',
           'expected_tests': expected_tests, 'observed_tests': None}
    if not HEX.fullmatch(expected_sha256):
        out['reason'] = 'INVALID_EXPECTED_SHA256'
        return out
    if type(expected_tests) is not int or not 1 <= expected_tests <= 10000:
        out['reason'] = 'INVALID_EXPECTED_TEST_COUNT'
        return out
    if type(timeout) is not int or not 1 <= timeout <= 60:
        out['reason'] = 'INVALID_TIMEOUT'
        return out
    try:
        raw = script.read_bytes()
    except OSError:
        out['reason'] = 'PINNED_EVALUATOR_NOT_READABLE'
        return out
    if hashlib.sha256(raw).hexdigest() != expected_sha256:
        out['reason'] = 'PINNED_EVALUATOR_HASH_MISMATCH'
        return out
    nonce = secrets.token_hex(16)
    args = evaluator_args[1:] if evaluator_args[:1] == ['--'] else evaluator_args
    try:
        result = subprocess.run([sys.executable, '-I', '-c', CHILD_BOOTSTRAP,
                                 str(script.resolve()), nonce, *args],
                                cwd=str(script.resolve().parent), capture_output=True,
                                text=True, timeout=timeout, errors='replace')
    except subprocess.TimeoutExpired:
        out['reason'] = 'EVALUATOR_TIMEOUT'
        return out
    except OSError:
        out['reason'] = 'EVALUATOR_EXECUTION_FAILED'
        return out
    try:
        after = hashlib.sha256(script.read_bytes()).hexdigest()
    except OSError:
        out['reason'] = 'EVALUATOR_DISAPPEARED'
        return out
    if after != expected_sha256:
        out['reason'] = 'EVALUATOR_CHANGED_DURING_EXECUTION'
        return out
    if len(result.stderr) + len(result.stdout) > 1_000_000:
        out['reason'] = 'EVALUATOR_OUTPUT_TOO_LARGE'
        return out
    prefix = 'NEXUS_RUN_RESULT_' + nonce + '='
    records = [line[len(prefix):] for line in result.stderr.splitlines()
               if line.startswith(prefix)]
    if result.returncode != 0:
        out['reason'] = 'NONZERO_EVALUATOR_EXIT'
        return out
    if len(records) != 1:
        out['reason'] = 'MISSING_OR_AMBIGUOUS_RUNNER_TELEMETRY'
        return out
    try:
        events = json.loads(records[0])
    except (ValueError, TypeError):
        out['reason'] = 'INVALID_RUNNER_TELEMETRY'
        return out
    if not isinstance(events, list) or len(events) != 1:
        out['reason'] = 'UNITTEST_RUNNER_NOT_CALLED_EXACTLY_ONCE'
        return out
    event = events[0]
    if not isinstance(event, dict) or set(event) != {'tests_run', 'successful'}:
        out['reason'] = 'INVALID_RUNNER_EVENT'
        return out
    observed = event['tests_run']
    out['observed_tests'] = observed
    if type(observed) is not int or observed != expected_tests:
        out['reason'] = 'UNITTEST_COUNT_MISMATCH'
    elif event['successful'] is not True:
        out['reason'] = 'UNITTEST_ACTUAL_RESULT_FAILED'
    else:
        out['status'] = 'PASS_ISOLATED'
        out['reason'] = 'UNITTEST_RESULT_OBJECT_MATCH'
    return out


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument('--script', type=Path, required=True)
    p.add_argument('--sha256', required=True)
    p.add_argument('--expected-tests', type=int, required=True)
    p.add_argument('--timeout', type=int, default=20)
    p.add_argument('evaluator_args', nargs=argparse.REMAINDER)
    args = p.parse_args()
    result = assess(args.script, args.sha256, args.expected_tests,
                    args.evaluator_args, args.timeout)
    print(json.dumps(result, sort_keys=True))
    return 0 if result['status'] == 'PASS_ISOLATED' else 1


if __name__ == '__main__':
    sys.exit(main())
