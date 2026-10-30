#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Offline C1 Git commit/tree/blob linkage check on caller-supplied raw objects.

This does NOT authenticate GitHub origin, actor identity, signatures, or SHA-1
collision resistance. Source retrieval and independent API readback are separate.
"""
import base64
import binascii
import hashlib
import json
import re
import sys

OBJECT = 'NEXUS_OMEGA_ALPHA_ISSUE93_GIT_TREE_BINDING_PREFLIGHT_V1'
REPO = 'nexusomegac27/NEXUS-OMEGA-EVIDENCE'
ROOT = 'research/r16/axiom-alpha-node-c1-adaptation-20261012/'
HEX40 = re.compile(r'[0-9a-f]{40}\Z')
HEX64 = re.compile(r'[0-9a-f]{64}\Z')
PATH = re.compile(r'[A-Za-z0-9_./-]+\Z')

class Fail(Exception):
    pass

def pairs_unique(pairs):
    out = {}
    for k, v in pairs:
        if k in out:
            raise Fail('DUPLICATE_JSON_KEY')
        out[k] = v
    return out

def decode(value, max_bytes):
    if not isinstance(value, str) or len(value) > (max_bytes * 4 // 3 + 8):
        raise Fail('INVALID_BASE64')
    try:
        data = base64.b64decode(value, validate=True)
    except (ValueError, binascii.Error):
        raise Fail('INVALID_BASE64')
    if len(data) > max_bytes:
        raise Fail('BYTE_LIMIT')
    return data

def oid(kind, raw):
    return hashlib.sha1(kind + b' ' + str(len(raw)).encode('ascii') + b'\0' + raw).hexdigest()

def commit_tree(commit):
    header = commit.split(b'\n\n', 1)[0]
    lines = header.split(b'\n')
    trees = [line[5:] for line in lines if line.startswith(b'tree ')]
    if len(trees) != 1 or not re.fullmatch(rb'[0-9a-f]{40}', trees[0]):
        raise Fail('INVALID_COMMIT_TREE')
    return trees[0].decode('ascii')

def tree_entries(raw):
    i, result = 0, {}
    while i < len(raw):
        space = raw.find(b' ', i)
        nul = raw.find(b'\0', space + 1) if space != -1 else -1
        if space < 0 or nul < 0 or nul + 21 > len(raw):
            raise Fail('MALFORMED_TREE')
        mode, name = raw[i:space], raw[space + 1:nul]
        if mode not in (b'40000', b'040000', b'100644', b'100755'):
            raise Fail('UNSUPPORTED_TREE_MODE')
        if not name or b'/' in name or name in (b'.', b'..') or name in result:
            raise Fail('INVALID_TREE_ENTRY')
        result[name] = (mode, raw[nul + 1:nul + 21].hex())
        i = nul + 21
    return result

def evaluate(doc):
    if not isinstance(doc, dict) or doc.get('object') != OBJECT or doc.get('repository') != REPO:
        raise Fail('INVALID_ENVELOPE')
    sha = doc.get('pinned_commit_sha')
    if not isinstance(sha, str) or not HEX40.fullmatch(sha):
        raise Fail('INVALID_COMMIT_SHA')
    path = doc.get('path')
    if (not isinstance(path, str) or not path.startswith(ROOT) or
        len(path) > 240 or not PATH.fullmatch(path) or
        any(x in ('', '.', '..') for x in path.split('/'))):
        raise Fail('INVALID_PATH')
    claimed_sha = doc.get('expected_sha256')
    claimed_bytes = doc.get('expected_bytes')
    if not isinstance(claimed_sha, str) or not HEX64.fullmatch(claimed_sha):
        raise Fail('INVALID_EXPECTED_SHA256')
    if type(claimed_bytes) is not int or claimed_bytes < 0 or claimed_bytes > 1048576:
        raise Fail('INVALID_EXPECTED_BYTES')
    commit = decode(doc.get('commit_base64'), 65536)
    if oid(b'commit', commit) != sha:
        raise Fail('COMMIT_OID_MISMATCH')
    expected_tree = commit_tree(commit)
    chain = doc.get('tree_chain_base64')
    parts = path.split('/')
    if not isinstance(chain, list) or len(chain) != len(parts):
        raise Fail('TREE_CHAIN_LENGTH')
    for index, encoded in enumerate(chain):
        raw_tree = decode(encoded, 1048576)
        if oid(b'tree', raw_tree) != expected_tree:
            raise Fail('TREE_OID_MISMATCH')
        entry = tree_entries(raw_tree).get(parts[index].encode('ascii'))
        if entry is None:
            raise Fail('PATH_NOT_IN_TREE')
        mode, target = entry
        if index < len(parts) - 1:
            if mode not in (b'40000', b'040000'):
                raise Fail('NOT_DIRECTORY')
            expected_tree = target
        else:
            if mode not in (b'100644', b'100755'):
                raise Fail('NOT_REGULAR_BLOB')
            expected_blob = target
    blob = decode(doc.get('blob_base64'), 1048576)
    if oid(b'blob', blob) != expected_blob:
        raise Fail('BLOB_OID_MISMATCH')
    if len(blob) != claimed_bytes:
        raise Fail('BYTE_COUNT_MISMATCH')
    if hashlib.sha256(blob).hexdigest() != claimed_sha:
        raise Fail('SHA256_MISMATCH')
    return {'object': OBJECT, 'claim_ceiling': 'C1_DESCRIPTIVE_ONLY',
            'pinned_commit_sha': sha, 'path': path, 'bytes': len(blob),
            'sha256': claimed_sha, 'git_blob_sha1': expected_blob,
            'git_tree_chain_verified': True,
            'provenance': 'CALLER_SUPPLIED_GIT_OBJECT_CHAIN_NOT_REMOTE_AUTHENTICATED'}

def main():
    try:
        raw = sys.stdin.buffer.read(1600000)
        if len(raw) >= 1600000:
            raise Fail('INPUT_LIMIT')
        try:
            doc = json.loads(raw.decode('utf-8'), object_pairs_hook=pairs_unique)
        except (ValueError, UnicodeError):
            raise Fail('INVALID_JSON')
        out = evaluate(doc)
    except Fail as exc:
        print('FAIL_CLOSED: ' + str(exc), file=sys.stderr)
        return 2
    print(json.dumps(out, sort_keys=True, separators=(',', ':')))
    return 0

if __name__ == '__main__':
    sys.exit(main())
