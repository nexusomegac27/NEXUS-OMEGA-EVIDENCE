"""Independent frozen evaluator: exact V2 baseline versus proposed exponent fail-closed V3.
Synthetic seven-PR fixture only; no GitHub authentication or runtime integration.
"""
import copy
import json
import runpy
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CHAIN = runpy.run_path(str(ROOT / 'alpha_publication_census_matrix_guard_v2_20261101.py'))['CHAIN']
BASELINE = ROOT / 'alpha_publication_ci_name_app_binding_guard_v2_20261101.py'
CANDIDATE = ROOT / 'alpha_publication_ci_nonfinite_exponent_guard_v3_20261101.py'
NAMES = [('nexus-preentry-lab', 'github-actions'),
         ('r27e-external-structural-firewall', 'github-actions'),
         ('validate', 'github-actions'), ('validate', 'github-actions'),
         ('validate', 'github-actions'), ('validate', 'github-actions'),
         ('validate-repository-structure', 'github-actions'),
         ('semgrep-cloud-platform/scan', 'semgrep-code-nexusomegac27')]


def fixture():
    rows = []
    for i, (pr, parent, main, receipt, file_count) in enumerate(CHAIN):
        head = f'{i + 201:040x}'
        rows.append({'pr': pr, 'parent': parent, 'main': main,
                     'receipt_id': receipt, 'additive': True, 'signature': True,
                     'files': [{'sha_match': True, 'blob_match': True, 'bytes_match': True}
                               for _ in range(file_count)],
                     'checks': ['success'] * 8, 'pr_head_sha': head,
                     'check_runs': [
                         {'id': i * 100 + j + 1, 'name': name, 'app_slug': app,
                          'head_sha': head, 'status': 'completed', 'conclusion': 'success'}
                         for j, (name, app) in enumerate(NAMES)]})
    return rows


def invoke(path, raw):
    result = subprocess.run([sys.executable, str(path)], input=raw,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            timeout=10, check=False)
    if result.returncode != 0:
        raise AssertionError(f'NONZERO_EXIT:{path.name}:{result.returncode}')
    return json.loads(result.stdout)['accepted']


def cases():
    positive = json.dumps(fixture(), separators=(',', ':')).encode('utf-8')
    assert positive.startswith(b'[{')
    yield 'positive_canonical', positive, True, True
    finite = positive.replace(b'[{', b'[{' + b'"probe":1e308,', 1)
    yield 'positive_finite_exponent', finite, True, True
    for label, token in [('positive_overflow', b'1e309'),
                         ('negative_overflow', b'-1e309'),
                         ('very_large_exponent', b'9e999'),
                         ('many_digit_exponent', b'1e999999'),
                         ('nested_overflow', b'3.14e9999')]:
        if label == 'nested_overflow':
            changed = positive.replace(b'[{', b'[{"probe":{"nested":' + token + b'},', 1)
        else:
            changed = positive.replace(b'[{', b'[{"probe":' + token + b',', 1)
        yield label, changed, True, False
    nan = positive.replace(b'[{', b'[{"probe":NaN,', 1)
    yield 'baseline_nan_rejected', nan, False, False
    dup = positive.replace(b'[{', b'[{"pr":"duplicate",', 1)
    yield 'baseline_duplicate_key_rejected', dup, False, False


def run():
    count = 0
    total = 0
    for label, raw, expect_v2, expect_v3 in cases():
        observed_v2 = invoke(BASELINE, raw)
        observed_v3 = invoke(CANDIDATE, raw)
        ok = (observed_v2, observed_v3) == (expect_v2, expect_v3)
        print(json.dumps({'fixture': label, 'baseline_v2': observed_v2,
                          'candidate_v3': observed_v3, 'expected_v2': expect_v2,
                          'expected_v3': expect_v3, 'pass': ok}, sort_keys=True))
        count += ok
        total += 1
    print(json.dumps({'total': total, 'pass': count, 'claim': 'SYNTHETIC_STRUCTURE_ONLY'},
                     sort_keys=True))
    return 0 if count == total else 1


if __name__ == '__main__':
    sys.exit(run())
