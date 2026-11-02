"""Frozen external evaluator: V1 omitted-event baseline versus V2 coverage.

This is synthetic research-only testing. Do not edit after first commit.
"""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import sys
import tempfile

HEAD = 'a' * 40
HASH = 'b' * 64
URL = 'https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/issues/93#issuecomment-123'


def load(path):
    spec = importlib.util.spec_from_file_location('module_under_test', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def event(ident, **changes):
    out = {'id': ident, 'public': 'YES', 'routine': 'YES',
           'authorized': 'YES', 'accessible': 'YES', 'unattended': 'YES',
           'operator_nudge': 'NO_VERIFIED', 'source_commit': HEAD,
           'source_path': 'research/r16/sample.txt', 'source_sha256': HASH,
           'readback_sha256': HASH, 'source_bytes': 123,
           'trigger_receipt': URL, 'handoff_receipt': URL,
           'independent_evaluator_receipt': URL}
    out.update(changes)
    return out


def population(ids):
    return {'scope': 'SYNTHETIC_BOUNDED', 'enumeration_complete': True,
            'enumeration_commit': HEAD, 'enumeration_sha256': HASH,
            'enumerated_event_ids': sorted(ids), 'enumerated_event_count': len(ids),
            'enumerated_event_ids_sha256': hashlib.sha256(
                json.dumps(sorted(ids), ensure_ascii=True,
                           separators=(',', ':')).encode('utf-8')).hexdigest()}


def check(name, module, events, pop, status, n, d, coverage=None):
    try:
        result = module.assess(copy.deepcopy(events), copy.deepcopy(pop))
        ok = (result.get('status') == status and result.get('numerator') == n
              and result.get('denominator') == d
              and result.get('project_rate') == 'NOT_COMPUTABLE'
              and result.get('evidence_class') == 'SUPPLIED_FIELDS_NOT_INDEPENDENTLY_AUTHENTICATED'
              and (coverage is None or result.get('coverage_status') == coverage))
        return {'case': name, 'ok': ok, 'status': result.get('status'),
                'n': result.get('numerator'), 'd': result.get('denominator'),
                'coverage': result.get('coverage_status')}
    except Exception as exc:
        return {'case': name, 'ok': False, 'exception': type(exc).__name__}


def run(v1_path, v2_path):
    v1, v2 = load(v1_path), load(v2_path)
    a, b, c = event('a'), event('b'), event('c')
    full = population(['a', 'b', 'c'])
    two = population(['a', 'b'])
    cases = [
        ('v1_accepts_omitted_event_2_of_2', v1, [a,b], full, 'COHORT_DECLARED_ONLY',2,2,None),
        ('v2_rejects_omitted_event', v2, [a,b], full, 'NOT_COMPUTABLE',None,None,'EVENT_ID_SET_MISMATCH'),
        ('v2_exact_population', v2, [a,b], two, 'COHORT_DECLARED_ONLY',2,2,'EXACT_DECLARED_ID_SET'),
        ('v2_extra_event', v2, [a,b,c], two, 'NOT_COMPUTABLE',None,None,'EVENT_ID_SET_MISMATCH'),
        ('v2_missing_evaluator_kept_denominator', v2, [a,event('b',independent_evaluator_receipt='MISSING')], two, 'COHORT_DECLARED_ONLY',1,2,'EXACT_DECLARED_ID_SET'),
        ('v2_private_excluded', v2, [a,event('b',public='NO')], two, 'COHORT_DECLARED_ONLY',1,1,'EXACT_DECLARED_ID_SET'),
        ('v2_unknown_eligibility', v2, [a,event('b',accessible='UNKNOWN')], two, 'NOT_COMPUTABLE',None,None,'NOT_ASSESSED_V1_GATE'),
        ('v2_missing_id_list', v2, [a,b], {k:v for k,v in two.items() if k!='enumerated_event_ids'}, 'NOT_COMPUTABLE',None,None,'ENUMERATED_IDS_MISSING'),
        ('v2_wrong_digest', v2, [a,b], {**two,'enumerated_event_ids_sha256':'0'*64}, 'NOT_COMPUTABLE',None,None,'ENUMERATED_ID_DIGEST_MISMATCH'),
        ('v2_duplicate_enumeration', v2, [a,b], {**two,'enumerated_event_ids':['a','a']}, 'INVALID_INPUT',None,None,'MALFORMED_OR_DUPLICATE_ENUMERATION'),
        ('v2_unsorted_enumeration', v2, [a,b], {**two,'enumerated_event_ids':['b','a']}, 'INVALID_INPUT',None,None,'MALFORMED_OR_DUPLICATE_ENUMERATION'),
        ('v2_wrong_count', v2, [a,b], {**two,'enumerated_event_count':3}, 'INVALID_INPUT',None,None,'ENUMERATION_COUNT_MISMATCH'),
        ('v2_bool_count', v2, [a,b], {**two,'enumerated_event_count':True}, 'INVALID_INPUT',None,None,'ENUMERATION_COUNT_MISMATCH'),
        ('v2_malformed_id', v2, [a,b], {**two,'enumerated_event_ids':['a','../b']}, 'INVALID_INPUT',None,None,'MALFORMED_OR_DUPLICATE_ENUMERATION'),
        ('v2_incomplete_population', v2, [a,b], {**two,'enumeration_complete':False}, 'NOT_COMPUTABLE',None,None,'NOT_ASSESSED_V1_GATE'),
        ('v2_falsifier_coforged_full_population', v2, [a,b], two, 'COHORT_DECLARED_ONLY',2,2,'EXACT_DECLARED_ID_SET'),
        ('v2_invalid_event', v2, ['not-a-record'], two, 'INVALID_INPUT',None,None,'NOT_ASSESSED_V1_GATE'),
    ]
    rows=[check(*case) for case in cases]
    with tempfile.TemporaryDirectory() as td:
        root=Path(td)
        v1_copy=root/Path(v1_path).name
        v2_copy=root/Path(v2_path).name
        shutil.copyfile(v1_path,v1_copy)
        shutil.copyfile(v2_path,v2_copy)
        v1_copy.write_bytes(v1_copy.read_bytes()+b'\n# unexpected mutation\n')
        rows.append(check('v2_pinned_v1_source_mutation',load(v2_copy),[a,b],two,
                          'HOLD_SCOPED',None,None,'V1_ORIGINAL_BYTES_MISMATCH_OR_MISSING'))
    return rows


if __name__ == '__main__':
    rows=run(sys.argv[1],sys.argv[2]); passed=sum(r['ok'] for r in rows)
    print(json.dumps({'passed':passed,'total':len(rows),'results':rows},sort_keys=True))
    sys.exit(0 if passed==len(rows) else 1)
