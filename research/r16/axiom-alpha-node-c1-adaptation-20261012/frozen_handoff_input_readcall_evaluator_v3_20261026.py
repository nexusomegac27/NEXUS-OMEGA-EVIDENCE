#!/usr/bin/env python3
"""Frozen, subprocess-only C1 evaluator for bounded short-read call budgets.

A byte cap does not imply a bound on read() invocations when each read yields
one byte. Tests do not modify the candidate, its predecessor, or GitHub.
"""
import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

DIR = Path(__file__).resolve().parent
V2 = DIR / 'alpha_handoff_census_stream_integrity_v2_20261026.py'
CANDIDATE = Path(os.environ.get('AXIOM_CANDIDATE', str(DIR / 'alpha_handoff_census_stream_readcall_v3_20261026.py')))
VALID = b'{"schema_version":2,"records":[]}'
LIMIT = 1_048_576
CALL_LIMIT = 4096

INJECT = r'''
import importlib.util, sys
from pathlib import Path
path, mode = sys.argv[1:3]
sys.path.insert(0, str(Path(path).parent))
spec = importlib.util.spec_from_file_location('isolated_candidate', path)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
valid = b'{"schema_version":2,"records":[]}'
class Stream:
    def __init__(self):
        self.calls = 0
        if mode == 'many': self.raw = valid + b' ' * (100000 - len(valid))
        elif mode == 'small_many': self.raw = valid + b' ' * (1000 - len(valid))
        elif mode == 'trailing': self.raw = valid + b'{"unexpected":1}'
        else: self.raw = valid
        self.offset = 0
    def read(self, n):
        self.calls += 1
        if mode == 'none' and self.calls == 2: return None
        if mode == 'oserror' and self.calls == 2: raise OSError('SYNTHETIC_IO_FAILURE')
        if mode == 'nonbytes': return 'not bytes'
        if self.offset >= len(self.raw): return b''
        if mode in ('many','small_many','none','oserror'):
            n = min(n, 1)
        chunk = self.raw[self.offset:self.offset+n]
        self.offset += len(chunk)
        return chunk
s = Stream()
status = m.run(stdin=s)
print('CALLS='+str(s.calls), file=sys.stderr)
sys.exit(status)
'''


def cli(program, raw):
    return subprocess.run([sys.executable, str(program)], input=raw,
                          capture_output=True, timeout=15)


def injected(program, mode):
    return subprocess.run([sys.executable, '-c', INJECT, str(program), mode],
                          capture_output=True, timeout=15)


def calls(proc):
    for line in proc.stderr.decode('utf-8').splitlines():
        if line.startswith('CALLS='):
            return int(line.split('=', 1)[1])
    raise AssertionError('MISSING_CALL_COUNT')


class FrozenReadCallBudgetOracle(unittest.TestCase):
    def test_01_predecessor_accepts_100k_single_byte_reads(self):
        x = injected(V2, 'many')
        self.assertEqual(x.returncode, 0, x.stderr)
        self.assertEqual(calls(x), 100001)

    def test_02_candidate_rejects_100k_single_byte_reads(self):
        x = injected(CANDIDATE, 'many')
        self.assertEqual(x.returncode, 2, x.stderr)
        self.assertIn(b'INPUT_READ_CALL_LIMIT_EXCEEDED', x.stderr)
        self.assertLessEqual(calls(x), CALL_LIMIT)
        self.assertEqual(x.stdout, b'')

    def test_03_1000_single_byte_reads_still_accepted(self):
        x = injected(CANDIDATE, 'small_many')
        self.assertEqual(x.returncode, 0, x.stderr)
        self.assertEqual(calls(x), 1001)
        self.assertEqual(json.loads(x.stdout)['project_rate'], 'NOT_COMPUTABLE')

    def test_04_normal_cli_matches_predecessor(self):
        a, b = cli(V2, VALID), cli(CANDIDATE, VALID)
        self.assertEqual((a.returncode, b.returncode), (0, 0))
        self.assertEqual(a.stdout, b.stdout)

    def test_05_exact_byte_limit_accepted(self):
        x = cli(CANDIDATE, VALID + b' ' * (LIMIT-len(VALID)))
        self.assertEqual(x.returncode, 0, x.stderr)

    def test_06_over_byte_limit_rejected(self):
        x = cli(CANDIDATE, VALID + b' ' * (LIMIT+1-len(VALID)))
        self.assertEqual(x.returncode, 2, x.stderr)
        self.assertIn(b'INPUT_BYTE_LIMIT_EXCEEDED', x.stderr)

    def test_07_duplicate_json_key_rejected(self):
        x = cli(CANDIDATE, b'{"schema_version":2,"records":[],"records":[]}')
        self.assertEqual(x.returncode, 2)
        self.assertIn(b'DUPLICATE_JSON_KEY', x.stderr)

    def test_08_nonfinite_json_rejected(self):
        x = cli(CANDIDATE, b'{"schema_version":2,"records":[NaN]}')
        self.assertEqual(x.returncode, 2)
        self.assertIn(b'NONFINITE_JSON', x.stderr)

    def test_09_incomplete_read_fails_closed(self):
        x = injected(CANDIDATE, 'none')
        self.assertEqual(x.returncode, 2)
        self.assertIn(b'INPUT_STREAM_INCOMPLETE', x.stderr)

    def test_10_read_oserror_fails_closed(self):
        x = injected(CANDIDATE, 'oserror')
        self.assertEqual(x.returncode, 2)
        self.assertIn(b'SYNTHETIC_IO_FAILURE', x.stderr)
        self.assertNotIn(b'Traceback', x.stderr)

    def test_11_nonbyte_read_fails_closed(self):
        x = injected(CANDIDATE, 'nonbytes')
        self.assertEqual(x.returncode, 2)
        self.assertIn(b'INPUT_STREAM_NONBYTES', x.stderr)

    def test_12_trailing_json_rejected(self):
        x = injected(CANDIDATE, 'trailing')
        self.assertEqual(x.returncode, 2)
        self.assertEqual(x.stdout, b'')

    def test_13_empty_project_not_promoted(self):
        x = cli(CANDIDATE, VALID)
        self.assertEqual(x.returncode, 0)
        y = json.loads(x.stdout)
        self.assertEqual((y['project_rate'], y['claim_ceiling']),
                         ('NOT_COMPUTABLE','C1_DESCRIPTIVE_ONLY'))


if __name__ == '__main__':
    unittest.main()
