#!/usr/bin/env python3
"""Bounded C1 census intake V4 for untrusted caller-supplied JSON samples.

Limits the raw input to 4 MiB and converts excessively deep JSON into an
explicit scoped failure. The original V3 census classification remains pinned
and unchanged. This is not a GitHub authentication or completeness oracle.
"""
import importlib.util
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
BASELINE = HERE / 'alpha_handoff_coverage_census_v3_20261026.py'
MAX_INPUT_BYTES = 4 * 1024 * 1024


def census_bytes(raw):
    if not isinstance(raw, bytes):
        raise TypeError('INPUT_NOT_BYTES')
    if len(raw) > MAX_INPUT_BYTES:
        raise ValueError('INPUT_TOO_LARGE')
    spec = importlib.util.spec_from_file_location('pinned_census_v3', BASELINE)
    baseline = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(baseline)
    payload = json.loads(raw.decode('utf-8'), object_pairs_hook=baseline.unique_pairs,
                         parse_constant=baseline.nonfinite)
    return baseline.census(payload)


def main():
    try:
        raw = sys.stdin.buffer.read(MAX_INPUT_BYTES + 1)
        print(json.dumps(census_bytes(raw), sort_keys=True, separators=(',', ':')))
        return 0
    except (ValueError, TypeError, UnicodeError, RecursionError) as exc:
        print('FAIL_CLOSED: ' + str(exc), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
