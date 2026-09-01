#!/usr/bin/env python3
"""Verify that each substantive path changed by a Git commit has a matching file event."""
from __future__ import annotations
import argparse, json, subprocess
from pathlib import Path

LEDGER_PREFIX="communication/file-events/"

def changed(commit):
    out=subprocess.check_output(["git","diff-tree","--no-commit-id","--name-status","-r",commit],text=True)
    rows=[]
    for line in out.splitlines():
        p=line.split("\t")
        status=p[0]
        if status.startswith("R") and len(p)>=3: rows.append(("MOVE",p[1],p[2]))
        elif status=="A": rows.append(("CREATE",None,p[1]))
        elif status=="D": rows.append(("DELETE",p[1],None))
        else: rows.append(("MODIFY",p[1],p[1]))
    return [r for r in rows if not ((r[1] or r[2] or "").startswith(LEDGER_PREFIX))]

def events(root,commit):
    found=[]
    for p in (root/"communication/file-events/objects/sha256").glob("*/*/*/event.json") if (root/"communication/file-events/objects/sha256").exists() else []:
        e=json.loads(p.read_text(encoding="utf-8"))
        if e.get("git",{}).get("result_commit")==commit: found.append(e)
    return found

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("commit"); ap.add_argument("--root",default=".")
    a=ap.parse_args(); root=Path(a.root); ev=events(root,a.commit); missing=[]
    for op,before,after in changed(a.commit):
        ok=any(e.get("operation")==op and e.get("before",{}).get("path")==before and e.get("after",{}).get("path")==after for e in ev)
        if not ok: missing.append({"operation":op,"before":before,"after":after})
    if missing:
        print(json.dumps({"commit":a.commit,"status":"FAIL","missing":missing},indent=2)); raise SystemExit(1)
    print(json.dumps({"commit":a.commit,"status":"PASS","events":len(ev)},sort_keys=True))
if __name__=="__main__": main()
