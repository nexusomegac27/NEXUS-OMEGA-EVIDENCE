#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Independent subprocess oracle: externally pinned raw census input bytes.

No candidate imports. Synthetic data only; no GitHub provenance/authentication claim.
"""
import copy
import hashlib
import json
import os
import subprocess
import sys
import unittest

TARGET = os.environ.get('AXIOM_CANDIDATE', 'alpha_handoff_pinned_input_guard_v4_20261028.py')


def fixture(coverage='DECLARED_COMPLETE'):
    e = dict(id='event-001', channel='PUBLIC_GITHUB', routine=True,
             authorized=True, accessible=True, published=True, automatic=True,
             commit_readback=True, source_readback=True, test_readback=True,
             receipt_readback=True, unauthorized_write=False,
             hidden_source_gap=False, source_overwrite=False,
             claim_promotion=False)
    return dict(object='NEXUS_OMEGA_ALPHA_HANDOFF_PAGE_CENSUS_V2',
                repository='nexusomegac27/NEXUS-OMEGA-EVIDENCE',
                scope=dict(scope_id='frozen-synthetic', coverage=coverage,
                           source_commit_sha='a'*40,
                           source_manifest_sha256='b'*64),
                pages=[dict(page=1, source_commit_sha='a'*40,
                            reported_total=1, next_page=None, events=[e])])


def raw(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':')).encode('utf-8')


def run(payload, pin=None, args=None):
    argv = [sys.executable, TARGET] + (args if args is not None else
            ['--expected-sha256', pin or hashlib.sha256(payload).hexdigest()])
    return subprocess.run(argv, input=payload, capture_output=True, timeout=8)


class PinnedInputOracle(unittest.TestCase):
    def test_positive_pinned_complete(self):
        p = run(raw(fixture()))
        self.assertEqual(p.returncode, 0, p.stderr.decode())
        d = json.loads(p.stdout)
        self.assertEqual(d['scope_readback_rate'], '1/1')
        self.assertEqual(d['scope_automation_rate'], '1/1')
        self.assertEqual(d['input_pinned_match'], True)
        self.assertEqual(d['input_bytes'], len(raw(fixture())))
        self.assertEqual(d['project_readback_rate'], 'NOT_COMPUTABLE')
        self.assertEqual(d['source_completeness_authenticated'], False)

    def test_partial_stays_not_computable(self):
        p = run(raw(fixture('PARTIAL')))
        self.assertEqual(p.returncode, 0, p.stderr.decode())
        self.assertEqual(json.loads(p.stdout)['scope_readback_rate'], 'NOT_COMPUTABLE')

    def test_changed_automatic_flag_same_pin_fails(self):
        original = raw(fixture())
        modified = copy.deepcopy(fixture())
        modified['pages'][0]['events'][0]['automatic'] = False
        p = run(raw(modified), hashlib.sha256(original).hexdigest())
        self.assertEqual(p.returncode, 2)
        self.assertIn(b'PINNED_INPUT_SHA256_MISMATCH', p.stderr)
        self.assertEqual(p.stdout, b'')

    def test_changed_readback_flag_same_pin_fails(self):
        original = raw(fixture())
        modified = copy.deepcopy(fixture())
        modified['pages'][0]['events'][0]['receipt_readback'] = False
        p = run(raw(modified), hashlib.sha256(original).hexdigest())
        self.assertEqual(p.returncode, 2)
        self.assertEqual(p.stdout, b'')

    def test_added_whitespace_same_pin_fails(self):
        original = raw(fixture())
        p = run(original+b' ', hashlib.sha256(original).hexdigest())
        self.assertEqual(p.returncode, 2)

    def test_missing_pin_fails(self):
        self.assertEqual(run(raw(fixture()), args=[]).returncode, 2)

    def test_invalid_pin_fails(self):
        self.assertEqual(run(raw(fixture()), args=['--expected-sha256', 'z'*64]).returncode, 2)

    def test_uppercase_pin_fails(self):
        self.assertEqual(run(raw(fixture()), args=['--expected-sha256', 'A'*64]).returncode, 2)

    def test_unexpected_arg_fails(self):
        self.assertEqual(run(raw(fixture()), args=['--expected-sha256', 'a'*64, '--override']).returncode, 2)

    def test_duplicate_json_key_fails(self):
        p = b'{"object":"a","object":"b"}'
        self.assertEqual(run(p).returncode, 2)

    def test_invalid_utf8_fails(self):
        self.assertEqual(run(b'\xff').returncode, 2)

    def test_invalid_repository_fails(self):
        x = fixture(); x['repository'] = 'wrong/repo'
        self.assertEqual(run(raw(x)).returncode, 2)

    def test_oversized_input_fails(self):
        self.assertEqual(run(b'x'*1_048_577).returncode, 2)

    def test_nonfinite_fails(self):
        p = raw(fixture()).replace(b'"reported_total":1', b'"reported_total":NaN')
        self.assertEqual(run(p).returncode, 2)


if __name__ == '__main__':
    unittest.main()
