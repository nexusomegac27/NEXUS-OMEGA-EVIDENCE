#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Additive C1 F0 source-identity consistency guard over immutable V1.

No network, writes, worker activation, dispatch or scientific ACK.
A commit/path pair must not denote conflicting bytes within one source graph.
The input remains caller supplied; external provenance is NOT authenticated.
"""
import hashlib
import json
from pathlib import Path
import sys

BASELINE_FILE = 'alpha_source_graph_closure_f0_v1_20261029.py'
BASELINE_SHA256 = 'c39208bffdc60ef8072cc7fb82a8aead459870f840e4ff7c9a0e4f79a59e051b'


def main():
    try:
        source = Path(__file__).with_name(BASELINE_FILE).read_bytes()
        if hashlib.sha256(source).hexdigest() != BASELINE_SHA256:
            raise ValueError('BASELINE_SOURCE_DRIFT')
        scope = {'__name__': 'pinned_f0_v1'}
        exec(compile(source, BASELINE_FILE, 'exec'), scope)
        raw = sys.stdin.buffer.read(scope['MAX_INPUT'] + 1)
        if len(raw) > scope['MAX_INPUT']:
            raise ValueError('INPUT_TOO_LARGE')
        doc = json.loads(raw.decode('utf-8'), object_pairs_hook=scope['unique_pairs'],
                         parse_constant=scope['nonfinite'])
        result = scope['audit'](doc)
        seen = {}
        for node in doc['nodes']:
            key = (node['commit'], node['path'])
            binding = (node['bytes'], node['sha256'], node['git_blob'], node['content_b64'])
            if key in seen and seen[key] != binding:
                raise ValueError('CONFLICTING_SOURCE_IDENTITY')
            seen[key] = binding
        result['state'] = 'C1_LOCAL_SOURCE_GRAPH_IDENTITY_CONSISTENT'
        result['distinct_source_identities'] = len(seen)
        result['api_origin_authenticated'] = False
        result['receiver_bytes_independently_fetched'] = False
        result['receiver_ack_established'] = False
        result['ready_for_expert'] = 'NOT_ESTABLISHED'
        result['expert_research_executed'] = False
        result['claim_ceiling'] = 'C1_DESCRIPTIVE_ONLY'
        print(json.dumps(result, sort_keys=True, separators=(',', ':')))
        return 0
    except (OSError, ValueError, TypeError, UnicodeError, RecursionError) as exc:
        print('FAIL_CLOSED: ' + str(exc), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
