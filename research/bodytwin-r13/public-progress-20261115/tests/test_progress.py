#!/usr/bin/env python3
"""Offline contract tests for additive BodyTwin public progress UI and guarded publisher."""
from __future__ import annotations
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
SPEC = importlib.util.spec_from_file_location("bt_progress_release", ROOT / "ops" / "apply_bodytwin_progress.py")
M = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(M)
BASE = b'<html lang="de"><head><meta charset="utf-8"></head><body><main><section>Existing 4D Viewer XY XZ XW YZ YW ZW Perspektive Orthographisch Stereographisch Schlegel Doppel-Perspektive</section></main><footer>existing footer</footer></body></html>'

class PublicProgressTests(unittest.TestCase):
    def setUp(self):
        self.work = tempfile.TemporaryDirectory()
        self.addCleanup(self.work.cleanup)
        self.base = Path(self.work.name)
        self.web = self.base / "www"
        self.backups = self.base / "backups"
        (self.web / "bodytwin").mkdir(parents=True)
        self.backups.mkdir()
        (self.web / "bodytwin" / "index.html").write_bytes(BASE)

    def test_source_manifest_c1_and_zero_sensor_runtime(self):
        j = json.loads((SITE / "updates" / "events.json").read_text(encoding="utf8"))
        self.assertEqual(j["claim_ceiling"], "C1_DESCRIPTIVE_ONLY")
        self.assertEqual(j["bodytwin"]["validated"], "NO")
        self.assertEqual(j["bodytwin"]["consent_bind"], "OPEN")
        self.assertEqual(j["bodytwin"]["physical_imu"], "NOT_AUTHORIZED")
        self.assertFalse(j["published_live"])
        self.assertEqual(len(j["events"]), 5)
        self.assertEqual(len({e["id"] for e in j["events"]}), 5)
        self.assertFalse(any(e["scientific_result"] for e in j["events"]))

    def test_fragment_boundary_and_accessibility(self):
        x = (SITE / "progress-fragment.html").read_text(encoding="utf-8")
        self.assertEqual(x.count("NEXUS_BODYTWIN_C1_PROGRESS_20261115_START"), 1)
        self.assertEqual(x.count("NEXUS_BODYTWIN_C1_PROGRESS_20261115_END"), 1)
        self.assertIn('aria-labelledby="nexus-bt-progress-heading"', x)
        self.assertIn('BODYTWIN_VALIDATED=NO', x)
        self.assertIn('datetime="2026-11-15"', x)
        self.assertIn('/bodytwin/live/current.json', x)
        self.assertNotIn("<script", x.lower())

    def test_css_scoped_no_fixed_overlay(self):
        css = (SITE / "progress.css").read_text(encoding="utf8")
        self.assertTrue(css.startswith("/* NEXUS OMEGA BodyTwin"))
        self.assertNotIn("position:fixed", css.replace(" ", ""))
        self.assertNotIn("position:absolute", css.replace(" ", ""))
        self.assertIn("@media(max-width:640px)", css)
        self.assertIn("focus-visible", css)

    def test_standalone_no_js(self):
        doc = (SITE / "updates" / "index.html").read_text(encoding="utf8")
        self.assertTrue(doc.startswith("<!doctype html>"))
        self.assertIn('href="/bodytwin/"', doc)
        self.assertIn('href="/bodytwin/updates/progress.css"', doc)
        self.assertIn("Was sich seit September verändert hat", doc)
        self.assertNotIn("<script", doc.lower())

    def test_plan_exactly_reversible(self):
        frag = (SITE / "progress-fragment.html").read_bytes()
        new, code = M.plan(BASE, frag)
        self.assertEqual(code, "READY")
        self.assertIn(b"<section>Existing 4D Viewer", new)
        self.assertIn(b"<footer>existing footer", new)
        self.assertEqual(new.count(b"id=\"nexus-bodytwin-progress-20261115\""), 1)
        self.assertEqual(new.count(b"</main>"), 1)
        self.assertEqual(M.plan(new, frag), (new, "ALREADY_PRESENT"))

    def test_dry_run_never_writes(self):
        result = M.run(self.web, SITE, False, "", None)
        self.assertEqual(result["mode"], "DRY_RUN")
        self.assertEqual(result["state"], "READY")
        self.assertEqual((self.web / "bodytwin" / "index.html").read_bytes(), BASE)
        self.assertFalse((self.web / "bodytwin" / "updates").exists())

    def test_apply_requires_release_ack(self):
        with self.assertRaisesRegex(ValueError, "EXPLICIT_OPERATOR_PUBLICATION_ACK_REQUIRED"):
            M.run(self.web, SITE, True, "", self.backups)
        self.assertEqual((self.web / "bodytwin" / "index.html").read_bytes(), BASE)

    def test_apply_atomic_and_backup(self):
        result = M.run(self.web, SITE, True, M.RELEASE, self.backups)
        self.assertTrue(result["html_on_disk_matches"])
        self.assertEqual(result["asset_files_deployed"], 3)
        b = list(self.backups.glob("*.html"))
        self.assertEqual(len(b), 1)
        self.assertEqual(b[0].read_bytes(), BASE)
        self.assertTrue((self.web / "bodytwin" / "updates" / "index.html").exists())
        self.assertTrue((self.web / "bodytwin" / "updates" / "events.json").exists())
        self.assertEqual(M.run(self.web, SITE, False, "", None)["state"], "ALREADY_PRESENT")

    def test_repeat_apply_is_noop(self):
        M.run(self.web, SITE, True, M.RELEASE, self.backups)
        result = M.run(self.web, SITE, True, M.RELEASE, self.backups)
        self.assertEqual(result["mode"], "ALREADY_DEPLOYED_LOCAL_FILES_NOT_HTTP_VERIFIED")
        self.assertEqual(len(list(self.backups.glob("*.html"))), 1)

    def test_partial_marker_fail_closed(self):
        html = BASE.replace(b"</main>", b"<!-- NEXUS_BODYTWIN_C1_PROGRESS_20261115_START --></main>")
        with self.assertRaisesRegex(ValueError, "PARTIAL_OR_DUPLICATE_UPDATE"):
            M.plan(html, (SITE / "progress-fragment.html").read_bytes())

    def test_missing_anchor_fail_closed(self):
        with self.assertRaisesRegex(ValueError, "NO_UNIQUE_HEAD_MAIN_INSERTION_ANCHORS"):
            M.plan(BASE.replace(b"</main>", b""), (SITE / "progress-fragment.html").read_bytes())

    def test_collision_fail_closed(self):
        u = self.web / "bodytwin" / "updates"
        u.mkdir()
        (u / "progress.css").write_text("foreign source", encoding="utf8")
        with self.assertRaisesRegex(ValueError, "EXISTING_ASSET_COLLISION"):
            M.run(self.web, SITE, False, "", None)

    def test_backup_directory_must_be_outside_webroot(self):
        with self.assertRaisesRegex(ValueError, "BACKUP_LOCATION_NOT_ISOLATED"):
            M.run(self.web, SITE, True, M.RELEASE, self.web)

if __name__ == "__main__":
    unittest.main(verbosity=2)
