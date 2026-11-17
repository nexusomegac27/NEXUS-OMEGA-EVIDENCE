#!/usr/bin/env python3
"""R33-R2 negative matrix B01–B12 + positive fences (meaningful mutations only)."""
from __future__ import annotations

import copy
import importlib.util
import json
import math
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src" / "render_methods_offline.py"
CAPSULE = ROOT / "data" / "07_BODYTWIN_R33_METHODS_CAPSULE.json"


def load_mod():
    spec = importlib.util.spec_from_file_location("render_methods_offline", SRC)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


MOD = load_mod()


def base_capsule() -> dict:
    return json.loads(CAPSULE.read_text(encoding="utf-8"))


def write_raw(tmpdir: Path, raw: bytes) -> Path:
    path = tmpdir / "mutant.json"
    path.write_bytes(raw)
    return path


def write_obj(tmpdir: Path, obj: dict) -> Path:
    return write_raw(
        tmpdir,
        (json.dumps(obj, ensure_ascii=False, indent=2) + "\n").encode("utf-8"),
    )


class R33R2NegativeMatrix(unittest.TestCase):
    def test_b01_html_injection_escaped_or_rejected(self) -> None:
        """B01: XSS / HTML injection in title must not survive unescaped."""
        obj = base_capsule()
        payload = '<img src=x onerror=alert(1)>'
        obj["new_methods"][0]["title"] = payload
        with tempfile.TemporaryDirectory() as td:
            path = write_obj(Path(td), obj)
            # Semantic fences allow title string; render must escape.
            receipt = MOD.render_once(path)
            html_text = (ROOT / "candidate_offline" / "methods_assurance.html").read_text(
                encoding="utf-8"
            )
            self.assertNotIn(payload, html_text)
            self.assertIn("&lt;img", html_text)
            self.assertFalse(receipt.get("absolute_host_paths"))

    def test_b02_duplicate_json_keys_fail_closed(self) -> None:
        """B02: duplicate JSON keys must FAIL (not last-wins)."""
        raw = b'{"object":"x","bodytwin_validated":"NO","bodytwin_validated":"YES","claim_ceiling":"C1_DESCRIPTIVE_ONLY","claim_promotion":false,"clinical_validated":false,"whole_body_pose_validated":false,"physical_measurement_validated":false,"consent_bind":"OPEN","trial_001":"DESIGNED_NOT_EXECUTED","publication_status":"OFFLINE_CANDIDATE_NOT_WWW_WITNESSED","new_methods":[]}'
        with self.assertRaises(MOD.ContractError) as ctx:
            MOD.load_bytes(raw)
        self.assertIn("duplicate_json_key", str(ctx.exception))

    def test_b03_nonfinite_nan_fail_closed(self) -> None:
        """B03: NaN / Infinity must FAIL."""
        raw = b'{"object":"x","observed":NaN,"bodytwin_validated":"NO","claim_ceiling":"C1_DESCRIPTIVE_ONLY","claim_promotion":false,"clinical_validated":false,"whole_body_pose_validated":false,"physical_measurement_validated":false,"consent_bind":"OPEN","trial_001":"DESIGNED_NOT_EXECUTED","publication_status":"OFFLINE_CANDIDATE_NOT_WWW_WITNESSED","new_methods":[]}'
        with self.assertRaises(MOD.ContractError) as ctx:
            MOD.load_bytes(raw)
        self.assertTrue(
            "nonfinite" in str(ctx.exception).lower()
            or "json_decode" in str(ctx.exception).lower()
        )

    def test_b04_bodytwin_validated_yes_fail(self) -> None:
        """B04: bodytwin_validated=YES must FAIL."""
        obj = base_capsule()
        obj["bodytwin_validated"] = "YES"
        with tempfile.TemporaryDirectory() as td:
            path = write_obj(Path(td), obj)
            with self.assertRaises(MOD.ContractError) as ctx:
                MOD.render_once(path)
            self.assertIn("bodytwin_validated", str(ctx.exception))

    def test_b05_clinical_validated_true_fail(self) -> None:
        """B05: clinical_validated=true must FAIL."""
        obj = base_capsule()
        obj["clinical_validated"] = True
        with tempfile.TemporaryDirectory() as td:
            path = write_obj(Path(td), obj)
            with self.assertRaises(MOD.ContractError) as ctx:
                MOD.render_once(path)
            self.assertIn("clinical_validated", str(ctx.exception))

    def test_b06_consent_bind_closed_fail(self) -> None:
        """B06: consent_bind!=OPEN must FAIL."""
        obj = base_capsule()
        obj["consent_bind"] = "CLOSED"
        with tempfile.TemporaryDirectory() as td:
            path = write_obj(Path(td), obj)
            with self.assertRaises(MOD.ContractError) as ctx:
                MOD.render_once(path)
            self.assertIn("consent_bind", str(ctx.exception))

    def test_b07_claim_ceiling_substring_trap(self) -> None:
        """B07: C10_DESCRIPTIVE_ONLY must FAIL exact equality (not substring)."""
        obj = base_capsule()
        obj["claim_ceiling"] = "C10_DESCRIPTIVE_ONLY"
        self.assertIn("C1", obj["claim_ceiling"])  # documents F03 trap
        with tempfile.TemporaryDirectory() as td:
            path = write_obj(Path(td), obj)
            with self.assertRaises(MOD.ContractError) as ctx:
                MOD.render_once(path)
            self.assertIn("claim_ceiling", str(ctx.exception))

    def test_b08_claim_promotion_true_fail(self) -> None:
        """B08: claim_promotion=true must FAIL."""
        obj = base_capsule()
        obj["claim_promotion"] = True
        with tempfile.TemporaryDirectory() as td:
            path = write_obj(Path(td), obj)
            with self.assertRaises(MOD.ContractError) as ctx:
                MOD.render_once(path)
            self.assertIn("claim_promotion", str(ctx.exception))

    def test_b09_private_topology_path_fail(self) -> None:
        """B09: absolute Windows / TRANSFER worker topology in payload must FAIL."""
        obj = base_capsule()
        obj["new_methods"][0]["observed"]["tool_version"] = (
            r"C:\Users\alexa\AppData\Local\Temp\evil"
        )
        with tempfile.TemporaryDirectory() as td:
            path = write_obj(Path(td), obj)
            with self.assertRaises(MOD.ContractError) as ctx:
                MOD.render_once(path)
            self.assertIn("private_topology", str(ctx.exception))

    def test_b10_invalid_utf8_fail(self) -> None:
        """B10: invalid UTF-8 must FAIL."""
        with self.assertRaises(MOD.ContractError) as ctx:
            MOD.load_bytes(b'{"object":"\xff"}')
        self.assertIn("invalid_utf8", str(ctx.exception))

    def test_b11_measurement_claim_true_fail(self) -> None:
        """B11: method bodytwin_measurement_claim=true must FAIL."""
        obj = base_capsule()
        obj["new_methods"][0]["bodytwin_measurement_claim"] = True
        with tempfile.TemporaryDirectory() as td:
            path = write_obj(Path(td), obj)
            with self.assertRaises(MOD.ContractError) as ctx:
                MOD.render_once(path)
            self.assertIn("bodytwin_measurement_claim", str(ctx.exception))

    def test_b12_physical_and_whole_body_pose_fail(self) -> None:
        """B12: physical_measurement / whole_body_pose true must FAIL."""
        for field in ("physical_measurement_validated", "whole_body_pose_validated"):
            obj = base_capsule()
            obj[field] = True
            with tempfile.TemporaryDirectory() as td:
                path = write_obj(Path(td), obj)
                with self.assertRaises(MOD.ContractError) as ctx:
                    MOD.render_once(path)
                self.assertIn(field, str(ctx.exception))

    def test_positive_exact_claim_ceiling(self) -> None:
        obj = base_capsule()
        self.assertEqual(obj["claim_ceiling"], "C1_DESCRIPTIVE_ONLY")
        self.assertNotEqual(obj["claim_ceiling"], "C10_DESCRIPTIVE_ONLY")

    def test_positive_render_once_and_relative_receipt(self) -> None:
        receipt = MOD.render_once()
        self.assertEqual(receipt["double_pass"], "PASS")
        self.assertFalse(receipt["absolute_host_paths"])
        self.assertNotIn("C:\\", receipt["capsule_path"])
        self.assertNotIn("C:/", receipt["capsule_path"])
        self.assertEqual(receipt["public_history_review"], "PUBLIC_HISTORY_REVIEW_PENDING")
        html_text = (ROOT / "candidate_offline" / "methods_assurance.html").read_text(
            encoding="utf-8"
        )
        self.assertIn("BODYTWIN_VALIDATED=NO", html_text)
        self.assertIn("CONSENT_BIND=OPEN", html_text)


if __name__ == "__main__":
    unittest.main()
