#!/usr/bin/env python3
"""Pre-implementation frozen black-box oracle: JSON integer interoperability.

Scope: an isolated evidence-capture policy, not general RFC 8259 validity,
scientific adjudication, actor authentication, or productive integration.
Test expectations are literal and independent of the candidate implementation.
"""
import hashlib
import json
import pathlib
import subprocess
import sys
import tempfile

CASES = [
    ('ordinary_object', b'{"claim_ceiling":"C1_DESCRIPTIVE_ONLY"}', True),
    ('safe_positive_boundary', b'{"bytes":9007199254740991}', True),
    ('safe_negative_boundary', b'{"bytes":-9007199254740991}', True),
    ('safe_positive_near', b'{"bytes":9007199254740990}', True),
    ('safe_negative_near', b'{"bytes":-9007199254740990}', True),
    ('zero', b'{"bytes":0}', True),
    ('negative_zero', b'{"bytes":-0}', True),
    ('nested_safe', b'{"a":[{"bytes":-9007199254740991},9007199254740991]}', True),
    ('booleans_and_null', b'{"enabled":true,"ok":false,"x":null}', True),
    ('finite_float', b'{"x":1e308,"y":1e-308}', True),
    ('fractional_float', b'{"x":0.1}', True),
    ('utf8_text', '{"title":"Prüfung"}'.encode('utf-8'), True),
    ('zero_exponent', b'{"x":0e-9999}', True),
    ('unsafe_positive_first', b'{"bytes":9007199254740992}', False),
    ('unsafe_positive_odd', b'{"bytes":9007199254740993}', False),
    ('unsafe_negative_first', b'{"bytes":-9007199254740992}', False),
    ('unsafe_negative_odd', b'{"bytes":-9007199254740993}', False),
    ('unsafe_nested', b'{"meta":{"source_bytes":9007199254740993}}', False),
    ('unsafe_array', b'{"counts":[1,9007199254740993]}', False),
    ('unsafe_64bit', b'{"id":9223372036854775807}', False),
    ('unsafe_very_large', b'{"n":123456789012345678901234567890}', False),
    ('duplicate_key', b'{"x":1,"x":2}', False),
    ('duplicate_escaped', b'{"sha256":"a","sha\\u003256":"b"}', False),
    ('nan_constant', b'{"x":NaN}', False),
    ('infinity_constant', b'{"x":Infinity}', False),
    ('float_overflow', b'{"x":1e309}', False),
    ('float_underflow', b'{"x":1e-9999}', False),
    ('root_array', b'[1,2]', False),
    ('invalid_utf8', b'{"x":"\xff"}', False),
    ('empty', b'', False),
]

def run(candidate):
    results=[]
    for name,raw,expected in CASES:
        with tempfile.TemporaryDirectory() as d:
            inp=pathlib.Path(d)/'capture.json';inp.write_bytes(raw)
            p=subprocess.run([sys.executable,candidate,str(inp)],capture_output=True,text=True,timeout=10)
            try:
                obj=json.loads(p.stdout)
                status=obj.get('status')
                protocol_ok=(status=='ACCEPT_STRICT_JSON' and p.returncode==0) or (status=='REJECT' and p.returncode==2)
                actual=status=='ACCEPT_STRICT_JSON' and p.returncode==0
                reason=obj.get('reason')
                if actual and (obj.get('claim_ceiling')!='C1_DESCRIPTIVE_ONLY' or obj.get('authentication')!='NOT_ESTABLISHED'):
                    protocol_ok=False
            except (ValueError,AttributeError,TypeError):
                protocol_ok=False;actual=False;reason='BAD_OUTPUT'
            results.append({'name':name,'raw_sha256':hashlib.sha256(raw).hexdigest(),'expected_accept':expected,
                            'actual_accept':actual,'reason':reason,'pass':bool(protocol_ok and actual==expected)})
    return {'oracle':'ALPHA_JSON_SAFE_INTEGER_FROZEN_EVALUATOR_V1','total':len(results),
            'pass':sum(x['pass'] for x in results),'negative_total':sum(not x['expected_accept'] for x in results),
            'negative_rejected':sum(x['pass'] for x in results if not x['expected_accept']),
            'positive_total':sum(x['expected_accept'] for x in results),
            'positive_accepted':sum(x['pass'] for x in results if x['expected_accept']),
            'cases':results}

if __name__=='__main__':
    r=run(sys.argv[1]);print(json.dumps(r,ensure_ascii=False,indent=2));sys.exit(0 if r['pass']==r['total'] else 1)
