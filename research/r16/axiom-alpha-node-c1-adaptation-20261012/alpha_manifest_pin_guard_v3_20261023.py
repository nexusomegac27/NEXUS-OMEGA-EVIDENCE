#!/usr/bin/env python3
"""C1 isolated V3: distinguish missing pinned dependencies from invalid manifests.

Append-only successor to V2. V1 and V2 are independently pinned to exact
published bytes and remain unchanged. This is a status-classification scaffold,
not a provenance authenticator, runtime integration, or publication authority.
"""
import hashlib
import importlib.util
from pathlib import Path

V1_NAME = 'alpha_manifest_pin_guard_v1_20261023.py'
V1_SHA256 = '06a8d4e589390a67187fd14194d7e32cbb56f824e5bf694b8b20b16b404eeadb'
V2_NAME = 'alpha_manifest_pin_guard_v2_20261023.py'
V2_SHA256 = 'b8d3e1089a1f972408e51e7795074e8157a49b2ecbef372908f1fec07c0d72f1'


def _dependencies_match():
    parent = Path(__file__).resolve().parent
    try:
        return all(hashlib.sha256((parent / name).read_bytes()).hexdigest() == digest
                   for name, digest in ((V1_NAME, V1_SHA256), (V2_NAME, V2_SHA256)))
    except OSError:
        return False


def check_pinned_manifest_exactness(manifest_raw, pinned_manifest_sha256,
                                    source_commit, source_path, source_raw,
                                    observed_blob_sha1):
    if not _dependencies_match():
        return {'status': 'INCOMPLETE'}
    path = Path(__file__).resolve().with_name(V2_NAME)
    try:
        spec = importlib.util.spec_from_file_location('pinned_manifest_guard_v2', path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        result = module.check_pinned_manifest_exactness(
            manifest_raw, pinned_manifest_sha256, source_commit,
            source_path, source_raw, observed_blob_sha1)
        # Recheck after V2: a dependency disappearing during the call is a gap,
        # not proof of an invalid manifest. This is not a concurrency guarantee.
        if not _dependencies_match():
            return {'status': 'INCOMPLETE'}
        return result
    except (OSError, ImportError, SyntaxError, TypeError, AttributeError):
        return {'status': 'INCOMPLETE'}
