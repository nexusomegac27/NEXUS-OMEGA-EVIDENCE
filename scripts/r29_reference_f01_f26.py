#!/usr/bin/env python3
"""R29R1 local offline *reference policy* fixtures F01..F26.
No phone, network, target sandbox, user data, or real agent code is accessed.
NOT a qualification of NEXUS runtime, Android, egress enforcement, or real device evidence.
"""
from __future__ import annotations
import hashlib, json, math, re, sys, time
import numpy as np

C1="C1_DESCRIPTIVE_ONLY"
KNOWN_COMMIT="21b6fd71bc34034badce24b83476678835f43e86"
SOURCE=b"synthetic-source-material"
H=hashlib.sha256(SOURCE).hexdigest()

def strict_json(s):
    def reject_duplicate(pairs):
        out={}
        for k,v in pairs:
            if k in out: raise ValueError("DUPLICATE_KEY")
            out[k]=v
        return out
    def reject_nonfinite(s): raise ValueError("NONFINITE")
    return json.loads(s,object_pairs_hook=reject_duplicate,parse_constant=reject_nonfinite)

def array_rank(x,tol=1e-10):
    import numpy.linalg as la
    return int(la.matrix_rank(np.asarray(x,dtype=float),tol))

def affine_test():
    g=9.81
    x=np.array([[g,0,0],[-g,0,0],[0,g,0],[0,-g,0],[0,0,g],[0,0,-g]],float)
    d=np.c_[np.ones((6,)),x]
    m=np.array([[1.03,.01,-.005],[.02,.99,.008],[-.01,.004,1.01]])
    b=np.array([.2,-.1,.03])
    y=x @ m.T + b
    estimate=np.linalg.lstsq(d,y,rcond=None)[0]
    expected=np.vstack([b,m.T])
    return {"rank_inputs":array_rank(x),"rank_affine":array_rank(d),
            "rank_total":3*array_rank(d),
            "max_err":float(np.max(abs(estimate-expected))),
            "max_residual":float(np.max(abs(d @ estimate - y)))}

def permitted(r):
    kind=r["kind"]
    if kind=="source":
        return r.get("source") is not None and hashlib.sha256(r["source"]).hexdigest()==r["sha256"]
    if kind=="json": 
        try: strict_json(r["value"]); return True
        except (ValueError, json.JSONDecodeError): return False
    if kind=="ci": return r.get("head")==KNOWN_COMMIT and bool(r.get("checks")) and all(c["head"]==KNOWN_COMMIT and c["conclusion"]=="success" for c in r["checks"])
    if kind=="independence": return r.get("claimed_families")==len({x["base_model"] for x in r["reports"]}) and r.get("claimed_families")==len({x["provider"] for x in r["reports"]})
    if kind=="sensor": return bool(r.get("device") and r.get("host") and r.get("consent"))
    if kind=="rank": return r.get("claimed_total_rank")==affine_test()["rank_total"]
    if kind=="known_rank_positive": 
        a=affine_test()
        return a["rank_inputs"]==3 and a["rank_affine"]==4 and a["rank_total"]==12 and a["max_err"]<1e-10 and a["max_residual"]<1e-10
    if kind=="physical_calibration": return r.get("orientation_reference")=="TRACEABLE_KNOWN" and r.get("orientation_uncertainty_documented") is True
    if kind=="metrology": return r.get("traceable_ref") is True and r.get("uncertainty_budget") is not None
    if kind=="object": return r.get("end_marker")==True and r.get("expected_len")==len(r["data"]) and hashlib.sha256(r["data"]).hexdigest()==r.get("hash")
    if kind=="commit": return r.get("consent_active_at_commit") is True
    if kind=="time": return r["start"]["boot_id"]==r["end"]["boot_id"] and r["end"]["monotonic_ns"]>=r["start"]["monotonic_ns"]
    if kind=="live_source": return r.get("retrieval_class")=="LIVE_OBSERVED" and r.get("live_timestamp") is not None
    if kind=="privacy": return not any(k in r.get("public_fields",[]) for k in ("private_raw_sensor","device_serial","api_secret"))
    if kind=="instructions": return r.get("instruction_origin")=="TRUSTED_OPERATOR" and r.get("source_data_may_command") is False
    if kind=="actor": return r.get("actor") in r.get("allowlist",[]) and r.get("actor") is not None
    if kind=="path": return r.get("path","").startswith("research/r27/sandbox-science-library-20261111/") and ".." not in r["path"].split("/") and r.get("operator_owns_edit") is True
    if kind=="reset": return r.get("history_delete") is False and r.get("node_restart") is False
    if kind=="manifest": return "self_sha256" not in r.get("manifest",{}) and r.get("detached_sha256") is not None
    if kind=="empirical": return r.get("real_measurements") is True and bool(r.get("reference"))
    if kind=="ack": return r.get("signed_by")=="INDEPENDENT_RECEIVER" and r.get("producer")!=r.get("signed_by")
    if kind=="private_source": return r.get("accessible") is True and r.get("byte_verified") is True
    if kind=="holdout": return r.get("threshold_selected_with_holdout") is False and r.get("fit_used_holdout") is False
    if kind=="prereg": return r.get("threshold_locked_before_observation") is True and r.get("lock_receipt") is not None
    if kind=="capture": return bool(r.get("device") and r.get("host") and r.get("consent") and r.get("bounded_session"))
    raise KeyError(kind)

