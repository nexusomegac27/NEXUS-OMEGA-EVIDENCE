#!/usr/bin/env python3
"""Fail-closed byte consistency extension of frozen C1 structural guard.

A MATCH here is only consistency of supplied bytes and metadata, NOT GitHub API
authentication, an independent CI execution receipt, scientific validation, or merge.
"""
import base64
import binascii
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

PINNED_LEGACY_SHA256 = '27e4ea850b63b234275e6a8b2bf89c87e47685bd8d8fc760f801a7f998f7ca9c'
LEGACY_NAME = 'ALPHA_CI_EVIDENCE_COVERAGE_GUARD_V1_20261021.py'
MAX_FILE_BYTES = 1048576
MAX_CAPTURE_CHARS = ((MAX_FILE_BYTES + 2) // 3) * 4


def fail(*reasons):
    return {'coverage': 'GAP', 'reasons': sorted(set(reasons)),
            'authentication': 'NOT_ESTABLISHED', 'main_verified': False,
            'scientific_independence': 'NOT_ESTABLISHED'}


def evaluate(data, legacy_path):
    if not isinstance(data, dict):
        return fail('INVALID_CAPTURE')
    try:
        p = Path(legacy_path)
        original = p.read_bytes()
        if hashlib.sha256(original).hexdigest() != PINNED_LEGACY_SHA256:
            return fail('LEGACY_GUARD_SHA256_MISMATCH')
        spec = importlib.util.spec_from_file_location('alpha_pinned_legacy_guard', p)
        if spec is None or spec.loader is None:
            return fail('LEGACY_GUARD_UNAVAILABLE')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        baseline = module.evaluate(data)
    except (OSError, ValueError, TypeError, ImportError, SyntaxError, AttributeError):
        return fail('LEGACY_GUARD_UNAVAILABLE')
    if baseline.get('coverage') != 'STRUCTURALLY_COVERED':
        return fail('LEGACY_STRUCTURAL_GAP', *(baseline.get('reasons') or []))

    claim = data['claim']
    files = data['files']
    problems = []
    for pkey in ('evaluator_path', 'fixture_path', 'result_path'):
        path = claim[pkey]
        entry = files[path]
        encoded = entry.get('raw_base64')
        if not isinstance(encoded, str) or not encoded or len(encoded) > MAX_CAPTURE_CHARS:
            problems.append('RAW_BYTES_MISSING_OR_OVERSIZE_'+pkey.upper())
            continue
        try:
            raw = base64.b64decode(encoded, validate=True)
        except (binascii.Error, ValueError):
            problems.append('INVALID_BASE64_'+pkey.upper())
            continue
        if not raw or len(raw) > MAX_FILE_BYTES:
            problems.append('RAW_BYTES_EMPTY_OR_OVERSIZE_'+pkey.upper())
            continue
        if base64.b64encode(raw).decode('ascii') != encoded:
            problems.append('NONCANONICAL_BASE64_'+pkey.upper())
        if len(raw) != entry['bytes']:
            problems.append('ACTUAL_BYTES_MISMATCH_'+pkey.upper())
        if hashlib.sha256(raw).hexdigest() != entry['sha256']:
            problems.append('ACTUAL_SHA256_MISMATCH_'+pkey.upper())
        blob = hashlib.sha1(b'blob '+str(len(raw)).encode('ascii')+b'\0'+raw).hexdigest()
        if blob != entry['git_blob']:
            problems.append('ACTUAL_GIT_BLOB_MISMATCH_'+pkey.upper())
    if problems:
        return fail(*problems)
    return {'coverage':'BYTE_CAPTURE_CONSISTENT','reasons':[],
            'authentication':'NOT_ESTABLISHED','main_verified':False,
            'scientific_independence':'NOT_ESTABLISHED',
            'qualification':'CAPTURE_CONSISTENCY_ONLY_NOT_GITHUB_SOURCE_OR_CI_AUTHENTICATION'}


if __name__ == '__main__':
    try:
        if len(sys.argv) < 2:
            raise ValueError('missing input path')
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            x = json.load(f)
        legacy = sys.argv[2] if len(sys.argv)>2 else str(Path(__file__).with_name(LEGACY_NAME))
        out = evaluate(x, legacy)
    except (OSError, ValueError, TypeError, json.JSONDecodeError):
        out = fail('INPUT_ERROR')
    print(json.dumps(out, sort_keys=True))
    sys.exit(0 if out['coverage']=='BYTE_CAPTURE_CONSISTENT' else 2)
