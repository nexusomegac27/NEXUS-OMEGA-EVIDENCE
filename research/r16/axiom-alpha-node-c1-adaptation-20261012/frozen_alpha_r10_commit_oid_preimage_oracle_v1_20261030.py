#!/usr/bin/env python3
"""Frozen external black-box evaluator: git hash-object independent of candidate hashlib.

This tests a bounded SHA-1 preimage search, not independent GitHub/API authentication.
"""
import copy
import json
import subprocess
import sys
import tempfile
from pathlib import Path

PIN = "dab7c59070d67e7e2a244bd6d05db9a4d37460e3"

def git_object_hash(obj, tz):
    from datetime import datetime, timezone
    def line(who):
        d = obj[who]
        ts = int(datetime.fromisoformat(d["date"].replace("Z", "+00:00")).timestamp())
        return f'{who} {d["name"]} <{d["email"]}> {ts} {tz}'
    data = (f'tree {obj["tree_sha"]}\nparent {obj["parents"][0]}\n'+line('author')+'\n'+line('committer')+'\n\n'+obj['message']).encode()
    proc = subprocess.run(["git", "hash-object", "-t", "commit", "--stdin"], input=data, capture_output=True, timeout=5)
    if proc.returncode:
        raise AssertionError(proc.stderr.decode())
    return proc.stdout.decode().strip(), len(data)

def run(gate, obj, raw=None, pin=PIN):
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "case.json"
        p.write_bytes(raw if raw is not None else (json.dumps(obj, ensure_ascii=False)+"\n").encode())
        proc = subprocess.run([sys.executable,"-S",str(gate),str(p),"--commit",pin],capture_output=True,text=True,timeout=10)
        try: result = json.loads(proc.stdout)
        except Exception: raise AssertionError("invalid output: "+proc.stdout+proc.stderr)
        return proc.returncode,result

def main():
    gate, fixture = Path(sys.argv[1]), Path(sys.argv[2])
    original = json.loads(fixture.read_text(encoding="utf-8"))
    assert original["commit_sha"] == PIN
    independent, byte_count = git_object_hash(original, "+0200")
    assert independent == PIN and byte_count == 304, (independent,byte_count)
    wrong, _ = git_object_hash(original, "+0000")
    assert wrong != PIN
    cases = [("real_r10_git_hash_object_positive",original,True,None,PIN)]
    def negative(name, mutation):
        x=copy.deepcopy(original);mutation(x);cases.append((name,x,False,None,PIN))
    negative("changed_tree_sha",lambda x:x.update(tree_sha="0"*40))
    negative("changed_parent_sha",lambda x:x["parents"].__setitem__(0,"0"*40))
    negative("changed_message_same_length",lambda x:x.update(message=x["message"][:-1]+"X"))
    negative("changed_author_name",lambda x:x["author"].update(name="FAKE"))
    negative("changed_author_email",lambda x:x["author"].update(email="fake@example.org"))
    negative("changed_committer_name",lambda x:x["committer"].update(name="FAKE"))
    negative("changed_author_time",lambda x:x["author"].update(date="2026-10-16T07:17:32Z"))
    negative("changed_committer_time",lambda x:x["committer"].update(date="2026-10-16T07:17:32Z"))
    negative("added_parent",lambda x:x["parents"].append("1"*40))
    negative("forged_actor_authenticated",lambda x:x.update(actor_authenticated=True))
    negative("forged_receiver_ack",lambda x:x.update(independent_receiver_ack=True))
    negative("claimed_signed",lambda x:x.update(api_signature_state="verified"))
    negative("wrong_commit_in_projection",lambda x:x.update(commit_sha="0"*40))
    cases.append(("wrong_external_pin",original,False,None,"0"*40))
    cases.append(("duplicate_json_keys",original,False,b'{"commit_sha":"x","commit_sha":"y"}',PIN))
    cases.append(("nonfinite_json",original,False,b'{"commit_sha":NaN}',PIN))
    cases.append(("malformed_json",original,False,b'{"bad":',PIN))
    passed=0
    for name,obj,positive,raw,pin in cases:
        rc,result=run(gate,obj,raw,pin)
        ok=(rc==0 and result.get("status")=="API_COMMIT_SHA1_PREIMAGE_MATCH_NOT_AUTHENTICATED" and result.get("matching_timezone_hypothesis")=="+0200" and result.get("reconstructed_commit_payload_bytes")==304 and result.get("original_raw_commit_bytes_obtained") is False and result.get("independent_receiver_ack") is False and result.get("actor_authenticated") is False) if positive else (rc!=0 and result.get("status")=="FAIL_CLOSED")
        print(("PASS" if ok else "FAIL")+" "+name)
        if not ok: raise AssertionError((name,rc,result))
        passed+=1
    print(f"FROZEN_ORACLE_PASS={passed}/{len(cases)}; NEGATIVE_FAIL_CLOSED={passed-1}/{len(cases)-1}; GIT_CLI_INDEPENDENT_HASH={independent}")

if __name__ == "__main__": main()
