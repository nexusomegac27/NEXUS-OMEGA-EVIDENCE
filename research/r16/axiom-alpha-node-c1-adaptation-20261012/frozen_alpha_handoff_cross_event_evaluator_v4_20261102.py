"""Frozen independent C1 offline evaluator. Must be committed before V4 candidate.

Tests only caller-declared synthetic cohorts, never real unattended Handoffs.
"""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import sys
import tempfile

URL = 'https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/issues/93#issuecomment-'


def load(path):
    spec = importlib.util.spec_from_file_location('alpha_under_test', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def event(name, n, **changes):
    e = {'id': name, 'public': 'YES', 'routine': 'YES', 'authorized': 'YES',
         'accessible': 'YES', 'unattended': 'YES', 'operator_nudge': 'NO_VERIFIED',
         'source_commit': 'a'*40, 'source_sha256': 'b'*64,
         'readback_sha256': 'b'*64, 'source_bytes': 100,
         'source_path': 'research/r16/sample.txt',
         'trigger_receipt': URL+'100', 'handoff_receipt': URL+str(200+n),
         'independent_evaluator_receipt': URL+str(300+n)}
    e.update(changes)
    return e


def population(names):
    ids = sorted(names)
    digest = hashlib.sha256(json.dumps(ids, ensure_ascii=True,
                         separators=(',', ':')).encode()).hexdigest()
    return {'scope': 'SYNTHETIC', 'enumeration_complete': True,
            'enumeration_commit': 'a'*40, 'enumeration_sha256': 'b'*64,
            'enumerated_event_ids': ids, 'enumerated_event_count': len(ids),
            'enumerated_event_ids_sha256': digest}


def check(label, module, events, pop, status, num, den, receipt=None):
    try:
        got = module.assess(copy.deepcopy(events), copy.deepcopy(pop))
        ok = (got.get('status') == status and got.get('numerator') == num
              and got.get('denominator') == den
              and got.get('project_rate') == 'NOT_COMPUTABLE'
              and got.get('evidence_class') == 'SUPPLIED_FIELDS_NOT_INDEPENDENTLY_AUTHENTICATED'
              and (receipt is None or got.get('receipt_status') == receipt))
        return {'case': label, 'pass': ok, 'status': got.get('status'),
                'numerator': got.get('numerator'), 'denominator': got.get('denominator'),
                'receipt_status': got.get('receipt_status')}
    except Exception as exc:
        return {'case': label, 'pass': False, 'exception': type(exc).__name__}


def run(v3path, v4path):
    v3, v4 = load(v3path), load(v4path)
    a, b, c = event('a', 1), event('b', 2), event('c', 3)
    shared = event('b', 2, handoff_receipt=a['handoff_receipt'])
    p2, p3 = population(['a', 'b']), population(['a', 'b', 'c'])
    duplicate = 'CROSS_EVENT_HANDOFF_RECEIPT_REUSED'
    distinct = 'DISTINCT_ELIGIBLE_HANDOFF_URLS_DECLARED_ONLY'
    tests = [
        ('v3_baseline_false_count', v3, [a, shared], p2, 'COHORT_DECLARED_ONLY', 2, 2, None),
        ('v4_duplicate_handoff_denied', v4, [a, shared], p2, 'NOT_COMPUTABLE', None, None, duplicate),
        ('v4_duplicate_handoff_three', v4, [a, shared, c], p3, 'NOT_COMPUTABLE', None, None, duplicate),
        ('v4_distinct_positive', v4, [a, b], p2, 'COHORT_DECLARED_ONLY', 2, 2, distinct),
        ('v4_shared_trigger_allowed', v4, [a, b], p2, 'COHORT_DECLARED_ONLY', 2, 2, distinct),
        ('v4_shared_evaluator_falsifier', v4, [a, event('b', 2, independent_evaluator_receipt=a['independent_evaluator_receipt'])], p2, 'COHORT_DECLARED_ONLY', 2, 2, distinct),
        ('v4_private_duplicate_ignored', v4, [a, event('b', 2, public='NO', handoff_receipt=a['handoff_receipt'])], p2, 'COHORT_DECLARED_ONLY', 1, 1, distinct),
        ('v4_unattended_no_duplicate_ignored', v4, [a, event('b', 2, unattended='NO', handoff_receipt=a['handoff_receipt'])], p2, 'COHORT_DECLARED_ONLY', 1, 2, distinct),
        ('v4_missing_evaluator_not_success', v4, [a, event('b', 2, independent_evaluator_receipt='MISSING')], p2, 'COHORT_DECLARED_ONLY', 1, 2, distinct),
        ('v4_omitted_population', v4, [a], p2, 'NOT_COMPUTABLE', None, None, 'NOT_ASSESSED_V3_GATE'),
        ('v4_unknown_eligibility', v4, [event('a', 1, accessible='UNKNOWN')], population(['a']), 'NOT_COMPUTABLE', None, None, 'NOT_ASSESSED_V3_GATE'),
        ('v4_intra_event_collision', v4, [event('a', 1, handoff_receipt=URL+'100')], population(['a']), 'NOT_COMPUTABLE', None, None, 'NOT_ASSESSED_V3_GATE'),
        ('v4_malformed', v4, ['bad'], population(['a']), 'INVALID_INPUT', None, None, 'NOT_ASSESSED_V3_GATE'),
    ]
    rows = [check(*t) for t in tests]
    with tempfile.TemporaryDirectory() as tmp:
        for p in [Path(v3path).with_name('alpha_handoff_denominator_guard_v1_20261102.py'),
                  Path(v3path).with_name('alpha_handoff_population_coverage_guard_v2_20261102.py'),
                  Path(v3path), Path(v4path)]:
            shutil.copyfile(p, Path(tmp)/p.name)
        path = Path(tmp)/Path(v3path).name
        path.write_bytes(path.read_bytes()+b'\n# mutation\n')
        rows.append(check('v4_mutated_pinned_v3_denied', load(Path(tmp)/Path(v4path).name),
                          [a,b], p2, 'HOLD_SCOPED', None, None, 'V3_ORIGINAL_BYTES_MISMATCH_OR_MISSING'))
    return rows


if __name__ == '__main__':
    rows = run(sys.argv[1], sys.argv[2])
    passed = sum(row['pass'] for row in rows)
    print(json.dumps({'passed': passed, 'total': len(rows), 'results': rows}, sort_keys=True))
    sys.exit(0 if passed == len(rows) else 1)
