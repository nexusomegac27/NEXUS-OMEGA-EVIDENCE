#!/usr/bin/env python3
"""NEXUS OMEGA / Bodytwin C1 public-status reducer.

Reads ONLY already-public, explicitly allowlisted website files. Writes ONLY
<bodytwin>/live/current.json, atomically. No network, sensor APIs, secrets,
private-repo access, health data, or truth/claim promotion.
"""
from __future__ import annotations
import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile

SCHEMA = 'nexus-bodytwin-live-feed/1'
CLAIM = 'C1_DESCRIPTIVE_ONLY'
PUB_STATUS = Path('research/bodytwin/state.json')
PUB_RECEIPT = Path('bodytwin/live/receipts.public.json')
OUTPUT = Path('bodytwin/live/current.json')
PUBLIC_STATE_KEYS = {
    'schema','object','BODYTWIN','BODYTWIN_VALIDATED','CONSENT_BIND',
    'TRIAL_001','layers','pipeline','invariants','claim_ceiling','claim_promotion'
}
RECEIPT_KEYS = {'schema','claim_ceiling','source_object','source_date','windows','gates'}
WINDOWS_KEYS = {'status','node_pass','node_total','mutation_pass','mutation_total','schema_pass','schema_total'}
GATES_KEYS = {'a72','r13_stage_ii','physical_imu','bodytwin_validated','consent','gate_v2'}
EXPECTED_LAYERS = {'L0','L1','L2','L3','UNKNOWN_UNOBSERVED'}
EXPECTED_PIPELINE = {'Capture','Normalize','Align','Refine','Metrics'}
EXPECTED_INVARIANTS = {'RAW_NE_REFINED','PHOTOREALISM_GAIN_MAY_CAUSE_IDENTITY_LOSS','NO_PRIVATE_HUMAN_REFERENCE_MEDIA'}

class ContractError(ValueError):
    pass

def _require(cond, error):
    if not cond: raise ContractError(error)

def _keys(obj, expected, name):
    _require(type(obj) is dict and set(obj) == expected, 'INVALID_KEYS_'+name)

def _set(v, expected, name):
    _require(type(v) is list and len(v) == len(expected) and all(type(x) is str for x in v) and set(v) == expected, 'INVALID_SET_'+name)

def validate_state(s):
    _keys(s,PUBLIC_STATE_KEYS,'PUBLIC_STATE')
    _require(s['schema']=='nexus-research-bodytwin-state/1' and s['object']=='BODYTWIN_PUBLIC_SURFACE','INVALID_STATE_SCHEMA')
    for k,v in {'BODYTWIN':'RESEARCH_FOUNDATION_C1','BODYTWIN_VALIDATED':'NO','CONSENT_BIND':'OPEN',
                'TRIAL_001':'DESIGNED_NOT_EXECUTED','claim_ceiling':CLAIM,'claim_promotion':False}.items():
        _require(type(s[k]) is type(v) and s[k] == v, 'INVALID_STATE_'+k)
    _set(s['layers'],EXPECTED_LAYERS,'LAYERS')
    _set(s['pipeline'],EXPECTED_PIPELINE,'PIPELINE')
    _set(s['invariants'],EXPECTED_INVARIANTS,'INVARIANTS')
    return s

def validate_receipt(r, now_utc):
    _keys(r,RECEIPT_KEYS,'RECEIPT')
    _require(r['schema']=='nexus-bodytwin-public-receipts/1' and r['claim_ceiling']==CLAIM,'INVALID_RECEIPT_SCHEMA')
    _require(r['source_object']=='NEXUS_OMEGA_AXIOM_R14_R2R1_WINDOWS_PORTABILITY_HARNESS_REPAIR_HANDOFF_20261107_R0','WRONG_RECEIPT_SOURCE')
    _require(type(r['source_date']) is str and re.fullmatch(r'20\d\d-\d\d-\d\d',r['source_date']), 'INVALID_SOURCE_DATE')
    try: date = datetime.strptime(r['source_date'], '%Y-%m-%d').replace(tzinfo=timezone.utc)
    except ValueError as exc: raise ContractError('INVALID_SOURCE_DATE') from exc
    _require(date.date()<=now_utc.date(),'FUTURE_RECEIPT_DATE')
    _keys(r['windows'],WINDOWS_KEYS,'WINDOWS')
    _require(r['windows']['status']=='CURSOR_REPORTED_PASS_C1','UNSUPPORTED_WINDOWS_ASSERTION')
    for k in ['node_pass','node_total','mutation_pass','mutation_total','schema_pass','schema_total']:
        _require(type(r['windows'][k]) is int and 0<=r['windows'][k]<=100000,'INVALID_COUNTER_'+k)
    for a,b in [('node_pass','node_total'),('mutation_pass','mutation_total'),('schema_pass','schema_total')]:
        _require(r['windows'][a]<=r['windows'][b],'COUNT_OVERFLOW_'+a)
    _keys(r['gates'],GATES_KEYS,'GATES')
    fixed = {'a72':'SOURCE_GAP','r13_stage_ii':'HOLD_DEPLOY_GAP','physical_imu':'NOT_AUTHORIZED',
             'bodytwin_validated':'NO','consent':'OPEN','gate_v2':'HOLD_R9_MJS_PREREQUISITE'}
    for k,v in fixed.items(): _require(r['gates'][k]==v,'UNAUTHORIZED_GATE_CHANGE_'+k)
    return r

