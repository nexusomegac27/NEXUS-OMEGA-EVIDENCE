#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Frozen, synthetic C1 oracle. Run in a separate subprocess against candidate CLI.

This evaluator must be versioned BEFORE the candidate. No GitHub authentication.
"""
import base64
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import unittest

CANDIDATE = Path(__file__).with_name('alpha_issue93_receipt_byte_preflight_v1_20261030.py')
ROOT = 'research/r16/axiom-alpha-node-c1-adaptation-20261012/'
COMMIT = 'c57b255c983f30674ca037c6f6fe703b8552a1b8'
OBJECT = 'NEXUS_OMEGA_ALPHA_ISSUE93_RECEIPT_BYTE_PREFLIGHT_V1'
REPO = 'nexusomegac27/NEXUS-OMEGA-EVIDENCE'


def file_entry(raw=b'abc\n', path=ROOT + 'synthetic.md'):
    return {'path': path, 'status': 'added',
            'content_base64': base64.b64encode(raw).decode('ascii'),
            'api_blob_sha1': hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()}


def fixture(raw=b'abc\n'):
    return {'object': OBJECT, 'repository': REPO, 'commit_sha': COMMIT,
            'files': [file_entry(raw)]}


def run(doc, raw_json=None):
    return subprocess.run([sys.executable, str(CANDIDATE)],
                          input=json.dumps(doc, ensure_ascii=False) if raw_json is None else raw_json,
                          capture_output=True, text=True, timeout=4)


class FrozenReceiptPreflightOracle(unittest.TestCase):
    def reject(self, doc, code, raw_json=None):
        p = run(doc, raw_json)
        self.assertEqual(p.returncode, 2, p.stdout + p.stderr)
        self.assertIn('FAIL_CLOSED: ' + code, p.stderr)
        self.assertEqual(p.stdout, '')

    def test_01_ascii_positive(self):
        p = run(fixture())
        self.assertEqual(p.returncode, 0, p.stderr)
        o = json.loads(p.stdout)
        self.assertEqual(o['files'][0]['bytes'], 4)
        self.assertEqual(o['files'][0]['sha256'], hashlib.sha256(b'abc\n').hexdigest())
        self.assertEqual(o['provenance'], 'CALLER_SUPPLIED_BYTES_AND_BLOB_NOT_GITHUB_AUTHENTICATED')

    def test_02_unicode_positive(self):
        raw = ('a'*6076 + '\u2014\u00b7').encode('utf-8')
        self.assertEqual((len(raw), len(raw.decode('utf-8'))), (6081, 6078))
        p = run(fixture(raw))
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual(json.loads(p.stdout)['files'][0]['bytes'], 6081)

    def test_03_unicode_character_count_rejected(self):
        text = 'a'*6076 + '\u2014\u00b7'
        d = fixture(text.encode('utf-8'))
        d['files'][0]['claimed_bytes'] = len(text)
        self.assertEqual(len(text), 6078)  # frozen naive baseline: false size accepted
        self.reject(d, 'BYTE_COUNT_MISMATCH')

    def test_04_correct_declared_size(self):
        d = fixture('x\u2014'.encode())
        d['files'][0]['claimed_bytes'] = 4
        self.assertEqual(run(d).returncode, 0)

    def test_05_wrong_sha256(self):
        d = fixture(); d['files'][0]['claimed_sha256'] = '0'*64
        self.reject(d, 'SHA256_MISMATCH')

    def test_06_wrong_api_blob(self):
        d = fixture(); d['files'][0]['api_blob_sha1'] = '0'*40
        self.reject(d, 'GIT_BLOB_MISMATCH')

    def test_07_missing_api_blob(self):
        d = fixture(); del d['files'][0]['api_blob_sha1']
        self.reject(d, 'INVALID_API_BLOB')

    def test_08_invalid_base64(self):
        d = fixture(); d['files'][0]['content_base64'] = '!!'
        self.reject(d, 'INVALID_BASE64')

    def test_09_duplicate_path(self):
        d = fixture(); d['files'].append(d['files'][0].copy())
        self.reject(d, 'DUPLICATE_PATH')

    def test_10_path_traversal(self):
        d = fixture(); d['files'][0]['path'] = ROOT + '../evil.md'
        self.reject(d, 'INVALID_PATH')

    def test_11_wrong_repository(self):
        d = fixture(); d['repository'] = 'other/repo'
        self.reject(d, 'INVALID_REPOSITORY')

    def test_12_invalid_commit(self):
        d = fixture(); d['commit_sha'] = 'main'
        self.reject(d, 'INVALID_COMMIT')

    def test_13_duplicate_json_key(self):
        d = fixture()
        raw = json.dumps(d).replace('"object":', '"object":"spoof","object":', 1)
        self.reject(d, 'DUPLICATE_JSON_KEY', raw)

    def test_14_boolean_claimed_bytes(self):
        d = fixture(); d['files'][0]['claimed_bytes'] = True
        self.reject(d, 'INVALID_CLAIMED_BYTES')

    def test_15_nonadditive_status(self):
        d = fixture(); d['files'][0]['status'] = 'modified'
        self.reject(d, 'INVALID_STATUS')

    def test_16_missing_files(self):
        d = fixture(); d['files'] = []
        self.reject(d, 'INVALID_FILES')

    def test_17_multiple_files_positive(self):
        d = fixture(); d['files'].append(file_entry('\u2014'.encode(), ROOT+'second.md'))
        p = run(d)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual([x['bytes'] for x in json.loads(p.stdout)['files']], [4,3])

    def test_18_noncanonical_unicode_path(self):
        d = fixture(); d['files'][0]['path'] = ROOT+'é.md'
        self.reject(d, 'INVALID_PATH')

    def test_19_non_json(self):
        self.reject({}, 'INVALID_JSON', '{')

    def test_20_wrong_object(self):
        d = fixture(); d['object'] = 'SPOOF'
        self.reject(d, 'INVALID_OBJECT')

if __name__ == '__main__':
    unittest.main(verbosity=2)
