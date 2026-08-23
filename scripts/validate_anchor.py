#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Validate NEXUS OMEGA anchor manifests using only the Python standard library."""

from __future__ import annotations

import argparse
from datetime import datetime
import hashlib
import json
import re
import sys
from pathlib import Path

HEX64 = re.compile(r"^[0-9a-f]{64}$")
LOCAL_PATH_PATTERNS = [
    re.compile(r"%TEMP%", re.IGNORECASE),
    re.compile(r"\b[A-Za-z]:\\"),
    re.compile(r"/(?:home|Users|tmp)/"),
]
SECRET_PATTERNS = [
    re.compile(r"\bghp_[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b"),
    re.compile(r"\bsk-[A-Za-z0-9]{20,}\b"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
]


class ValidationError(Exception):
    def __init__(self, code: str):
        super().__init__(code)
        self.code = code


def reject_duplicates(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValidationError("DUPLICATE_JSON_KEY")
        result[key] = value
    return result


def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    except UnicodeDecodeError as exc:
        raise ValidationError("UTF8_DECODE_FAILED") from exc
    except json.JSONDecodeError as exc:
        raise ValidationError("MANIFEST_JSON_INVALID") from exc


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def require(condition: bool, code: str) -> None:
    if not condition:
        raise ValidationError(code)


def scan_public_bytes(data: bytes) -> None:
    text = data.decode("utf-8", errors="strict")
    for pattern in SECRET_PATTERNS:
        require(not pattern.search(text), "SECRET_SCAN_FAILED")
    for pattern in LOCAL_PATH_PATTERNS:
        require(not pattern.search(text), "LOCAL_PATH_DISCLOSURE")


def validate_manifest(root: Path, manifest_path: Path, strict_external: bool) -> dict:
    manifest = load_json(manifest_path)
    required = {
        "schema_version", "object_id", "version", "lane", "title", "claim",
        "verdict", "caveats", "asset", "parents", "publication", "authority",
        "semantic_scopes", "supersedes", "issued_at",
    }
    require(set(manifest) == required, "MANIFEST_FIELD_SET_MISMATCH")
    require(manifest["schema_version"] == "1.0.0", "SCHEMA_VERSION_UNSUPPORTED")
    require(manifest["claim"] == "C1_ONLY", "CLAIM_CEILING_VIOLATION")
    require(manifest["authority"] == {
        "claim_ceiling": "C1",
        "promotion_authorized": False,
        "deployment_authorized": False,
    }, "AUTHORITY_VIOLATION")

    asset = manifest["asset"]
    require(set(asset) == {"path", "media_type", "bytes", "sha256"}, "ASSET_FIELD_SET_MISMATCH")
    require(HEX64.fullmatch(asset["sha256"]) is not None, "ASSET_HASH_FORMAT_INVALID")
    asset_path = (root / asset["path"]).resolve()
    require(str(asset_path).startswith(str(root.resolve()) + "/"), "ASSET_PATH_ESCAPE")
    require(asset_path.is_file(), "ASSET_SOURCE_NOT_PRESENT")
    data = asset_path.read_bytes()
    require(len(data) == int(asset["bytes"]), "ASSET_LENGTH_MISMATCH")
    require(sha256(data) == asset["sha256"], "ASSET_HASH_MISMATCH")
    path_parts = Path(asset["path"]).parts
    require(
        len(path_parts) == 6
        and path_parts[:2] == ("objects", "sha256")
        and path_parts[2] == asset["sha256"][:2]
        and path_parts[3] == asset["sha256"][2:4]
        and path_parts[4] == asset["sha256"],
        "CONTENT_ADDRESS_MISMATCH",
    )
    scan_public_bytes(data)

    scope_ids = set()
    for scope in manifest["semantic_scopes"]:
        require(set(scope) == {"scope_id", "bytes", "sha256"}, "SEMANTIC_SCOPE_FIELD_SET_MISMATCH")
        require(scope["scope_id"] not in scope_ids, "SEMANTIC_SCOPE_ID_DUPLICATE")
        scope_ids.add(scope["scope_id"])
        require(HEX64.fullmatch(scope["sha256"]) is not None, "SEMANTIC_SCOPE_HASH_FORMAT_INVALID")
        length = int(scope["bytes"])
        require(0 < length <= len(data), "SEMANTIC_SCOPE_LENGTH_INVALID")
        require(sha256(data[:length]) == scope["sha256"], "SEMANTIC_SCOPE_MISMATCH")

    parent_ids = set()
    for parent in manifest["parents"]:
        require(set(parent) == {"object_id", "bytes", "sha256"}, "PARENT_FIELD_SET_MISMATCH")
        require(parent["object_id"] not in parent_ids, "PARENT_ID_DUPLICATE")
        parent_ids.add(parent["object_id"])
        require(int(parent["bytes"]) > 0, "PARENT_LENGTH_INVALID")
        require(HEX64.fullmatch(parent["sha256"]) is not None, "PARENT_HASH_FORMAT_INVALID")

    try:
        issued_at = datetime.fromisoformat(manifest["issued_at"])
    except (TypeError, ValueError) as exc:
        raise ValidationError("ISSUED_AT_INVALID") from exc
    require(issued_at.tzinfo is not None, "ISSUED_AT_TIMEZONE_MISSING")

    publication = manifest["publication"]
    publication_fields = {
        "anchor_level", "github_repository", "git_commit", "release_tag",
        "release_url", "immutable_release_verified", "release_asset_verified",
        "zenodo_doi", "software_heritage_swhid",
    }
    require(set(publication) == publication_fields, "PUBLICATION_FIELD_SET_MISMATCH")
    if strict_external:
        require(publication["anchor_level"] in {
            "A3_INDEPENDENT_ARCHIVE_WITNESS", "A4_MULTI_AGENT_REPRODUCTION"
        }, "INDEPENDENT_WITNESS_MISSING")
        require(publication["immutable_release_verified"] is True, "IMMUTABLE_RELEASE_NOT_VERIFIED")
        require(publication["release_asset_verified"] is True, "RELEASE_ASSET_VERIFY_FAILED")
        require(publication["github_repository"] == "https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE", "REPOSITORY_BINDING_MISMATCH")
        require(bool(publication["zenodo_doi"] or publication["software_heritage_swhid"]), "INDEPENDENT_WITNESS_MISSING")
    else:
        require(publication["anchor_level"] == "A0_LOCAL_STAGING", "STAGING_ANCHOR_LEVEL_INVALID")
        require(publication["github_repository"] == "SOURCE_NOT_BOUND", "STAGING_REPOSITORY_MUST_BE_UNBOUND")
        require(publication["immutable_release_verified"] is False, "STAGING_RELEASE_STATE_INVALID")
        require(publication["release_asset_verified"] is False, "STAGING_RELEASE_STATE_INVALID")

    return manifest


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--strict-external", action="store_true")
    args = parser.parse_args()
    try:
        manifest = validate_manifest(args.root, args.manifest, args.strict_external)
    except ValidationError as exc:
        print(json.dumps({"status": "FAIL", "code": exc.code}, sort_keys=True))
        return 1
    code = "EXTERNAL_ANCHOR_VALID" if args.strict_external else "A0_STAGING_VALID"
    print(json.dumps({"status": "PASS", "code": code, "object_id": manifest["object_id"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
