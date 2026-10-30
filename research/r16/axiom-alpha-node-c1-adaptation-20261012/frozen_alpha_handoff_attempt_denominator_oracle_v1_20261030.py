#!/usr/bin/env python3
"""Independent subprocess oracle: invokes candidate CLI only; does not import it."""
import copy
import json
import subprocess
import sys

SHA = "eab11408bf56d3ce1e848fe391e2fe185f7237e0"
BASE = {"schema": "ALPHA_HANDOFF_ATTEMPT_DENOMINATOR_V1", "scope": "SYNTHETIC_ONLY",
        "pinned_main": SHA, "coverage": "INCOMPLETE", "attempts": []}

def row(i, **kw):
    d = {"attempt_id": str(i), "source_ref": "https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/issues/93",
         "source_commit": SHA, "public": True, "routine": True, "authorized": True,
         "accessible": True, "autonomous": True, "handoff_verified": True,
         "published": False, "full_readback": None, "unauthorized_write": False,
         "hidden_source_gap": False, "source_overwrite": False, "claim_promotion": False}
    d.update(kw)
    return d

def call(path, obj, raw=None):
    p = subprocess.run([sys.executable, path], input=raw if raw is not None else json.dumps(obj),
                       text=True, capture_output=True, timeout=5)
    return p.returncode, json.loads(p.stdout)

def main(path):
    tests = []
    def check(name, obj, expected=None, bad=False, raw=None):
        code, out = call(path, obj, raw)
        good = (code != 0 and out.get("state") == "FAIL_CLOSED") if bad else (code == 0 and all(out.get(k) == v for k,v in expected.items()))
        tests.append((name, good))
    a = copy.deepcopy(BASE)
    a["attempts"] = [row(1), row(2, autonomous=False, handoff_verified=False, published=True, full_readback=False),
                     row(3, accessible=False), row(4, routine=None)]
    check("eligible failures stay denominator", a, {"eligible":2,"excluded":1,"unknown":1,"autonomous_verified":1,"sample_autonomous_rate":0.5,"published":1,"complete_readback":0,"sample_readback_rate":0.0,"project_automation_rate":None})
    b=copy.deepcopy(BASE);b["attempts"]=[row(1, unauthorized_write=True)]
    check("nominal success not safety success",b,{"autonomous_verified":1,"safety_qualified_autonomous":0,"observed_violations":1,"project_zero_violation_claim":"NOT_ESTABLISHED"})
    b=copy.deepcopy(BASE);b["attempts"]=[row(1, hidden_source_gap=None)]
    check("unknown safety not safety qualified",b,{"safety_qualified_autonomous":0,"unknown_safety_rows":1})
    b=copy.deepcopy(BASE);b["attempts"]=[row(1, published=True, full_readback=None)]
    check("missing readback counts failure",b,{"published":1,"complete_readback":0,"sample_readback_rate":0.0})
    b=copy.deepcopy(BASE);b["attempts"]=[row(1, accessible=None)]
    check("unknown access excluded from numerator",b,{"eligible":0,"unknown":1,"autonomous_verified":0,"sample_autonomous_rate":None})
    b=copy.deepcopy(BASE);b["attempts"]=[row(1),row(1)]
    check("duplicate attempt fails",b,bad=True)
    b=copy.deepcopy(BASE);b["attempts"]=[row(1, accessible=1)]
    check("integer boolean fails",b,bad=True)
    b=copy.deepcopy(BASE);b["attempts"]=[row(1, source_ref="none")]
    check("missing source ref fails",b,bad=True)
    b=copy.deepcopy(BASE);b["attempts"]=[row(1, source_commit="bad")]
    check("invalid source sha fails",b,bad=True)
    b=copy.deepcopy(BASE);b["attempts"]=[row(1, published=True, full_readback=True)]
    check("complete readback positive",b,{"published":1,"complete_readback":1,"sample_readback_rate":1.0})
    b=copy.deepcopy(BASE);b["attempts"]=[row(1, public=False, autonomous=True)]
    check("ineligible success not numerator",b,{"eligible":0,"excluded":1,"autonomous_verified":0})
    b=copy.deepcopy(BASE);b["coverage"]="DECLARED_COMPLETE_NOT_AUTHENTICATED";b["attempts"]=[row(1)]
    check("coverage assertion not project success",b,{"project_automation_rate":None,"project_full_readback_rate":None})
    check("duplicate JSON keys fail",BASE,bad=True,raw='{"schema":"ALPHA_HANDOFF_ATTEMPT_DENOMINATOR_V1","schema":"ALPHA_HANDOFF_ATTEMPT_DENOMINATOR_V1"}')
    check("NaN fail",BASE,bad=True,raw='{"schema":NaN}')
    check("malformed JSON fail",BASE,bad=True,raw='{"')
    b=copy.deepcopy(BASE);b["attempts"]="bad"
    check("invalid attempt collection fail",b,bad=True)
    for name,ok in tests:
        print(("PASS" if ok else "FAIL")+" "+name)
    print(f"RESULT {sum(x[1] for x in tests)}/{len(tests)}")
    return 0 if all(x[1] for x in tests) else 1

if __name__=="__main__":
    sys.exit(main(sys.argv[1]))
