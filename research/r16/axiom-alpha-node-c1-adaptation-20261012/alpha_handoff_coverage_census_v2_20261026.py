#!/usr/bin/env python3
"""Isolated read-only C1 sample handoff census. No project-wide coverage claim.
V2 is a new candidate; original V1 local-only source is not reconstructed.
"""
import json
import sys

KEYS={'id','scope','accessible','authorized','routine','automated','outcome','source_readback','publication_readback'}

def reject(msg):
    raise ValueError(msg)

def pairs(items):
    out={}
    for key,value in items:
        if key in out: reject('DUPLICATE_JSON_KEY')
        out[key]=value
    return out

def finite(_):
    reject('NONFINITE_JSON')

def boolean(value):
    return type(value) is bool

def classify(record):
    if type(record) is not dict or set(record)!=KEYS: reject('INVALID_RECORD_FIELDS')
    if type(record['id']) is not str or not record['id'] or len(record['id'])>128: reject('INVALID_ID')
    if record['scope'] not in ('PUBLIC','PRIVATE','LOCAL'): reject('INVALID_SCOPE')
    for key in ('accessible','authorized','routine'):
        if record[key] is not None and not boolean(record[key]): reject('INVALID_ELIGIBILITY_FIELD')
    if not boolean(record['automated']): reject('INVALID_AUTOMATED')
    if record['outcome'] not in ('SUCCESS','FAILED','PENDING'): reject('INVALID_OUTCOME')
    for key in ('source_readback','publication_readback'):
        if record[key] not in ('MATCH','GAP'): reject('INVALID_READBACK')
    if record['scope'] in ('PRIVATE','LOCAL') and record['accessible'] is True:
        reject('NONPUBLIC_ACCESS_CONFLICT')
    if None in (record['accessible'],record['authorized'],record['routine']):
        return 'UNKNOWN'
    if record['scope']!='PUBLIC' or not record['accessible'] or not record['authorized'] or not record['routine']:
        return 'EXCLUDED'
    return 'SUCCESS' if (record['automated'] and record['outcome']=='SUCCESS' and
        record['source_readback']=='MATCH' and record['publication_readback']=='MATCH') else 'ELIGIBLE_NOT_SUCCESS'

def census(payload):
    if type(payload) is not dict or set(payload)!={'schema_version','records'} or type(payload['schema_version']) is not int or payload['schema_version']!=2:
        reject('INVALID_ENVELOPE')
    records=payload['records']
    if type(records) is not list or len(records)>10000: reject('INVALID_RECORDS')
    seen=set(); counts={'SUCCESS':0,'ELIGIBLE_NOT_SUCCESS':0,'EXCLUDED':0,'UNKNOWN':0}
    for rec in records:
        state=classify(rec)
        if rec['id'] in seen: reject('DUPLICATE_ID')
        seen.add(rec['id']); counts[state]+=1
    d=counts['SUCCESS']+counts['ELIGIBLE_NOT_SUCCESS']
    rate=('WITHHELD_UNKNOWN_ELIGIBILITY' if counts['UNKNOWN'] else
          'NOT_COMPUTABLE_ZERO_DENOMINATOR' if d==0 else f"{counts['SUCCESS']}/{d}")
    return {'eligible_denominator':d,'automated_numerator':counts['SUCCESS'],
            'excluded_count':counts['EXCLUDED'],'unknown_eligibility_count':counts['UNKNOWN'],
            'sample_rate':rate,'project_rate':'NOT_COMPUTABLE',
            'evidence_class':'UNVERIFIED_SAMPLE_ONLY','claim_ceiling':'C1_DESCRIPTIVE_ONLY'}

def main():
    try:
        data=json.loads(sys.stdin.read(),object_pairs_hook=pairs,parse_constant=finite)
        print(json.dumps(census(data),sort_keys=True,separators=(',',':')))
    except (ValueError,TypeError,UnicodeError) as exc:
        print('FAIL_CLOSED: '+str(exc),file=sys.stderr)
        return 2
    return 0

if __name__=='__main__':
    sys.exit(main())
