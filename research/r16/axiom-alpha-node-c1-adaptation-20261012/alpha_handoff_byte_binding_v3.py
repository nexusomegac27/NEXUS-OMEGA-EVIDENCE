#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Isolated C1 handoff-denominator reducer; metadata only, no API authentication.

Never infer successful GitHub publication from this local calculation. Caller must
independently read back GitHub source bytes, commit, CI and Issue #93 receipt.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path

FIELDS = (
    'routine','public','authorized','source_accessible','write_access_verified',
    'branch_published','main_published','source_hash_readback','test_readback',
    'commit_readback','issue93_receipt_readback','source_gap','claim_promotion',
)

def measure(records: list[dict]) -> dict:
    if not isinstance(records, list):
        raise ValueError('RECORDS_NOT_LIST')
    seen = set()
    eligible = completed = 0
    exclusions = {}
    flags = []
    for idx, item in enumerate(records):
        if not isinstance(item, dict) or not isinstance(item.get('artifact'), str) or not item['artifact']:
            raise ValueError(f'INVALID_ARTIFACT_AT_{idx}')
        if item['artifact'] in seen:
            raise ValueError(f'DUPLICATE_ARTIFACT_{item["artifact"]}')
        seen.add(item['artifact'])
        if any(type(item.get(key)) is not bool for key in FIELDS):
            raise ValueError(f'INVALID_BOOLEAN_FIELDS_AT_{idx}')
        if item['main_published'] and (not item['authorized'] or not item['public']):
            flags.append({'artifact':item['artifact'],'code':'POTENTIAL_UNAUTHORIZED_OR_PRIVATE_PUBLICATION'})
        if item['main_published'] and item['source_gap']:
            flags.append({'artifact':item['artifact'],'code':'SOURCE_GAP_WITH_PUBLICATION'})
        # Safety invariants apply to ALL observations, including excluded handoffs.
        # Exclusion from the automation-rate denominator never erases a violation.
        if item['claim_promotion']:
            flags.append({'artifact':item['artifact'],'code':'CLAIM_PROMOTION_PROHIBITED'})
        if item['main_published'] and not item['source_accessible']:
            flags.append({'artifact':item['artifact'],'code':'PUBLICATION_WITH_UNVERIFIED_SOURCE_ACCESS'})
        if item['main_published'] and not item['write_access_verified']:
            flags.append({'artifact':item['artifact'],'code':'PUBLICATION_WITH_UNVERIFIED_WRITE_ACCESS'})
        if item['main_published'] and not all(item[k] for k in (
                'source_hash_readback','test_readback','commit_readback',
                'issue93_receipt_readback')):
            flags.append({'artifact':item['artifact'],'code':'PUBLICATION_READBACK_INCOMPLETE'})
        reason = next((key for key in ('routine','public','authorized','source_accessible','write_access_verified')
                       if not item[key]), None)
        if reason is None and item['source_gap']:
            reason='source_gap'
        if reason is not None:
            exclusions[reason] = exclusions.get(reason, 0) + 1
            continue
        eligible += 1
        # A branch commit is not a main publication. All gates must be separately read back.
        if (item['main_published'] and item['source_hash_readback'] and
            item['test_readback'] and item['commit_readback'] and
            item['issue93_receipt_readback'] and not item['claim_promotion']):
            completed += 1
    return {
        'object':'NEXUS_ALPHA_HANDOFF_DENOMINATOR_SAFETY_FLAGS_V2',
        'claim_ceiling':'C1_DESCRIPTIVE_ONLY',
        'evidence_class':'METADATA_ONLY_REQUIRES_INDEPENDENT_GITHUB_READBACK',
        'eligible_denominator':eligible,
        'completed_numerator':completed,
        'rate':completed/eligible if eligible else None,
        'rate_defined':bool(eligible),
        'excluded':dict(sorted(exclusions.items())),
        'flags':flags,
        'external_authority_authenticated':False,
        'publication_performed':False,
    }

def main() -> int:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('observations',type=Path)
    args=p.parse_args()
    try:
        report=measure(json.loads(args.observations.read_text(encoding='utf-8')))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({'state':'HOLD_SCOPED','reason':str(exc)},sort_keys=True))
        return 2
    print(json.dumps(report,sort_keys=True))
    return 0 if not report['flags'] else 1

if __name__=='__main__':
    raise SystemExit(main())

# V3 is deliberately additive: V2's metadata-only measure() and its historical
# semantics remain unchanged. This stricter layer is NOT a GitHub authenticator.
import hashlib as _hashlib


def _hex(value, n):
    return isinstance(value, str) and len(value) == n and all(c in '0123456789abcdef' for c in value)


def _sha(data):
    return _hashlib.sha256(data).hexdigest()


def _blob(data):
    return _hashlib.sha1(b'blob ' + str(len(data)).encode('ascii') + b'\x00' + data).hexdigest()


