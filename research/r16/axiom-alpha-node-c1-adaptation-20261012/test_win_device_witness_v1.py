#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Frozen, independent black-box evaluator for a research-only path witness."""
import importlib.util
import pathlib
import re
import sys
import unittest

# Source-exact predicate transcribed from scripts/nexus_repository_steward.py
# at bfd1a3f35ec6d565519f9a2de256e9d6d4ca5e8e; this is not
# a full black-box invocation of the productive steward.
BASELINE_RESERVED = re.compile(r"^(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(?:\..*)?$", re.I)


def load_candidate():
    path = pathlib.Path(__file__).with_name("win_device_name_witness_v1.py")
    spec = importlib.util.spec_from_file_location("candidate", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class FrozenDeviceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.candidate = load_candidate()

    def test_microsoft_superscript_devices(self):
        for prefix in ("COM", "LPT"):
            for digit in ("¹", "²", "³"):
                for suffix in ("", ".txt"):
                    with self.subTest(prefix=prefix, digit=digit, suffix=suffix):
                        name = prefix + digit + suffix
                        self.assertFalse(bool(BASELINE_RESERVED.fullmatch(name)))
                        self.assertTrue(self.candidate.reserved_device_component(name))

    def test_classic_device_controls(self):
        for name in ("CON", "NUL.txt", "COM1", "LPT9.log", "prn.TXT"):
            with self.subTest(name=name):
                self.assertTrue(self.candidate.reserved_device_component(name))

    def test_negative_controls_nondevices(self):
        for name in ("COM0", "COM10", "LPT0", "COM⁴", "COM₁", "myCOM¹", "COM¹notes", "report.txt"):
            with self.subTest(name=name):
                self.assertFalse(self.candidate.reserved_device_component(name))

    def test_nested_paths(self):
        self.assertEqual(self.candidate.flagged_components("research/COM¹/readme.md"), ["COM¹"])
        self.assertEqual(self.candidate.flagged_components("research/ok/LPT².txt"), ["LPT².txt"])
        self.assertEqual(self.candidate.flagged_components("research/ok/report.txt"), [])

    def test_fail_closed_bad_input(self):
        for value in ("", "/absolute", "a//b", "a/../b", "a/./b"):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    self.candidate.flagged_components(value)
        with self.assertRaises(TypeError):
            self.candidate.flagged_components(None)


if __name__ == "__main__":
    unittest.main(verbosity=2)
