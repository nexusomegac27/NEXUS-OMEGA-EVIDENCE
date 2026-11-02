"""Frozen, independent C1 evaluator: V2 receipt-role collision versus V3.

Synthetic fixtures only. Commit this evaluator before committing the V3 candidate.
Do not modify it after its first commit. A distinct URL is not actor authentication.
"""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import sys
import tempfile

REPO = 'https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/issues/93#issuecomment-'
H40 = 'a' * 40
H64 = 'b' * 64


def load(path):
    spec = importlib.util.spec_from_file_location('isolated_under_test', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def event(ident, **kw):
    e = {'id': ident, 'public': 'YES', 'routine': 'YES',
         'authorized': 'YES', 'accessible': 'YES', 'unattended': 'YES',
         'operator_nudge': 'NO_VERIFIED', 'source_commit': H40,
         'source_sha256': H64, 'readback_sha256': H64,
         'source_path': 'research/r16/sample.txt', 'source_bytes': 100,
         'trigger_receipt': REPO + '101',
         'handoff_receipt': REPO + '102',
         'independent_evaluator_receipt': REPO + '103'}
    e.update(kw)
    return e


def population(ids):
    ids = sorted(ids)
    digest = hashlib.sha256(json.dumps(ids, ensure_ascii=True,
                                     separators=(',', ':')).encode()).hexdigest()
    return {'scope': 'SYNTHETIC_BOUNDED', 'enumeration_complete': True,
            'enumeration_commit': H40, 'enumeration_sha256': H64,
            'enumerated_event_ids': ids, 'enumerated_event_count': len(ids),
            'enumerated_event_ids_sha256': digest}


def check(name, mod, events, pop, status, numerator, denominator, receipt=None):
    try:
        got = mod.assess(copy.deepcopy(events), copy.deepcopy(pop))
        ok = (got.get('status') == status and got.get('numerator') == numerator
              and got.get('denominator') == denominator
              and got.get('project_rate') == 'NOT_COMPUTABLE'
              and got.get('evidence_class') == 'SUPPLIED_FIELDS_NOT_INDEPENDENTLY_AUTHENTICATED'
              and (receipt is None or got.get('receipt_status') == receipt))
        return {'case': name, 'pass': ok, 'status': got.get('status'),
                'numerator': got.get('numerator'), 'denominator': got.get('denominator'),
                'receipt_status': got.get('receipt_status')}
    except Exception as ex:
        return {'case': name, 'pass': False, 'exception': type(ex).__name__}


def run(v2_path, v3_path):
    v2, v3 = load(v2_path), load(v3_path)
    a = event('a')
    all_same = event('a', handoff_receipt=REPO+'101',
                     independent_evaluator_receipt=REPO+'101')
    p1 = population(['a'])
    p2 = population(['a', 'b'])
    collided = 'RECEIPT_ROLE_URL_COLLISION'
    distinct = 'DISTINCT_DECLARED_URLS_NOT_AUTHENTICATED'
    cases = [
        ('v2_accepts_same_url_three_roles', v2, [all_same], p1, 'COHORT_DECLARED_ONLY', 1, 1, None),
        ('v3_rejects_same_url_three_roles', v3, [all_same], p1, 'NOT_COMPUTABLE', None, None, collided),
        ('v3_rejects_trigger_handoff_collision', v3, [event('a',handoff_receipt=REPO+'101')], p1, 'NOT_COMPUTABLE', None, None, collided),
        ('v3_rejects_handoff_evaluator_collision', v3, [event('a',independent_evaluator_receipt=REPO+'102')], p1, 'NOT_COMPUTABLE', None, None, collided),
        ('v3_rejects_trigger_evaluator_collision', v3, [event('a',independent_evaluator_receipt=REPO+'101')], p1, 'NOT_COMPUTABLE', None, None, collided),
        ('v3_accepts_distinct_declared_only', v3, [a], p1, 'COHORT_DECLARED_ONLY', 1, 1, distinct),
        ('v3_falsifier_three_owner_urls_not_authentication', v3, [a], p1, 'COHORT_DECLARED_ONLY', 1, 1, distinct),
        ('v3_one_colliding_event_holds_cohort', v3, [a,event('b',handoff_receipt=REPO+'101')], p2, 'NOT_COMPUTABLE', None, None, collided),
        ('v3_private_colliding_event_not_counted', v3, [a,event('b',public='NO',handoff_receipt=REPO+'101')], p2, 'COHORT_DECLARED_ONLY', 1, 1, distinct),
        ('v3_unknown_eligibility_preserved', v3, [event('a',accessible='UNKNOWN')], p1, 'NOT_COMPUTABLE', None, None, 'NOT_ASSESSED_V2_GATE'),
        ('v3_missing_evaluator_not_success', v3, [event('a',independent_evaluator_receipt='MISSING')], p1, 'COHORT_DECLARED_ONLY', 0, 1, distinct),
        ('v3_omitted_population_event_preserved', v3, [a], p2, 'NOT_COMPUTABLE', None, None, 'NOT_ASSESSED_V2_GATE'),
        ('v3_malformed_input_preserved', v3, ['bad'], p1, 'INVALID_INPUT', None, None, 'NOT_ASSESSED_V2_GATE'),
    ]
    rows = [check(*c) for c in cases]
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        for p in [Path(v2_path).with_name('alpha_handoff_denominator_guard_v1_20261102.py'),
                  Path(v2_path), Path(v3_path)]:
            shutil.copyfile(p, root/p.name)
        (root/Path(v2_path).name).write_bytes((root/Path(v2_path).name).read_bytes()+b'\n# mutation\n')
        rows.append(check('v3_pinned_v2_mutation', load(root/Path(v3_path).name), [a], p1,
                          'HOLD_SCOPED', None, None, 'V2_ORIGINAL_BYTES_MISMATCH_OR_MISSING'))
    return rows


if __name__ == '__main__':
    rows = run(sys.argv[1], sys.argv[2])
    n = sum(x['pass'] for x in rows)
    print(json.dumps({'passed': n, 'total': len(rows), 'results': rows}, sort_keys=True))
    sys.exit(0 if n == len(rows) else 1)