fixture_set=[
 ("F01","SOURCE_HASH_MISMATCH",False,{"kind":"source","source":SOURCE,"sha256":"0"*64}),
 ("F02","STRICT_JSON_REJECT",False,{"kind":"json","value":'{"x":1,"x":2,"rate":NaN}'}),
 ("F03","WRONG_COMMIT_CI",False,{"kind":"ci","head":KNOWN_COMMIT,"checks":[{"head":"f"*40,"conclusion":"success"}]}),
 ("F04","COMMON_BASE_MODEL",False,{"kind":"independence","claimed_families":2,"reports":[{"base_model":"GLM","provider":"ZAI"},{"base_model":"GLM","provider":"ZAI"}]}),
 ("F05","MULTIPLE_LANES_SAME_PROVIDER",False,{"kind":"independence","claimed_families":5,"reports":[{"base_model":"M","provider":"P"}]*5}),
 ("F06","FAKE_DEVICE_RECEIPT",False,{"kind":"sensor","device":None,"host":None,"consent":None}),
 ("F07","FALSE_AFFINE_RANK_CLAIM",False,{"kind":"rank","claimed_total_rank":3}),
 ("F08","POSITIVE_KNOWN_INPUT_RANK_RECOVERY",True,{"kind":"known_rank_positive"}),
 ("F09","MANUAL_ORIENTATION_ASSUMED_EXACT",False,{"kind":"physical_calibration","orientation_reference":"NOMINAL_USER_FACE","orientation_uncertainty_documented":False}),
 ("F10","METROLOGY_REFERENCE_MISSING",False,{"kind":"metrology","traceable_ref":False,"uncertainty_budget":None}),
 ("F11","TRUNCATED_OBJECT",False,{"kind":"object","data":b"abc","expected_len":4,"end_marker":False,"hash":hashlib.sha256(b"abc").hexdigest()}),
 ("F12","REVOKED_CONSENT_AT_COMMIT",False,{"kind":"commit","consent_active_at_commit":False}),
 ("F13","REBOOT_CLOCK_DOMAIN",False,{"kind":"time","start":{"boot_id":"boot-a","monotonic_ns":123},"end":{"boot_id":"boot-b","monotonic_ns":456}}),
 ("F14","ARCHIVE_CLAIMED_LIVE",False,{"kind":"live_source","retrieval_class":"ARCHIVE_SNAPSHOT","live_timestamp":None}),
 ("F15","PUBLIC_PRIVATE_FIELD_LEAK",False,{"kind":"privacy","public_fields":["public_order","device_serial"]}),
 ("F16","UNTRUSTED_SOURCE_INSTRUCTIONS",False,{"kind":"instructions","instruction_origin":"EXTERNAL_PAGE","source_data_may_command":True}),
 ("F17","UNREGISTERED_EXTERNAL_ACTOR",False,{"kind":"actor","actor":"unknown-researcher","allowlist":[]}),
 ("F18","EXTERNAL_ROOT_STRUCTURE_WRITE",False,{"kind":"path","path":"other/new-root/fixture.json","operator_owns_edit":False}),
 ("F19","DESTRUCTIVE_DRIFT_RESET",False,{"kind":"reset","history_delete":True,"node_restart":True}),
 ("F20","MANIFEST_SELF_HASH_CYCLE",False,{"kind":"manifest","manifest":{"self_sha256":"aa"},"detached_sha256":None}),
 ("F21","EMPIRICAL_GAIN_WITHOUT_MEASUREMENTS",False,{"kind":"empirical","real_measurements":False,"reference":None}),
 ("F22","PRODUCER_SELF_ACK",False,{"kind":"ack","producer":"CURSOR","signed_by":"CURSOR"}),
 ("F23","INACCESSIBLE_PRIVATE_SOURCE",False,{"kind":"private_source","accessible":False,"byte_verified":False}),
 ("F24","HOLDOUT_LEAKAGE",False,{"kind":"holdout","threshold_selected_with_holdout":True,"fit_used_holdout":True}),
 ("F25","POSTHOC_PREREG",False,{"kind":"prereg","threshold_locked_before_observation":False,"lock_receipt":None}),
 ("F26","UNAUTHORIZED_SENSOR_CAPTURE",False,{"kind":"capture","device":None,"host":None,"consent":None,"bounded_session":False}),
]
def positive_twin(fid, original):
    """Non-device synthetic positive comparator to detect degenerate ALL_REJECT rules.
    These are STRUCTURE controls; they do not attest physical source/consent.
    """
    twins={
        "F01":{"kind":"source","source":SOURCE,"sha256":H},
        "F02":{"kind":"json","value":'{"x":1,"rate":1.0}'},
        "F03":{"kind":"ci","head":KNOWN_COMMIT,"checks":[{"head":KNOWN_COMMIT,"conclusion":"success"}]},
        "F04":{"kind":"independence","claimed_families":2,"reports":[{"base_model":"Model_A","provider":"Provider_A"},{"base_model":"Model_B","provider":"Provider_B"}]},
        "F05":{"kind":"independence","claimed_families":5,"reports":[{"base_model":f"Base{i}","provider":f"Provider{i}"} for i in range(5)]},
        "F06":{"kind":"sensor","device":"SYNTH_DEVICE_RECEIPT","host":"SYNTH_HOST_RECEIPT","consent":"SYNTH_CONSENT_RECEIPT"},
        "F07":{"kind":"rank","claimed_total_rank":12},
        "F09":{"kind":"physical_calibration","orientation_reference":"TRACEABLE_KNOWN","orientation_uncertainty_documented":True},
        "F10":{"kind":"metrology","traceable_ref":True,"uncertainty_budget":{"unit":"m/s2","u":.01}},
        "F11":{"kind":"object","data":b"abc","expected_len":3,"end_marker":True,"hash":hashlib.sha256(b"abc").hexdigest()},
        "F12":{"kind":"commit","consent_active_at_commit":True},
        "F13":{"kind":"time","start":{"boot_id":"boot-a","monotonic_ns":123},"end":{"boot_id":"boot-a","monotonic_ns":456}},
        "F14":{"kind":"live_source","retrieval_class":"LIVE_OBSERVED","live_timestamp":"SYNTHETIC_TIME"},
        "F15":{"kind":"privacy","public_fields":["public_order","source_digest"]},
        "F16":{"kind":"instructions","instruction_origin":"TRUSTED_OPERATOR","source_data_may_command":False},
        "F17":{"kind":"actor","actor":"TEST_OPERATOR","allowlist":["TEST_OPERATOR"]},
        "F18":{"kind":"path","path":"research/r27/sandbox-science-library-20261111/orders/valid.md","operator_owns_edit":True},
        "F19":{"kind":"reset","history_delete":False,"node_restart":False},
        "F20":{"kind":"manifest","manifest":{"files":[]},"detached_sha256":"SYNTH_SHA"},
        "F21":{"kind":"empirical","real_measurements":True,"reference":"SYNTHETIC_REFERENCE_MARKER"},
        "F22":{"kind":"ack","producer":"CURSOR","signed_by":"INDEPENDENT_RECEIVER"},
        "F23":{"kind":"private_source","accessible":True,"byte_verified":True},
        "F24":{"kind":"holdout","threshold_selected_with_holdout":False,"fit_used_holdout":False},
        "F25":{"kind":"prereg","threshold_locked_before_observation":True,"lock_receipt":"SYNTH_LOCK"},
        "F26":{"kind":"capture","device":"SYNTH_DEVICE","host":"SYNTH_HOST","consent":"SYNTH_CONSENT","bounded_session":"SYNTH_BOUNDED"},
    }
    return twins.get(fid)

