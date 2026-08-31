#!/usr/bin/env python3
import importlib.util
import tempfile
import unittest
from argparse import Namespace
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("research_pipeline", ROOT / "scripts" / "research_pipeline.py")
RP = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(RP)


class ResearchPipelineTests(unittest.TestCase):
    def new_package(self, root: Path) -> str:
        ns = Namespace(
            root=root, phase="R5", strand="github-framework", title="Pipeline test",
            objective="Exercise package lifecycle", slug="pipeline-test", producer="AXIOM",
            processor="CURSOR_PRAXIS", predecessor=None, question=["Does sealing preserve fixity?"],
        )
        RP.cmd_new(ns)
        packages = RP.package_dirs(root)
        self.assertEqual(len(packages), 1)
        return packages[0].name

    def test_new_package_is_valid(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            package_id = self.new_package(root)
            self.assertTrue(package_id.startswith("NEXUS_RP_"))
            self.assertEqual(RP.validate(root), [])

    def test_add_item_activates_package(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); package_id = self.new_package(root)
            RP.cmd_add(Namespace(
                root=root, package=package_id, role="SOURCE_OBJECT", path_ref="research/example.md",
                repository="nexusomegac27/NEXUS-OMEGA-EVIDENCE", commit="a" * 40,
                git_blob="b" * 40, bytes=10, sha256="c" * 64, source_status="PRESENT",
                producer="AXIOM", relevance="test source", uncertainty=None,
            ))
            pkg = RP.find_package(root, package_id)
            manifest = RP.load_json(pkg / "manifest.json")
            self.assertEqual(manifest["state"], "ACTIVE")
            self.assertEqual(manifest["item_count"], 1)
            self.assertEqual(RP.validate(root), [])

    def test_sealed_snapshot_fixity_validates(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); package_id = self.new_package(root)
            RP.cmd_seal(Namespace(root=root, package=package_id, actor="AXIOM"))
            pkg = RP.find_package(root, package_id)
            snap = pkg / "snapshots" / "v1"
            self.assertTrue((snap / "SHA256SUMS.txt").is_file())
            self.assertEqual(RP.validate(root), [])

    def test_snapshot_mutation_is_detected(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); package_id = self.new_package(root)
            RP.cmd_seal(Namespace(root=root, package=package_id, actor="AXIOM"))
            pkg = RP.find_package(root, package_id)
            (pkg / "snapshots" / "v1" / "manifest.json").write_text("{}\n", encoding="utf-8")
            errors = RP.validate(root)
            self.assertTrue(any(e.startswith("SNAPSHOT_DIGEST_MISMATCH:") for e in errors))


if __name__ == "__main__":
    unittest.main()
