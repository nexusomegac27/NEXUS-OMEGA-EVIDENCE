#!/usr/bin/env python3
"""Fail-closed semantic validator for NEXUS scientific communication records.

Stdlib-only by design. This does not claim full JSON-Schema Draft 2020-12
implementation. It enforces the high-risk semantic invariants used by the
negative-fixture suite. Full JSON-Schema validation may be layered on later.
"""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path

SHA256 = re.compile(r"^[0-9a-f]{64}$")
OBS = {"OBS0_UNOBSERVABLE","OBS1_PROVIDER_AGGREGATE","OBS2_PROVIDER_EVENT","OBS3_MEDIATED_EVENT","OBS4_MUTUAL_RECEIPT"}
RA = {"RA0_NONE","RA1_SELF_ASSERTED","RA2_MUTUAL_BYTE_BOUND","RA3_AUTHENTICATED_PLATFORM","RA4_SIGNED_OR_TIMESTAMPED","RA5_EXTERNAL_TRANSPARENCY_WITNESS"}
SR = {"SR0_OPERATIONAL","SR1_PROVENANCE_SUPPORT","SR2_PROCESS_EVENT","SR3_CLAIM_EVIDENCE","SR4_GOVERNANCE_VALIDATION","SR5_SECURITY_INTEGRITY"}
PRIVACY = {"PUBLIC_FULL_TEXT","PUBLIC_REDACTED_TEXT","HASH_ONLY_PUBLIC_PRIVATE_PAYLOAD","METADATA_ONLY","WITHHELD"}

def errors(record: dict) -> list[str]:
    out: list[str] = []
    if record.get("claim_ceiling") != "C1":
        out.append("CLAIM_CEILING_VIOLATION")
    if record.get("claim_promotion") is not False:
        out.append("CLAIM_PROMOTION_PROHIBITED")
    if record.get("observability_class") not in OBS:
        out.append("INVALID_OBSERVABILITY_CLASS")
    if record.get("receipt_assurance") not in RA:
        out.append("INVALID_RECEIPT_ASSURANCE")
    if record.get("scientific_relevance_class") not in SR:
        out.append("INVALID_SCIENTIFIC_RELEVANCE")
    if record.get("privacy_class") not in PRIVACY:
        out.append("INVALID_PRIVACY_CLASS")

    rt = record.get("record_type")
    completeness = record.get("completeness_status")

    # Do not invent individual public-reader events from aggregate/unobservable telemetry.
    if rt == "access_receipt":
        mode = record.get("access_mode")
        identified = record.get("actor_identified")
        obs = record.get("observability_class")
        if mode in {"PUBLIC_BROWSER","RAW_FETCH","GIT_CLONE","GIT_FETCH","GITHUB_PAGES"}:
            if obs in {"OBS0_UNOBSERVABLE","OBS1_PROVIDER_AGGREGATE"} and identified is True:
                out.append("ANONYMOUS_OR_AGGREGATE_ACCESS_IDENTIFIED")
        if obs == "OBS1_PROVIDER_AGGREGATE" and record.get("provider_aggregate_window_days") is None:
            out.append("AGGREGATE_WINDOW_REQUIRED")
        if completeness == "COMPLETE" and obs in {"OBS0_UNOBSERVABLE","OBS1_PROVIDER_AGGREGATE"}:
            out.append("INCOMPLETE_OBSERVABILITY_MARKED_COMPLETE")

    if rt == "observability_snapshot":
        if record.get("individual_events_available") is not False:
            out.append("AGGREGATE_SNAPSHOT_CANNOT_ASSERT_INDIVIDUAL_EVENTS")
        if record.get("observability_class") != "OBS1_PROVIDER_AGGREGATE":
            out.append("AGGREGATE_SNAPSHOT_WRONG_OBSERVABILITY")

    if rt == "communication_receipt":
        trunc = record.get("truncation_status")
        if trunc not in {None,"NONE"} and completeness == "COMPLETE":
            out.append("TRUNCATED_COMMUNICATION_MARKED_COMPLETE")
        if completeness == "COMPLETE":
            if not record.get("request_sha256") or not record.get("response_sha256"):
                out.append("COMPLETE_COMMUNICATION_REQUIRES_BOTH_DIGESTS")

    if rt == "validation_receipt":
        if record.get("validator_independence") == "SELF" and record.get("verdict") == "PASS":
            out.append("SELF_VALIDATION_CANNOT_ESTABLISH_INDEPENDENT_PASS")

    # Semantic anti-confusion sentinel fields are accepted only in fixtures; a production
    # record with any of these assertions fails closed.
    assertions = record.get("_test_assertions", {})
    if assertions:
        mapping = {
          "hash_is_timestamp":"HASH_IS_NOT_TIMESTAMP",
          "hash_is_identity_proof":"HASH_IS_NOT_IDENTITY_PROOF",
          "signature_is_scientific_truth":"SIGNATURE_IS_NOT_SCIENTIFIC_TRUTH",
          "views_are_scientific_validity":"POPULARITY_IS_NOT_VALIDATION",
          "clones_are_scientific_validity":"POPULARITY_IS_NOT_VALIDATION",
          "stars_are_scientific_validity":"POPULARITY_IS_NOT_VALIDATION",
          "agent_count_is_scientific_validity":"CONSENSUS_IS_NOT_VALIDATION",
          "watch_alert_authorizes_execution":"WATCH_HAS_NO_AUTHORITY",
          "missing_bytes_reconstructed_from_chat":"MISSING_BYTES_MUST_REMAIN_MISSING",
          "old_hash_reused_after_edit":"EDIT_REQUIRES_NEW_DIGEST",
          "private_chain_of_thought_required":"PRIVATE_COT_NOT_REQUIRED",
          "unredacted_personal_data_public":"PRIVACY_POLICY_VIOLATION",
          "force_push_rewrites_history":"HISTORY_REWRITE_PROHIBITED",
          "model_ui_label_is_verified_identity":"ASSERTED_IDENTITY_NOT_VERIFIED_IDENTITY",
          "gateway_observation_represents_all_access":"MEDIATED_SAMPLE_NOT_ALL_ACCESS",
          "external_witness_required_for_base_record":"WITNESS_MUST_BE_OPTIONAL",
          "rekor_failure_promotes_record":"WITNESS_FAILURE_CANNOT_PROMOTE",
          "missing_access_counted_as_zero":"UNOBSERVABLE_IS_NOT_ZERO",
          "source_substitution":"SOURCE_OBJECT_SUBSTITUTION",
          "invented_receipt":"INVENTED_RECEIPT",
          "invented_hash":"INVENTED_HASH",
          "posthoc_schema_change":"POSTHOC_SCHEMA_CHANGE",
          "duplicate_event_id":"DUPLICATE_EVENT_ID",
          "replayed_receipt":"REPLAYED_RECEIPT",
          "causal_parent_missing_reconstructed":"MISSING_PARENT_NOT_RECONSTRUCTED",
          "redaction_without_provenance":"REDACTION_PROVENANCE_REQUIRED",
          "low_entropy_secret_hash_public":"LOW_ENTROPY_HASH_PRIVACY_RISK",
          "provider_aggregate_as_complete_history":"AGGREGATE_NOT_COMPLETE_HISTORY",
        }
        for k,code in mapping.items():
            if assertions.get(k) is True:
                out.append(code)
    return sorted(set(out))

