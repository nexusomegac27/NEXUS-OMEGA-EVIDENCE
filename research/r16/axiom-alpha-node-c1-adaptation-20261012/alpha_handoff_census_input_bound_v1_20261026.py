#!/usr/bin/env python3
"""Isolated C1 stdin byte-budget guard for the historical census V3.

This is research-only. The underlying V3 classifications are not modified.
The 1 MiB limit is a proposed operational bound, not an empirical production limit.
"""
import json
import sys
from alpha_handoff_coverage_census_v3_20261026 import census, nonfinite, unique_pairs

MAX_INPUT_BYTES = 1_048_576


def run(stdin=None, stdout=None, stderr=None):
    stdin = sys.stdin.buffer if stdin is None else stdin
    stdout = sys.stdout if stdout is None else stdout
    stderr = sys.stderr if stderr is None else stderr
    try:
        raw = stdin.read(MAX_INPUT_BYTES + 1)
        if len(raw) > MAX_INPUT_BYTES:
            raise ValueError('INPUT_BYTE_LIMIT_EXCEEDED')
        payload = json.loads(raw.decode('utf-8', errors='strict'),
                             object_pairs_hook=unique_pairs, parse_constant=nonfinite)
        print(json.dumps(census(payload), sort_keys=True, separators=(',', ':')), file=stdout)
        return 0
    except (ValueError, TypeError, UnicodeError) as exc:
        print('FAIL_CLOSED: ' + str(exc), file=stderr)
        return 2


if __name__ == '__main__':
    sys.exit(run())
