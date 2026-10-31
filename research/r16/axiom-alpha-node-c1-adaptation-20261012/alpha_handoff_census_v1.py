#!/usr/bin/env python3
"""Isolated, structural-only C1 handoff census. No GitHub calls or writes."""
import json
import re
import sys

HEX40 = re.compile(r"[0-9a-f]{40}\\Z")
HEX64 = re.compile(r"[0-9a-f]{64}\\Z")
OUT_REASONS = {"PRIVATE_INACCESSIBLE", "NOT_ROUTINE", "NOT_PUBLIC", "NOT_AUTHORIZED"}


def unique_object(pairs):
    obj = {}
    for key, value in pairs:
        if key in obj:
            raise ValueError("duplicate_json_key")
        obj[key] = value
    return obj


def source_pinned(source):
    return (isinstance(source, dict)
            and isinstance(source.get("commit"), str) and bool(HEX40.fullmatch(source["commit"]))
            and isinstance(source.get("git_blob"), str) and bool(HEX40.fullmatch(source["git_blob"]))
            and isinstance(source.get("sha256"), str) and bool(HEX64.fullmatch(source["sha256"]))
            and type(source.get("bytes")) is int and source["bytes"] >= 0
            and isinstance(source.get("path"), str) and bool(source["path"].strip())
            and not source["path"].startswith("/") and ".." not in source["path"].split("/"))


def census(payload):
    if not isinstance(payload, dict) or payload.get("schema_version") != "1" or not isinstance(payload.get("events"), list):
        return {"status": "FAIL_CLOSED", "reason": "invalid_envelope"}
    seen = {}
    unique = []
    for item in payload["events"]:
        if not isinstance(item, dict) or not isinstance(item.get("event_id"), str) or not item["event_id"].strip():
            return {"status": "FAIL_CLOSED", "reason": "invalid_event_id"}
        key = item["event_id"]
        canonical = json.dumps(item, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        if key in seen:
            if seen[key] != canonical:
                return {"status": "FAIL_CLOSED", "reason": "conflicting_event_id", "event_id": key}
            continue
        seen[key] = canonical
        unique.append(item)
    eligible = auto = unresolved = excluded = publications = publication_complete = publication_unknown = 0
    for item in unique:
        if item.get("kind") not in {"HANDOFF_ATTEMPT", "PUBLICATION"}:
            unresolved += 1
            continue
        scope = item.get("scope")
        if scope == "OUT_OF_SCOPE" and item.get("exclusion_reason") in OUT_REASONS and isinstance(item.get("evidence_ref"), str) and item["evidence_ref"].strip():
            excluded += 1
            continue
        if scope != "PUBLIC_ROUTINE_AUTHORIZED_ACCESSIBLE" or not source_pinned(item.get("source")) or not isinstance(item.get("evidence_ref"), str) or not item["evidence_ref"].strip():
            unresolved += 1
            continue
        if item["kind"] == "HANDOFF_ATTEMPT":
            if item.get("result") not in {"SUCCESS", "FAILURE"} or type(item.get("manual_restart")) is not bool:
                unresolved += 1
                continue
            eligible += 1
            if (item["result"] == "SUCCESS" and item["manual_restart"] is False
                and item.get("receiver_ack") == "VERIFIED" and item.get("readback") == "COMPLETE"
                and isinstance(item.get("receiver_actor"), str) and item["receiver_actor"].strip()
                and item.get("receiver_actor") != item.get("sender_actor")):
                auto += 1
        else:
            if item.get("readback") not in {"COMPLETE", "INCOMPLETE"}:
                publication_unknown += 1
                continue
            publications += 1
            publication_complete += (item["readback"] == "COMPLETE")
    return {
        "status": "STRUCTURAL_ONLY_NOT_AUTHENTICATED",
        "unique_events": len(unique), "duplicate_events": len(payload["events"]) - len(unique),
        "excluded_with_declared_reason": excluded,
        "unresolved": unresolved + publication_unknown,
        "handoff": {"eligible_attempts": eligible, "automated_with_structural_ack": auto,
                    "rate_percent": round(100 * auto / eligible, 4) if eligible and not (unresolved or publication_unknown) else None},
        "publication": {"observed_published": publications, "complete_readbacks": publication_complete,
                        "rate_percent": round(100 * publication_complete / publications, 4) if publications and not (unresolved or publication_unknown) else None},
        "operational_claim": "NOT_COMPUTABLE_UNTIL_INDEPENDENT_API_SOURCE_AND_ACTOR_VERIFICATION"
    }


def main():
    try:
        data = json.loads(sys.stdin.read(), object_pairs_hook=unique_object,
                          parse_constant=lambda _: (_ for _ in ()).throw(ValueError("nonfinite_json")))
        result = census(data)
    except (ValueError, TypeError, RecursionError, UnicodeError) as exc:
        result = {"status": "FAIL_CLOSED", "reason": type(exc).__name__}
    print(json.dumps(result, sort_keys=True))
    return 2 if result["status"] == "FAIL_CLOSED" else 0


if __name__ == "__main__":
    sys.exit(main())
