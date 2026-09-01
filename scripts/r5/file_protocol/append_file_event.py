#!/usr/bin/env python3
"""Append an immutable NEXUS file event to the local canonical file-event archive."""
from __future__ import annotations
import argparse, hashlib, json, os, tempfile
from pathlib import Path

DERIVED_ROOT = Path("communication/file-events")

def canon(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")

def sha(b): return hashlib.sha256(b).hexdigest()

def atomic_write(path: Path, data: bytes):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=".nexus-", dir=str(path.parent))
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(data); f.flush(); os.fsync(f.fileno())
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp): os.unlink(tmp)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("event_json"); ap.add_argument("--root",default=".")
    args=ap.parse_args(); root=Path(args.root)
    event=json.loads(Path(args.event_json).read_text(encoding="utf-8"))
    required={"schema_version","event_id","recorded_at_utc","actor","task","operation","artifact_class","digest_domain","before","after","reason","git","claim_ceiling"}
    missing=sorted(required-set(event))
    if missing: raise SystemExit("missing fields: "+",".join(missing))
    if event["schema_version"]!="1.0.0" or event["claim_ceiling"]!="C1" or event["digest_domain"]!="SHA256_RAW_BYTES_V1": raise SystemExit("profile mismatch")
    data=canon(event); digest=sha(data)
    obj=root/DERIVED_ROOT/"objects"/"sha256"/digest[:2]/digest[2:4]/digest/"event.json"
    if obj.exists() and obj.read_bytes()!=data: raise SystemExit("content-address collision")
    if not obj.exists(): atomic_write(obj, data+b"\n")
    idx=root/DERIVED_ROOT/"index"/"v1"/"events.jsonl"; latest=root/DERIVED_ROOT/"index"/"v1"/"latest.json"
    previous=None; seq=1
    if latest.exists():
        cur=json.loads(latest.read_text(encoding="utf-8")); previous=cur.get("head_index_line_sha256"); seq=int(cur.get("sequence",0))+1
    line={"sequence":seq,"event_id":event["event_id"],"event_bytes":len(data)+1,"event_sha256":digest,"object_path":obj.relative_to(root).as_posix(),"previous_index_line_sha256":previous}
    line_bytes=canon(line)
    idx.parent.mkdir(parents=True,exist_ok=True)
    with idx.open("ab") as f:
        f.write(line_bytes+b"\n"); f.flush(); os.fsync(f.fileno())
    head=sha(line_bytes)
    atomic_write(latest, canon({"object":"NEXUS_FILE_EVENT_LEDGER_HEAD_V1","sequence":seq,"head_index_line_sha256":head,"event_sha256":digest})+b"\n")
    print(json.dumps({"event_sha256":digest,"sequence":seq,"head_index_line_sha256":head},sort_keys=True))
if __name__=="__main__": main()
