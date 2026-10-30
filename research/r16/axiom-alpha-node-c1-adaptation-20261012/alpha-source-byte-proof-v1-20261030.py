#!/usr/bin/env python3
"""Isolated offline C1 byte-identity gate; no GitHub authentication or commit-tree proof."""
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys
from urllib.parse import urlsplit

REPO = 'nexusomegac27/NEXUS-OMEGA-EVIDENCE'
SCHEMA = 'NEXUS_ALPHA_SOURCE_BYTE_PROOF_V1'
HEX40 = re.compile(r'[0-9a-f]{40}\Z')
HEX64 = re.compile(r'[0-9a-f]{64}\Z')
SAFE = re.compile(r'[A-Za-z0-9._/-]+\Z')
KEYS = {'schema', 'repository', 'source_ref', 'source_commit', 'path', 'bytes',
        'sha256', 'git_blob_sha1', 'claim_ceiling'}


def unique_pairs(pairs):
    out = {}
    for key, value in pairs:
        if key in out:
            raise ValueError('DUPLICATE_JSON_KEY')
        out[key] = value
    return out


def reject_constant(_):
    raise ValueError('NONFINITE_JSON')


def check(data, root):
    if type(data) is not dict or set(data) != KEYS:
        raise ValueError('SCHEMA_FIELDS')
    if data['schema'] != SCHEMA or data['repository'] != REPO or data['claim_ceiling'] != 'C1_DESCRIPTIVE_ONLY':
        raise ValueError('SCOPE_OR_CLAIM')
    commit, path, url = data['source_commit'], data['path'], data['source_ref']
    if type(commit) is not str or not HEX40.fullmatch(commit):
        raise ValueError('COMMIT')
    if type(path) is not str or not path or len(path) > 512 or not SAFE.fullmatch(path):
        raise ValueError('PATH')
    parts = path.split('/')
    if any(p in ('', '.', '..') for p in parts) or path.startswith('/'):
        raise ValueError('PATH_TRAVERSAL')
    if type(url) is not str or len(url) > 1024 or any(ord(c) < 33 or ord(c) > 126 for c in url) or '%' in url or '\\' in url:
        raise ValueError('URL_BYTES')
    u = urlsplit(url)
    if u.scheme != 'https' or u.netloc != 'github.com' or u.query or u.fragment:
        raise ValueError('URL_ORIGIN')
    if u.path != '/' + REPO + '/blob/' + commit + '/' + path:
        raise ValueError('URL_COMMIT_PATH_MISMATCH')
    if type(data['bytes']) is not int or data['bytes'] < 0 or data['bytes'] > 1048576:
        raise ValueError('BYTES')
    if type(data['sha256']) is not str or not HEX64.fullmatch(data['sha256']):
        raise ValueError('SHA256')
    if type(data['git_blob_sha1']) is not str or not HEX40.fullmatch(data['git_blob_sha1']):
        raise ValueError('GIT_BLOB')
    base = Path(root).resolve(strict=True)
    if not base.is_dir():
        raise ValueError('ROOT')
    current = base
    for component in parts:
        current = current / component
        mode = current.lstat().st_mode
        if stat.S_ISLNK(mode):
            raise ValueError('SYMLINK')
    if not current.is_file() or not current.resolve(strict=True).is_relative_to(base):
        raise ValueError('NOT_REGULAR_IN_ROOT')
    if current.stat().st_size != data['bytes']:
        raise ValueError('BYTE_LENGTH_MISMATCH')
    with current.open('rb') as f:
        raw = f.read(1048577)
    if len(raw) != data['bytes']:
        raise ValueError('BYTE_LENGTH_MISMATCH')
    sha256 = hashlib.sha256(raw).hexdigest()
    blob = hashlib.sha1(b'blob ' + str(len(raw)).encode('ascii') + b'\x00' + raw).hexdigest()
    if sha256 != data['sha256']:
        raise ValueError('SHA256_MISMATCH')
    if blob != data['git_blob_sha1']:
        raise ValueError('GIT_BLOB_MISMATCH')
    return {'state': 'LOCAL_SOURCE_BYTES_MATCH', 'bytes': len(raw), 'sha256': sha256,
            'git_blob_sha1': blob, 'source_commit': commit, 'path': path,
            'commit_tree_membership': 'NOT_VERIFIED', 'transport_authentication': 'NOT_VERIFIED',
            'claim_ceiling': 'C1_DESCRIPTIVE_ONLY'}


def main():
    try:
        if len(sys.argv) != 2:
            raise ValueError('USAGE_ROOT_REQUIRED')
        raw = sys.stdin.buffer.read(16385)
        if len(raw) > 16384:
            raise ValueError('OVERSIZE_JSON')
        data = json.loads(raw.decode('utf-8', 'strict'), object_pairs_hook=unique_pairs,
                          parse_constant=reject_constant)
        out = check(data, sys.argv[1])
        print(json.dumps(out, sort_keys=True, separators=(',', ':')))
        return 0
    except (ValueError, TypeError, KeyError, OSError, UnicodeError, json.JSONDecodeError) as e:
        print(json.dumps({'state': 'FAIL_CLOSED', 'reason': str(e)}, sort_keys=True))
        return 2


if __name__ == '__main__':
    sys.exit(main())
