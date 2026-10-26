#!/usr/bin/env python3
"""Isolated C1 sample census V3: short-circuit known ineligibility before unknowns.
Never asserts completeness of a project-wide handoff inventory.
"""
import json
import sys

KEYS = {'id','scope','accessible','authorized','routine','automated','outcome','source_readback','publication_readback'}

def reject(message):
    raise ValueError(message)

def unique_pairs(items):
    result = {}
    for key, value in items:
        if key in result:
            reject('DUPLICATE_JSON_KEY')
        result[key] = value
    return result

def nonfinite(_):
    reject('NONFINITE_JSON')

def classify(record):
    if type(record) is not dict or set(record) != KEYS:
        reject('INVALID_RECORD_FIELDS')
    if type(record['id']) is not str or not record['id'] or len(record['id']) > 128:
        reject('INVALID_ID')
    if record['scope'] not in ('PUBLIC','PRIVATE','LOCAL'):
        reject('INVALID_SCOPE')
    for key in ('accessible','authorized','routine'):
        if record[key] is not None and type(record[key]) is not bool:
            reject('INVALID_ELIGIBILITY_FIELD')
    if type(record['automated']) is not bool:
        reject('INVALID_AUTOMATED')
    if record['outcome'] not in ('SUCCESS','FAILED','PENDING'):
        reject('INVALID_OUTCOME')
    for key in ('source_readback','publication_readback'):
        if record[key] not in ('MATCH','GAP'):
            reject('INVALID_READBACK')
    if record['scope'] in ('PRIVATE','LOCAL') and record['accessible'] is True:
        reject('NONPUBLIC_ACCESS_CONFLICT')
    # Known exclusion dominates unknown values in unrelated eligibility fields.
    if (record['scope'] != 'PUBLIC' or record['accessible'] is False or
            record['authorized'] is False or record['routine'] is False):
        return 'EXCLUDED'
    if any(record[key] is None for key in ('accessible','authorized','routine')):
        return 'UNKNOWN'
    if (record['automated'] and record['outcome'] == 'SUCCESS' and
            record['source_readback'] == 'MATCH' and record['publication_readback'] == 'MATCH'):
        return 'SUCCESS'
    return 'ELIGIBLE_NOT_SUCCESS'

def census(payload):
    if (type(payload) is not dict or set(payload) != {'schema_version','records'} or
            type(payload['schema_version']) is not int or payload['schema_version'] != 2):
        reject('INVALID_ENVELOPE')
    records = payload['records']
    if type(records) is not list or len(records) > 10000:
        reject('INVALID_RECORDS')
    seen = set()
    counts = {'SUCCESS':0,'ELIGIBLE_NOT_SUCCESS':0,'EXCLUDED':0,'UNKNOWN':0}
    for record in records:
        state = classify(record)
        if record['id'] in seen:
            reject('DUPLICATE_ID')
        seen.add(record['id'])
        counts[state] += 1
    denominator = counts['SUCCESS'] + counts['ELIGIBLE_NOT_SUCCESS']
    sample_rate = ('WITHHELD_UNKNOWN_ELIGIBILITY' if counts['UNKNOWN'] else
                   'NOT_COMPUTABLE_ZERO_DENOMINATOR' if not denominator else
                   f"{counts['SUCCESS']}/{denominator}")
    return {'eligible_denominator':denominator,'automated_numerator':counts['SUCCESS'],
            'excluded_count':counts['EXCLUDED'],'unknown_eligibility_count':counts['UNKNOWN'],
            'sample_rate':sample_rate,'project_rate':'NOT_COMPUTABLE',
            'evidence_class':'UNVERIFIED_SAMPLE_ONLY','claim_ceiling':'C1_DESCRIPTIVE_ONLY'}

def main():
    try:
        payload = json.loads(sys.stdin.read(),object_pairs_hook=unique_pairs,parse_constant=nonfinite)
        print(json.dumps(census(payload),sort_keys=True,separators=(',',':')))
        return 0
    except (ValueError,TypeError,UnicodeError) as exc:
        print('FAIL_CLOSED: '+str(exc),file=sys.stderr)
        return 2

if __name__ == '__main__':
    sys.exit(main())
