#!/usr/bin/env python3
"""Precommitted black-box tests for the isolated census stdin budget guard.

Checks are specified independently of the candidate implementation and only
inspect process status/output; they do not import candidate internals.
"""
import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

DIR = Path(__file__).resolve().parent
CANDIDATE = Path(os.environ.get('AXIOM_CANDIDATE', str(DIR / 'alpha_handoff_census_input_bound_v1_20261026.py')))
BASELINE = DIR / 'alpha_handoff_coverage_census_v3_20261026.py'
LIMIT = 1_048_576


def payload():
    return {'schema_version': 2, 'records': [
        {'id': 'a', 'scope': 'PUBLIC', 'accessible': True, 'authorized': True,
         'routine': True, 'automated': True, 'outcome': 'SUCCESS',
         'source_readback': 'MATCH', 'publication_readback': 'MATCH'},
        {'id': 'b', 'scope': 'PUBLIC', 'accessible': True, 'authorized': True,
         'routine': True, 'automated': False, 'outcome': 'FAILED',
         'source_readback': 'GAP', 'publication_readback': 'GAP'}]}


def execute(program, raw):
    return subprocess.run([sys.executable, str(program)], input=raw,
                          capture_output=True, timeout=10)


class FrozenInputBoundOracle(unittest.TestCase):
    def test_normal_matches_v3_exact_output(self):
        raw = json.dumps(payload()).encode()
        old, new = execute(BASELINE, raw), execute(CANDIDATE, raw)
        self.assertEqual((old.returncode, new.returncode), (0, 0))
        self.assertEqual(new.stdout, old.stdout)
        self.assertEqual(json.loads(new.stdout)['sample_rate'], '1/2')

    def test_negative_large_valid_json_baseline_accepts_candidate_rejects(self):
        raw = b'{"schema_version":2,"records":[]}' + b' ' * LIMIT
        old, new = execute(BASELINE, raw), execute(CANDIDATE, raw)
        self.assertEqual(old.returncode, 0)
        self.assertEqual(new.returncode, 2)
        self.assertIn(b'INPUT_BYTE_LIMIT_EXCEEDED', new.stderr)
        self.assertEqual(new.stdout, b'')

    def test_boundary_exact_limit_accepted(self):
        raw = b'{"schema_version":2,"records":[]}'
        raw += b' ' * (LIMIT - len(raw))
        result = execute(CANDIDATE, raw)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)['sample_rate'], 'NOT_COMPUTABLE_ZERO_DENOMINATOR')

    def test_boundary_plus_one_rejected(self):
        raw = b'{"schema_version":2,"records":[]}'
        raw += b' ' * (LIMIT + 1 - len(raw))
        self.assertEqual(execute(CANDIDATE, raw).returncode, 2)

    def test_oversized_invalid_payload_rejected_before_parse(self):
        result = execute(CANDIDATE, b'X' * (LIMIT + 5))
        self.assertEqual(result.returncode, 2)
        self.assertIn(b'INPUT_BYTE_LIMIT_EXCEEDED', result.stderr)

    def test_invalid_utf8_fail_closed(self):
        self.assertEqual(execute(CANDIDATE, b'\xff').returncode, 2)

    def test_duplicate_json_keys_fail_closed(self):
        raw = b'{"schema_version":2,"records":[],"records":[]}'
        self.assertEqual(execute(CANDIDATE, raw).returncode, 2)

    def test_nonfinite_fail_closed(self):
        self.assertEqual(execute(CANDIDATE, b'{"schema_version":2,"records":[NaN]}').returncode, 2)

    def test_duplicate_ids_fail_closed(self):
        p = payload()
        p['records'][1]['id'] = 'a'
        self.assertEqual(execute(CANDIDATE, json.dumps(p).encode()).returncode, 2)

    def test_unknown_eligibility_still_withheld(self):
        p = payload()
        p['records'][1]['authorized'] = None
        x = execute(CANDIDATE, json.dumps(p).encode())
        self.assertEqual(x.returncode, 0, x.stderr)
        self.assertEqual(json.loads(x.stdout)['sample_rate'], 'WITHHELD_UNKNOWN_ELIGIBILITY')

    def test_private_with_unknown_still_excluded(self):
        p = payload()
        p['records'][1].update(scope='PRIVATE', accessible=False, authorized=None)
        x = execute(CANDIDATE, json.dumps(p).encode())
        self.assertEqual(x.returncode, 0, x.stderr)
        self.assertEqual(json.loads(x.stdout)['sample_rate'], '1/1')

    def test_claim_ceiling_and_no_project_rate(self):
        x = execute(CANDIDATE, json.dumps(payload()).encode())
        self.assertEqual(x.returncode, 0)
        y = json.loads(x.stdout)
        self.assertEqual((y['project_rate'], y['evidence_class'], y['claim_ceiling']),
                         ('NOT_COMPUTABLE', 'UNVERIFIED_SAMPLE_ONLY', 'C1_DESCRIPTIVE_ONLY'))


if __name__ == '__main__':
    unittest.main()