def load_fixture_lines(path: Path):
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        yield line_no, json.loads(line)

def fixture_base(fid: str) -> dict:
    return {
      "schema_version":"1.0.0","record_id":f"fixture:{fid.lower()}:00000001","record_type":"event",
      "observed_at_utc":"2026-08-31T00:00:00Z","recorded_at_utc":"2026-08-31T00:00:01Z",
      "actor_class":"UNKNOWN","actor_asserted_identity":"fixture","actor_verified_identity":None,
      "provider":"fixture","transport_class":"OTHER","observability_class":"OBS2_PROVIDER_EVENT",
      "receipt_assurance":"RA1_SELF_ASSERTED","scientific_relevance_class":"SR1_PROVENANCE_SUPPORT",
      "privacy_class":"METADATA_ONLY","claim_ceiling":"C1","claim_promotion":False,
      "content_sha256":None,"content_bytes":None,"canonicalization_method":"NONE",
      "causal_parent_record_ids":[],"previous_record_sha256":None,"external_witness_refs":[],
      "completeness_status":"PARTIAL","uncertainty":[]
    }

def run_fixtures(path: Path) -> int:
    count=0
    failures=[]
    seen=set()
    for line_no, fx in load_fixture_lines(path):
        count+=1
        fid=fx["id"]
        if fid in seen:
            failures.append(f"{fid}: duplicate fixture id")
            continue
        seen.add(fid)
        record=fixture_base(fid)
        record.update(fx.get("mutate", {}))
        if fx.get("assertions"):
            record["_test_assertions"]=fx["assertions"]
        got=errors(record)
        want=fx["expected_error"]
        if want not in got:
            failures.append(f"{fid}: expected {want}; got {got}")
    if count < 36:
        failures.append(f"fixture count {count} < 36")
    if failures:
        for item in failures: print("FAIL", item)
        return 1
    print(f"PASS fixtures={count}")
    return 0

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--fixtures", type=Path)
    ap.add_argument("--record", type=Path)
    ns=ap.parse_args()
    if ns.fixtures:
        raise SystemExit(run_fixtures(ns.fixtures))
    if ns.record:
        record=json.loads(ns.record.read_text(encoding="utf-8"))
        errs=errors(record)
        print(json.dumps({"errors":errs}, indent=2))
        raise SystemExit(1 if errs else 0)
    ap.error("provide --fixtures or --record")

if __name__ == "__main__":
    main()
