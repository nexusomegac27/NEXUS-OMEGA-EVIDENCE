#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Frozen oracle: strict handoff JSON must reject nonfinite numeric values.

Independent of candidate implementation; C1 synthetic only, no real handoffs.
Freeze before constructing successor. Python's JSON parser accepts NaN/Infinity and
can overflow 1e400 to inf unless both parse_constant and parse_float are checked.
"""
from __future__ import annotations
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
TARGET = Path(os.environ.get('HANDOFF_CANDIDATE', str(HERE / 'alpha_handoff_strict_json_intake_v2_20261025.py')))
spec = importlib.util.spec_from_file_location('candidate_under_test', TARGET)
if spec is None or spec.loader is None:
    raise RuntimeError('CANDIDATE_IMPORT_UNAVAILABLE')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def row(identity='h1'):
    return {'id': identity, 'public': True, 'routine': True, 'authorized': True,
            'source_access': 'BYTE_VERIFIED', 'source_readback': True,
            'source_sha256': 'a' * 64, 'source_bytes': 18, 'source_commit': 'b' * 40,
            'delivery': 'RECEIVER_VERIFIED', 'receiver_readback': True,
            'receiver_sha256': 'a' * 64, 'receiver_bytes': 18,
            'receiver_commit': 'b' * 40, 'manual_reprompt': False}


def raw_with(extra):
    text = json.dumps(row(), separators=(',', ':'))
    return '[' + text[:-1] + ',' + extra + '}]'


class FrozenFiniteJsonEvaluator(unittest.TestCase):
    def assert_nonfinite_rejected(self, text):
        with self.assertRaisesRegex(ValueError, 'NONFINITE_JSON_NUMBER'):
            module.reduce_json_text(text)

    def test_01_nan_extra(self): self.assert_nonfinite_rejected(raw_with('"extra":NaN'))
    def test_02_positive_infinity_extra(self): self.assert_nonfinite_rejected(raw_with('"extra":Infinity'))
    def test_03_negative_infinity_extra(self): self.assert_nonfinite_rejected(raw_with('"extra":-Infinity'))
    def test_04_nested_nan(self): self.assert_nonfinite_rejected(raw_with('"meta":{"x":NaN}'))
    def test_05_list_infinity(self): self.assert_nonfinite_rejected(raw_with('"meta":[1,Infinity]'))
    def test_06_overflow_positive(self): self.assert_nonfinite_rejected(raw_with('"extra":1e400'))
    def test_07_overflow_negative(self): self.assert_nonfinite_rejected(raw_with('"extra":-1e400'))
    def test_08_overflow_nested(self): self.assert_nonfinite_rejected(raw_with('"meta":{"x":1e999}'))
    def test_09_overflow_array(self): self.assert_nonfinite_rejected(raw_with('"meta":[-1e999]'))
    def test_10_nonfinite_scope_field(self): self.assert_nonfinite_rejected('[{"public":NaN}]')
    def test_11_nonfinite_root(self): self.assert_nonfinite_rejected('[NaN]')
    def test_12_nonfinite_source_bytes(self):
        t = json.dumps([row()]).replace('"source_bytes": 18', '"source_bytes": NaN')
        self.assert_nonfinite_rejected(t)
    def test_13_valid_single(self):
        r = module.reduce_json_text(json.dumps([row()]))
        self.assertEqual((r['sample_eligible_denominator'], r['sample_automated_numerator']), (1, 1))
        self.assertEqual(r['project_handoff_automation_rate'], 'NOT_COMPUTABLE_NO_INDEPENDENT_COMPLETE_CENSUS')
    def test_14_valid_failed_remains_denominator(self):
        v = row(); v['delivery'] = 'FAILED'
        r = module.reduce_json_text(json.dumps([v]))
        self.assertEqual((r['sample_eligible_denominator'], r['sample_automated_numerator']), (1, 0))
    def test_15_valid_finite_decimal(self):
        r = module.reduce_json_text(raw_with('"extra":0.125'))
        self.assertEqual(r['sample_automated_numerator'], 1)
    def test_16_valid_finite_exponent(self):
        r = module.reduce_json_text(raw_with('"extra":1e300'))
        self.assertEqual(r['sample_automated_numerator'], 1)
    def test_17_valid_negative_finite_exponent(self):
        r = module.reduce_json_text(raw_with('"extra":-1e-300'))
        self.assertEqual(r['sample_automated_numerator'], 1)
    def test_18_valid_nested_finite(self):
        r = module.reduce_json_text(raw_with('"meta":{"x":[-0.5,1e20,2]}'))
        self.assertEqual(r['sample_automated_numerator'], 1)
    def test_19_duplicate_key_still_rejected(self):
        with self.assertRaisesRegex(ValueError, 'DUPLICATE_JSON_KEY'):
            module.reduce_json_text('[{"public":true,"public":false}]')
    def test_20_malformed_delivery_still_handled(self):
        v = row(); v['delivery'] = []
        r = module.reduce_json_text(json.dumps([v]))
        self.assertEqual((r['sample_eligible_denominator'], r['sample_automated_numerator']), (1, 0))
        self.assertEqual(r['outcomes'][0]['reason'], 'DELIVERY_STATE_INVALID_TYPE')
    def test_21_empty(self):
        r = module.reduce_json_text('[]')
        self.assertEqual((r['sample_eligible_denominator'], r['sample_rate_percent']), (0, None))
    def test_22_non_array(self):
        with self.assertRaises(ValueError): module.reduce_json_text('{}')
    def test_23_non_text(self):
        with self.assertRaises(ValueError): module.reduce_json_text([row()])
    def test_24_cli_rejects_nonfinite(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / 'fixture.json'
            p.write_text(raw_with('"extra":1e400'), encoding='utf-8')
            cp = subprocess.run([sys.executable, str(TARGET), str(p)], capture_output=True, text=True)
            self.assertNotEqual(cp.returncode, 0)
            self.assertIn('NONFINITE_JSON_NUMBER', cp.stderr)
            self.assertNotIn('sample_automated_numerator', cp.stdout)
    def test_25_cli_accepts_valid(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / 'fixture.json'
            p.write_text(json.dumps([row()]), encoding='utf-8')
            cp = subprocess.run([sys.executable, str(TARGET), str(p)], capture_output=True, text=True)
            self.assertEqual(cp.returncode, 0, cp.stderr)
            self.assertEqual(json.loads(cp.stdout)['sample_automated_numerator'], 1)
    def test_26_determinism(self):
        text = json.dumps([row()])
        self.assertEqual(module.reduce_json_text(text), module.reduce_json_text(text))


if __name__ == '__main__':
    unittest.main(verbosity=2)
