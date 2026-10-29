#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Frozen independent black-box oracle for F0 source identity collision checks.

Subprocess-only. Does not import, change, or approve the candidate.
"""
import base64
import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest

CANDIDATE = Path(os.environ.get('AXIOM_CANDIDATE', Path(__file__).with_name('alpha_source_graph_identity_f0_v2_20261029.py')))
OBJECT = 'NEXUS_OMEGA_ALPHA_SOURCE_GRAPH_CLOSURE_F0_V1'
REPO = 'nexusomegac27/NEXUS-OMEGA-EVIDENCE'


def node(name, text, requires=(), path=None, commit=None):
    raw = text.encode('utf-8')
    return {'id': name, 'requires': list(requires), 'commit': commit or 'a'*40,
            'path': path or f'research/r16/{name}.txt', 'bytes': len(raw),
            'sha256': hashlib.sha256(raw).hexdigest(),
            'git_blob': hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\x00'+raw).hexdigest(),
            'content_b64': base64.b64encode(raw).decode('ascii'),
            'public_safe': True, 'rights_cleared': True}


def fixture():
    return {'object': OBJECT, 'repository': REPO, 'target': 'task',
            'nodes': [node('task', 'order', ['a', 'b']),
                      node('a', 'source-a'), node('b', 'source-b')]}


def invoke(doc):
    raw = doc if isinstance(doc, bytes) else json.dumps(doc, separators=(',', ':')).encode()
    return subprocess.run([sys.executable, '-B', str(CANDIDATE)], input=raw,
                          capture_output=True, timeout=8)


class FrozenOracle(unittest.TestCase):
    def accept(self, doc, count):
        p = invoke(doc)
        self.assertEqual(p.returncode, 0, p.stderr.decode(errors='replace'))
        result = json.loads(p.stdout)
        self.assertEqual(result['nodes_checked'], count)
        self.assertFalse(result['api_origin_authenticated'])
        self.assertFalse(result['receiver_ack_established'])
        self.assertEqual(result['ready_for_expert'], 'NOT_ESTABLISHED')
        self.assertEqual(result['claim_ceiling'], 'C1_DESCRIPTIVE_ONLY')
    def reject(self, doc, reason):
        p = invoke(doc)
        self.assertEqual(p.returncode, 2, p.stdout.decode(errors='replace'))
        self.assertIn(reason.encode(), p.stderr)

    def test_01_distinct_sources_accepted(self):
        self.accept(fixture(), 3)
    def test_02_same_source_same_bytes_accepted(self):
        x=fixture();x['nodes'][2]=node('b','source-a',path=x['nodes'][1]['path']);self.accept(x,3)
    def test_03_same_path_different_commit_accepted(self):
        x=fixture();x['nodes'][2]=node('b','source-b',path=x['nodes'][1]['path'],commit='b'*40);self.accept(x,3)
    def test_04_same_commit_different_path_accepted(self):
        self.accept(fixture(),3)
    def test_05_single_node_accepted(self):
        x=fixture();x['nodes']=[node('task','single')];self.accept(x,1)
    def test_06_same_identity_different_bytes_rejected(self):
        x=fixture();x['nodes'][2]=node('b','other',path=x['nodes'][1]['path']);self.reject(x,'CONFLICTING_SOURCE_IDENTITY')
    def test_07_same_identity_equal_size_different_bytes_rejected(self):
        x=fixture();x['nodes'][2]=node('b','SOURCE-A',path=x['nodes'][1]['path']);self.reject(x,'CONFLICTING_SOURCE_IDENTITY')
    def test_08_same_identity_empty_vs_nonempty_rejected(self):
        x=fixture();x['nodes'][2]=node('b','',path=x['nodes'][1]['path']);self.reject(x,'CONFLICTING_SOURCE_IDENTITY')
    def test_09_three_way_identity_conflict_rejected(self):
        x=fixture();x['nodes'][0]['requires']=['a','b','c'];x['nodes'].append(node('c','source-a',path=x['nodes'][1]['path']));x['nodes'][2]=node('b','changed',path=x['nodes'][1]['path']);self.reject(x,'CONFLICTING_SOURCE_IDENTITY')
    def test_10_missing_parent_rejected(self):
        x=fixture();x['nodes'].pop();self.reject(x,'REQUIRED_SOURCE_NOT_PRESENT')
    def test_11_cycle_rejected(self):
        x=fixture();x['nodes'][1]['requires']=['task'];self.reject(x,'CYCLIC_SOURCE_GRAPH')
    def test_12_sha_mismatch_rejected(self):
        x=fixture();x['nodes'][1]['sha256']='f'*64;self.reject(x,'SOURCE_SHA256_MISMATCH')
    def test_13_blob_mismatch_rejected(self):
        x=fixture();x['nodes'][1]['git_blob']='f'*40;self.reject(x,'SOURCE_GIT_BLOB_MISMATCH')
    def test_14_duplicate_json_key_rejected(self):
        self.reject(b'{"object":1,"object":2}','DUPLICATE_JSON_KEY')
    def test_15_private_rejected(self):
        x=fixture();x['nodes'][1]['public_safe']=False;self.reject(x,'SOURCE_NOT_PUBLIC_SAFE')
    def test_16_traversal_rejected(self):
        x=fixture();x['nodes'][1]['path']='../secret';self.reject(x,'UNSAFE_SOURCE_PATH')
    def test_17_unpinned_commit_rejected(self):
        x=fixture();x['nodes'][1]['commit']='main';self.reject(x,'UNPINNED_COMMIT')
    def test_18_invalid_target_rejected(self):
        x=fixture();x['target']='missing';self.reject(x,'TARGET_NOT_PRESENT')

if __name__=='__main__':
    unittest.main()