def _unique_json_pairs(pairs):
    obj = {}
    for key, value in pairs:
        if key in obj:
            raise ValueError('DUPLICATE_RECEIPT_JSON_KEY')
        obj[key] = value
    return obj


def _verify_byte_proof(proof, observed_main_sha):
    """Check *local* bytes and references, not GitHub actor/transport identity."""
    if not isinstance(proof, dict):
        return 'PROOF_INVALID'
    if not _hex(observed_main_sha, 40):
        return 'MAIN_READBACK_NOT_ESTABLISHED'
    if not _hex(proof.get('commit_sha'), 40) or proof['commit_sha'] != observed_main_sha:
        return 'MAIN_COMMIT_MISMATCH'
    if proof.get('repository') != 'nexusomegac27/NEXUS-OMEGA-EVIDENCE':
        return 'PROOF_REPOSITORY_INVALID'
    path = proof.get('path')
    if not isinstance(path, str) or not path.startswith('research/') or '..' in path.split('/'):
        return 'PROOF_PATH_INVALID'
    src = proof.get('source_bytes')
    if not isinstance(src, bytes) or not _hex(proof.get('source_sha256'), 64) or type(proof.get('source_byte_count')) is not int:
        return 'SOURCE_BYTES_MISMATCH'
    if len(src) != proof['source_byte_count'] or _sha(src) != proof['source_sha256']:
        return 'SOURCE_BYTES_MISMATCH'
    if not _hex(proof.get('source_blob_sha1'), 40) or _blob(src) != proof['source_blob_sha1']:
        return 'SOURCE_BLOB_MISMATCH'
    test = proof.get('test_bytes')
    if not isinstance(test, bytes) or not _hex(proof.get('test_sha256'), 64) or _sha(test) != proof['test_sha256']:
        return 'TEST_BYTES_MISMATCH'
    comment = proof.get('issue_comment_bytes')
    if not isinstance(comment, bytes) or not _hex(proof.get('issue_comment_sha256'), 64) or _sha(comment) != proof['issue_comment_sha256']:
        return 'ISSUE_RECEIPT_BYTES_MISMATCH'
    if type(proof.get('issue_comment_id')) is not int or proof['issue_comment_id'] <= 0:
        return 'ISSUE_RECEIPT_ID_INVALID'
    try:
        receipt = json.loads(comment.decode('utf-8'), object_pairs_hook=_unique_json_pairs)
    except (UnicodeError, ValueError):
        return 'ISSUE_RECEIPT_BINDING_MISMATCH'
    if not isinstance(receipt, dict) or any(receipt.get(k) != v for k, v in {
        'main_sha': observed_main_sha,
        'source_sha256': proof['source_sha256'],
        'test_sha256': proof['test_sha256'],
        'claim_ceiling': 'C1_DESCRIPTIVE_ONLY',
    }.items()):
        return 'ISSUE_RECEIPT_BINDING_MISMATCH'
    return None


def measure_bound(records, proofs, observed_main_sha):
    """Proof-binding preflight only; caller MUST authenticate actual API reads.

    A synthetic valid proof can pass this function. Consequently project-level
    success numerator/rate intentionally remain NULL, never auto-promoted.
    """
    base = measure(records)
    if not isinstance(proofs, dict):
        raise ValueError('PROOFS_NOT_MAPPING')
    flags = list(base['flags'])
    bound = 0
    for item in records:
        artifact = item['artifact']
        eligible = all(item[k] for k in (
            'routine','public','authorized','source_accessible','write_access_verified')) and not item['source_gap']
        completed_metadata = (eligible and item['main_published'] and
            all(item[k] for k in ('source_hash_readback','test_readback','commit_readback',
                                   'issue93_receipt_readback')) and not item['claim_promotion'])
        if not completed_metadata:
            continue
        if any(f['artifact'] == artifact for f in flags):
            continue
        if artifact not in proofs:
            flags.append({'artifact':artifact,'code':'PROOF_NOT_PRESENT'})
            continue
        problem = _verify_byte_proof(proofs[artifact], observed_main_sha)
        if problem:
            flags.append({'artifact':artifact,'code':problem})
        else:
            bound += 1
    return {
        'object':'NEXUS_ALPHA_HANDOFF_BYTE_BINDING_V3',
        'claim_ceiling':'C1_DESCRIPTIVE_ONLY',
        'evidence_class':'LOCAL_BYTE_BINDING_ONLY_API_AUTHENTICATION_REQUIRED',
        'eligible_denominator':base['eligible_denominator'],
        'metadata_only_numerator':base['completed_numerator'],
        'byte_bound_numerator':bound,
        'byte_bound_rate':bound/base['eligible_denominator'] if base['eligible_denominator'] else None,
        'project_handoff_numerator':None,
        'project_handoff_rate':None,
        'external_authentication_established':False,
        'flags':flags,
        'publication_performed':False,
    }
