#!/usr/bin/env python3
"""NEXUS R31 deterministic publication reconciliation core (offline; NO deploy).
A bounded HMAC adapter for tests/operator-controlled offline signatures, NOT an
implementation of Sigstore, SLSA, TUF, RFC8785 or OS-level signer isolation.
Signer secrets must come from an external secrets facility, never Git or web.
"""
from __future__ import annotations
import hashlib
import hmac
import json
import re
from datetime import datetime, timezone
from typing import Any

C1 = "C1_DESCRIPTIVE_ONLY"
HEX64 = re.compile(r"^[a-f0-9]{64}$")
EVENT_TYPE = "nexus.publication.candidate.v1"
CANON = "NEXUS_JSON_SORTED_V1_NOT_RFC8785"
SENSITIVE_TERMS = ("raw_sensor", "api_secret", "device_serial", "patient_record")

class Refusal(ValueError):
    pass

def unique_pairs(pairs):
    d = {}
    for k, v in pairs:
        if k in d:
            raise Refusal("DUPLICATE_JSON_KEY")
        d[k] = v
    return d

def bad_constant(_):
    raise Refusal("NONFINITE_JSON")

def strict_load(raw: bytes) -> Any:
    if len(raw) > 262144:
        raise Refusal("JSON_INPUT_TOO_LARGE")
    return json.loads(raw.decode("utf-8", "strict"), object_pairs_hook=unique_pairs, parse_constant=bad_constant)

def canonical(obj: Any) -> bytes:
    # Restricted, well-defined local domain; does NOT claim RFC8785 equivalence.
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")

def sha(obj: Any) -> str:
    return hashlib.sha256(canonical(obj)).hexdigest()

def hex64(x: Any) -> bool:
    return isinstance(x, str) and HEX64.fullmatch(x) is not None

def signature_body(obj: dict) -> bytes:
    return canonical({k: v for k, v in obj.items() if k != "signature"})

def sign_test_receipt(body: dict, key: bytes) -> dict:
    """FOR SYNTHETIC TESTS ONLY. Production signer is an external adapter."""
    return dict(body, signature=hmac.new(key, signature_body(body), hashlib.sha256).hexdigest())

def verify_receipt(obj: Any, keys: dict, principal_field: str, trusted_role: str) -> bool:
    if not isinstance(obj, dict):
        return False
    principal = obj.get(principal_field)
    signer = keys.get(principal)
    if not isinstance(signer, dict) or signer.get("role") != trusted_role:
        return False
    key = signer.get("key")
    sig = obj.get("signature")
    if not isinstance(key, bytes) or not hex64(sig):
        return False
    expected = hmac.new(key, signature_body(obj), hashlib.sha256).hexdigest()
    return hmac.compare_digest(sig, expected)

def valid_timestamp(s):
    if not isinstance(s, str) or not s.endswith("Z"):
        return False
    try:
        t = datetime.fromisoformat(s.replace("Z", "+00:00"))
        return t.tzinfo is not None and t.utcoffset().total_seconds() == 0
    except (ValueError, TypeError, AttributeError):
        return False

def assess_event(event: Any):
    if not isinstance(event, dict):
        raise Refusal("BAD_EVENT")
    for key in ("specversion", "id", "source", "type", "time", "data"):
        if key not in event:
            raise Refusal("MISSING_EVENT_FIELD_" + key)
    if event["specversion"] != "1.0" or event["type"] != EVENT_TYPE:
        raise Refusal("UNSUPPORTED_EVENT_SCHEMA_OR_TYPE")
    if not isinstance(event["id"], str) or not event["id"] or len(event["id"]) > 200:
        raise Refusal("INVALID_EVENT_ID")
    if not isinstance(event["source"], str) or not event["source"].startswith("urn:nexus:"):
        raise Refusal("UNTRUSTED_EVENT_SOURCE_FORMAT")
    if not valid_timestamp(event["time"]):
        raise Refusal("INVALID_EVENT_TIME")
    data = event["data"]
    if not isinstance(data, dict):
        raise Refusal("BAD_EVENT_DATA")
    if not isinstance(data.get("release_id"), str) or not data["release_id"]:
        raise Refusal("BAD_RELEASE_ID")
    if data.get("claim_ceiling") != C1:
        raise Refusal("CLAIM_CEILING_MISMATCH")
    if data.get("source_class") != "C1_VERIFIED_PUBLIC_SAFE":
        raise Refusal("SOURCE_NOT_VERIFIED_PUBLIC_SAFE")
    if data.get("public_safe") is not True or data.get("reversible") is not True:
        raise Refusal("PUBLIC_OR_ROLLBACK_GATE_MISSING")
    if data.get("visibility") != "public_metadata_only":
        raise Refusal("PRIVATE_OR_UNSCOPED_VISIBILITY")
    if not hex64(data.get("source_sha256")) or not hex64(data.get("review_sha256")):
        raise Refusal("SOURCE_OR_REVIEW_DIGEST_MISSING")
    if not isinstance(data.get("release_seq"), int) or isinstance(data["release_seq"], bool) or data["release_seq"] < 1:
        raise Refusal("INVALID_RELEASE_SEQUENCE")
    if not isinstance(data.get("topics"), list) or not data["topics"] or any(not isinstance(x, str) for x in data["topics"]):
        raise Refusal("INVALID_TOPICS")
    if not isinstance(data.get("targets"), dict) or not data["targets"]:
        raise Refusal("NO_TARGETS")
    if any(not str(k).startswith("/") or not hex64(v) for k, v in data["targets"].items()):
        raise Refusal("UNBOUND_TARGET_DIGEST")
    if any(term in canonical(data).decode("utf-8").lower() for term in SENSITIVE_TERMS):
        raise Refusal("PRIVATE_MARKER_IN_PUBLIC_EVENT")

