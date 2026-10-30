#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Isolated C1 receipt-byte preflight, no network, GitHub authentication or writes.

Reads strict JSON on stdin with caller-supplied original bytes as Base64 and
caller-supplied GitHub API blob SHA-1. Derives physical byte lengths and hashes.
Does NOT establish that the bytes were fetched from the stated GitHub commit.
"""
import base64
import binascii
import hashlib
import json
import re
import sys

OBJECT = 'NEXUS_OMEGA_ALPHA_ISSUE93_RECEIPT_BYTE_PREFLIGHT_V1'
REPO = 'nexusomegac27/NEXUS-OMEGA-EVIDENCE'
ROOT = 'research/r16/axiom-alpha-node-c1-adaptation-20261012/'
HEX40 = re.compile(r'[0-9a-f]{40}\Z')
HEX64 = re.compile(r'[0-9a-f]{64}\Z')
PATH = re.compile(r'[A-Za-z0-9_./-]+\Z')


class Fail(Exception):
    pass


def strict_pairs(pairs):
    d = {}
    for key, value in pairs:
        if key in d:
            raise Fail('DUPLICATE_JSON_KEY')
        d[key] = value
    return d


def valid_path(path):
    return (isinstance(path, str) and path.startswith(ROOT)
            and PATH.fullmatch(path) is not None and len(path) <= 240
            and all(part not in ('', '.', '..') for part in path.split('/')))


def evaluate(doc):
    if not isinstance(doc, dict) or doc.get('object') != OBJECT:
        raise Fail('INVALID_OBJECT')
    if doc.get('repository') != REPO:
        raise Fail('INVALID_REPOSITORY')
    if not isinstance(doc.get('commit_sha'), str) or not HEX40.fullmatch(doc['commit_sha']):
        raise Fail('INVALID_COMMIT')
    files = doc.get('files')
    if not isinstance(files, list) or not 1 <= len(files) <= 20:
        raise Fail('INVALID_FILES')
    seen, output, total = set(), [], 0
    for entry in files:
        if not isinstance(entry, dict) or not valid_path(entry.get('path')):
            raise Fail('INVALID_PATH')
        path = entry['path']
        if path in seen:
            raise Fail('DUPLICATE_PATH')
        seen.add(path)
        if entry.get('status') != 'added':
            raise Fail('INVALID_STATUS')
        blob = entry.get('api_blob_sha1')
        if not isinstance(blob, str) or not HEX40.fullmatch(blob):
            raise Fail('INVALID_API_BLOB')
        content = entry.get('content_base64')
        if not isinstance(content, str) or len(content) > 1398104:
            raise Fail('INVALID_BASE64')
        try:
            raw = base64.b64decode(content, validate=True)
        except (ValueError, binascii.Error):
            raise Fail('INVALID_BASE64')
        if len(raw) > 1048576 or total + len(raw) > 1048576:
            raise Fail('BYTE_LIMIT')
        total += len(raw)
        actual_sha = hashlib.sha256(raw).hexdigest()
        actual_blob = hashlib.sha1(b'blob ' + str(len(raw)).encode('ascii') + b'\0' + raw).hexdigest()
        if actual_blob != blob:
            raise Fail('GIT_BLOB_MISMATCH')
        if 'claimed_bytes' in entry:
            claimed = entry['claimed_bytes']
            if type(claimed) is not int or claimed < 0:
                raise Fail('INVALID_CLAIMED_BYTES')
            if claimed != len(raw):
                raise Fail('BYTE_COUNT_MISMATCH')
        if 'claimed_sha256' in entry:
            claimed_sha = entry['claimed_sha256']
            if not isinstance(claimed_sha, str) or not HEX64.fullmatch(claimed_sha):
                raise Fail('INVALID_CLAIMED_SHA256')
            if claimed_sha != actual_sha:
                raise Fail('SHA256_MISMATCH')
        output.append({'path': path, 'bytes': len(raw), 'sha256': actual_sha,
                       'git_blob_sha1': actual_blob})
    return {'object': OBJECT, 'repository': REPO, 'commit_sha': doc['commit_sha'],
            'provenance': 'CALLER_SUPPLIED_BYTES_AND_BLOB_NOT_GITHUB_AUTHENTICATED',
            'claim_ceiling': 'C1_DESCRIPTIVE_ONLY', 'files': output,
            'total_bytes': total}


def main():
    try:
        raw = sys.stdin.buffer.read(1600000)
        if len(raw) >= 1600000:
            raise Fail('INPUT_LIMIT')
        try:
            doc = json.loads(raw.decode('utf-8'), object_pairs_hook=strict_pairs)
        except (ValueError, UnicodeError):
            raise Fail('INVALID_JSON')
        result = evaluate(doc)
    except Fail as exc:
        print('FAIL_CLOSED: ' + str(exc), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=True, sort_keys=True, separators=(',', ':')))
    return 0

if __name__ == '__main__':
    sys.exit(main())