def _bytes(path, root, max_size=25000):
    p=root/path
    _require(p.resolve().is_relative_to(root.resolve()),'PATH_ESCAPE')
    _require(p.is_file() and not p.is_symlink(), 'SOURCE_MISSING_OR_SYMLINK_'+str(path))
    b=p.read_bytes()
    _require(0<len(b)<=max_size, 'SOURCE_SIZE_INVALID_'+str(path))
    try: return b,json.loads(b.decode('utf-8','strict'))
    except (UnicodeError,json.JSONDecodeError) as exc: raise ContractError('SOURCE_JSON_INVALID_'+str(path)) from exc

def _utc(t):
    return t.astimezone(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')

def build(root: Path, now: datetime):
    _require(now.tzinfo is not None,'UTC_CLOCK_REQUIRED')
    now=now.astimezone(timezone.utc)
    _require(root.is_dir() and root.resolve() == root, 'ROOT_NOT_RESOLVED')
    bs,s=_bytes(PUB_STATUS,root); br,r=_bytes(PUB_RECEIPT,root)
    validate_state(s);validate_receipt(r,now)
    out=root/OUTPUT
    old=None
    if out.is_symlink(): raise ContractError('OUTPUT_IS_SYMLINK')
    if out.exists():
        _,old=_bytes(OUTPUT,root)
        _require(type(old) is dict and old.get('schema')==SCHEMA, 'OLD_FEED_UNRECOGNIZED')
        _require(type(old.get('producer')) is dict and type(old['producer'].get('seq')) is int and old['producer']['seq']>=1, 'OLD_SEQUENCE_INVALID')
        _require(type(old['producer'].get('run_utc')) is str and old['producer']['run_utc'] < _utc(now), 'OLD_FEED_CLOCK_ROLLBACK')
    state_sha=hashlib.sha256(bs).hexdigest(); receipt_sha=hashlib.sha256(br).hexdigest()
    old_digests=old.get('sources') if old else None
    src={'bodytwin_state':{'url':'/research/bodytwin/state.json','sha256':state_sha},
         'research_receipt':{'url':'/bodytwin/live/receipts.public.json','sha256':receipt_sha}}
    changed=(old_digests!=src)
    last_changed=_utc(now) if changed else old['producer']['last_change_utc']
    seq=1 if old is None else old['producer']['seq']+1
    result={
      'schema':SCHEMA,'claim_ceiling':CLAIM,'trust':'SELF_HOSTED_PUBLIC_C1_NOT_INDEPENDENT_WITNESS',
      'producer':{'run_utc':_utc(now),'seq':seq,'interval_seconds':300,
                  'source_changed':changed,'last_change_utc':last_changed},
      'sources':src,
      'bodytwin':{'state':s['BODYTWIN'],'validated':s['BODYTWIN_VALIDATED'],
                  'consent':s['CONSENT_BIND'],'trial':s['TRIAL_001']},
      'research':{'source_date':r['source_date'],'source_object':r['source_object'],**r['windows']},
      'gates':r['gates']
    }
    return result

@contextmanager
def process_lock(root:Path):
    lock=root/'bodytwin/live/.refresh.lock'
    if lock.is_symlink(): raise ContractError('LOCK_IS_SYMLINK')
    lock.parent.mkdir(parents=True,exist_ok=True)
    with lock.open('a+') as f:
        try:
            import fcntl
            fcntl.flock(f.fileno(),fcntl.LOCK_EX|fcntl.LOCK_NB)
        except ImportError: raise ContractError('HOSTINGER_LINUX_FLOCK_REQUIRED')
        except BlockingIOError: raise ContractError('PARALLEL_REFRESH_REJECTED')
        try: yield
        finally:
            fcntl.flock(f.fileno(),fcntl.LOCK_UN)

def write_atomic(root:Path,body:dict):
    p=root/OUTPUT
    _require(not p.is_symlink(),'OUTPUT_IS_SYMLINK')
    p.parent.mkdir(parents=True,exist_ok=True)
    data=(json.dumps(body,ensure_ascii=True,sort_keys=True,separators=(',',':'))+'\n').encode('utf-8')
    _require(len(data)<25000,'OUTPUT_TOO_LARGE')
    tmp=None
    try:
        with tempfile.NamedTemporaryFile(mode='wb',dir=p.parent,prefix='.feed-',delete=False) as f:
            tmp=Path(f.name);f.write(data);f.flush();os.fsync(f.fileno())
        os.chmod(tmp,0o644);os.replace(tmp,p)
        dfd=os.open(p.parent,os.O_RDONLY)
        try: os.fsync(dfd)
        finally:os.close(dfd)
    finally:
        if tmp and tmp.exists():tmp.unlink()
    return hashlib.sha256(data).hexdigest()

def main():
    p=argparse.ArgumentParser();p.add_argument('--document-root',required=True);args=p.parse_args()
    root=Path(args.document_root).resolve(strict=True)
    try:
        with process_lock(root):
            body=build(root,datetime.now(timezone.utc))
            sha=write_atomic(root,body)
        print(json.dumps({'object':'BODYTWIN_C1_PUBLIC_FEED_TICK','state':'ATOMIC_PUBLIC_C1_UPDATE',
            'seq':body['producer']['seq'],'source_changed':body['producer']['source_changed'],
            'bytes_sha256':sha,'run_utc':body['producer']['run_utc']},sort_keys=True))
    except (ContractError,OSError,ValueError) as exc:
        raise SystemExit('HOLD_PUBLIC_FEED_'+str(exc))
if __name__=='__main__':main()