def run():
    rows=[]
    for fid,label,expected,fixture in fixture_set:
        actual=bool(permitted(fixture))
        fixture_serialized=json.dumps(fixture,sort_keys=True,default=lambda x:x.hex() if isinstance(x,bytes) else str(x),allow_nan=False)
        rows.append({"id":fid,"label":label,"oracle_accept":expected,"actual_accept":actual,
                     "outcome":"PASS_EXPECTED" if actual==expected else "FAIL_UNEXPECTED",
                     "evidence_class":"EXECUTED_SYNTHETIC_OFFLINE_REFERENCE_ONLY",
                     "fixture_sha256":hashlib.sha256(fixture_serialized.encode()).hexdigest(),
                     "no_real_device":True})
    twins=[]
    for fid,label,expected,fixture in fixture_set:
        if expected is True:
            continue
        good=positive_twin(fid,fixture)
        if good is None:
            raise RuntimeError(f"missing positive twin {fid}")
        actual=bool(permitted(good))
        twins.append({"id":fid+"_positive_twin", "expected_accept":True,
                      "actual_accept":actual,
                      "outcome":"PASS_EXPECTED" if actual else "FAIL_UNEXPECTED",
                      "evidence_class":"EXECUTED_SYNTHETIC_OFFLINE_REFERENCE_ONLY"})
    result={"object":"NEXUS_OMEGA_R29R1_AXIOM_MINIMAL_GATE_REFERENCE_F01_F26_EXECUTION_20261112_R0",
            "claim_ceiling":C1,
            "execution_environment":"AXIOM_LOCAL_OFFLINE_PYTHON_REFERENCE_NOT_NEXUS_SANDBOX_RUNTIME",
            "numpy_version":np.__version__,
            "tests":rows,
            "positive_twins":twins,
            "positive_twin_pass":sum(x["outcome"]=="PASS_EXPECTED" for x in twins),
            "positive_twin_expected":len(twins),
            "expected_count":len(fixture_set),
            "pass_count":sum(x["outcome"]=="PASS_EXPECTED" for x in rows),
            "source_hash":hashlib.sha256(open(__file__,"rb").read()).hexdigest(),
            "device_captured":False,
            "sandbox_runtime_validated":False}
    return result
if __name__=="__main__":
    result=run()
    print(json.dumps(result,ensure_ascii=False,indent=2))
    sys.exit(0 if result["pass_count"]==result["expected_count"]==26 and result["positive_twin_pass"]==result["positive_twin_expected"]==25 else 1)
