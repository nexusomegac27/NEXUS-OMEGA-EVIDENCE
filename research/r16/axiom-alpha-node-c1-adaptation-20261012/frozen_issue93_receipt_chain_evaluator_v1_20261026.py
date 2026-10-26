#!/usr/bin/env python3
"""Frozen black-box C1 oracle for a caller-supplied Issue #93 receipt chain.

Fixture ids are illustrative; this suite does not authenticate GitHub responses.
This oracle is committed before the candidate and must not be modified to pass it.
"""
import importlib.util
import os
from pathlib import Path
import unittest

HERE = Path(__file__).resolve().parent
CANDIDATE = Path(os.environ.get('AXIOM_CANDIDATE', HERE / 'alpha_issue93_receipt_chain_audit_v1_20261026.py'))

def load():
    spec = importlib.util.spec_from_file_location('candidate_receipt_audit', CANDIDATE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def comment(cid, predecessor, main='a' * 40, ceiling='C1_DESCRIPTIVE_ONLY'):
    return {'id': cid, 'actor_login': 'nexusomegac27',
            'body': 'OBJECT=NEXUS_TEST_%d\nCLAIM_CEILING=%s\nPREDECESSOR_ISSUE93_RECEIPT=%s\nACTUAL_MAIN_READBACK=%s\n' %
                    (cid, ceiling, predecessor, main)}

def sample():
    return {'repository': 'nexusomegac27/NEXUS-OMEGA-EVIDENCE', 'issue_number': 93,
            'anchor_predecessor_id': 100, 'expected_tail_id': 103,
            'comments': [comment(101, 100), comment(102, 101), comment(103, 102)]}

class FrozenReceiptOracle(unittest.TestCase):
    def good(self, payload):
        result = load().audit(payload)
        self.assertEqual(result['state'], 'PASS_RECEIPT_CHAIN_STRUCTURE_C1')
        self.assertEqual(result['checked_edges'], len(payload['comments']))
        self.assertEqual(result['source_authentication'], 'NOT_ESTABLISHED_BY_CALLER_SNAPSHOT')
        self.assertEqual(result['github_main_readback'], 'NOT_ESTABLISHED_BY_THIS_TOOL')
        self.assertEqual(result['project_automation_rate'], 'NOT_COMPUTABLE')

    def bad(self, payload):
        with self.assertRaises((ValueError, TypeError)):
            load().audit(payload)

    def test_01_clean_three_receipts(self): self.good(sample())
    def test_02_one_receipt_with_external_anchor(self):
        p = sample(); p['comments'] = p['comments'][:1]; p['expected_tail_id'] = 101; self.good(p)
    def test_03_broken_middle_predecessor(self):
        p = sample(); p['comments'][1] = comment(102, 100); self.bad(p)
    def test_04_broken_first_anchor(self):
        p = sample(); p['comments'][0] = comment(101, 99); self.bad(p)
    def test_05_duplicate_comment_id(self):
        p = sample(); p['comments'][1]['id'] = 101; self.bad(p)
    def test_06_nonmonotonic_comment_order(self):
        p = sample(); p['comments'].reverse(); self.bad(p)
    def test_07_missing_predecessor_field(self):
        p = sample(); p['comments'][1]['body'] = p['comments'][1]['body'].replace('PREDECESSOR_ISSUE93_RECEIPT=101\n', ''); self.bad(p)
    def test_08_duplicate_predecessor_field(self):
        p = sample(); p['comments'][1]['body'] += 'PREDECESSOR_ISSUE93_RECEIPT=101\n'; self.bad(p)
    def test_09_missing_tail(self):
        p = sample(); p['expected_tail_id'] = 104; self.bad(p)
    def test_10_claim_promotion(self):
        p = sample(); p['comments'][2] = comment(103, 102, ceiling='C2'); self.bad(p)
    def test_11_malformed_main_sha(self):
        p = sample(); p['comments'][2] = comment(103, 102, main='abcd'); self.bad(p)
    def test_12_wrong_repository(self):
        p = sample(); p['repository'] = 'untrusted/other'; self.bad(p)
    def test_13_duplicate_main_readback(self):
        p = sample(); p['comments'][1]['body'] += 'ACTUAL_MAIN_READBACK=' + 'b'*40 + '\n'; self.bad(p)
    def test_14_invalid_actor_metadata(self):
        p = sample(); p['comments'][0]['actor_login'] = ''; self.bad(p)
    def test_15_unbounded_body(self):
        p = sample(); p['comments'][0]['body'] += 'X'*33000; self.bad(p)
    def test_16_not_json_like(self): self.bad('not-a-snapshot')

if __name__ == '__main__': unittest.main()
