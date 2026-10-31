#!/usr/bin/env python3
"""NEXUS GitHub Expert Exchange: deterministic, fail-closed package intake.

Stdlib only. Offline audit/packing; NO network, GitHub writes or execution of artifacts.
Public-safe infrastructure candidate. C1_DESCRIPTIVE_ONLY.
"""
from __future__ import annotations
import argparse
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import sys
import zipfile

MAX_MEMBERS = 1000
MAX_UNCOMPRESSED = 512 * 1024 * 1024
MAX_MEMBER = 128 * 1024 * 1024
MAX_COMPRESSION_RATIO = 2000
HASH_RE = re.compile(r'^[0-9a-f]{64}$')
SUM_RE = re.compile(r'^([0-9a-f]{64})  (.+)$')

class VerificationError(Exception):
    pass

def sha256(blob: bytes) -> str:
    return hashlib.sha256(blob).hexdigest()

def strict_json(blob: bytes):
    def pairs_no_duplicates(pairs):
        result = {}
        for k,v in pairs:
            if k in result: raise VerificationError('DUPLICATE_JSON_KEY')
            result[k] = v
        return result
    try:
        return json.loads(blob.decode('utf-8'), object_pairs_hook=pairs_no_duplicates,
                          parse_constant=lambda x: (_ for _ in ()).throw(VerificationError('NONFINITE_JSON')))
    except (UnicodeError, json.JSONDecodeError) as e:
        raise VerificationError('INVALID_JSON') from e

def safe_name(name: str) -> bool:
    if '\\' in name or not name or name.startswith('/') or '\x00' in name: return False
    p = PurePosixPath(name)
    return not any(x in ('.','..','') for x in p.parts) and ':' not in p.parts[0]

def _inspection(z: zipfile.ZipFile):
    infos=z.infolist(); errors=[]; names=set(); normalized=set(); size=0
    if len(infos)>MAX_MEMBERS: errors.append('TOO_MANY_MEMBERS')
    for i in infos:
        n=i.filename
        if not safe_name(n) or n.endswith('/') and not safe_name(n.rstrip('/')):
            errors.append('UNSAFE_MEMBER_PATH'); continue
        if n in names or n.casefold() in normalized: errors.append('DUPLICATE_MEMBER_NAME')
        names.add(n); normalized.add(n.casefold())
        if ((i.external_attr>>16)&stat.S_IFMT((i.external_attr>>16))) == stat.S_IFLNK: errors.append('SYMLINK_MEMBER')
        if i.file_size>MAX_MEMBER: errors.append('MEMBER_TOO_LARGE')
        size += i.file_size
        if i.file_size>0 and i.file_size/max(i.compress_size,1)>MAX_COMPRESSION_RATIO:
            errors.append('SUSPICIOUS_COMPRESSION')
    if size>MAX_UNCOMPRESSED: errors.append('ARCHIVE_TOO_LARGE')
    return sorted(set(errors)), names

def declared_paths_from_manifest(manifest):
    refs=set()
    if not isinstance(manifest,dict): raise VerificationError('MANIFEST_NOT_OBJECT')
    # Dispatch manifests can be additive to their physical SHA256SUMS ledger.
    for e in manifest.get('artifacts',[]):
        if not isinstance(e,dict): raise VerificationError('INVALID_ARTIFACT_RECORD')
        n=e.get('name')
        if n: refs.add(n)
    for e in manifest.get('lanes',[]):
        if not isinstance(e,dict): raise VerificationError('INVALID_LANE_RECORD')
        n=e.get('envelope')
        if n: refs.add(n)
    for n in manifest.get('required_members',[]):refs.add(n)
    if any(not isinstance(x,str) or not safe_name(x) for x in refs):
        raise VerificationError('MANIFEST_UNSAFE_PATH')
    return refs

def audit_zip(path: Path, manifest: str|None=None) -> dict:
    report={'object':'NEXUS_EXPERT_EXCHANGE_INTAKE_AUDIT_V1', 'file':path.name,
            'state':'NOT_VERIFIED','claim_ceiling':'C1_DESCRIPTIVE_ONLY',
            'errors':[],'missing':[],'mismatch':[],'declared_count':0,'member_count':0}
    try:
        with zipfile.ZipFile(path) as z:
            err,names=_inspection(z)
            report['member_count']=len(z.infolist())
            report['errors']+=err
            # No unbounded reads before size/path checks
            if err:
                report['state']='FAIL_CLOSED'
                return report
            checks=[]
            if 'SHA256SUMS' in names:
                sums=z.read('SHA256SUMS').decode('utf-8')
                for line in sums.splitlines():
                    m=SUM_RE.fullmatch(line)
                    if not m:
                        report['errors'].append('MALFORMED_SHA256SUMS'); continue
                    digest,name=m.groups()
                    if not safe_name(name): report['errors'].append('UNSAFE_SUM_PATH');continue
                    if name=='SHA256SUMS': report['errors'].append('SELF_HASH_RECURSION');continue
                    checks.append((name,digest))
            else:report['errors'].append('SHA256SUMS_NOT_PRESENT')
            report['declared_count']=len(checks)
            for name,digest in checks:
                if name not in names:report['missing'].append(name)
                elif sha256(z.read(name))!=digest:report['mismatch'].append(name)
            if manifest:
                if manifest not in names:
                    report['missing'].append(manifest)
                else:
                    data=strict_json(z.read(manifest))
                    for name in declared_paths_from_manifest(data):
                        if name not in names:report['missing'].append(name)
                    if 'parent_round' in data:report['parent_round']=data['parent_round']
                    if 'lanes' in data: report['lane_count']=len(data['lanes'])
            # Outer archive integrity cannot establish remote source availability.
            report['missing']=sorted(set(report['missing']))
            report['state']='SEALED_INTAKE_PASS_ONLY' if not(report['errors'] or report['mismatch'] or report['missing']) else 'FAIL_CLOSED'
            report['zip_bytes']=path.stat().st_size
            report['zip_sha256']=sha256(path.read_bytes())
            report['scope']='LOCAL_CONTAINER_ONLY;REMOTE_SOURCE_CLOSURE_NOT_ESTABLISHED'
            return report
    except (OSError,zipfile.BadZipFile,RuntimeError,UnicodeError,VerificationError) as exc:
        report['errors'].append(type(exc).__name__ if not isinstance(exc,VerificationError) else str(exc))
        report['state']='FAIL_CLOSED';return report

