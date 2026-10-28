#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Frozen subprocess-only oracle for v3 scope readback, synthetic inputs."""
import json
import os
import subprocess
import sys
import unittest

TARGET = os.environ.get('AXIOM_CANDIDATE', 'alpha_handoff_readback_scope_adapter_v3_20261028.py')


def payload(coverage='DECLARED_COMPLETE', readback=True):
    e = dict(id='h1', channel='PUBLIC_GITHUB', routine=True, authorized=True,
             accessible=True, published=True, automatic=True,
             commit_readback=True, source_readback=True, test_readback=True,
             receipt_readback=readback, unauthorized_write=False,
             hidden_source_gap=False, source_overwrite=False, claim_promotion=False)
    return dict(object='NEXUS_OMEGA_ALPHA_HANDOFF_PAGE_CENSUS_V2',
                repository='nexusomegac27/NEXUS-OMEGA-EVIDENCE',
                scope=dict(scope_id='test', coverage=coverage,
                           source_commit_sha='a'*40, source_manifest_sha256='b'*64),
                pages=[dict(page=1, source_commit_sha='a'*40, reported_total=1,
                            next_page=None, events=[e])])


def invoke(obj):
    p = subprocess.run([sys.executable, TARGET], input=json.dumps(obj).encode(),
                       capture_output=True, timeout=8)
    if p.returncode: raise AssertionError(p.stderr.decode())
    return json.loads(p.stdout)


class Oracle(unittest.TestCase):
    def test_complete(self):
        r=invoke(payload()); self.assertEqual(r['scope_readback_rate'], '1/1')
        self.assertEqual(r['readback_rate'], '1/1')
    def test_partial(self):
        r=invoke(payload('PARTIAL')); self.assertEqual(r['scope_readback_rate'], 'NOT_COMPUTABLE')
        self.assertEqual(r['observed_readback_sample_rate'], '1/1')
    def test_partial_missing_readback(self):
        r=invoke(payload('PARTIAL',False)); self.assertEqual(r['scope_readback_rate'], 'NOT_COMPUTABLE')
        self.assertEqual(r['observed_readback_sample_rate'], '0/1')
    def test_complete_missing_readback(self):
        r=invoke(payload(readback=False)); self.assertEqual(r['scope_readback_rate'], '0/1')
    def test_project_not_claimed(self):
        r=invoke(payload()); self.assertEqual(r['project_readback_rate'], 'NOT_COMPUTABLE')
        self.assertIs(r['source_completeness_authenticated'], False)
    def test_unknown_publication(self):
        x=payload(); x['pages'][0]['events'][0]['channel']='UNKNOWN'
        r=invoke(x); self.assertEqual(r['scope_readback_rate'], 'NOT_COMPUTABLE')


if __name__=='__main__': unittest.main()