def reconcile(event: dict, grant: dict | None, witnesses: list, registry: dict,
              prior: dict, keys: dict, static_flags: dict | None = None) -> dict:
    """Pure, no HTTP/disk/network, no state changes or side-effecting deployment."""
    assess_event(event)
    data, event_sha = event["data"], sha(event)
    flags = static_flags or {}
    if not isinstance(witnesses, list):
        raise Refusal("WITNESSES_NOT_LIST")
    if not isinstance(registry, dict) or not isinstance(prior, dict):
        raise Refusal("INVALID_REGISTRY_OR_PRIOR")
    results = {}
    for route, expected_sha in sorted(data["targets"].items()):
        conf = registry.get(route)
        if not isinstance(conf, dict) or conf.get("visibility") != "public_metadata_only":
            results[route] = {"state": "HOLD_UNKNOWN_OR_PRIVATE_SURFACE"}
            continue
        if not set(data["topics"]).intersection(conf.get("topics", [])):
            results[route] = {"state": "HOLD_UNRELATED_SURFACE"}
            continue
        if not verify_receipt(grant, keys, "signer", "operator_release"):
            results[route] = {"state": "HOLD_NO_VERIFIED_OPERATOR_GRANT"}
            continue
        if grant.get("event_sha256") != event_sha or grant.get("release_id") != data["release_id"]:
            results[route] = {"state": "HOLD_GRANT_EVENT_BINDING"}
            continue
        if grant.get("release_seq") != data["release_seq"] or route not in grant.get("allowed_routes", []):
            results[route] = {"state": "HOLD_GRANT_ROUTE_OR_SEQUENCE"}
            continue
        prev = prior.get(route)
        if prev:
            pseq = prev.get("release_seq")
            if not isinstance(pseq, int) or isinstance(pseq, bool):
                results[route] = {"state": "HOLD_CORRUPT_PRIOR"}
                continue
            if pseq > data["release_seq"]:
                results[route] = {"state": "HOLD_ROLLBACK"}
                continue
            if pseq == data["release_seq"] and prev.get("sha256") != expected_sha:
                results[route] = {"state": "HOLD_SEQUENCE_EQUIVOCATION"}
                continue
        matches = [w for w in witnesses if isinstance(w, dict) and w.get("route") == route]
        valid = [w for w in matches if verify_receipt(w, keys, "observer", "independent_observer")
                 and w.get("observer") != grant.get("signer")
                 and w.get("release_id") == data["release_id"]
                 and w.get("event_sha256") == event_sha
                 and w.get("http_status") == 200
                 and w.get("observed_sha256") == expected_sha
                 and w.get("content_type") in ("text/html", "application/json", "text/css")
                 and valid_timestamp(w.get("observed_at"))]
        # Contradictory *verified* observations are a HOLD, never vote by majority.
        conflict = any(
            verify_receipt(w, keys, "observer", "independent_observer")
            and w.get("event_sha256") == event_sha
            and w.get("release_id") == data["release_id"]
            and w.get("observed_sha256") != expected_sha
            for w in matches)
        if conflict:
            results[route] = {"state": "HOLD_CONFLICTING_WWW_WITNESS"}
        elif valid:
            results[route] = {
                "state": "RECONCILED_WITH_STATIC_METADATA_DRIFT" if flags.get(route) is False else "RECONCILED",
                "source_sha256": data["source_sha256"],
                "observed_sha256": expected_sha,
                "release_seq": data["release_seq"],
                "static_metadata_drift": flags.get(route) is False
            }
        elif matches:
            results[route] = {"state": "HOLD_WWW_WITNESS_UNVERIFIED_OR_MISMATCH"}
        else:
            results[route] = {"state": "PENDING_INDEPENDENT_WWW_WITNESS"}
    return {
        "object": "NEXUS_OMEGA_R31_PUBLICATION_RECONCILIATION_EVALUATION_V1",
        "claim_ceiling": C1,
        "event_sha256": event_sha,
        "release_id": data["release_id"],
        "source_digest_bound": data["source_sha256"],
        "state": (
            "ALL_RECONCILED"
            if results and all(x["state"] == "RECONCILED" for x in results.values())
            else "WWW_OBSERVED_METADATA_DRIFT_OPEN"
            if results and all(x["state"] in ("RECONCILED", "RECONCILED_WITH_STATIC_METADATA_DRIFT") for x in results.values())
            else "PARTIAL_OR_HOLD"
        ),
        "metadata_drift_routes": sorted(
            route for route, state in results.items()
            if state["state"] == "RECONCILED_WITH_STATIC_METADATA_DRIFT"
        ),
        "self_audit_note": "Observed WWW bytes and publication metadata are distinct. A detected drift prevents ALL_RECONCILED.",
        "surfaces": results,
        "www_write_performed": False,
        "claim_promotion": False,
        "cryptographic_note": "HMAC offline test adapter, not deployment signer verification or SLSA/Sigstore certification"
    }

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--case", required=True, help="offline JSON: event,grant,witnesses,registry,prior,static_flags")
    args = ap.parse_args()
    try:
        with open(args.case, "rb") as f:
            obj = strict_load(f.read())
        # No secrets accepted in JSON; no claim that an unsigned envelope is authoritative.
        print(json.dumps(reconcile(obj["event"], obj.get("grant"), obj.get("witnesses", []),
            obj["registry"], obj.get("prior", {}), keys={}, static_flags=obj.get("static_flags")),
            sort_keys=True, indent=2))
    except (Refusal, ValueError, KeyError, TypeError) as e:
        print(json.dumps({"state": "FAIL_CLOSED", "reason": str(e), "claim_ceiling": C1}))
        raise SystemExit(2)
