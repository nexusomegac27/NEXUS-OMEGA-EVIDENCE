#!/usr/bin/env python3
"""Offline BYTE-ONLY validator for AXIOM expert manifest candidates.
Identity/PR authority/science are NOT proven by this tool. No network and no writes.
"""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath

MAX_TOTAL = 1048576
MAX_FILE = 262144
REQUIRED = {"schema_version","object","recipient","order_object","order_sha256","order_bytes","repo",
            "transport_class","sender_role","github_actor","predecessor","claim_ceiling",
            "runtime","receiver_ack","children"}
KEYS = {"path","bytes","sha256","git_blob_sha1"}
ROLES = {"GROK","PERPLEXITY","MISTRAL_VIBE","QWEN","GEMINI","MANUS","DEEPSEEK"}
HEX = set("0123456789abcdef")
def strict_pairs(pairs):
    out={}
    for k,v in pairs:
        if k in out: raise ValueError("DUPLICATE_JSON_KEY:"+k)
        out[k]=v
    return out
def hexstr(v,n):
    return isinstance(v,str) and len(v)==n and all(c in HEX for c in v)
def clean_path(path):
    if not isinstance(path,str) or not path or "\\" in path or "\x00" in path: raise ValueError("UNSAFE_PATH")
    p=PurePosixPath(path)
    if p.is_absolute() or any(x in (".","..","") for x in path.split("/")) or ":" in path: raise ValueError("UNSAFE_PATH")
    if str(p)!=path: raise ValueError("NONCANONICAL_PATH")
    return p
def verify(manifest_bytes,root,approved_prefix,expected_order_sha):
    if len(manifest_bytes)>MAX_FILE: raise ValueError("MANIFEST_OVERSIZE")
    m=json.loads(manifest_bytes.decode("utf-8"),object_pairs_hook=strict_pairs)
    if set(m)-REQUIRED-{"pr_url","commit_sha"}: raise ValueError("UNDECLARED_MANIFEST_KEYS")
    if not REQUIRED.issubset(m): raise ValueError("REQUIRED_FIELD_MISSING")
    if m["schema_version"]!="1.0.0" or m["repo"]!="nexusomegac27/NEXUS-OMEGA-EVIDENCE": raise ValueError("SCHEMA_OR_REPO")
    if m["recipient"]!="NEXUS_OPERATOR_AXIOM" or m["claim_ceiling"]!="C1_DESCRIPTIVE_ONLY": raise ValueError("INVALID_RECEIVER_OR_CLAIM")
    if m["runtime"]!="NOT_AUTHORIZED" or m["receiver_ack"]!="PENDING_AXIOM_INDEPENDENT_REHASH": raise ValueError("FORGED_RUNTIME_OR_ACK")
    if m["sender_role"] not in ROLES: raise ValueError("UNKNOWN_ROLE")
    if m["transport_class"] not in ("REGISTERED_ACTOR_PR","OPERATOR_TO_AXIOM_BRIDGE"): raise ValueError("TRANSPORT_CLASS")
    if not hexstr(m["order_sha256"],64) or m["order_sha256"]!=expected_order_sha: raise ValueError("ORDER_BIND_MISMATCH")
    if type(m["order_bytes"]) is not int or m["order_bytes"]<=0: raise ValueError("INVALID_ORDER_SIZE")
    if "commit_sha" in m and m["commit_sha"]!="NOT_ESTABLISHED" and not hexstr(m["commit_sha"],40): raise ValueError("INVALID_COMMIT")
    if not isinstance(m["children"],list) or not 1<=len(m["children"])<=6: raise ValueError("INVALID_CHILD_COUNT")
    if not isinstance(m["github_actor"],str) or not m["github_actor"]: raise ValueError("GITHUB_ACTOR_UNDECLARED")
    prefix=clean_path(approved_prefix)
    root=Path(root).resolve(strict=True)
    seen=set()
    total=len(manifest_bytes)
    for child in m["children"]:
        if not isinstance(child,dict) or set(child)!=KEYS: raise ValueError("CHILD_SCHEMA")
        path=clean_path(child["path"])
        if path==prefix or prefix not in path.parents: raise ValueError("UNAPPROVED_SLOT_PATH")
        if child["path"] in seen: raise ValueError("DUPLICATE_CHILD_PATH")
        seen.add(child["path"])
        n=child["bytes"]
        if type(n) is not int or not 1<=n<=MAX_FILE: raise ValueError("INVALID_CHILD_SIZE")
        if not hexstr(child["sha256"],64) or not hexstr(child["git_blob_sha1"],40): raise ValueError("INVALID_CHILD_HASH")
        target=root.joinpath(*path.parts)
        # Reject symlinks at all segments, not only final. resolve() may otherwise escape.
        curr=root
        for part in path.parts:
            curr=curr/part
            if curr.is_symlink(): raise ValueError("SYMLINK_PATH")
        resolved=target.resolve(strict=True)
        if root not in resolved.parents: raise ValueError("ESCAPED_ROOT")
        b=resolved.read_bytes()
        if len(b)!=n or hashlib.sha256(b).hexdigest()!=child["sha256"]: raise ValueError("BYTES_SHA256_MISMATCH:"+child["path"])
        blob=hashlib.sha1(b"blob "+str(len(b)).encode("ascii")+bytes([0])+b).hexdigest()
        if blob!=child["git_blob_sha1"]: raise ValueError("GIT_BLOB_MISMATCH:"+child["path"])
        total+=n
        if total>MAX_TOTAL: raise ValueError("PACKAGE_TOO_LARGE")
    # Important: this result never asserts GitHub actor/PR trust or independent scientific validity.
    return {"result":"BYTE_MATCH_ONLY","verified_children":len(seen),
            "manifest_bytes":len(manifest_bytes),"manifest_sha256":hashlib.sha256(manifest_bytes).hexdigest(),
            "actor_auth":"NOT_ESTABLISHED_OFFLINE","science":"NOT_ADJUDICATED",
            "receiver_ack":"PENDING_AXIOM_INDEPENDENT_REHASH"}
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--manifest",required=True,type=Path)
    p.add_argument("--root",required=True,type=Path)
    p.add_argument("--approved-prefix",required=True)
    p.add_argument("--expected-order-sha256",required=True)
    a=p.parse_args()
    print(json.dumps(verify(a.manifest.read_bytes(),a.root,a.approved_prefix,a.expected_order_sha256),sort_keys=True))
if __name__=="__main__": main()
