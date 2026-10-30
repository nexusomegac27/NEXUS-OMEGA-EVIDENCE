#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Independent offline Git-tree witness evaluator; never authenticates API actor/origin.

Input: a caller-supplied JSON witness containing GitHub API-derived tree bytes.
The independent byte-level witness is a scoped C1 check, not a GitHub login proof.
"""
import base64
import binascii
import hashlib
import json
import re
import sys

REPO = 'nexusomegac27/NEXUS-OMEGA-EVIDENCE'
ROOT = 'research/r16/axiom-alpha-node-c1-adaptation-20261012/'
OBJECT = 'NEXUS_OMEGA_ALPHA_ISSUE93_REAL_GIT_API_TREE_WITNESS_V1'
HEX40 = re.compile(r'[a-f0-9]{40}\Z')
HEX64 = re.compile(r'[a-f0-9]{64}\Z')

class Fail(Exception):
    pass

def pairs_unique(pairs):
    d = {}
    for k, v in pairs:
        if k in d:
            raise Fail('DUPLICATE_JSON_KEY')
        d[k] = v
    return d

def b64(raw, limit):
    if not isinstance(raw, str) or len(raw) > limit * 4 // 3 + 8:
        raise Fail('INVALID_BASE64')
    try:
        out = base64.b64decode(raw, validate=True)
    except (ValueError, binascii.Error):
        raise Fail('INVALID_BASE64')
    if len(out) > limit:
        raise Fail('BYTE_LIMIT')
    return out

def git_oid(kind, raw):
    return hashlib.sha1(kind.encode() + b' ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()

def entries(raw):
    pos, result = 0, {}
    while pos < len(raw):
        space = raw.find(b' ', pos)
        nul = raw.find(b'\0', space + 1) if space >= 0 else -1
        if space <= pos or nul <= space + 1 or nul + 21 > len(raw):
            raise Fail('MALFORMED_TREE')
        mode, name = raw[pos:space], raw[space+1:nul]
        if mode not in (b'40000', b'100644', b'100755'):
            raise Fail('UNSUPPORTED_MODE')
        if name in result or name in (b'.', b'..') or b'/' in name:
            raise Fail('INVALID_ENTRY')
        result[name] = (mode, raw[nul+1:nul+21].hex())
        pos = nul + 21
    return result

def evaluate(d):
    if not isinstance(d, dict) or d.get('object') != OBJECT or d.get('repository') != REPO:
        raise Fail('INVALID_ENVELOPE')
    commit = d.get('pinned_commit_sha')
    root = d.get('api_commit_tree_sha')
    path = d.get('path')
    if not isinstance(commit, str) or not HEX40.fullmatch(commit):
        raise Fail('INVALID_COMMIT')
    if not isinstance(root, str) or not HEX40.fullmatch(root):
        raise Fail('INVALID_ROOT_TREE')
    if not isinstance(path, str) or not path.startswith(ROOT) or len(path) > 240:
        raise Fail('INVALID_PATH')
    parts = path.split('/')
    if any(not p or p in ('.', '..') or not re.fullmatch('[A-Za-z0-9_.-]+', p) for p in parts):
        raise Fail('INVALID_PATH')
    chain = d.get('tree_chain_base64')
    if not isinstance(chain, list) or len(chain) != len(parts):
        raise Fail('CHAIN_LENGTH')
    expected = root
    for i, encoded in enumerate(chain):
        raw = b64(encoded, 131072)
        if git_oid('tree', raw) != expected:
            raise Fail('TREE_OID_MISMATCH')
        entry = entries(raw).get(parts[i].encode('ascii'))
        if entry is None:
            raise Fail('PATH_NOT_IN_TREE')
        mode, target = entry
        if i + 1 < len(parts):
            if mode != b'40000':
                raise Fail('NOT_DIRECTORY')
            expected = target
        else:
            if mode not in (b'100644', b'100755'):
                raise Fail('NOT_FILE')
            expected_blob = target
    blob = b64(d.get('blob_base64'), 1048576)
    if git_oid('blob', blob) != expected_blob:
        raise Fail('BLOB_OID_MISMATCH')
    if type(d.get('expected_bytes')) is not int or len(blob) != d['expected_bytes']:
        raise Fail('BYTE_COUNT_MISMATCH')
    if not isinstance(d.get('expected_sha256'), str) or not HEX64.fullmatch(d['expected_sha256']):
        raise Fail('INVALID_SHA256')
    if hashlib.sha256(blob).hexdigest() != d['expected_sha256']:
        raise Fail('SHA256_MISMATCH')
    return {'result': 'MATCH', 'tree_count': len(chain), 'bytes': len(blob),
            'sha256': d['expected_sha256'], 'git_blob_sha1': expected_blob,
            'pinned_commit_sha': commit, 'api_commit_tree_sha': root,
            'provenance': 'GITHUB_API_DERIVED_INPUT_NOT_INDEPENDENT_ACTOR_AUTHENTICATION',
            'claim_ceiling': 'C1_DESCRIPTIVE_ONLY'}

def fixture():
    path = ROOT + 'synthetic.md'
    blob = b'abc\n'
    parts = path.split('/')
    target = git_oid('blob', blob)
    chain = []
    for i in range(len(parts)-1, -1, -1):
        mode = b'100644' if i == len(parts)-1 else b'40000'
        raw = mode + b' ' + parts[i].encode() + b'\0' + bytes.fromhex(target)
        chain.insert(0, base64.b64encode(raw).decode())
        target = git_oid('tree', raw)
    return {'object': OBJECT, 'repository': REPO, 'pinned_commit_sha': 'a'*40,
            'api_commit_tree_sha': target, 'path': path, 'tree_chain_base64': chain,
            'blob_base64': base64.b64encode(blob).decode(),
            'expected_bytes': len(blob), 'expected_sha256': hashlib.sha256(blob).hexdigest()}

def selftest():
    import copy
    base = fixture()
    assert evaluate(base)['result'] == 'MATCH'
    tests = [
        ('ROOT_OID', lambda d: d.update(api_commit_tree_sha='0'*40), 'TREE_OID_MISMATCH'),
        ('TREE_BYTES', lambda d: d['tree_chain_base64'].__setitem__(0, base64.b64encode(base64.b64decode(d['tree_chain_base64'][0])+b'!').decode()), 'TREE_OID_MISMATCH'),
        ('BLOB', lambda d: d.update(blob_base64=base64.b64encode(b'xyz\n').decode()), 'BLOB_OID_MISMATCH'),
        ('BYTES', lambda d: d.update(expected_bytes=3), 'BYTE_COUNT_MISMATCH'),
        ('SHA256', lambda d: d.update(expected_sha256='0'*64), 'SHA256_MISMATCH'),
        ('PATH', lambda d: d.update(path=ROOT+'absent.md'), 'PATH_NOT_IN_TREE'),
        ('TRAVERSAL', lambda d: d.update(path=ROOT+'../escape.md'), 'INVALID_PATH'),
        ('CHAIN', lambda d: d['tree_chain_base64'].pop(), 'CHAIN_LENGTH'),
    ]
    for name, mutate, expected in tests:
        d = copy.deepcopy(base)
        mutate(d)
        try:
            evaluate(d)
        except Fail as exc:
            assert str(exc) == expected, (name, str(exc), expected)
        else:
            raise AssertionError(name + ' incorrectly passed')
    try:
        json.loads('{"x":1,"x":2}', object_pairs_hook=pairs_unique)
    except Fail as exc:
        assert str(exc) == 'DUPLICATE_JSON_KEY'
    else:
        raise AssertionError('duplicate key accepted')
    print('SELFTEST_PASS 10/10 (1 positive, 9 negative)')

def main():
    if sys.argv[1:] == ['--selftest']:
        selftest()
        return 0
    try:
        raw = sys.stdin.buffer.read(1500000)
        if len(raw) >= 1500000:
            raise Fail('INPUT_LIMIT')
        d = json.loads(raw.decode('utf-8'), object_pairs_hook=pairs_unique)
        result = evaluate(d)
    except (Fail, UnicodeError, ValueError) as exc:
        print('FAIL_CLOSED: ' + str(exc), file=sys.stderr)
        return 2
    print(json.dumps(result, sort_keys=True, separators=(',', ':')))
    return 0

if __name__ == '__main__':
    sys.exit(main())
