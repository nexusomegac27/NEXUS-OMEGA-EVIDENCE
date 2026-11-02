"""Frozen external evaluator for a research-only C1 handoff denominator guard.

Synthetic fixtures are intentionally not actual handoff receipts. This oracle
must remain unchanged after the candidate is committed.
"""
import copy
import importlib.util
import json
import sys

HEAD = 'a' * 40
HASH = 'b' * 64
URL = 'https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/issues/93#issuecomment-123'


def event(ident, *, flags=('YES',)*4, auto='YES', complete=True):
    e = {'id': ident, 'public': flags[0], 'routine': flags[1],
         'authorized': flags[2], 'accessible': flags[3],
         'unattended': auto, 'source_commit': HEAD,
         'source_path': 'research/r16/sample.txt', 'source_sha256': HASH,
         'readback_sha256': HASH, 'source_bytes': 123,
         'trigger_receipt': URL, 'handoff_receipt': URL,
         'independent_evaluator_receipt': URL,
         'operator_nudge': 'NO_VERIFIED'}
    if not complete:
        e['independent_evaluator_receipt'] = 'NOT_ESTABLISHED'
    return e


def population(complete=True):
    return {'scope': 'PR_274_283_BOUNDED', 'enumeration_complete': complete,
            'enumeration_commit': HEAD, 'enumeration_sha256': HASH}


def run(path):
    spec = importlib.util.spec_from_file_location('candidate', path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    a = event('a')
    b = event('b', complete=False)
    p = event('private', flags=('NO','YES','YES','YES'))
    unknown = event('unknown', flags=('UNKNOWN','YES','YES','YES'))
    gap = event('gap'); gap['source_sha256'] = 'SOURCE_NOT_PRESENT'
    nudged = event('nudged'); nudged['operator_nudge'] = 'YES'
    no_trigger = event('no_trigger'); no_trigger['trigger_receipt'] = 'NOT_ESTABLISHED'
    hash_mismatch = event('mismatch'); hash_mismatch['readback_sha256'] = 'c'*64
    tests = [
      ('positive_declared_1_of_2', [a,b], population(), 'COHORT_DECLARED_ONLY',1,2),
      ('private_excluded', [a,p], population(), 'COHORT_DECLARED_ONLY',1,1),
      ('unknown_eligibility', [a,unknown], population(), 'NOT_COMPUTABLE',None,None),
      ('incomplete_population', [a], population(False), 'NOT_COMPUTABLE',None,None),
      ('missing_population_hash', [a], {**population(), 'enumeration_sha256':'UNKNOWN'}, 'NOT_COMPUTABLE',None,None),
      ('source_gap_in_denominator', [a,gap], population(), 'COHORT_DECLARED_ONLY',1,2),
      ('operator_nudge_excluded', [a,nudged], population(), 'COHORT_DECLARED_ONLY',1,2),
      ('missing_trigger_excluded', [a,no_trigger], population(), 'COHORT_DECLARED_ONLY',1,2),
      ('mismatched_source_hash_excluded', [a,hash_mismatch], population(), 'COHORT_DECLARED_ONLY',1,2),
      ('duplicate_id_invalid', [a,a], population(), 'INVALID_INPUT',None,None),
      ('empty_invalid', [], population(), 'INVALID_INPUT',None,None),
      ('malformed_invalid', ['a'], population(), 'INVALID_INPUT',None,None),
      ('all_ineligible_zero_denominator', [p], population(), 'COHORT_DECLARED_ONLY',0,0),
      ('falsifier_self_attested_forgery_still_structurally_accepted', [event('forged')], population(), 'COHORT_DECLARED_ONLY',1,1),
    ]
    out=[]
    for name,events,pop,status,numer,denom in tests:
        try:
            got=mod.assess(copy.deepcopy(events),copy.deepcopy(pop))
            ok=(got.get('status')==status and got.get('numerator')==numer
                and got.get('denominator')==denom
                and got.get('project_rate')=='NOT_COMPUTABLE'
                and got.get('evidence_class')=='SUPPLIED_FIELDS_NOT_INDEPENDENTLY_AUTHENTICATED')
            obs={k:got.get(k) for k in ('status','numerator','denominator','project_rate')}
        except Exception as exc:
            ok=False; obs='EXCEPTION_'+type(exc).__name__
        out.append({'case':name,'ok':ok,'observed':obs})
    return out


if __name__=='__main__':
    rows=run(sys.argv[1]); print(json.dumps({'passed':sum(x['ok'] for x in rows),'total':len(rows),'results':rows},sort_keys=True))
    sys.exit(0 if all(x['ok'] for x in rows) else 1)
