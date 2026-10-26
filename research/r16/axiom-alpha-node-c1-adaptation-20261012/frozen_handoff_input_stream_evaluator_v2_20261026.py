#!/usr/bin/env python3
"""Frozen black-box C1 tests for partial-read census input integrity V2.

Independent process boundaries: candidate is only executed by subprocess.
This evaluator never imports candidate functions or rewrites historical oracles.
"""
import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

DIR = Path(__file__).resolve().parent
CANDIDATE = Path(os.environ.get('AXIOM_CANDIDATE', str(DIR / 'alpha_handoff_census_stream_integrity_v2_20261026.py')))
V1 = DIR / 'alpha_handoff_census_input_bound_v1_20261026.py'
LIMIT = 1_048_576
VALID = b'{"schema_version":2,"records":[]}'
INJECT = r"""
import importlib.util, sys
from pathlib import Path
path, mode = sys.argv[1:3]
sys.path.insert(0, str(Path(path).parent))
spec = importlib.util.spec_from_file_location('candidate_under_test', path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
valid = b'{"schema_version":2,"records":[]}'
limit = 1048576
class Stream:
    def __init__(self):
        if mode == 'oversize':
            self.parts = [valid, b' ' * (limit + 1)]
        elif mode == 'trailing':
            self.parts = [valid, b'{"unexpected":1}']
        elif mode == 'valid_chunks':
            self.parts = [valid[:2], valid[2:17], valid[17:]]
        elif mode == 'oserror':
            self.parts = [valid[:4]]
        elif mode == 'none':
            self.parts = [valid[:4]]
        else:
            raise RuntimeError('UNKNOWN_FIXTURE')
        self.calls = 0
    def read(self, n):
        self.calls += 1
        if mode == 'oserror' and self.calls == 2:
            raise OSError('SYNTHETIC_IO_FAILURE')
        if mode == 'none' and self.calls == 2:
            return None
        if not self.parts:
            return b''
        p = self.parts.pop(0)
        if len(p) > n:
            self.parts.insert(0, p[n:])
            return p[:n]
        return p
sys.exit(module.run(stdin=Stream()))
"""


def cli(program, raw):
    return subprocess.run([sys.executable, str(program)], input=raw,
                          capture_output=True, timeout=10)


def injected(program, mode):
    return subprocess.run([sys.executable, '-c', INJECT, str(program), mode],
                          capture_output=True, timeout=10)


class FrozenStreamIntegrityOracle(unittest.TestCase):
    def test_01_normal_cli_matches_original_v1(self):
        a, b = cli(V1, VALID), cli(CANDIDATE, VALID)
        self.assertEqual((a.returncode, b.returncode), (0, 0))
        self.assertEqual(a.stdout, b.stdout)

    def test_02_exact_limit_accepted(self):
        raw = VALID + b' ' * (LIMIT - len(VALID))
        x = cli(CANDIDATE, raw)
        self.assertEqual(x.returncode, 0, x.stderr)

    def test_03_limit_plus_one_rejected(self):
        x = cli(CANDIDATE, VALID + b' ' * (LIMIT + 1 - len(VALID)))
        self.assertEqual(x.returncode, 2)
        self.assertIn(b'INPUT_BYTE_LIMIT_EXCEEDED', x.stderr)

    def test_04_short_read_oversize_fails_closed(self):
        x = injected(CANDIDATE, 'oversize')
        self.assertEqual(x.returncode, 2, x.stderr)
        self.assertIn(b'INPUT_BYTE_LIMIT_EXCEEDED', x.stderr)
        self.assertEqual(x.stdout, b'')

    def test_05_short_read_trailing_json_rejected(self):
        x = injected(CANDIDATE, 'trailing')
        self.assertEqual(x.returncode, 2, x.stderr)
        self.assertEqual(x.stdout, b'')

    def test_06_valid_short_reads_accepted(self):
        x = injected(CANDIDATE, 'valid_chunks')
        self.assertEqual(x.returncode, 0, x.stderr)
        self.assertEqual(json.loads(x.stdout)['sample_rate'], 'NOT_COMPUTABLE_ZERO_DENOMINATOR')

    def test_07_read_oserror_controlled(self):
        x = injected(CANDIDATE, 'oserror')
        self.assertEqual(x.returncode, 2, x.stderr)
        self.assertIn(b'FAIL_CLOSED: SYNTHETIC_IO_FAILURE', x.stderr)
        self.assertNotIn(b'Traceback', x.stderr)

    def test_08_incomplete_nonblocking_read_controlled(self):
        x = injected(CANDIDATE, 'none')
        self.assertEqual(x.returncode, 2, x.stderr)
        self.assertIn(b'INPUT_STREAM_INCOMPLETE', x.stderr)

    def test_09_deep_json_controlled(self):
        raw = b'{"schema_version":2,"records":' + b'[' * 1500 + b']' * 1500 + b'}'
        x = cli(CANDIDATE, raw)
        self.assertEqual(x.returncode, 2, x.stderr)
        self.assertIn(b'FAIL_CLOSED:', x.stderr)
        self.assertNotIn(b'Traceback', x.stderr)

    def test_10_duplicate_json_key_rejected(self):
        x = cli(CANDIDATE, b'{"schema_version":2,"records":[],"records":[]}')
        self.assertEqual(x.returncode, 2)
        self.assertIn(b'DUPLICATE_JSON_KEY', x.stderr)

    def test_11_nonfinite_json_rejected(self):
        x = cli(CANDIDATE, b'{"schema_version":2,"records":[NaN]}')
        self.assertEqual(x.returncode, 2)
        self.assertIn(b'NONFINITE_JSON', x.stderr)

    def test_12_project_claim_never_computable(self):
        x = cli(CANDIDATE, VALID)
        self.assertEqual(x.returncode, 0)
        data = json.loads(x.stdout)
        self.assertEqual((data['project_rate'], data['claim_ceiling']),
                         ('NOT_COMPUTABLE', 'C1_DESCRIPTIVE_ONLY'))


if __name__ == '__main__':
    unittest.main()
