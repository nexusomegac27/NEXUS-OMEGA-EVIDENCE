#!/usr/bin/env python3
"""Build a deterministic, non-scoring NEXUS OMEGA R6 scientific livecount."""
from __future__ import annotations
import argparse, hashlib, json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DIMS = [
    "CLAIM_BOUNDARY","PROVENANCE","UNCERTAINTY","DISSENT_PRESERVATION",
    "SOURCE_INDEPENDENCE","TEMPORAL_DRIFT","AUTHORITY_SEPARATION",
    "TOOL_BOUNDARY","MEMORY_CONSISTENCY","ADVERSARIAL_RESILIENCE",
]

def canonical_bytes(obj):
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")

def sha(obj):
    return hashlib.sha256(canonical_bytes(obj)).hexdigest()

def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))

def dependency_clusters(obs):
    # Conservative lower-bound clustering: observations sharing provider, model family,
    # source set, or toolchain are connected. Components are quasi-independent clusters,
    # not truth votes and not a substitute for ICC/HiBayES when repeated data exist.
    n=len(obs)
    adj=[set() for _ in range(n)]
    keys=("provider","model_family","source_set_hash","toolchain")
    for i in range(n):
        for j in range(i+1,n):
            a,b=obs[i].get("independence",{}),obs[j].get("independence",{})
            if any(a.get(k) and a.get(k)==b.get(k) for k in keys):
                adj[i].add(j); adj[j].add(i)
    seen=set(); comps=[]
    for i in range(n):
        if i in seen: continue
        stack=[i]; seen.add(i); comp=[]
        while stack:
            x=stack.pop(); comp.append(x)
            for y in adj[x]:
                if y not in seen: seen.add(y); stack.append(y)
        comps.append(comp)
    return comps

def build(generated_at=None):
    sources=load_json(ROOT/"sources.json")
    observations=[]
    for p in sorted((ROOT/"observations").glob("*.json")):
        if p.name.startswith("_"): continue
        observations.append(load_json(p))
    clusters=dependency_clusters(observations) if observations else []
    raw_n=len(observations)
    cluster_lower_bound=len(clusters) if observations else 0
    distributions={d:{"PASS":0,"CAVEAT":0,"FAIL":0,"NOT_TESTED":0} for d in DIMS}
    for o in observations:
        sv=o.get("stability_vector",{})
        for d in DIMS:
            v=sv.get(d,"NOT_TESTED")
            if v not in distributions[d]: v="NOT_TESTED"
            distributions[d][v]+=1
    source_manifest_hash=sha(sources)
    payload={
      "phase":"R6",
      "phase_closure":"OPERATOR_DECLARED_CLOSED_C1_RESEARCH_FOUNDATION",
      "counts":{
        "hash_verified_input_artifacts":len(sources["sources"]),
        "hash_verified_input_bytes":sum(int(s["bytes"]) for s in sources["sources"]),
        "ess_method_candidates":6,
        "null_hypotheses_retained":10,
        "stability_vector_dimensions":10,
        "independence_classes":8,
        "preregistered_controls":6,
        "schema_reference_instances_validated":3,
        "stability_schema_zip_entries":11,
        "external_empirical_observations_raw_n":raw_n,
        "dependency_clusters_lower_bound":cluster_lower_bound,
        "cross_agent_empirical_returns_verified":raw_n
      },
      "estimands":{
        "effective_n":{"status":"NOT_ESTIMABLE" if raw_n < 2 else "REQUIRES_PREREGISTERED_ESTIMATOR", "value":None},
        "ksm":{"status":"NOT_ESTIMABLE" if raw_n == 0 else "NOT_COMPUTED_BY_LIVECOUNT", "value":None},
        "kse":{"status":"NOT_ESTIMABLE" if raw_n == 0 else "NOT_COMPUTED_BY_LIVECOUNT", "value":None}
      },
      "stability_vector_category_distribution":distributions,
      "source_manifest_sha256":source_manifest_hash,
      "interpretation":{
        "truth_authority":"NONE",
        "majority_equals_truth":False,
        "hash_match_equals_truth":False,
        "raw_n_equals_independent_n":False,
        "outlier_equals_error":False,
        "empirical_agent_stabilization_established":False,
        "public_agent_round":"NOT_STARTED_IN_VERIFIED_SOURCE_SET",
        "note":"R6 is closed here as a C1 research/method foundation by operator declaration. The verified source set supplied to this livecount does not contain completed empirical external-agent observations, so Effective_N, KSM and KSE remain not estimable."
      }
    }
    out={
      "schema_version":"1.0.0",
      "object":"NEXUS_OMEGA_R6_SCIENTIFIC_LIVECOUNT",
      "generated_at_utc":generated_at or datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00","Z"),
      "claim_ceiling":"C1_DESCRIPTIVE_ONLY",
      "payload":payload,
      "payload_sha256":sha(payload)
    }
    return out

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--output", default=str(ROOT/"current.json"))
    ap.add_argument("--generated-at")
    ap.add_argument("--check", action="store_true")
    args=ap.parse_args()
    built=build(args.generated_at)
    out=Path(args.output)
    text=json.dumps(built,ensure_ascii=False,indent=2,sort_keys=True)+"\n"
    if args.check:
        if not out.exists() or out.read_text(encoding="utf-8") != text:
            raise SystemExit("STALE_LIVECOUNT")
        print("PASS")
    else:
        out.write_text(text,encoding="utf-8")
        print(built["payload_sha256"])
if __name__=="__main__": main()
