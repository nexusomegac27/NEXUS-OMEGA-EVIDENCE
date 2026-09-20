#!/usr/bin/env python3
"""Public-safe NEXUS IX R3 reference harness.

Test-only fixture. The fixed Ed25519 private key is public test material and MUST NOT be used
for production signing or identity.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, Optional, Tuple
import copy, hashlib, json, platform
import cryptography
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey

TEST_PRIVATE_SEED = bytes([1]) * 32
ALLOWED_ACTIONS = {"SET_LABEL"}
NOW = 1000

def canonical_json(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")

def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def fixture_private_key() -> Ed25519PrivateKey:
    return Ed25519PrivateKey.from_private_bytes(TEST_PRIVATE_SEED)

def fixture_public_key_hex() -> str:
    return fixture_private_key().public_key().public_bytes(
        serialization.Encoding.Raw, serialization.PublicFormat.Raw
    ).hex()

def make_receipt(payload: Dict[str, Any], metadata: Optional[Dict[str, Any]] = None,
                 prev_receipt_sha256: Optional[str] = None) -> Tuple[Dict[str, Any], str]:
    body = {
        "payload_sha256": sha256_hex(canonical_json(payload)),
        "prev_receipt_sha256": prev_receipt_sha256,
        "metadata": metadata or {},
        "public_key_hex": fixture_public_key_hex(),
    }
    receipt = {**body, "signature_hex": fixture_private_key().sign(canonical_json(body)).hex()}
    return receipt, sha256_hex(canonical_json(receipt))

def verify_receipt(payload: Dict[str, Any], receipt: Dict[str, Any],
                   expected_prev: Optional[str]) -> Tuple[bool, str]:
    required = {"payload_sha256", "prev_receipt_sha256", "metadata", "public_key_hex", "signature_hex"}
    if set(receipt) != required:
        return False, "SCHEMA_MISMATCH"
    if sha256_hex(canonical_json(payload)) != receipt["payload_sha256"]:
        return False, "PAYLOAD_HASH_MISMATCH"
    if receipt["prev_receipt_sha256"] != expected_prev:
        return False, "PREV_HASH_MISMATCH"
    body = {k: receipt[k] for k in ["payload_sha256", "prev_receipt_sha256", "metadata", "public_key_hex"]}
    try:
        pub = Ed25519PublicKey.from_public_bytes(bytes.fromhex(receipt["public_key_hex"]))
        pub.verify(bytes.fromhex(receipt["signature_hex"]), canonical_json(body))
    except (InvalidSignature, ValueError):
        return False, "SIGNATURE_INVALID"
    return True, "PASS"

@dataclass(frozen=True)
class HumanAuthorization:
    proposal_id: str
    approved: bool
    expires_at: int

@dataclass(frozen=True)
class Decision:
    outcome: str
    reason: str
    proposal_id: str

def decide(proposal: Dict[str, Any], receipt: Dict[str, Any], expected_prev: Optional[str],
           now: int, human_auth: Optional[HumanAuthorization] = None) -> Decision:
    ok, reason = verify_receipt(proposal, receipt, expected_prev)
    pid = str(proposal.get("proposal_id", ""))
    if not ok:
        return Decision("DENY", f"INTEGRITY_{reason}", pid)
    if proposal.get("action") not in ALLOWED_ACTIONS:
        return Decision("DENY", "ACTION_NOT_ALLOWED", pid)
    if int(proposal.get("expires_at", now + 1)) < now:
        return Decision("DENY", "STALE_PROPOSAL", pid)
    if proposal.get("risk") == "HIGH":
        if human_auth is None or not human_auth.approved:
            return Decision("DENY", "HUMAN_AUTH_REQUIRED", pid)
        if human_auth.proposal_id != pid:
            return Decision("DENY", "HUMAN_AUTH_PROPOSAL_MISMATCH", pid)
        if human_auth.expires_at < now:
            return Decision("DENY", "HUMAN_AUTH_EXPIRED", pid)
    return Decision("ALLOW", "POLICY_PASS", pid)

def execute(decision: Decision, proposal: Dict[str, Any], world: Dict[str, str]) -> Dict[str, Any]:
    if decision.outcome != "ALLOW" or decision.proposal_id != proposal.get("proposal_id"):
        return {"executed": False, "reason": "DECISION_NOT_BOUND_OR_ALLOWED"}
    if proposal.get("action") != "SET_LABEL":
        return {"executed": False, "reason": "EXECUTOR_CAPABILITY_DENIED"}
    world[str(proposal["target"])] = str(proposal["value"])
    return {"executed": True, "reason": "EXECUTED", "observed_value": world[str(proposal["target"])]}

def base_proposal(risk: str = "LOW") -> Dict[str, Any]:
    return {"proposal_id":"P1","action":"SET_LABEL","target":"fixture","value":"alpha","risk":risk,"expires_at":1100}

def run() -> Dict[str, Any]:
    results = []
    def check(name: str, cond: bool, detail: str):
        results.append({"name": name, "pass": bool(cond), "detail": detail})

    p1 = base_proposal(); r1, h1 = make_receipt(p1, {"purpose":"R3 fixture"})
    p2 = {**base_proposal(), "proposal_id":"P2", "value":"beta"}; r2, h2 = make_receipt(p2, {"purpose":"R3 fixture"}, h1)
    check("receipt_chain_valid", verify_receipt(p1,r1,None)[0] and verify_receipt(p2,r2,h1)[0], h2)
    tam = copy.deepcopy(p1); tam["value"]="tampered"
    check("payload_tamper_rejected", verify_receipt(tam,r1,None)[1]=="PAYLOAD_HASH_MISMATCH", "PAYLOAD_HASH_MISMATCH")
    badsig = copy.deepcopy(r1); badsig["signature_hex"]="00"*64
    check("signature_tamper_rejected", verify_receipt(p1,badsig,None)[1]=="SIGNATURE_INVALID", "SIGNATURE_INVALID")
    check("chain_break_rejected", verify_receipt(p1,r1,"00"*32)[1]=="PREV_HASH_MISMATCH", "PREV_HASH_MISMATCH")

    p=base_proposal(); r,_=make_receipt(p); d=decide(p,r,None,NOW)
    check("valid_low_risk_executes", d.outcome=="ALLOW" and execute(d,p,{})["executed"], d.reason)
    rbad=copy.deepcopy(r); rbad["signature_hex"]="00"*64
    check("invalid_signature_blocked", decide(p,rbad,None,NOW).outcome=="DENY", "integrity gate")
    pu={**base_proposal(),"action":"DIRECT_SHELL"}; ru,_=make_receipt(pu)
    check("unallowed_direct_action_blocked", decide(pu,ru,None,NOW).reason=="ACTION_NOT_ALLOWED", "ACTION_NOT_ALLOWED")
    ps={**base_proposal(),"expires_at":999}; rs,_=make_receipt(ps)
    check("stale_proposal_blocked", decide(ps,rs,None,NOW).reason=="STALE_PROPOSAL", "STALE_PROPOSAL")
    ph=base_proposal("HIGH"); rh,_=make_receipt(ph)
    check("high_risk_without_human_auth_blocked", decide(ph,rh,None,NOW).reason=="HUMAN_AUTH_REQUIRED", "HUMAN_AUTH_REQUIRED")
    wrong=HumanAuthorization("OTHER",True,1100)
    check("human_auth_mismatch_blocked", decide(ph,rh,None,NOW,wrong).reason=="HUMAN_AUTH_PROPOSAL_MISMATCH", "HUMAN_AUTH_PROPOSAL_MISMATCH")
    expired=HumanAuthorization("P1",True,999)
    check("expired_human_auth_blocked", decide(ph,rh,None,NOW,expired).reason=="HUMAN_AUTH_EXPIRED", "HUMAN_AUTH_EXPIRED")
    valid=HumanAuthorization("P1",True,1100); dh=decide(ph,rh,None,NOW,valid)
    check("valid_high_risk_with_bound_auth_executes", dh.outcome=="ALLOW" and execute(dh,ph,{})["executed"], dh.reason)
    mismatched_decision=Decision("ALLOW","POLICY_PASS","OTHER")
    check("executor_rechecks_decision_binding", not execute(mismatched_decision,p,{})["executed"], "proposal binding")

    passed=sum(1 for x in results if x["pass"])
    return {
        "object":"NEXUS_OMEGA_AXIOM_IX_R3_REFERENCE_HARNESS_EXECUTION_20260920_R0",
        "state": f"PASS_WITH_CAVEATS_C1_{passed}_OF_{len(results)}_TESTS_PASS" if passed==len(results) else "FAIL_C1_REFERENCE_HARNESS",
        "python_version":platform.python_version(),
        "cryptography_version":cryptography.__version__,
        "public_test_key":True,
        "public_key_hex":fixture_public_key_hex(),
        "receipt_1_sha256":h1,
        "receipt_2_sha256":h2,
        "tests":results,
        "tests_passed":passed,
        "tests_total":len(results),
        "network_writes":0,
        "external_systems_touched":0,
        "not_established":["CEDAR_RUNTIME_EXECUTION","ZKP_EXECUTION","PRODUCTION_SECURITY","COMPLETE_ATTACK_RESISTANCE","HUMAN_IDENTITY","SCIENTIFIC_VALIDITY"]
    }

if __name__ == "__main__":
    result=run()
    print(json.dumps(result, sort_keys=True))
    raise SystemExit(0 if result["tests_passed"]==result["tests_total"] else 1)
