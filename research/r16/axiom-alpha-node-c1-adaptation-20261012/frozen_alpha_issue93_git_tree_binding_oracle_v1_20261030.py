#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Frozen independent synthetic oracle; subprocess-only candidate invocation.

Creates Git object bytes independently, without importing candidate code.
This oracle is not a GitHub authentication or scientific validation test.
"""
import base64
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import unittest

CANDIDATE = Path(__file__).with_name('alpha_issue93_git_tree_binding_preflight_v1_20261030.py')
ROOT = 'research/r16/axiom-alpha-node-c1-adaptation-20261012/'
OBJECT = 'NEXUS_OMEGA_ALPHA_ISSUE93_GIT_TREE_BINDING_PREFLIGHT_V1'
REPO = 'nexusomegac27/NEXUS-OMEGA-EVIDENCE'

def git_oid(kind, raw):
    return hashlib.sha1(kind.encode() + b' ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()

def b64(raw):
    return base64.b64encode(raw).decode('ascii')

def make_fixture(blob=b'abc\n', path=ROOT+'synthetic.md'):
    parts = path.split('/')
    leaf = git_oid('blob', blob)
    chain = []
    target = leaf
    for idx in range(len(parts)-1, -1, -1):
        mode = b'100644' if idx == len(parts)-1 else b'40000'
        tree = mode + b' ' + parts[idx].encode('ascii') + b'\0' + bytes.fromhex(target)
        chain.insert(0, b64(tree))
        target = git_oid('tree', tree)
    commit = (b'tree ' + target.encode('ascii') + b'\nauthor Oracle <oracle@example.invalid> 0 +0000'
              b'\ncommitter Oracle <oracle@example.invalid> 0 +0000\n\nsynthetic\n')
    return {'object': OBJECT, 'repository': REPO,
            'pinned_commit_sha': git_oid('commit', commit), 'commit_base64': b64(commit),
            'path': path, 'tree_chain_base64': chain, 'blob_base64': b64(blob),
            'expected_bytes': len(blob), 'expected_sha256': hashlib.sha256(blob).hexdigest()}

def run(doc, raw=None):
    return subprocess.run([sys.executable, str(CANDIDATE)],
                          input=json.dumps(doc) if raw is None else raw,
                          capture_output=True, text=True, timeout=4)

class FrozenGitTreeBindingOracle(unittest.TestCase):
    def reject(self, d, code, raw=None):
        p = run(d, raw)
        self.assertEqual(p.returncode, 2, p.stdout+p.stderr)
        self.assertIn('FAIL_CLOSED: '+code, p.stderr)
        self.assertEqual(p.stdout, '')

    def test_01_valid_nested_tree_positive(self):
        d = make_fixture()
        p = run(d)
        self.assertEqual(p.returncode, 0, p.stderr)
        o = json.loads(p.stdout)
        self.assertEqual(o['bytes'], 4)
        self.assertTrue(o['git_tree_chain_verified'])
        self.assertIn('NOT_REMOTE_AUTHENTICATED', o['provenance'])

    def test_02_unicode_byte_positive(self):
        d = make_fixture('x—'.encode('utf-8'))
        self.assertEqual(run(d).returncode, 0)

    def test_03_fake_commit_rejected_even_with_matching_blob(self):
        d = make_fixture()
        d['pinned_commit_sha'] = '0'*40
        self.reject(d, 'COMMIT_OID_MISMATCH')

    def test_04_commit_bytes_tamper(self):
        d = make_fixture()
        d['commit_base64'] = b64(base64.b64decode(d['commit_base64']) + b'evil')
        self.reject(d, 'COMMIT_OID_MISMATCH')

    def test_05_tampered_root_tree(self):
        d = make_fixture()
        d['tree_chain_base64'][0] = b64(base64.b64decode(d['tree_chain_base64'][0]) + b'X')
        self.reject(d, 'TREE_OID_MISMATCH')

    def test_06_missing_leaf(self):
        d = make_fixture()
        d['path'] = ROOT + 'absent.md'
        self.reject(d, 'PATH_NOT_IN_TREE')

    def test_07_swapped_blob_same_size(self):
        d = make_fixture(b'abcd')
        d['blob_base64'] = b64(b'WXYZ')
        self.reject(d, 'BLOB_OID_MISMATCH')

    def test_08_wrong_byte_count(self):
        d = make_fixture('x—'.encode('utf-8'))
        d['expected_bytes'] = 2
        self.reject(d, 'BYTE_COUNT_MISMATCH')

    def test_09_wrong_sha256(self):
        d = make_fixture()
        d['expected_sha256'] = '0'*64
        self.reject(d, 'SHA256_MISMATCH')

    def test_10_missing_tree_level(self):
        d = make_fixture()
        d['tree_chain_base64'].pop()
        self.reject(d, 'TREE_CHAIN_LENGTH')

    def test_11_duplicate_json_key(self):
        d = make_fixture()
        raw = json.dumps(d).replace('"object":', '"object":"spoof","object":', 1)
        self.reject(d, 'DUPLICATE_JSON_KEY', raw)

    def test_12_path_traversal(self):
        d = make_fixture()
        d['path'] = ROOT+'../escape.md'
        self.reject(d, 'INVALID_PATH')

    def test_13_invalid_base64(self):
        d = make_fixture()
        d['blob_base64'] = '!'
        self.reject(d, 'INVALID_BASE64')

    def test_14_symlink_tree_mode(self):
        d = make_fixture()
        parts = d['path'].split('/')
        raw = b'120000 ' + parts[-1].encode() + b'\0' + bytes.fromhex(git_oid('blob', b'abc\n'))
        chain = [None]*len(parts)
        chain[-1] = b64(raw)
        target = git_oid('tree', raw)
        for i in range(len(parts)-2, -1, -1):
            tree = b'40000 '+parts[i].encode()+b'\0'+bytes.fromhex(target)
            chain[i] = b64(tree)
            target = git_oid('tree', tree)
        commit = b'tree '+target.encode()+b'\nauthor Oracle <oracle@example.invalid> 0 +0000\n\nsymlink\n'
        d['tree_chain_base64'] = chain
        d['commit_base64'] = b64(commit)
        d['pinned_commit_sha'] = git_oid('commit', commit)
        self.reject(d, 'UNSUPPORTED_TREE_MODE')

    def test_15_nonfinite_extra_json_does_not_claim_github_auth(self):
        d = make_fixture()
        d['untrusted'] = 'owner'
        p = run(d)
        self.assertEqual(p.returncode, 0)
        self.assertIn('NOT_REMOTE_AUTHENTICATED', json.loads(p.stdout)['provenance'])

    def test_16_invalid_tree_entry_truncation(self):
        d = make_fixture()
        parts = d['path'].split('/')
        raw = b'100644 '+parts[-1].encode()+b'\0'+b'123'  # short object id
        chain = [None]*len(parts)
        chain[-1] = b64(raw)
        target = git_oid('tree', raw)
        for i in range(len(parts)-2, -1, -1):
            tree = b'40000 '+parts[i].encode()+b'\0'+bytes.fromhex(target)
            chain[i] = b64(tree)
            target = git_oid('tree', tree)
        commit = b'tree '+target.encode()+b'\nauthor Oracle <oracle@example.invalid> 0 +0000\n\nmalformed\n'
        d['tree_chain_base64'] = chain
        d['commit_base64'] = b64(commit)
        d['pinned_commit_sha'] = git_oid('commit', commit)
        self.reject(d, 'MALFORMED_TREE')

if __name__ == '__main__':
    unittest.main(verbosity=2)
