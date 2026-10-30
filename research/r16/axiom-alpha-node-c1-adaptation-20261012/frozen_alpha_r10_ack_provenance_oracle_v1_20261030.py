#!/usr/bin/env python3
"""Independent subprocess-only C1 evaluator; frozen before candidate publication."""
import copy
import json
import subprocess
import sys

BASE = {
    'source_commit': 'dab7c59070d67e7e2a244bd6d05db9a4d37460e3',
    'source_sha256': '60768179f203a8a17df81280d056784084406d2e32502fdf9188be1f939835c5',
    'source_bytes': 4380,
    'source_git_blob': '4e31f92be1f673f49a2c27e570b5849e754cca78',
    'source_bytes_rehashed': True,
    'source_blob_rehashed': True,
    'owner_login': 'nexusomegac27',
    'actor_login': 'nexusomegac27',
    'actor_origin': 'GITHUB_API',
    'external_actor_allowlist': [],
    'receipt_origin': 'OWNER_MEDIATED_FILE',
    'claims_independent_receiver_ack': True,
    'claims_expert_research_executed': True,
}


def run(path, obj, raw=None):
    payload = raw if raw is not None else json.dumps(obj, separators=(',', ':'))
    p = subprocess.run([sys.executable, path], input=payload.encode('utf-8'),
                       capture_output=True, timeout=5)
    try:
        output = json.loads(p.stdout)
    except Exception as exc:
        raise AssertionError(f'non-JSON output: {p.stdout[:150]!r}') from exc
    return p.returncode, output


def main(path):
    cases = []
    def add(name, change, expected, raw=None):
        obj = copy.deepcopy(BASE)
        obj.update(change)
        cases.append((name, obj, expected, raw))

    add('real_owner_assertion_rejected', {}, 'NOT_ESTABLISHED')
    add('owner_with_forged_allowlist_rejected', {'external_actor_allowlist': ['nexusomegac27'], 'receipt_origin': 'EXTERNAL_GITHUB_ASSET'}, 'NOT_ESTABLISHED')
    add('unregistered_external_rejected', {'actor_login': 'external-reviewer', 'receipt_origin': 'EXTERNAL_GITHUB_ASSET'}, 'NOT_ESTABLISHED')
    add('self_declared_external_rejected', {'actor_login': 'external-reviewer', 'external_actor_allowlist': ['external-reviewer'], 'actor_origin': 'SELF_DECLARED', 'receipt_origin': 'EXTERNAL_GITHUB_ASSET'}, 'NOT_ESTABLISHED')
    add('owner_bridge_rejected', {'actor_login': 'external-reviewer', 'external_actor_allowlist': ['external-reviewer']}, 'NOT_ESTABLISHED')
    add('unhashed_source_rejected', {'actor_login': 'external-reviewer', 'external_actor_allowlist': ['external-reviewer'], 'receipt_origin': 'EXTERNAL_GITHUB_ASSET', 'source_bytes_rehashed': False}, 'NOT_ESTABLISHED')
    add('blob_gap_rejected', {'actor_login': 'external-reviewer', 'external_actor_allowlist': ['external-reviewer'], 'receipt_origin': 'EXTERNAL_GITHUB_ASSET', 'source_blob_rehashed': False}, 'NOT_ESTABLISHED')
    add('no_ack_claim_rejected', {'actor_login': 'external-reviewer', 'external_actor_allowlist': ['external-reviewer'], 'receipt_origin': 'EXTERNAL_GITHUB_ASSET', 'claims_independent_receiver_ack': False}, 'NOT_ESTABLISHED')
    add('qualified_only_review_eligible', {'actor_login': 'external-reviewer', 'external_actor_allowlist': ['external-reviewer'], 'receipt_origin': 'EXTERNAL_GITHUB_ASSET'}, 'ELIGIBLE_FOR_SEPARATE_AUTHENTICATION_AND_ADJUDICATION')
    add('casefold_allowlist_review_eligible', {'actor_login': 'External-Reviewer', 'external_actor_allowlist': ['external-reviewer'], 'receipt_origin': 'EXTERNAL_GITHUB_ASSET'}, 'ELIGIBLE_FOR_SEPARATE_AUTHENTICATION_AND_ADJUDICATION')
    add('invalid_sha', {'source_sha256': '0'*63}, 'ERROR')
    add('boolean_as_bytecount', {'source_bytes': True}, 'ERROR')
    add('duplicate_allowlist', {'external_actor_allowlist': ['reviewer', 'Reviewer']}, 'ERROR')
    add('unknown_field', {'elevate_claim': True}, 'ERROR')
    add('nonfinite_json', {}, 'ERROR', raw=json.dumps(BASE)[:-1]+',"source_bytes":NaN}')
    add('duplicate_json_key', {}, 'ERROR', raw=json.dumps(BASE)[:-1]+',"source_bytes":999}')

    passed = 0
    for name, obj, expected, raw in cases:
        code, output = run(path, obj, raw)
        if expected == 'ERROR':
            good = code != 0 and output.get('ok') is False
        else:
            good = (code == 0 and output.get('ok') is True
                    and output['result']['receiver_ack'] == expected
                    and output['result']['axiom_scientific_adjudication'] == 'NOT_PERFORMED'
                    and output['result']['claim_ceiling'] == 'C1_DESCRIPTIVE_ONLY')
        print(('PASS' if good else 'FAIL') + ' ' + name)
        if not good:
            raise AssertionError(f'{name}: {output}')
        passed += 1
    print(f'RESULT {passed}/{len(cases)} PASS')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('usage: oracle.py candidate.py')
    main(sys.argv[1])
