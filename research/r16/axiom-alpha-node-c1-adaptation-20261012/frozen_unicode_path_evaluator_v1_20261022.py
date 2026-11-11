#!/usr/bin/env python3
"""Frozen held-out evaluator: invisible path controls and canonical Unicode aliases.

Independent requirement: a C1 PR scope checker must fail closed on Unicode
Cc/Cf/Cs path characters and normalization-equivalent duplicate filenames;
ordinary printable Unicode names remain acceptable. Synthetic fixtures only.
This is a research policy, not a statement of GitHub filename validity.
"""
import copy
import importlib.util
import json
import sys

LANE = 'research/r16/axiom-alpha-node-c1-adaptation-20261012/'
BASE = 'd355400dabed3c280e1fce5030cab69ea099428b'
HEAD = '5fb35be25870e3a8785f0b41a82bcba652b43088'
BODY = (f'Research-only C1 candidate from pinned main {BASE} to pinned head {HEAD}. '
        f'GitHub compare: 2 commits ahead; two added Markdown files only under '
        f'the existing {LANE} lane.')

# Cases fixed before candidate changes; expectation is independent of code.
CASES = [
 ('positive_ascii', ['alpha.md', 'beta.md'], True),
 ('positive_nfc_accent', ['café.md', 'beta.md'], True),
 ('positive_cjk', ['研究.md', 'beta.md'], True),
 ('positive_emoji', ['test🧪.md', 'beta.md'], True),
 ('positive_single_nfd', ['cafe\u0301.md', 'beta.md'], True),
 ('negative_del_control', ['a\u007fb.md', 'beta.md'], False),
 ('negative_c1_control', ['a\u0085b.md', 'beta.md'], False),
 ('negative_bidi_override', ['a\u202eb.md', 'beta.md'], False),
 ('negative_zero_width_space', ['a\u200bb.md', 'beta.md'], False),
 ('negative_bom', ['a\ufeffb.md', 'beta.md'], False),
 ('negative_surrogate', ['a\ud800b.md', 'beta.md'], False),
 ('negative_nfc_equivalent_1', ['café.md', 'cafe\u0301.md'], False),
 ('negative_nfc_equivalent_2', ['Å.md', 'A\u030a.md'], False),
]

def evaluate(path):
    spec = importlib.util.spec_from_file_location('candidate_under_test', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rows = []
    for name, relative_paths, positive in CASES:
        snapshot = {'body': BODY, 'base_sha': BASE, 'head_sha': HEAD,
                    'commits': 2, 'changed_files': 2,
                    'filenames': [LANE + p for p in relative_paths]}
        try:
            result = module.check_scope(copy.deepcopy(snapshot))
            status = result.get('status') if isinstance(result, dict) else 'INVALID_RESULT'
        except Exception as exc:
            status = 'EXCEPTION_' + type(exc).__name__
        passed = (status == 'MATCH') if positive else status in ('DRIFT', 'INCOMPLETE')
        rows.append({'case': name, 'positive': positive, 'status': status, 'passed': passed})
    return {'total': len(rows), 'passed': sum(x['passed'] for x in rows),
            'positive_total': sum(x['positive'] for x in rows),
            'positive_passed': sum(x['positive'] and x['passed'] for x in rows),
            'negative_total': sum(not x['positive'] for x in rows),
            'negative_detected': sum(not x['positive'] and x['passed'] for x in rows),
            'oracle': 'FROZEN_INDEPENDENT_UNICODE_PATH_POLICY', 'rows': rows}

if __name__ == '__main__':
    output = evaluate(sys.argv[1]); print(json.dumps(output, indent=2, ensure_ascii=True))
    sys.exit(0 if output['passed'] == output['total'] else 1)
