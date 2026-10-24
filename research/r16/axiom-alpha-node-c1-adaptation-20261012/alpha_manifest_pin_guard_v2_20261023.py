#!/usr/bin/env python3
"""C1 isolated V2: reject nonfinite JSON numeric overflow in pinned manifests.

Preserves V1 source exactly and delegates its existing evidence/status checks.
This adds a strict finite-float parse only after V1 returns MATCH. The expected
manifest digest still must be pinned independently of the producer; this does
not authenticate sources, GitHub actors, experts, or authorize publication.
"""
import hashlib
import importlib.util
import json
import math
from pathlib import Path

V1_NAME = 'alpha_manifest_pin_guard_v1_20261023.py'
V1_SHA256 = '06a8d4e589390a67187fd14194d7e32cbb56f824e5bf694b8b20b16b404eeadb'


def _finite_float(token):
    number = float(token)
    if not math.isfinite(number):
        raise ValueError('nonfinite float overflow')
    return number


def _reject_constant(_token):
    raise ValueError('nonfinite JSON constant')


def _unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('duplicate JSON key')
        result[key] = value
    return result


def check_pinned_manifest_exactness(manifest_raw, pinned_manifest_sha256,
                                    source_commit, source_path, source_raw,
                                    observed_blob_sha1):
    path = Path(__file__).with_name(V1_NAME)
    try:
        source = path.read_bytes()
        if hashlib.sha256(source).hexdigest() != V1_SHA256:
            return {'status': 'INCOMPLETE'}
        spec = importlib.util.spec_from_file_location('pinned_manifest_guard_v1', path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        baseline = module.check_pinned_manifest_exactness(
            manifest_raw, pinned_manifest_sha256, source_commit,
            source_path, source_raw, observed_blob_sha1)
        if baseline.get('status') != 'MATCH':
            return baseline
        json.loads(manifest_raw.decode('utf-8'), parse_float=_finite_float,
                   parse_constant=_reject_constant, object_pairs_hook=_unique_pairs)
        return baseline
    except (OSError, ValueError, UnicodeDecodeError, ImportError, SyntaxError, TypeError):
        return {'status': 'MANIFEST_INVALID'}
