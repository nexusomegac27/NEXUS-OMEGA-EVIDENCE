#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Isolated C1 F0 graph/byte closure witness. No network, writes or dispatch.

Input is caller-supplied source bytes, NOT authenticated GitHub retrieval.
This program never grants READY_FOR_EXPERT or an independent receiver ACK.
"""
import base64
import binascii
import hashlib
import json
import re
import sys

OBJECT = 'NEXUS_OMEGA_ALPHA_SOURCE_GRAPH_CLOSURE_F0_V1'
REPO = 'nexusomegac27/NEXUS-OMEGA-EVIDENCE'
MAX_INPUT = 3_000_000
MAX_NODES = 64
SHA40 = re.compile(r'[0-9a-f]{40}\Z')
SHA64 = re.compile(r'[0-9a-f]{64}\Z')
NODE_ID = re.compile(r'[A-Za-z][A-Za-z0-9._-]{0,95}\Z')
SAFE_SEG = re.compile(r'[A-Za-z0-9_.-]+\Z')


def fail(reason):
    raise ValueError(reason)


def unique_pairs(pairs):
    out = {}
    for k, v in pairs:
        if k in out:
            fail('DUPLICATE_JSON_KEY')
        out[k] = v
    return out


def nonfinite(_):
    fail('NONFINITE_JSON')


def validate_path(path):
    if (type(path) is not str or not 1 <= len(path) <= 256 or
            path.startswith('/') or '\' in path or '%' in path or
            any(not SAFE_SEG.fullmatch(x) or x in ('.', '..') for x in path.split('/'))):
        fail('UNSAFE_SOURCE_PATH')


def audit(doc):
    if type(doc) is not dict or set(doc) != {'object', 'repository', 'target', 'nodes'}:
        fail('INVALID_ENVELOPE')
    if doc['object'] != OBJECT or doc['repository'] != REPO:
        fail('INVALID_SCOPE')
    nodes = doc['nodes']
    if type(nodes) is not list or not 1 <= len(nodes) <= MAX_NODES:
        fail('INVALID_NODE_COUNT')
    graph = {}
    for n in nodes:
        required = {'id', 'requires', 'commit', 'path', 'bytes', 'sha256',
                    'git_blob', 'content_b64', 'public_safe', 'rights_cleared'}
        if type(n) is not dict or set(n) != required:
            fail('INVALID_NODE_FIELDS')
        name = n['id']
        if type(name) is not str or not NODE_ID.fullmatch(name) or name in graph:
            fail('DUPLICATE_OR_INVALID_NODE_ID')
        parents = n['requires']
        if (type(parents) is not list or len(parents) > MAX_NODES or
                any(type(p) is not str or not NODE_ID.fullmatch(p) for p in parents) or
                len(set(parents)) != len(parents)):
            fail('INVALID_PARENT_LIST')
        if type(n['commit']) is not str or not SHA40.fullmatch(n['commit']):
            fail('UNPINNED_COMMIT')
        validate_path(n['path'])
        if (type(n['bytes']) is not int or not 0 <= n['bytes'] <= 262144 or
                type(n['sha256']) is not str or not SHA64.fullmatch(n['sha256']) or
                type(n['git_blob']) is not str or not SHA40.fullmatch(n['git_blob']) or
                type(n['content_b64']) is not str or len(n['content_b64']) > 350000):
            fail('INVALID_SOURCE_BINDING')
        if n['public_safe'] is not True or n['rights_cleared'] is not True:
            fail('SOURCE_NOT_PUBLIC_SAFE')
        try:
            raw = base64.b64decode(n['content_b64'], validate=True)
        except (binascii.Error, ValueError):
            fail('INVALID_BASE64')
        if base64.b64encode(raw).decode('ascii') != n['content_b64']:
            fail('NONCANONICAL_BASE64')
        if len(raw) != n['bytes']:
            fail('SOURCE_SIZE_MISMATCH')
        if hashlib.sha256(raw).hexdigest() != n['sha256']:
            fail('SOURCE_SHA256_MISMATCH')
        blob = hashlib.sha1(b'blob ' + str(len(raw)).encode('ascii') + b'\x00' + raw).hexdigest()
        if blob != n['git_blob']:
            fail('SOURCE_GIT_BLOB_MISMATCH')
        graph[name] = parents
    target = doc['target']
    if type(target) is not str or target not in graph:
        fail('TARGET_NOT_PRESENT')
    state, seen = {}, set()
    def visit(name):
        if name not in graph:
            fail('REQUIRED_SOURCE_NOT_PRESENT')
        if state.get(name) == 1:
            fail('CYCLIC_SOURCE_GRAPH')
        if state.get(name) == 2:
            return
        state[name] = 1
        for parent in graph[name]:
            visit(parent)
        state[name] = 2
        seen.add(name)
    visit(target)
    if len(seen) != len(graph):
        fail('UNREACHABLE_SOURCE_IN_INVENTORY')
    return {
        'state': 'C1_LOCAL_SOURCE_GRAPH_BYTES_CONSISTENT',
        'nodes_checked': len(seen),
        'sha256_matches': len(seen),
        'git_blob_matches': len(seen),
        'required_edges_checked': sum(len(x) for x in graph.values()),
        'api_origin_authenticated': False,
        'receiver_bytes_independently_fetched': False,
        'receiver_ack_established': False,
        'ready_for_expert': 'NOT_ESTABLISHED',
        'expert_research_executed': False,
        'claim_ceiling': 'C1_DESCRIPTIVE_ONLY',
    }


def main():
    try:
        raw = sys.stdin.buffer.read(MAX_INPUT + 1)
        if len(raw) > MAX_INPUT:
            fail('INPUT_TOO_LARGE')
        doc = json.loads(raw.decode('utf-8'), object_pairs_hook=unique_pairs, parse_constant=nonfinite)
        print(json.dumps(audit(doc), sort_keys=True, separators=(',', ':')))
        return 0
    except (ValueError, TypeError, UnicodeError, RecursionError) as exc:
        print('FAIL_CLOSED: ' + str(exc), file=sys.stderr)
        return 2

if __name__ == '__main__':
    sys.exit(main())
