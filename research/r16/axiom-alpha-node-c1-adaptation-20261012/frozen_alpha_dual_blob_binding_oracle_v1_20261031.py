#!/usr/bin/env python3
"""Independent frozen subprocess oracle: dual-endpoint blob cross-binding C1."""
import base64
import hashlib
import json
import subprocess
import sys

R = 'nexusomegac27/NEXUS-OMEGA-EVIDENCE'
P = ['research/r16/axiom-alpha-node-c1-adaptation-20261012/' + n for n in ('a.py', 'b.md')]
B = [b'alpha\n', b'beta\r\n']
BASE = '0e32161a7599291ff581b8c8c1b072c37d2d99ec'
HEAD = '0af4961cec47093e8e99de8811b593fe167e661f'


def blob(b):
    return hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest()


def fixture():
    return {'dual_endpoint': {'schema_version': '1', 'repository': R,
            'pr': {'number': 240, 'changed_files': 2, 'base_sha': BASE, 'head_sha': HEAD},
            'api_file_listing': {'pages': [
                {'page': 1, 'request_url': f'https://api.github.com/repos/{R}/pulls/240/files?per_page=100&page=1',
                 'items': [{'filename': p, 'status': 'added', 'sha': blob(b)} for p, b in zip(P, B)]},
                {'page': 2, 'request_url': f'https://api.github.com/repos/{R}/pulls/240/files?per_page=100&page=2', 'items': []}]},
            'compare': {'base_sha': BASE, 'head_sha': HEAD, 'merge_base_sha': BASE,
                        'status': 'ahead', 'ahead_by': 2, 'behind_by': 0,
                        'files': [{'filename': p, 'status': 'added'} for p in P]},
            'local_preflight': {'pr_number': 240, 'head_sha': HEAD,
                'status': 'LOCAL_BYTES_MATCH_UNAUTHENTICATED_INPUT',
                'claim_ceiling': 'C1_DESCRIPTIVE_ONLY',
                'changed_file_paths': P[:], 'declared_changed_files': 2}},
            'source_bytes': {'pr_number': 240, 'head_sha': HEAD,
                'files': [{'path': p, 'content_b64': base64.b64encode(b).decode(),
                           'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest(),
                           'git_blob': blob(b)} for p, b in zip(P, B)]}}


def run(script, data):
    proc = subprocess.run([sys.executable, script], input=json.dumps(data),
                          capture_output=True, text=True, timeout=10)
    return proc.returncode, json.loads(proc.stdout)


def main(candidate, baseline):
    x = fixture()
    assert run(candidate, x)[0] == 0
    assert run(candidate, x)[1]['api_transport_authenticated'] is False
    forged = fixture()
    forged['dual_endpoint']['api_file_listing']['pages'][0]['items'][0]['sha'] = 'f'*40
    assert run(baseline, forged['dual_endpoint'])[0] == 0, 'baseline falsifier'
    mutants = [
        lambda x: x['dual_endpoint']['api_file_listing']['pages'][0]['items'][0].update(sha='f'*40),
        lambda x: x['source_bytes']['files'][0].update(content_b64='QUxQSEEK'),
        lambda x: x['source_bytes']['files'][0].update(bytes=99),
        lambda x: x['source_bytes']['files'][0].update(sha256='f'*64),
        lambda x: x['source_bytes']['files'][0].update(git_blob='f'*40),
        lambda x: x['source_bytes']['files'].pop(),
        lambda x: x['source_bytes']['files'][1].update(path=P[0]),
        lambda x: x['source_bytes'].update(head_sha='f'*40),
        lambda x: x['dual_endpoint']['compare']['files'].pop(),
        lambda x: x['source_bytes']['files'][0].update(content_b64='YWxwaGEK=='),
    ]
    for i, mutate in enumerate(mutants):
        x = fixture()
        mutate(x)
        rc, result = run(candidate, x)
        assert rc == 2 and result['status'] == 'FAIL_CLOSED', f'mutant {i}'
    # Scope falsifier: consistently fabricated API and source bytes remain unauthenticated.
    x = fixture()
    x['dual_endpoint']['api_file_listing']['pages'][0]['items'].pop()
    x['dual_endpoint']['compare']['files'].pop()
    x['dual_endpoint']['local_preflight']['changed_file_paths'].pop()
    x['dual_endpoint']['local_preflight']['declared_changed_files'] = 1
    x['dual_endpoint']['pr']['changed_files'] = 1
    x['source_bytes']['files'].pop()
    assert run(candidate, x)[0] == 0, 'residual must be disclosed'
    print(json.dumps({'status': 'PASS', 'assertions': 14, 'mutants_rejected': 10,
                      'baseline_forged_blob': 'ACCEPTED', 'candidate_forged_blob': 'REJECTED',
                      'joint_forgery': 'STILL_ACCEPTED_NOT_AUTHENTICATED'}))


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
