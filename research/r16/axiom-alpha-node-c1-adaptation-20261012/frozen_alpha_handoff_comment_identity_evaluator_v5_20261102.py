"""Frozen C1 negative oracle for GitHub comment-ID receipt aliasing.

Commit this evaluator before the candidate. It uses only synthetic supplied
cohorts; neither GitHub actor identity nor actual unattended work is attested.
"""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import sys
import tempfile

BASE = 'https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE'


def load(path):
    spec = importlib.util.spec_from_file_location('alpha_tested_module', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def event(name, n, **kw):
    e = dict(id=name, public='YES', routine='YES', authorized='YES',
             accessible='YES', unattended='YES', operator_nudge='NO_VERIFIED',
             source_commit='a'*40, source_sha256='b'*64,
             readback_sha256='b'*64, source_bytes=123,
             source_path='research/r16/example.txt',
             trigger_receipt=f'{BASE}/issues/93#issuecomment-{100+n}',
             handoff_receipt=f'{BASE}/issues/93#issuecomment-{200+n}',
             independent_evaluator_receipt=f'{BASE}/issues/93#issuecomment-{300+n}')
    e.update(kw)
    return e


def population(names):
    ids = sorted(names)
    digest = hashlib.sha256(json.dumps(ids, ensure_ascii=True,
                        separators=(',', ':')).encode()).hexdigest()
    return dict(scope='SYNTHETIC', enumeration_complete=True,
                enumeration_commit='a'*40, enumeration_sha256='b'*64,
                enumerated_event_ids=ids, enumerated_event_count=len(ids),
                enumerated_event_ids_sha256=digest)


def check(label, module, events, pop, status, num, den, reason=None):
    try:
        got = module.assess(copy.deepcopy(events), copy.deepcopy(pop))
        ok = (got.get('status') == status and got.get('numerator') == num
              and got.get('denominator') == den
              and got.get('project_rate') == 'NOT_COMPUTABLE'
              and got.get('evidence_class') == 'SUPPLIED_FIELDS_NOT_INDEPENDENTLY_AUTHENTICATED'
              and (reason is None or got.get('receipt_status') == reason))
        return dict(case=label, passed=ok, status=got.get('status'),
                    numerator=got.get('numerator'), denominator=got.get('denominator'),
                    reason=got.get('receipt_status'))
    except Exception as exc:
        return dict(case=label, passed=False, exception=type(exc).__name__)


def run(v4path, v5path):
    v4, v5 = load(v4path), load(v5path)
    a, b = event('a', 1), event('b', 2)
    p2, p1 = population(['a', 'b']), population(['a'])
    alias = event('b', 2, handoff_receipt=f'{BASE}/pull/115#issuecomment-201')
    zeros = event('b', 2, handoff_receipt=f'{BASE}/issues/94#issuecomment-000201')
    role_alias = event('a', 1, handoff_receipt=f'{BASE}/pull/115#issuecomment-101')
    root_a = event('a', 1, handoff_receipt=f'{BASE}/pull/100')
    root_b = event('b', 2, handoff_receipt=f'{BASE}/pull/101')
    neg_cross = 'CANONICAL_HANDOFF_COMMENT_ID_REUSED'
    neg_role = 'CANONICAL_RECEIPT_ROLE_ID_COLLISION'
    positive = 'DISTINCT_CANONICAL_HANDOFF_IDENTITIES_DECLARED_ONLY'
    tests = [
        ('v4_alias_baseline', v4, [a, alias], p2, 'COHORT_DECLARED_ONLY', 2, 2, None),
        ('v5_alias_cross_event', v5, [a, alias], p2, 'NOT_COMPUTABLE', None, None, neg_cross),
        ('v5_leading_zero_cross_event', v5, [a, zeros], p2, 'NOT_COMPUTABLE', None, None, neg_cross),
        ('v4_role_alias_baseline', v4, [role_alias], p1, 'COHORT_DECLARED_ONLY', 1, 1, None),
        ('v5_role_alias', v5, [role_alias], p1, 'NOT_COMPUTABLE', None, None, neg_role),
        ('v5_distinct_positive', v5, [a, b], p2, 'COHORT_DECLARED_ONLY', 2, 2, positive),
        ('v5_distinct_root_urls', v5, [root_a, root_b], p2, 'COHORT_DECLARED_ONLY', 2, 2, positive),
        ('v5_shared_trigger_across_events', v5, [a, event('b', 2, trigger_receipt=a['trigger_receipt'])], p2, 'COHORT_DECLARED_ONLY', 2, 2, positive),
        ('v5_shared_evaluator_across_events', v5, [a, event('b', 2, independent_evaluator_receipt=a['independent_evaluator_receipt'])], p2, 'COHORT_DECLARED_ONLY', 2, 2, positive),
        ('v5_private_alias_excluded', v5, [a, event('b', 2, public='NO', handoff_receipt=alias['handoff_receipt'])], p2, 'COHORT_DECLARED_ONLY', 1, 1, positive),
        ('v5_missing_evaluator_not_success', v5, [a, event('b', 2, independent_evaluator_receipt='MISSING')], p2, 'COHORT_DECLARED_ONLY', 1, 2, positive),
        ('v5_missing_population', v5, [a], p2, 'NOT_COMPUTABLE', None, None, 'NOT_ASSESSED_V4_GATE'),
        ('v5_unknown_eligibility', v5, [event('a', 1, accessible='UNKNOWN')], p1, 'NOT_COMPUTABLE', None, None, 'NOT_ASSESSED_V4_GATE'),
        ('v5_malformed', v5, ['bad'], p1, 'INVALID_INPUT', None, None, 'NOT_ASSESSED_V4_GATE'),
        ('v5_same_exact_url_v4_gate', v5, [a, event('b', 2, handoff_receipt=a['handoff_receipt'])], p2, 'NOT_COMPUTABLE', None, None, 'NOT_ASSESSED_V4_GATE'),
    ]
    rows = [check(*t) for t in tests]
    with tempfile.TemporaryDirectory() as temp:
        for path in Path(v4path).parent.glob('alpha_handoff*20261102.py'):
            shutil.copyfile(path, Path(temp)/path.name)
        path = Path(temp)/Path(v4path).name
        path.write_bytes(path.read_bytes()+b'\n# changed\n')
        rows.append(check('v5_mutated_pinned_v4_denied', load(Path(temp)/Path(v5path).name),
                          [a,b], p2, 'HOLD_SCOPED', None, None, 'V4_ORIGINAL_BYTES_MISMATCH_OR_MISSING'))
    return rows


if __name__ == '__main__':
    rows = run(sys.argv[1], sys.argv[2])
    passed = sum(x['passed'] for x in rows)
    print(json.dumps(dict(passed=passed, total=len(rows), results=rows), sort_keys=True))
    sys.exit(0 if passed == len(rows) else 1)
