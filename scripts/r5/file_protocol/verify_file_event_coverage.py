#!/usr/bin/env python3
"""Verify every substantive path in a Git commit has an exact raw-byte File Event."""
from __future__ import annotations
import argparse, hashlib, json, subprocess
from pathlib import Path

LEDGER_PREFIX="communication/file-events/"

def git(*args, binary=False):
    return subprocess.check_output(["git",*args], text=not binary)

def blob(ref,path):
    try: return git("show",f"{ref}:{path}",binary=True)
    except subprocess.CalledProcessError: return None

def state(ref,path):
    if path is None: return {"exists":False,"path":None,"bytes":None,"sha256":None}
    b=blob(ref,path)
    if b is None: return {"exists":False,"path":path,"bytes":None,"sha256":None}
    return {"exists":True,"path":path,"bytes":len(b),"sha256":hashlib.sha256(b).hexdigest()}

def changed(commit):
    out=git("diff-tree","--no-commit-id","--name-status","-r","-M",commit)
    rows=[]
    for line in out.splitlines():
        p=line.split("\t"); status=p[0]
        if status.startswith("R") and len(p)>=3: rows.append(("MOVE",p[1],p[2]))
        elif status=="A": rows.append(("CREATE",None,p[1]))
        elif status=="D": rows.append(("DELETE",p[1],None))
        else: rows.append(("MODIFY",p[1],p[1]))
    return [r for r in rows if not ((r[1] or r[2] or "").startswith(LEDGER_PREFIX))]

def events(root,commit):
    base=root/"communication/file-events/objects/sha256"
    paths=base.glob("*/*/*/event.json") if base.exists() else []
    found=[]
    for p in paths:
        e=json.loads(p.read_text(encoding="utf-8"))
        if e.get("git",{}).get("result_commit")==commit: found.append(e)
    return found

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("commit"); ap.add_argument("--root",default=".")
    a=ap.parse_args(); root=Path(a.root); ev=events(root,a.commit); parent=git("rev-parse",f"{a.commit}^").strip(); missing=[]
    for op,before_path,after_path in changed(a.commit):
        expected_before=state(parent,before_path); expected_after=state(a.commit,after_path)
        match=None
        for e in ev:
            if e.get("operation")==op and e.get("before")==expected_before and e.get("after")==expected_after:
                match=e; break
        if match is None:
            missing.append({"operation":op,"before":expected_before,"after":expected_after})
    if missing:
        print(json.dumps({"commit":a.commit,"status":"FAIL","missing":missing},indent=2,sort_keys=True)); raise SystemExit(1)
    print(json.dumps({"commit":a.commit,"status":"PASS","covered_paths":len(changed(a.commit)),"matching_events":len(ev)},sort_keys=True))
if __name__=="__main__": main()