def pack_from_manifest(root: Path, manifest_name: str, target: Path):
    """Build bounded, complete deterministic transport from a pre-approved staging dir.

    A missing declared member is a HARD STOP, never a partial ZIP.
    SHA256SUMS is generated over all members except itself, without self reference.
    """
    manifest_path=root/manifest_name
    if not manifest_path.is_file(): raise VerificationError('MANIFEST_NOT_PRESENT')
    manifest=strict_json(manifest_path.read_bytes())
    paths=declared_paths_from_manifest(manifest)|{manifest_name}
    if any(not safe_name(x) for x in paths):raise VerificationError('UNSAFE_PATH')
    blobs={}
    for relative in sorted(paths):
        full=root/relative
        if not full.is_file() or full.is_symlink():raise VerificationError('MISSING_OR_SYMLINK:'+relative)
        if not full.resolve().is_relative_to(root.resolve()):raise VerificationError('ESCAPE_PATH:'+relative)
        data=full.read_bytes()
        if len(data)>MAX_MEMBER:raise VerificationError('MEMBER_TOO_LARGE:'+relative)
        blobs[relative]=data
        # A declared digest must match, but raw files might only declare existence.
    for a in manifest.get('artifacts',[]):
        name=a.get('name'); h=a.get('sha256'); n=a.get('bytes')
        if name and h and (not HASH_RE.fullmatch(h) or sha256(blobs[name])!=h):raise VerificationError('ARTIFACT_HASH_MISMATCH:'+name)
        if name and n is not None and len(blobs[name])!=n:raise VerificationError('ARTIFACT_BYTES_MISMATCH:'+name)
    if len(blobs)+1>MAX_MEMBERS or sum(map(len,blobs.values()))>MAX_UNCOMPRESSED:raise VerificationError('ARCHIVE_SIZE_LIMIT')
    sums=''.join(f'{sha256(data)}  {name}\n' for name,data in sorted(blobs.items())).encode()
    blobs['SHA256SUMS']=sums
    # Build entirely in memory; no file is written on failure.
    buffer=io.BytesIO()
    with zipfile.ZipFile(buffer,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for name,data in sorted(blobs.items()):
            info=zipfile.ZipInfo(name,date_time=(1980,1,1,0,0,0))
            info.compress_type=zipfile.ZIP_DEFLATED
            info.external_attr=0o100644<<16
            z.writestr(info,data,compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
    target.parent.mkdir(parents=True,exist_ok=True)
    new=buffer.getvalue()
    # Still verify exact archive bytes before atomic placement.
    temp=target.with_suffix('.tmp')
    try:
        temp.write_bytes(new)
        result=audit_zip(temp,manifest_name)
        if result['state']!='SEALED_INTAKE_PASS_ONLY':raise VerificationError('SELF_AUDIT_FAILED')
        os.replace(temp,target)
    finally:
        if temp.exists():temp.unlink()
    return {'state':'PACKED_VERIFIED_LOCAL_ONLY','bytes':len(new),'sha256':sha256(new),'members':len(blobs)}

def main(argv=None):
    p=argparse.ArgumentParser(description='NEXUS expert exchange fail-closed offline intake')
    sub=p.add_subparsers(dest='cmd',required=True)
    a=sub.add_parser('audit');a.add_argument('zip');a.add_argument('--manifest',default=None);a.add_argument('--report',default=None)
    b=sub.add_parser('pack');b.add_argument('--source',required=True);b.add_argument('--manifest',required=True);b.add_argument('--out',required=True)
    args=p.parse_args(argv)
    try:
        if args.cmd=='audit':
            result=audit_zip(Path(args.zip),args.manifest)
            if args.report:Path(args.report).write_text(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)+'\n')
        else:result=pack_from_manifest(Path(args.source),args.manifest,Path(args.out))
    except (OSError,VerificationError) as e:
        result={'state':'FAIL_CLOSED','error':str(e)}
    print(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2))
    return 0 if result['state'] in ('SEALED_INTAKE_PASS_ONLY','PACKED_VERIFIED_LOCAL_ONLY') else 2
if __name__=='__main__':sys.exit(main())
