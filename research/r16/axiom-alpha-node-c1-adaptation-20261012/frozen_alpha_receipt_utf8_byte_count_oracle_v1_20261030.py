#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""C1 frozen regression oracle for UTF-8 byte-count vs Unicode character-count.

Exercises the pre-existing, unchanged Oct-28 digest witness as a subprocess.
Synthetic fixtures only; GitHub API source identity must be checked separately.
No network, writes to repository, or production integration.
"""
import base64
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parent
WITNESS = ROOT / 'alpha_receipt_file_digest_witness_v1_20261028.py'
OBJECT = 'NEXUS_OMEGA_ALPHA_RECEIPT_FILE_DIGEST_WITNESS_V1'
REPO = 'nexusomegac27/NEXUS-OMEGA-EVIDENCE'
COMMIT = '91b0a6d800bce25208c1137fb087c25e1846e089'
PATH = 'research/r16/axiom-alpha-node-c1-adaptation-20261012/synthetic_unicode_fixture.md'


def fixture(raw, claimed=None):
    actual_sha = hashlib.sha256(raw).hexdigest()
    blob = hashlib.sha1(b'blob ' + str(len(raw)).encode('ascii') + b'\0' + raw).hexdigest()
    return {'object': OBJECT, 'repository': REPO, 'commit_sha': COMMIT,
            'commit_files': [{'filename': PATH, 'status': 'added', 'sha': blob}],
            'receipt_files': [{'path': PATH, 'bytes': len(raw) if claimed is None else claimed,
                               'sha256': actual_sha, 'git_blob_sha1': blob}],
            'original_bytes_b64': [{'path': PATH, 'content_base64':
                                    base64.b64encode(raw).decode('ascii')}]}


def run(doc, raw_json=None):
    payload = json.dumps(doc, ensure_ascii=False) if raw_json is None else raw_json
    return subprocess.run([sys.executable, str(WITNESS)], input=payload,
                          capture_output=True, text=True, timeout=5)


class Utf8ByteCountOracle(unittest.TestCase):
    def assert_reject(self, doc, code):
        p = run(doc)
        self.assertEqual(p.returncode, 2, p.stdout + p.stderr)
        self.assertIn('FAIL_CLOSED: ' + code, p.stderr)

    def test_01_ascii_control(self):
        p = run(fixture(b'abc\n'))
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual(json.loads(p.stdout)['files'][0]['bytes'], 4)

    def test_02_unicode_true_byte_count_passes(self):
        raw = ('a' * 6076 + '\u2014\u00b7').encode('utf-8')
        self.assertEqual((len(raw), len(raw.decode('utf-8'))), (6081, 6078))
        p = run(fixture(raw, 6081))
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual(json.loads(p.stdout)['files'][0]['bytes'], 6081)

    def test_03_unicode_character_count_fails_closed(self):
        text = 'a' * 6076 + '\u2014\u00b7'
        self.assertEqual(len(text), 6078)  # naive character-count baseline
        self.assert_reject(fixture(text.encode('utf-8'), len(text)), 'BYTE_COUNT_MISMATCH')

    def test_04_ascii_wrong_count_fails_closed(self):
        self.assert_reject(fixture(b'abc\n', 3), 'BYTE_COUNT_MISMATCH')

    def test_05_same_byte_length_mutation_detected(self):
        d = fixture(b'abc\n')
        d['original_bytes_b64'][0]['content_base64'] = base64.b64encode(b'axc\n').decode('ascii')
        self.assert_reject(d, 'SHA256_MISMATCH')

    def test_06_wrong_blob_detected(self):
        d = fixture(b'abc\n')
        d['receipt_files'][0]['git_blob_sha1'] = '0' * 40
        self.assert_reject(d, 'GIT_BLOB_MISMATCH')

    def test_07_wrong_sha256_detected(self):
        d = fixture(b'abc\n')
        d['receipt_files'][0]['sha256'] = '0' * 64
        self.assert_reject(d, 'SHA256_MISMATCH')

    def test_08_duplicate_json_key_detected(self):
        d = fixture(b'abc\n')
        raw = json.dumps(d).replace('"object": ', '"object": "spoof", "object": ', 1)
        p = run(d, raw_json=raw)
        self.assertEqual(p.returncode, 2)
        self.assertIn('DUPLICATE_JSON_KEY', p.stderr)

    def test_09_invalid_base64_detected(self):
        d = fixture(b'abc\n')
        d['original_bytes_b64'][0]['content_base64'] = '!'
        self.assert_reject(d, 'INVALID_BASE64')

    def test_10_boolean_count_detected(self):
        d = fixture(b'abc\n')
        d['receipt_files'][0]['bytes'] = True
        self.assert_reject(d, 'INVALID_DECLARED_BYTE_COUNT')

    def test_11_non_additive_status_detected(self):
        d = fixture(b'abc\n')
        d['commit_files'][0]['status'] = 'modified'
        self.assert_reject(d, 'UNEXPECTED_COMMIT_STATUS')

    def test_12_missing_original_detected(self):
        d = fixture(b'abc\n')
        d['original_bytes_b64'] = []
        self.assert_reject(d, 'INVALID_ORIGINAL_COUNT')


if __name__ == '__main__':
    unittest.main(verbosity=2)
