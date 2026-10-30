#!/usr/bin/env python3
"""Independent frozen subprocess oracle for alpha_issue93_full_comment_census_v1.

Oracle is authored and versioned before the candidate. It does not import candidate code.
"""
import copy
import json
import subprocess
import sys

SOURCE = "nexusomegac27/NEXUS-OMEGA-EVIDENCE/issues/93"

def base():
    return {"schema_version":"alpha_issue93_comment_census_v1", "source":SOURCE,
            "declared_count":3, "page_sizes":[3], "comments":[
                {"id":100,"author":"nexusomegac27","created_at":"2026-10-30T01:00:00Z","updated_at":"2026-10-30T01:00:00Z","predecessor_id":None},
                {"id":101,"author":"nexusomegac27","created_at":"2026-10-30T02:00:00Z","updated_at":"2026-10-30T02:00:00Z","predecessor_id":100},
                {"id":102,"author":"nexusomegac27","created_at":"2026-10-30T03:00:00Z","updated_at":"2026-10-30T03:00:00Z","predecessor_id":101}]}

def run(candidate, fixture):
    payload = fixture if isinstance(fixture, str) else json.dumps(fixture)
    p = subprocess.run([sys.executable, candidate], input=payload, text=True, capture_output=True, timeout=10)
    try: output=json.loads(p.stdout)
    except ValueError: raise AssertionError("candidate did not return JSON: " + p.stdout[:300])
    return p.returncode, output

def main(candidate):
    tests = []
    good=base()
    tests.append(("positive", good, True, None))
    for name, mutate, err in [
        ("omitted_row", lambda x:x["comments"].pop(),"POPULATION_INCOMPLETE"),
        ("wrong_declared_count", lambda x:x.update(declared_count=4),"PAGE_COUNT_MISMATCH"),
        ("wrong_page_size", lambda x:x.update(page_sizes=[2]),"PAGE_COUNT_MISMATCH"),
        ("duplicate_id", lambda x:x["comments"][2].update(id=101),"DUPLICATE_OR_UNSORTED_ID"),
        ("foreign_actor", lambda x:x["comments"][1].update(author="unregistered"),"UNREGISTERED_ACTOR"),
        ("edited_comment", lambda x:x["comments"][1].update(updated_at="2026-10-30T02:01:00Z"),"EDITED_COMMENT_METADATA"),
        ("broken_predecessor", lambda x:x["comments"][2].update(predecessor_id=100),"BROKEN_PREDECESSOR"),
        ("future_predecessor", lambda x:x["comments"][1].update(predecessor_id=102),"BROKEN_PREDECESSOR"),
        ("wrong_source", lambda x:x.update(source="other/repo/issues/93"),"SOURCE_MISMATCH"),
        ("bad_time", lambda x:x["comments"][1].update(created_at="yesterday"),"BAD_TIMESTAMP"),
        ("time_reversal", lambda x:x["comments"][1].update(created_at="2026-10-29T02:00:00Z",updated_at="2026-10-29T02:00:00Z"),"UNSORTED_TIME"),
        ("boolean_id", lambda x:x["comments"][1].update(id=True),"BAD_COMMENT_ID"),
    ]:
        f=copy.deepcopy(good);mutate(f);tests.append((name,f,False,err))
    tests.append(("duplicate_json_key",'{"schema_version":"alpha_issue93_comment_census_v1","source":"'+SOURCE+'","source":"other"}',False,"DUPLICATE_JSON_KEY"))
    tests.append(("malformed_json",'{not-json}',False,None))
    passed=0
    for name,fixture,should_pass,error in tests:
        rc,out=run(candidate,fixture)
        ok=(rc==0 and out.get("status")=="PASS_METADATA_CENSUS") if should_pass else (rc!=0 and out.get("status")=="FAIL_CLOSED" and (error is None or out.get("error")==error))
        print(name, "PASS" if ok else "FAIL", out)
        passed+=int(ok)
    print(f"RESULT={passed}/{len(tests)}")
    return 0 if passed==len(tests) else 1

if __name__ == "__main__":
    if len(sys.argv)!=2: raise SystemExit("usage: frozen_oracle.py candidate.py")
    raise SystemExit(main(sys.argv[1]))
