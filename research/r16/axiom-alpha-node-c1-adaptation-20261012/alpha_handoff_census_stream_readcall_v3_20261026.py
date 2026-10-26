#!/usr/bin/env python3
"""C1 research-only V3: bounded bytes AND read() invocations.

An adversarial short-read stream can force many read() calls without crossing
its byte budget. The call cap is a synthetic research guard, not a measured
production threshold. Census V3 semantics and predecessor remain unchanged.
"""
import json
import sys
from alpha_handoff_coverage_census_v3_20261026 import census, nonfinite, unique_pairs

MAX_INPUT_BYTES = 1_048_576
READ_CHUNK = 65_536
MAX_READ_CALLS = 4096


def bounded_read(stdin):
    raw = bytearray()
    calls = 0
    while True:
        if calls >= MAX_READ_CALLS:
            raise ValueError('INPUT_READ_CALL_LIMIT_EXCEEDED')
        budget = MAX_INPUT_BYTES + 1 - len(raw)
        part = stdin.read(min(READ_CHUNK, budget))
        calls += 1
        if part is None:
            raise ValueError('INPUT_STREAM_INCOMPLETE')
        if not isinstance(part, bytes):
            raise TypeError('INPUT_STREAM_NONBYTES')
        if not part:
            break
        raw.extend(part)
        if len(raw) > MAX_INPUT_BYTES:
            raise ValueError('INPUT_BYTE_LIMIT_EXCEEDED')
    return bytes(raw)


def run(stdin=None, stdout=None, stderr=None):
    stdin = sys.stdin.buffer if stdin is None else stdin
    stdout = sys.stdout if stdout is None else stdout
    stderr = sys.stderr if stderr is None else stderr
    try:
        raw = bounded_read(stdin)
        payload = json.loads(raw.decode('utf-8', errors='strict'),
                             object_pairs_hook=unique_pairs, parse_constant=nonfinite)
        print(json.dumps(census(payload), sort_keys=True, separators=(',', ':')), file=stdout)
        return 0
    except (ValueError, TypeError, UnicodeError, RecursionError, OSError) as exc:
        print('FAIL_CLOSED: ' + str(exc), file=stderr)
        return 2


if __name__ == '__main__':
    sys.exit(run())
