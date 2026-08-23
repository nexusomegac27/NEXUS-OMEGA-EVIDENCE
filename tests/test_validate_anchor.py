#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from scripts.validate_anchor import ValidationError, load_json, validate_manifest


class AnchorValidationTests(unittest.TestCase):
    def make_case(self, asset_text="evidence\n"):
        temp = tempfile.TemporaryDirectory()
        root = Path(temp.name)
        data = asset_text.encode("utf-8")
        digest = hashlib.sha256(data).hexdigest()
        asset = root / "objects" / "sha256" / digest[:2] / digest[2:4] / digest / "artifact.md"
        asset.parent.mkdir(parents=True)
        asset.write_bytes(data)
        manifest = {
            "schema_version": "1.0.0",
            "object_id": "TEST_OBJECT_R0",
            "version": "R0",
            "lane": "TEST",
            "title": "Good",
            "claim": "C1_ONLY",
            "verdict": "PASS_WITH_CAVEATS",
            "caveats": ["TEST_ONLY"],
            "asset": {
                "path": str(asset.relative_to(root)).replace("\\", "/"),
                "media_type": "text/markdown",
                "bytes": str(len(data)),
                "sha256": digest,
            },
            "semantic_scopes": [],
            "parents": [],
            "publication": {
                "anchor_level": "A0_LOCAL_STAGING",
                "github_repository": "SOURCE_NOT_BOUND",
                "git_commit": "SOURCE_NOT_BOUND",
                "release_tag": "SOURCE_NOT_BOUND",
                "release_url": "SOURCE_NOT_BOUND",
                "immutable_release_verified": False,
                "release_asset_verified": False,
                "zenodo_doi": "SOURCE_NOT_BOUND",
                "software_heritage_swhid": "SOURCE_NOT_BOUND"
            },
            "authority": {
                "claim_ceiling": "C1",
                "promotion_authorized": False,
                "deployment_authorized": False
            },
            "supersedes": None,
            "issued_at": "2026-08-23T23:00:00+02:00"
        }
        path = root / "manifest.json"
        path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8", newline="\n")
        return temp, root, path, manifest

    def test_good_staging(self):
        temp, root, path, _ = self.make_case()
        self.addCleanup(temp.cleanup)
        self.assertEqual(validate_manifest(root, path, False)["object_id"], "TEST_OBJECT_R0")

    def test_hash_mismatch(self):
        temp, root, path, manifest = self.make_case()
        self.addCleanup(temp.cleanup)
        manifest["asset"]["sha256"] = "f" * 64
        path.write_text(json.dumps(manifest), encoding="utf-8")
        with self.assertRaisesRegex(ValidationError, "ASSET_HASH_MISMATCH"):
            validate_manifest(root, path, False)

    def test_local_path_rejected(self):
        temp, root, path, _ = self.make_case("%TEMP%\\private\n")
        self.addCleanup(temp.cleanup)
        with self.assertRaisesRegex(ValidationError, "LOCAL_PATH_DISCLOSURE"):
            validate_manifest(root, path, False)

    def test_content_address_mismatch(self):
        temp, root, path, manifest = self.make_case()
        self.addCleanup(temp.cleanup)
        old_asset = root / manifest["asset"]["path"]
        wrong = root / "objects" / "sha256" / "00" / "00" / ("0" * 64) / "artifact.md"
        wrong.parent.mkdir(parents=True)
        wrong.write_bytes(old_asset.read_bytes())
        manifest["asset"]["path"] = str(wrong.relative_to(root)).replace("\\", "/")
        path.write_text(json.dumps(manifest), encoding="utf-8")
        with self.assertRaisesRegex(ValidationError, "CONTENT_ADDRESS_MISMATCH"):
            validate_manifest(root, path, False)

    def test_claim_escalation_rejected(self):
        temp, root, path, manifest = self.make_case()
        self.addCleanup(temp.cleanup)
        manifest["claim"] = "C2"
        path.write_text(json.dumps(manifest), encoding="utf-8")
        with self.assertRaisesRegex(ValidationError, "CLAIM_CEILING_VIOLATION"):
            validate_manifest(root, path, False)

    def test_duplicate_key_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "dup.json"
            path.write_text('{"a":1,"a":2}', encoding="utf-8")
            with self.assertRaisesRegex(ValidationError, "DUPLICATE_JSON_KEY"):
                load_json(path)

    def test_external_without_witness_rejected(self):
        temp, root, path, _ = self.make_case()
        self.addCleanup(temp.cleanup)
        with self.assertRaisesRegex(ValidationError, "INDEPENDENT_WITNESS_MISSING"):
            validate_manifest(root, path, True)


if __name__ == "__main__":
    unittest.main()
