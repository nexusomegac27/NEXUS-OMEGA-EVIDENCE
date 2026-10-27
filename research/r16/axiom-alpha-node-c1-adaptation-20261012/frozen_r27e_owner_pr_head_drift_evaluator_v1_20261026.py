#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Frozen independent synthetic evaluator for R27-E PR-head pagination drift.
Run: python frozen_r27e_owner_pr_head_drift_evaluator_v1_20261026.py PATH_TO_V2
Synthetic boundary checks do not prove atomicity or authenticated API reads.
"""
import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest

PATH = Path(sys.argv[1]).resolve()
HEAD, DRIFT = 'a'*40, 'b'*40
V1 = 'alpha_r27e_owner_pr_pagination_candidate_v1_20261026.py'

def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

v2, v1 = load(PATH, 'v2'), load(PATH.with_name(V1), 'v1')
sys.argv = sys.argv[:1]

def fixture(n, state, change=False):
    rows = [{'filename': f'research/r16/f_{i}.md', 'status':'added'} for i in range(n)]
    def page(i):
        if change and i == 2: state['head'] = DRIFT
        return rows[(i-1)*100:i*100]
    return page

def run(n=128, state=None, change=False, actor='nexusomegac27', allow=()):
    state = state if state is not None else {'head': HEAD}
    return v2.enumerate_pr_files_with_boundary_recheck(fetch_page=fixture(n,state,change),
        fetch_head=lambda: state['head'], actor=actor, owner='nexusomegac27',
        external_allowlist=allow, expected_count=n, expected_head_sha=HEAD)

class Frozen(unittest.TestCase):
    def test_legacy_accepts_midflight_drift(self):
        state = {'head':HEAD}
        out = v1.enumerate_pr_files(fetch_page=fixture(128,state,True),
            actor='nexusomegac27', owner='nexusomegac27', external_allowlist=(),
            expected_count=128, expected_head_sha=HEAD, observed_head_sha=HEAD)
        self.assertEqual((len(out),state['head']), (128,DRIFT))
    def test_v2_rejects_midflight_drift(self):
        with self.assertRaisesRegex(ValueError,'HEAD_DRIFT'): run(change=True)
    def test_owner_128(self):
        out=run()
        self.assertEqual(len(out['files']),128)
        self.assertEqual(out['atomic_snapshot'],'NOT_ESTABLISHED')
    def test_owner_200(self): self.assertEqual(len(run(200)['files']),200)
    def test_external_unregistered(self):
        with self.assertRaises(ValueError): run(2,actor='unknown')
    def test_external_8_denied(self):
        with self.assertRaises(ValueError): run(8,actor='expert',allow=('expert',))
    def test_external_7_allowed(self):
        self.assertEqual(len(run(7,actor='expert',allow=('expert',))['files']),7)
    def test_preflight_head_drift(self):
        with self.assertRaisesRegex(ValueError,'HEAD_DRIFT'): run(state={'head':DRIFT})
    def test_pinned_v1_missing(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/PATH.name
            p.write_bytes(PATH.read_bytes())
            other=load(p,'missing_v1')
            with self.assertRaisesRegex(ValueError,'PINNED_V1'):
                other.enumerate_pr_files_with_boundary_recheck(fetch_page=fixture(2,{'head':HEAD}),
                    fetch_head=lambda:HEAD,actor='nexusomegac27',owner='nexusomegac27',
                    external_allowlist=(),expected_count=2,expected_head_sha=HEAD)
    def test_boundary_read_count(self):
        reads=[]
        out=v2.enumerate_pr_files_with_boundary_recheck(fetch_page=fixture(128,{'head':HEAD}),
            fetch_head=lambda:reads.append(HEAD) or HEAD, actor='nexusomegac27',
            owner='nexusomegac27',external_allowlist=(),expected_count=128,
            expected_head_sha=HEAD)
        self.assertEqual((len(reads),len(out['files'])),(2,128))

if __name__=='__main__': unittest.main(verbosity=1)
