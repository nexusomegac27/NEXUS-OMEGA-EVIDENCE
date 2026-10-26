#!/usr/bin/env python3
"""Frozen black-box tests for strict JSON intake of the Issue #93 C1 receipt auditor.

The candidate is supplied by AXIOM_CANDIDATE; this evaluator neither imports
nor edits candidate internals. No GitHub actor or source authentication is claimed.
"""
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest

HERE = Path(__file__).resolve().parent
CANDIDATE = Path(os.environ.get('AXIOM_CANDIDATE', HERE / 'alpha_issue93_receipt_chain_json_strict_v2_20261027.py'))


def comment(cid, predecessor):
    return {'id': cid, 'actor_login': 'nexusomegac27',
            'body': ('OBJECT=NEXUS_TEST_%d\nCLAIM_CEILING=C1_DESCRIPTIVE_ONLY\n'
                     'PREDECESSOR_ISSUE93_RECEIPT=%d\nACTUAL_MAIN_READBACK=%s\n') %
                    (cid, predecessor, 'a' * 40)}


def sample():
    return {'repository': 'nexusomegac27/NEXUS-OMEGA-EVIDENCE',
            'issue_number': 93, 'anchor_predecessor_id': 100,
            'expected_tail_id': 102, 'comments': [comment(101, 100), comment(102, 101)]}


def run(raw):
    return subprocess.run([sys.executable, str(CANDIDATE)], input=raw,
                          capture_output=True, timeout=10)


class FrozenEnvelopeOracle(unittest.TestCase):
    def good(self, raw):
        proc = run(raw)
        self.assertEqual(proc.returncode, 0, proc.stderr.decode(errors='replace'))
        self.assertEqual(json.loads(proc.stdout)['state'], 'PASS_RECEIPT_CHAIN_STRUCTURE_C1')

    def bad(self, raw):
        proc = run(raw)
        self.assertEqual(proc.returncode, 2, proc.stdout.decode(errors='replace'))
        self.assertIn(b'FAIL_CLOSED:', proc.stderr)

    def test_01_clean_two_comments(self): self.good(json.dumps(sample()).encode())
    def test_02_clean_single_comment(self):
        p = sample(); p['comments'] = p['comments'][:1]; p['expected_tail_id'] = 101
        self.good(json.dumps(p).encode())
    def test_03_clean_pretty_json(self): self.good(json.dumps(sample(), indent=2).encode())
    def test_04_clean_utf8_whitespace(self): self.good((' \n' + json.dumps(sample()) + '\t').encode())
    def test_05_duplicate_repository(self):
        raw = json.dumps(sample()).replace('"repository":', '"repository":"untrusted/repo", "repository":', 1)
        self.bad(raw.encode())
    def test_06_duplicate_issue_number(self):
        raw = json.dumps(sample()).replace('"issue_number":', '"issue_number": 999, "issue_number":', 1)
        self.bad(raw.encode())
    def test_07_duplicate_expected_tail(self):
        raw = json.dumps(sample()).replace('"expected_tail_id":', '"expected_tail_id": 999, "expected_tail_id":', 1)
        self.bad(raw.encode())
    def test_08_duplicate_comment_id(self):
        raw = json.dumps(sample()).replace('"id": 101', '"id": 999, "id": 101', 1)
        self.bad(raw.encode())
    def test_09_duplicate_actor_login(self):
        raw = json.dumps(sample()).replace('"actor_login":', '"actor_login": "attacker", "actor_login":', 1)
        self.bad(raw.encode())
    def test_10_duplicate_body(self):
        raw = json.dumps(sample()).replace('"body":', '"body": "BAD", "body":', 1)
        self.bad(raw.encode())
    def test_11_duplicate_unused_nested_key(self):
        raw = json.dumps(sample()).replace('"id": 101', '"metadata":{"x":1,"x":2}, "id": 101', 1)
        self.bad(raw.encode())
    def test_12_broken_predecessor(self):
        p = sample(); p['comments'][1] = comment(102, 100)
        self.bad(json.dumps(p).encode())
    def test_13_malformed_json(self): self.bad(b'{"repository":')
    def test_14_oversized_input(self): self.bad(b' ' * 1048577)


if __name__ == '__main__': unittest.main()
