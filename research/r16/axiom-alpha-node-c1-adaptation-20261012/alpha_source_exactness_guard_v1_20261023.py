#!/usr/bin/env python3
"""C1 research-only exact-byte GitHub readback guard; no scientific approval.

Caller must obtain actual raw bytes and blob ID at a pinned commit independently.
This validator cannot authenticate the transport, actor, branch or claimed source.
"""
import hashlib
import re

_SHA256 = re.compile(r'[0-9a-f]{64}\Z')
_SHA1 = re.compile(r'[0-9a-f]{40}\Z')


def check_source_exactness(raw, expected_bytes, expected_sha256, observed_blob_sha1):
    if (type(raw) is not bytes or type(expected_bytes) is not int
        or expected_bytes < 0 or type(expected_sha256) is not str
        or type(observed_blob_sha1) is not str
        or _SHA256.fullmatch(expected_sha256) is None
        or _SHA1.fullmatch(observed_blob_sha1) is None):
        return {'status': 'INCOMPLETE'}
    if (len(raw) != expected_bytes
        or hashlib.sha256(raw).hexdigest() != expected_sha256):
        return {'status': 'SOURCE_MISMATCH'}
    blob = hashlib.sha1(b'blob ' + str(len(raw)).encode('ascii') + b'\0' + raw).hexdigest()
    if blob != observed_blob_sha1:
        return {'status': 'BLOB_MISMATCH'}
    return {'status': 'MATCH'}
