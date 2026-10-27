#!/usr/bin/env python3
"""Independent black-box evaluator for R27E required 'validate' GitHub App source binding.
Synthetic snapshots only. Frozen before isolated candidate edit. No live GitHub authority.
"""
import copy
import json
from pathlib import Path
import subprocess
import sys
import unittest

HERE = Path(__file__).resolve().parent
CANDIDATE = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / 'alpha_r27e_ruleset_enforcement_audit_v1_20261027.py'
sys.argv = [sys.argv[0]]

def baseline():
    return {
        'ruleset': {'id': 21252293, 'target': 'branch',
            'source': 'nexusomegac27/NEXUS-OMEGA-EVIDENCE', 'enforcement': 'active',
            'conditions': {'ref_name': {'include': ['refs/heads/main'], 'exclude': []}},
            'bypass_actors': [],
            'rules': [
                {'type': 'required_status_checks', 'parameters': {
                    'strict_required_status_checks_policy': True,
                    'required_status_checks': [
                        {'context': 'validate', 'integration_id': 15368},
                        {'context': 'r27e-external-structural-firewall'},
                        {'context': 'nexus-preentry-lab'}]}},
                {'type': 'pull_request', 'parameters': {
                    'required_approving_review_count': 1,
                    'require_code_owner_review': True}}]},
        'registry': {'object': 'NEXUS_OMEGA_EXTERNAL_AGENT_WRITE_SLOTS_V1',
            'anchor_repo': 'nexusomegac27/NEXUS-OMEGA-EVIDENCE',
            'claim_ceiling': 'C1_DESCRIPTIVE_ONLY', 'default': 'DENY',
            'external_actor_allowlist': []}}

def run(x):
    p = subprocess.run([sys.executable, str(CANDIDATE)], input=json.dumps(x).encode(),
                       capture_output=True, timeout=10)
    if p.returncode != 0:
        return 'ERROR'
    return json.loads(p.stdout)['state']

class TestSourceBinding(unittest.TestCase):
    def test_01_positive_pinned_source(self):
        self.assertEqual(run(baseline()), 'PASS_REQUIRED_CONFIG_WITNESSES_C1')
    def test_02_positive_reordered_contexts(self):
        x = baseline(); x['ruleset']['rules'][0]['parameters']['required_status_checks'].reverse()
        self.assertEqual(run(x), 'PASS_REQUIRED_CONFIG_WITNESSES_C1')
    def test_03_wrong_integration_id(self):
        x = baseline(); x['ruleset']['rules'][0]['parameters']['required_status_checks'][0]['integration_id'] = 99999
        self.assertEqual(run(x), 'HOLD_SCOPED_ENFORCEMENT_GAP')
    def test_04_missing_integration_id(self):
        x = baseline(); del x['ruleset']['rules'][0]['parameters']['required_status_checks'][0]['integration_id']
        self.assertEqual(run(x), 'HOLD_SCOPED_ENFORCEMENT_GAP')
    def test_05_boolean_integration_id(self):
        x = baseline(); x['ruleset']['rules'][0]['parameters']['required_status_checks'][0]['integration_id'] = True
        self.assertEqual(run(x), 'HOLD_SCOPED_ENFORCEMENT_GAP')
    def test_06_other_required_check_missing(self):
        x = baseline(); x['ruleset']['rules'][0]['parameters']['required_status_checks'].pop()
        self.assertEqual(run(x), 'HOLD_SCOPED_ENFORCEMENT_GAP')

if __name__ == '__main__': unittest.main(verbosity=2)
