#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Frozen independent subprocess F0 oracle; does not import candidate code."""
import base64
import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest

CANDIDATE = Path(os.environ.get('AXIOM_CANDIDATE', Path(__file__).with_name('alpha_source_graph_closure_f0_v1_20261029.py')))

def node(name, content, requires=()):
    raw = content.encode()
    return {'id':name,'requires':list(requires),'commit':'a'*40,
            'path':f'research/r16/{name}.txt','bytes':len(raw),
            'sha256':hashlib.sha256(raw).hexdigest(),
            'git_blob':hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest(),
            'content_b64':base64.b64encode(raw).decode(),
            'public_safe':True,'rights_cleared':True}

def fixture():
    return {'object':'NEXUS_OMEGA_ALPHA_SOURCE_GRAPH_CLOSURE_F0_V1',
            'repository':'nexusomegac27/NEXUS-OMEGA-EVIDENCE',
            'target':'task','nodes':[node('task','order',['manifest']),
                                    node('manifest','index',['source']),
                                    node('source','original')]}

def invoke(x):
    data=x if type(x) is bytes else json.dumps(x).encode()
    return subprocess.run([sys.executable,str(CANDIDATE)],input=data,capture_output=True,timeout=8)

class Oracle(unittest.TestCase):
    def good(self,x):
        p=invoke(x)
        self.assertEqual(p.returncode,0,p.stderr.decode(errors='replace'))
        o=json.loads(p.stdout)
        self.assertEqual(o['ready_for_expert'],'NOT_ESTABLISHED')
        self.assertFalse(o['api_origin_authenticated'])
        self.assertFalse(o['receiver_ack_established'])
        return o
    def bad(self,x,code):
        p=invoke(x)
        self.assertEqual(p.returncode,2,p.stdout.decode(errors='replace'))
        self.assertIn(code.encode(),p.stderr)
    def test_01_valid(self):
        x=self.good(fixture());self.assertEqual((x['nodes_checked'],x['required_edges_checked']),(3,2))
    def test_02_single(self):
        x=fixture();x['nodes']=[node('task','x')];self.good(x)
    def test_03_empty_bytes_valid(self):
        x=fixture();x['nodes'][2]=node('source','');self.good(x)
    def test_04_missing_required_parent(self):
        x=fixture();x['nodes'].pop();self.bad(x,'REQUIRED_SOURCE_NOT_PRESENT')
    def test_05_cycle(self):
        x=fixture();x['nodes'][2]['requires']=['task'];self.bad(x,'CYCLIC_SOURCE_GRAPH')
    def test_06_unreachable(self):
        x=fixture();x['nodes'].append(node('orphan','x'));self.bad(x,'UNREACHABLE_SOURCE_IN_INVENTORY')
    def test_07_sha_mismatch(self):
        x=fixture();x['nodes'][2]['sha256']='f'*64;self.bad(x,'SOURCE_SHA256_MISMATCH')
    def test_08_blob_mismatch(self):
        x=fixture();x['nodes'][2]['git_blob']='f'*40;self.bad(x,'SOURCE_GIT_BLOB_MISMATCH')
    def test_09_size_mismatch(self):
        x=fixture();x['nodes'][2]['bytes']+=1;self.bad(x,'SOURCE_SIZE_MISMATCH')
    def test_10_unpinned(self):
        x=fixture();x['nodes'][2]['commit']='main';self.bad(x,'UNPINNED_COMMIT')
    def test_11_private(self):
        x=fixture();x['nodes'][2]['public_safe']=False;self.bad(x,'SOURCE_NOT_PUBLIC_SAFE')
    def test_12_unlicensed(self):
        x=fixture();x['nodes'][2]['rights_cleared']=False;self.bad(x,'SOURCE_NOT_PUBLIC_SAFE')
    def test_13_traversal(self):
        x=fixture();x['nodes'][2]['path']='../secret';self.bad(x,'UNSAFE_SOURCE_PATH')
    def test_14_duplicate_node(self):
        x=fixture();x['nodes'].append(copy.deepcopy(x['nodes'][2]));self.bad(x,'DUPLICATE_OR_INVALID_NODE_ID')
    def test_15_duplicate_parent(self):
        x=fixture();x['nodes'][0]['requires']=['manifest','manifest'];self.bad(x,'INVALID_PARENT_LIST')
    def test_16_duplicate_json_key(self):
        self.bad(b'{"object":1,"object":2}','DUPLICATE_JSON_KEY')
    def test_17_nonfinite(self):
        self.bad(b'{"object":NaN}','NONFINITE_JSON')
    def test_18_invalid_base64(self):
        x=fixture();x['nodes'][2]['content_b64']='??';self.bad(x,'INVALID_BASE64')
    def test_19_wrong_target(self):
        x=fixture();x['target']='missing';self.bad(x,'TARGET_NOT_PRESENT')
    def test_20_bad_scope(self):
        x=fixture();x['repository']='other/repo';self.bad(x,'INVALID_SCOPE')
    def test_21_bad_claimed_bytes(self):
        x=fixture();x['nodes'][2]['content_b64']=base64.b64encode(b'forged!').decode();self.bad(x,'SOURCE_SIZE_MISMATCH')
    def test_22_bogus_parent_self(self):
        x=fixture();x['nodes'][0]['requires']=['task'];self.bad(x,'CYCLIC_SOURCE_GRAPH')

if __name__=='__main__':
    unittest.main()
