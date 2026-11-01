"""Frozen independent C1 subprocess oracle for the historical seven-PR check-run inventory.
Commit this evaluator before publishing any candidate. Synthetic fixtures only.
"""
import copy
import json
import runpy
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CHAIN = runpy.run_path(str(ROOT / 'alpha_publication_census_matrix_guard_v2_20261101.py'))['CHAIN']
V1 = ROOT / 'alpha_publication_ci_run_identity_guard_v1_20261101.py'
V2 = ROOT / 'alpha_publication_ci_name_app_binding_guard_v2_20261101.py'
NAMES = [('nexus-preentry-lab', 'github-actions'),
         ('r27e-external-structural-firewall', 'github-actions'),
         ('validate', 'github-actions'), ('validate', 'github-actions'),
         ('validate', 'github-actions'), ('validate', 'github-actions'),
         ('validate-repository-structure', 'github-actions'),
         ('semgrep-cloud-platform/scan', 'semgrep-code-nexusomegac27')]


def fixture():
    records = []
    for i, (pr, parent, main, receipt, file_count) in enumerate(CHAIN):
        head = f'{i + 101:040x}'
        records.append({
            'pr': pr, 'parent': parent, 'main': main, 'receipt_id': receipt,
            'files': [{'sha_match': True, 'blob_match': True, 'bytes_match': True}
                      for _ in range(file_count)],
            'checks': ['success'] * 8, 'additive': True, 'signature': True,
            'pr_head_sha': head,
            'check_runs': [
                {'id': i * 100 + j + 1, 'name': name, 'app_slug': app,
                 'head_sha': head, 'status': 'completed', 'conclusion': 'success'}
                for j, (name, app) in enumerate(NAMES)]})
    return records


def invoke(path, records):
    proc = subprocess.run([sys.executable, str(path)],
                          input=json.dumps(records, ensure_ascii=False).encode('utf-8'),
                          capture_output=True, timeout=10)
    if proc.returncode != 0:
        raise AssertionError(f'NONZERO_EXIT:{path.name}:{proc.returncode}')
    return json.loads(proc.stdout)['accepted']


def run():
    base = fixture()
    cases = [('positive_exact_inventory', base, True, True)]
    shuffled = copy.deepcopy(base)
    for row in shuffled:
        row['check_runs'].reverse()
    cases.append(('positive_order_invariant', shuffled, True, True))
    mutations = [
        ('missing_semgrep_replaced_by_other', 0, 7, 'name', 'other-successful-check'),
        ('semgrep_wrong_app', 1, 7, 'app_slug', 'github-actions'),
        ('missing_preentry', 2, 0, 'name', 'other-preentry'),
        ('missing_firewall', 3, 1, 'name', 'other-firewall'),
        ('missing_structure', 4, 6, 'name', 'other-structure'),
        ('validate_count_reduced', 5, 2, 'name', 'other-validate'),
        ('semgrep_name_case_changed', 6, 7, 'name', 'Semgrep-cloud-platform/scan'),
        ('validate_wrong_app', 0, 3, 'app_slug', 'untrusted-app'),
        ('semgrep_replaced_by_validate', 1, 7, 'name', 'validate'),
        ('preentry_wrong_app', 2, 0, 'app_slug', 'untrusted-app'),
    ]
    for label, row, run, key, value in mutations:
        changed = copy.deepcopy(base)
        changed[row]['check_runs'][run][key] = value
        cases.append((label, changed, True, False))
    passed = 0
    for label, records, expect_v1, expect_v2 in cases:
        observed_v1, observed_v2 = invoke(V1, records), invoke(V2, records)
        ok = (observed_v1, observed_v2) == (expect_v1, expect_v2)
        print(json.dumps({'fixture': label, 'v1': observed_v1, 'v2': observed_v2,
                          'expected_v1': expect_v1, 'expected_v2': expect_v2,
                          'pass': ok}))
        passed += ok
    print(json.dumps({'total': len(cases), 'pass': passed,
                      'negative': len(mutations), 'claim': 'SYNTHETIC_STRUCTURE_ONLY'}))
    return 0 if passed == len(cases) else 1


if __name__ == '__main__':
    sys.exit(run())
