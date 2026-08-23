#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Cross-check repository discovery indexes against validated object manifests."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

from validate_anchor import ValidationError, load_json, require, validate_manifest


def digest(path: Path) -> tuple[str, str]:
    data = path.read_bytes()
    return str(len(data)), hashlib.sha256(data).hexdigest()


def load_jsonl(path: Path) -> list[dict]:
    rows = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        require(bool(line.strip()), "OBJECT_INDEX_BLANK_LINE")
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise ValidationError(f"OBJECT_INDEX_JSON_INVALID_LINE_{number}") from exc
    return rows


def validate_repository(root: Path) -> dict:
    root = root.resolve()
    latest = load_json(root / "index/v1/latest.json")
    rows = load_jsonl(root / "index/v1/objects.jsonl")
    require(rows, "OBJECT_INDEX_EMPTY")

    manifests = sorted(root.glob("objects/sha256/*/*/*/manifest.json"))
    require(manifests, "MANIFEST_INVENTORY_EMPTY")
    validated = {}
    for manifest_path in manifests:
        manifest = validate_manifest(root, manifest_path, strict_external=False)
        require(manifest["object_id"] not in validated, "OBJECT_ID_DUPLICATE")
        validated[manifest["object_id"]] = (manifest, manifest_path)

    row_ids = [row["object_id"] for row in rows]
    require(len(row_ids) == len(set(row_ids)), "OBJECT_INDEX_ID_DUPLICATE")
    require(set(row_ids) == set(validated), "OBJECT_INDEX_MANIFEST_SET_MISMATCH")

    for row in rows:
        manifest, manifest_path = validated[row["object_id"]]
        manifest_bytes, manifest_hash = digest(manifest_path)
        require(row["manifest_path"] == manifest_path.relative_to(root).as_posix(), "OBJECT_INDEX_MANIFEST_PATH_MISMATCH")
        require(row["manifest_bytes"] == manifest_bytes, "OBJECT_INDEX_MANIFEST_LENGTH_MISMATCH")
        require(row["manifest_sha256"] == manifest_hash, "OBJECT_INDEX_MANIFEST_HASH_MISMATCH")
        require(row["asset_path"] == manifest["asset"]["path"], "OBJECT_INDEX_ASSET_PATH_MISMATCH")
        require(row["asset_bytes"] == manifest["asset"]["bytes"], "OBJECT_INDEX_ASSET_LENGTH_MISMATCH")
        require(row["asset_sha256"] == manifest["asset"]["sha256"], "OBJECT_INDEX_ASSET_HASH_MISMATCH")
        require(row["claim"] == manifest["claim"], "OBJECT_INDEX_CLAIM_MISMATCH")
        require(row["verdict"] == manifest["verdict"], "OBJECT_INDEX_VERDICT_MISMATCH")

    require(latest["object_id"] in validated, "LATEST_OBJECT_NOT_FOUND")
    head_manifest, head_path = validated[latest["object_id"]]
    head_bytes, head_hash = digest(head_path)
    require(latest["manifest_path"] == head_path.relative_to(root).as_posix(), "LATEST_MANIFEST_PATH_MISMATCH")
    require(latest["manifest_bytes"] == head_bytes, "LATEST_MANIFEST_LENGTH_MISMATCH")
    require(latest["manifest_sha256"] == head_hash, "LATEST_MANIFEST_HASH_MISMATCH")
    require(latest["asset_path"] == head_manifest["asset"]["path"], "LATEST_ASSET_PATH_MISMATCH")
    require(latest["asset_bytes"] == head_manifest["asset"]["bytes"], "LATEST_ASSET_LENGTH_MISMATCH")
    require(latest["asset_sha256"] == head_manifest["asset"]["sha256"], "LATEST_ASSET_HASH_MISMATCH")
    require(latest["claim_ceiling"] == "C1", "LATEST_CLAIM_CEILING_VIOLATION")
    require(latest["canonical_promotion"] is False, "LATEST_PROMOTION_VIOLATION")

    return {"objects": len(validated), "latest_object_id": latest["object_id"]}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    try:
        result = validate_repository(args.root)
    except (OSError, KeyError, TypeError, ValidationError) as exc:
        code = exc.code if isinstance(exc, ValidationError) else type(exc).__name__.upper()
        print(json.dumps({"status": "FAIL", "code": code}, sort_keys=True))
        return 1
    print(json.dumps({"status": "PASS", "code": "REPOSITORY_INDEX_VALID", **result}, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
