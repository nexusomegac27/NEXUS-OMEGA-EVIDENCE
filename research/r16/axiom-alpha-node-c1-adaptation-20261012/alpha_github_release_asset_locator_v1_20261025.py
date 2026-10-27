#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""C1 read-only GitHub release-asset locator; metadata is never byte evidence.

Input is a caller-provided GitHub REST release JSON snapshot and the exact
source URL. The caller must independently authenticate the API response.
No network calls, downloads, writes, release mutations, or handoff completion.
"""
from __future__ import annotations
import re

SHA256 = re.compile(r'^sha256:[0-9a-f]{64}$')
OWNER = re.compile(r'^[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,37})$')
REPO = re.compile(r'^[a-zA-Z0-9_.-]{1,100}$')
TOKEN = re.compile(r'^[a-zA-Z0-9][a-zA-Z0-9._-]{0,160}$')
MAX_ASSETS = 2000
MAX_SAFE_INT = 2**53 - 1


def _result(status: str, reason: str) -> dict:
    return {'status': status, 'reason': reason,
            'original_bytes_verified': False, 'sha256_verified': False,
            'claim_ceiling': 'C1_DESCRIPTIVE_ONLY'}


def _integer(value: object) -> bool:
    return type(value) is int and 0 < value <= MAX_SAFE_INT


def locate_release_asset(snapshot: object, api_source_url: object,
                         owner: object, repo: object, tag: object,
                         filename: object) -> dict:
    """Distinguish a discovered release asset from verified downloaded bytes.

    SOURCE_NOT_PRESENT_IN_RELEASE_METADATA means only absence in this one
    supplied release response; it does not establish global absence.
    """
    bad = lambda reason: _result('INCOMPLETE_FAIL_CLOSED', reason)
    if (not isinstance(owner, str) or not OWNER.fullmatch(owner)
        or not isinstance(repo, str) or not REPO.fullmatch(repo)
        or not isinstance(tag, str) or not TOKEN.fullmatch(tag)
        or not isinstance(filename, str) or not TOKEN.fullmatch(filename)):
        return bad('invalid_expected_locator')
    api = f'https://api.github.com/repos/{owner}/{repo}/releases/tags/{tag}'
    if not isinstance(api_source_url, str) or api_source_url != api:
        return bad('unbound_api_source_url')
    if not isinstance(snapshot, dict):
        return bad('invalid_release_response')
    if (not _integer(snapshot.get('id')) or snapshot.get('tag_name') != tag
        or snapshot.get('draft') is not False
        or snapshot.get('prerelease') is not False):
        return bad('invalid_or_nonpublic_release')
    assets = snapshot.get('assets')
    if not isinstance(assets, list) or len(assets) > MAX_ASSETS:
        return bad('invalid_asset_collection')
    names = set()
    selected = None
    for asset in assets:
        if not isinstance(asset, dict) or not isinstance(asset.get('name'), str):
            return bad('invalid_asset_name')
        name = asset['name']
        if not TOKEN.fullmatch(name):
            return bad('invalid_asset_name')
        folded = name.casefold()
        if folded in names:
            return bad('ambiguous_asset_name_collision')
        names.add(folded)
        if name == filename:
            selected = asset
    if selected is None:
        return _result('SOURCE_NOT_PRESENT_IN_RELEASE_METADATA', 'no_exact_name_match')
    aid, size = selected.get('id'), selected.get('size')
    if not _integer(aid) or not _integer(size):
        return bad('invalid_asset_id_or_size')
    if selected.get('state') != 'uploaded' or selected.get('content_type') != 'application/zip':
        return bad('asset_not_uploaded_zip')
    url = f'https://github.com/{owner}/{repo}/releases/download/{tag}/{filename}'
    asset_api = f'https://api.github.com/repos/{owner}/{repo}/releases/assets/{aid}'
    if selected.get('browser_download_url') != url or selected.get('url') != asset_api:
        return bad('asset_url_identity_mismatch')
    digest = selected.get('digest')
    if digest is not None and (not isinstance(digest, str) or not SHA256.fullmatch(digest)):
        return bad('invalid_reported_digest')
    return {**_result('ASSET_LOCATED_METADATA_ONLY_C1', 'download_and_rehash_not_performed'),
            'release_id': snapshot['id'], 'asset_id': aid,
            'asset_size_reported': size, 'asset_digest_reported': digest,
            'asset_url': url, 'asset_api_url': asset_api}
