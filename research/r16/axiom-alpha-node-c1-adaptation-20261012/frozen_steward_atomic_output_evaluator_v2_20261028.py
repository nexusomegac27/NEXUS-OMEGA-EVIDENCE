#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Independent black-box POSIX evaluator: partial write and no-replace output.

No candidate imports; invokes isolated modules in separate Python processes.
The evaluator's assertions are independent of candidate implementation.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import resource
import signal
import subprocess
import sys
import tempfile

BASE_SHA256 = "0640f1c23c236880fed6400319bfacf523442fd103b4f1ebafeeb85daa2dfd74"
PAYLOAD = b"NEXUS_ATOMIC_NEGATIVE_FIXTURE\n" * 4096


def child(module: Path, root: Path, destination: Path, *, size_limit: int | None = None):
    code = ("import importlib.util,sys; from pathlib import Path; "
            "s=importlib.util.spec_from_file_location('guard_under_test',sys.argv[1]); "
            "m=importlib.util.module_from_spec(s); s.loader.exec_module(m); "
            "m.guarded_write(Path(sys.argv[2]),Path(sys.argv[3]), "
            "b'NEXUS_ATOMIC_NEGATIVE_FIXTURE\\n'*4096)")
    def limit():
        if size_limit is not None:
            signal.signal(signal.SIGXFSZ, signal.SIG_IGN)
            resource.setrlimit(resource.RLIMIT_FSIZE, (size_limit, size_limit))
    return subprocess.run([sys.executable,"-c",code,str(module),str(root),str(destination)],
                          capture_output=True, text=True, preexec_fn=limit)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--baseline",required=True,type=Path)
    ap.add_argument("--candidate",type=Path)
    args=ap.parse_args()
    if hashlib.sha256(args.baseline.read_bytes()).hexdigest()!=BASE_SHA256:
        raise SystemExit("FAIL_CLOSED_BASELINE_SHA256")
    tests=[]
    def check(name, condition):
        tests.append({"name":name,"pass":bool(condition)})
    with tempfile.TemporaryDirectory(prefix="nexus-atomic-evaluator-") as d:
        tmp=Path(d); root=tmp/"checkout";root.mkdir();out=tmp/"external";out.mkdir()
        partial=out/"baseline-partial.jsonl"
        old=child(args.baseline,root,partial,size_limit=4096)
        check("baseline_fails_under_file_size_limit",old.returncode!=0)
        check("baseline_exposes_partial_final_file",partial.exists() and 0<partial.stat().st_size<len(PAYLOAD))
        good=out/"baseline-positive.jsonl"
        check("baseline_positive_control",child(args.baseline,root,good).returncode==0 and good.read_bytes()==PAYLOAD)
        if args.candidate:
            new=out/"atomic-failure.jsonl"
            failed=child(args.candidate,root,new,size_limit=4096)
            check("candidate_fails_under_file_size_limit",failed.returncode!=0)
            check("candidate_never_exposes_partial_final_file",not new.exists())
            check("candidate_removes_failed_temp",not list(out.glob(".nexus-alpha-atomic-*.tmp")))
            success=out/"atomic-success.jsonl"
            check("candidate_positive_control",child(args.candidate,root,success).returncode==0 and success.read_bytes()==PAYLOAD)
            old_bytes=b"DO_NOT_REPLACE\n";existing=out/"existing.jsonl";existing.write_bytes(old_bytes)
            check("candidate_refuses_existing_file",child(args.candidate,root,existing).returncode!=0 and existing.read_bytes()==old_bytes)
            protected=root/"README.md";protected.write_bytes(old_bytes)
            check("candidate_refuses_checkout_output",child(args.candidate,root,protected).returncode!=0 and protected.read_bytes()==old_bytes)
            linked=tmp/"linked";linked.symlink_to(out,target_is_directory=True)
            check("candidate_refuses_symlink_parent",child(args.candidate,root,linked/"alias.jsonl").returncode!=0 and not (out/"alias.jsonl").exists())
            leaf=out/"leaf.jsonl";leaf.symlink_to(protected)
            check("candidate_refuses_symlink_leaf",child(args.candidate,root,leaf).returncode!=0 and protected.read_bytes()==old_bytes)
            check("candidate_refuses_relative_path",child(args.candidate,root,Path("relative.jsonl")).returncode!=0)
            check("candidate_refuses_traversal",child(args.candidate,root,out/".."/"traversal.jsonl").returncode!=0 and not (tmp/"traversal.jsonl").exists())
            check("candidate_no_orphan_temp_after_success",not list(out.glob(".nexus-alpha-atomic-*.tmp")))
    result={"baseline_sha256":BASE_SHA256,"candidate_executed":bool(args.candidate),"passed":sum(t["pass"] for t in tests),"total":len(tests),"tests":tests}
    print(json.dumps(result,sort_keys=True))
    return 0 if all(t["pass"] for t in tests) else 1


if __name__=="__main__":
    raise SystemExit(main())
