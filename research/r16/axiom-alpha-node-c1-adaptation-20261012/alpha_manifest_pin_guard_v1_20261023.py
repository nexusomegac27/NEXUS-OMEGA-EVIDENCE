#!/usr/bin/env python3
"""C1 isolated scaffold: reject self-consistent, but UNPINNED source declarations.

The caller MUST obtain the expected manifest SHA-256 from an independent,
immutable authority and fetch the manifest and source bytes at pinned commits.
This function checks byte-level consistency only; it does NOT authenticate the
caller, GitHub actor, repository, transport, scientific claims or write rights.
It does not replace ALPHA_SOURCE_EXACTNESS_GUARD_V1 or its frozen evaluator.
"""
import hashlib
import json
import re

SHA256 = re.compile(r'[0-9a-f]{64}\Z')
SHA1 = re.compile(r'[0-9a-f]{40}\Z')


def _safe_path(path):
    return (type(path) is str and bool(path) and not path.startswith('/')
            and '\\' not in path and not any(ord(c) < 32 or ord(c) == 127 for c in path)
            and all(s not in ('', '.', '..') for s in path.split('/')))


def _unique_pairs(pairs):
    obj = {}
    for key, value in pairs:
        if key in obj:
            raise ValueError('duplicate JSON key')
        obj[key] = value
    return obj


def _reject_constant(value):
    raise ValueError('nonfinite JSON number')


def _blob(raw):
    return hashlib.sha1(b'blob ' + str(len(raw)).encode('ascii') + b'\0' + raw).hexdigest()


def check_pinned_manifest_exactness(manifest_raw, pinned_manifest_sha256,
                                    source_commit, source_path, source_raw,
                                    observed_blob_sha1):
    """Return status only; never infer provenance or authority from MATCH."""
    if (type(manifest_raw) is not bytes or type(source_raw) is not bytes
        or type(pinned_manifest_sha256) is not str or not SHA256.fullmatch(pinned_manifest_sha256)
        or type(source_commit) is not str or not SHA1.fullmatch(source_commit)
        or not _safe_path(source_path)
        or type(observed_blob_sha1) is not str or not SHA1.fullmatch(observed_blob_sha1)):
        return {'status': 'INCOMPLETE'}
    if hashlib.sha256(manifest_raw).hexdigest() != pinned_manifest_sha256:
        return {'status': 'MANIFEST_MISMATCH'}
    try:
        manifest = json.loads(manifest_raw.decode('utf-8'),
                              object_pairs_hook=_unique_pairs,
                              parse_constant=_reject_constant)
    except (ValueError, UnicodeDecodeError):
        return {'status': 'MANIFEST_INVALID'}
    if type(manifest) is not dict or type(manifest.get('files')) is not list:
        return {'status': 'MANIFEST_INVALID'}
    parent = manifest.get('immutable_assets_parent_commit')
    if type(parent) is not str or not SHA1.fullmatch(parent):
        return {'status': 'MANIFEST_INVALID'}
    paths = set()
    matched = None
    for item in manifest['files']:
        if type(item) is not dict or not _safe_path(item.get('path')):
            return {'status': 'MANIFEST_INVALID'}
        path = item['path']
        if path in paths:
            return {'status': 'MANIFEST_AMBIGUOUS'}
        paths.add(path)
        size, digest, blob_id = item.get('bytes'), item.get('sha256'), item.get('git_blob_sha1')
        if (type(size) is not int or size < 0 or type(digest) is not str
            or not SHA256.fullmatch(digest) or type(blob_id) is not str
            or not SHA1.fullmatch(blob_id)):
            return {'status': 'MANIFEST_INVALID'}
        if path == source_path:
            matched = item
    if source_commit != parent:
        return {'status': 'COMMIT_MISMATCH'}
    if matched is None:
        return {'status': 'SOURCE_NOT_DECLARED'}
    if (len(source_raw) != matched['bytes']
        or hashlib.sha256(source_raw).hexdigest() != matched['sha256']):
        return {'status': 'SOURCE_MISMATCH'}
    if _blob(source_raw) != matched['git_blob_sha1'] or observed_blob_sha1 != matched['git_blob_sha1']:
        return {'status': 'BLOB_MISMATCH'}
    return {'status': 'MATCH'}
