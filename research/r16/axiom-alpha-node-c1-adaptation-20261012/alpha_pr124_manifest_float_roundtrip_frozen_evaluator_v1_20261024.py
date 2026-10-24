"""Frozen independent C1 oracle: JSON float token identity under Python roundtrip.

Evaluate the predecessor and candidate as separate subprocesses; the oracle
classifies raw lexical tokens with decimal.Decimal, not the candidate parser.
This checks JSON metadata precision only, not content hashes or science.
"""
import json
import subprocess
import sys
from decimal import Decimal

P='research/r16/axiom-alpha-node-c1-adaptation-20261012/'
ROW={'path':P+'Alpha.py','bytes':42,'sha256':'a'*64,'git_blob_sha1':'b'*40}
CASES=[
    ('ordinary_decimal','0.1',True),
    ('fraction_exact','1.25',True),
    ('small_scientific','1e-7',True),
    ('large_scientific','1e300',True),
    ('explicit_zero','0.0',True),
    ('negative_zero','-0.0',True),
    ('integer_float','42.0',True),
    ('small_subnormal','1e-320',True),
    ('underflow_positive','1e-999',False),
    ('underflow_negative','-1e-999',False),
    ('rounded_unit','1.0000000000000001',False),
    ('rounded_fraction','0.10000000000000001',False),
    ('unsafe_float_integer','9007199254740993.0',False),
    ('unsafe_float_negative','-9007199254740993.0',False),
    ('overflow_exponent','1e999',False),
]

def expected_by_independent_oracle(token):
    """Independent lexical criterion: Python float repr must preserve decimal value."""
    try:
        value=float(token)
        return value==value and value!=float('inf') and value!=float('-inf') and Decimal(str(value))==Decimal(token)
    except (ValueError,OverflowError):return False

def evaluate(script):
    failures=[]
    for name,token,expected in CASES:
        assert expected_by_independent_oracle(token)==expected,(name,'oracle mismatch')
        raw='{"count":1,"files":'+json.dumps([ROW])+',"metadata_probe":'+token+'}'
        p=subprocess.run([sys.executable,script],input=raw,text=True,capture_output=True,timeout=5)
        try:
            result=json.loads(p.stdout)
            actual=(p.returncode==0 and result['status']=='PASS_C1')
            coherent=(p.returncode==0)==(result['status']=='PASS_C1')
        except (ValueError,KeyError,TypeError):actual,coherent=False,False
        if actual!=expected or not coherent:failures.append(name)
    return {'correct':len(CASES)-len(failures),'total':len(CASES),'failures':failures}

if __name__=='__main__':print(json.dumps(evaluate(sys.argv[1]),sort_keys=True))
