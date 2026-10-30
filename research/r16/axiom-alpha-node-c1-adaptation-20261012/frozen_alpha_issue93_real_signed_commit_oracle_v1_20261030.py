#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Isolated, fail-closed Git signed-commit OID reconstruction.

Checks Git object-byte consistency of caller-supplied API payload/signature.
It does NOT authenticate GitHub, independently verify PGP signatures, or
prove that the API response was unmodified in transit.
"""
import copy
import hashlib
import json
import re
import sys

HEX40 = re.compile(r'[0-9a-f]{40}\Z')
OBJECT = 'NEXUS_OMEGA_ALPHA_ISSUE93_REAL_SIGNED_COMMIT_WITNESS_V1'

class Fail(Exception):
    pass

def unique_pairs(pairs):
    out = {}
    for key, value in pairs:
        if key in out:
            raise Fail('DUPLICATE_JSON_KEY')
        out[key] = value
    return out

def reconstruct(payload, signature):
    if not isinstance(payload, str) or not isinstance(signature, str):
        raise Fail('INVALID_TYPES')
    if len(payload.encode('utf-8')) > 100000 or len(signature.encode('utf-8')) > 20000:
        raise Fail('INPUT_LIMIT')
    if '\r' in payload or '\r' in signature:
        raise Fail('CRLF_REJECTED')
    if not (signature.startswith('-----BEGIN PGP SIGNATURE-----\n') and
            signature.endswith('-----END PGP SIGNATURE-----\n')):
        raise Fail('SIGNATURE_FORMAT')
    split = payload.find('\n\n')
    if split < 0:
        raise Fail('PAYLOAD_FORMAT')
    header, message = payload[:split], payload[split + 2:]
    lines = header.split('\n')
    if len(lines) < 4 or not lines[0].startswith('tree ') or not lines[1].startswith('parent '):
        raise Fail('PAYLOAD_HEADER')
    if any(line.startswith('gpgsig ') for line in lines):
        raise Fail('DUPLICATE_SIGNATURE')
    if not any(line.startswith('author ') for line in lines) or not any(line.startswith('committer ') for line in lines):
        raise Fail('PAYLOAD_HEADER')
    raw = (header + '\ngpgsig ' + signature.replace('\n', '\n ') + '\n\n' + message).encode('utf-8')
    return raw, lines

def oid(raw):
    return hashlib.sha1(b'commit ' + str(len(raw)).encode('ascii') + b'\0' + raw).hexdigest()

def evaluate(doc):
    if not isinstance(doc, dict) or doc.get('object') != OBJECT:
        raise Fail('INVALID_ENVELOPE')
    expected = doc.get('expected_commit_sha')
    tree = doc.get('expected_tree_sha')
    parent = doc.get('expected_parent_sha')
    if not all(isinstance(x, str) and HEX40.fullmatch(x) for x in (expected, tree, parent)):
        raise Fail('INVALID_OID')
    raw, lines = reconstruct(doc.get('payload'), doc.get('signature'))
    if lines[0] != 'tree ' + tree:
        raise Fail('TREE_BINDING_MISMATCH')
    if lines[1] != 'parent ' + parent:
        raise Fail('PARENT_BINDING_MISMATCH')
    actual = oid(raw)
    if actual != expected:
        raise Fail('COMMIT_OID_MISMATCH')
    return {'result': 'MATCH', 'raw_reconstructed_commit_bytes': len(raw),
            'git_commit_sha1': actual, 'tree_sha': tree, 'parent_sha': parent,
            'source_class': 'API_DERIVED_RECONSTRUCTION_NOT_RAW_GIT_OBJECT_FETCH',
            'pgp_signature_independently_verified': False,
            'actor_authentication': 'NOT_ESTABLISHED',
            'claim_ceiling': 'C1_DESCRIPTIVE_ONLY'}

def selftest():
    signature = '-----BEGIN PGP SIGNATURE-----\n\nabc123\n-----END PGP SIGNATURE-----\n'
    payload = ('tree ' + 'a'*40 + '\nparent ' + 'b'*40 + '\nauthor A <a@example.org> 0 +0000\n'
               'committer B <b@example.org> 0 +0000\n\nmessage')
    raw, _ = reconstruct(payload, signature)
    base = {'object': OBJECT, 'expected_commit_sha': oid(raw), 'expected_tree_sha': 'a'*40,
            'expected_parent_sha': 'b'*40, 'payload': payload, 'signature': signature}
    assert evaluate(base)['result'] == 'MATCH'
    cases = [
        ('COMMIT', lambda d: d.update(expected_commit_sha='0'*40), 'COMMIT_OID_MISMATCH'),
        ('TREE', lambda d: d.update(expected_tree_sha='0'*40), 'TREE_BINDING_MISMATCH'),
        ('PARENT', lambda d: d.update(expected_parent_sha='0'*40), 'PARENT_BINDING_MISMATCH'),
        ('MESSAGE', lambda d: d.update(payload=d['payload']+'!'), 'COMMIT_OID_MISMATCH'),
        ('SIGNATURE', lambda d: d.update(signature=d['signature'].replace('abc123', 'abc124')), 'COMMIT_OID_MISMATCH'),
        ('MISSING_SIGNATURE', lambda d: d.update(signature=''), 'SIGNATURE_FORMAT'),
        ('CRLF', lambda d: d.update(signature=d['signature'].replace('\n','\r\n')), 'CRLF_REJECTED'),
        ('WRONG_OBJECT', lambda d: d.update(object='WRONG'), 'INVALID_ENVELOPE'),
        ('INVALID_SHA', lambda d: d.update(expected_commit_sha='z'*40), 'INVALID_OID'),
        ('MISSING_HEADER', lambda d: d.update(payload='message'), 'PAYLOAD_FORMAT'),
    ]
    for name, mutate, expected in cases:
        d = copy.deepcopy(base)
        mutate(d)
        try:
            evaluate(d)
        except Fail as exc:
            assert str(exc) == expected, (name, str(exc), expected)
        else:
            raise AssertionError(name + ' incorrectly passed')
    try:
        json.loads('{"x":1,"x":2}', object_pairs_hook=unique_pairs)
    except Fail as exc:
        assert str(exc) == 'DUPLICATE_JSON_KEY'
    else:
        raise AssertionError('duplicate JSON key accepted')
    print('SELFTEST_PASS 12/12 (1 positive, 11 negative)')

def main():
    if sys.argv[1:] == ['--selftest']:
        selftest()
        return 0
    try:
        data = sys.stdin.buffer.read(150000)
        if len(data) >= 150000:
            raise Fail('INPUT_LIMIT')
        doc = json.loads(data.decode('utf-8'), object_pairs_hook=unique_pairs)
        result = evaluate(doc)
    except (Fail, UnicodeError, ValueError) as exc:
        print('FAIL_CLOSED: ' + str(exc), file=sys.stderr)
        return 2
    print(json.dumps(result, sort_keys=True, separators=(',', ':')))
    return 0

if __name__ == '__main__':
    sys.exit(main())
