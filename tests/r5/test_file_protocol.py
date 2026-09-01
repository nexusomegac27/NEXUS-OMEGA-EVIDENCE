import hashlib, json, subprocess, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]

def test_file_event_schema_is_strict_json():
    p=ROOT/"schema/r5/file-protocol/nexus-file-event-v1.schema.json"
    d=json.loads(p.read_text(encoding="utf-8"))
    assert d["additionalProperties"] is False
    assert d["properties"]["claim_ceiling"]["const"]=="C1"
    assert d["properties"]["digest_domain"]["const"]=="SHA256_RAW_BYTES_V1"

def test_capability_profile_denies_self_validation_and_force_push():
    p=ROOT/"schema/r5/agent-governance/nexus-agent-capability-profile-v1.schema.json"
    d=json.loads(p.read_text(encoding="utf-8"))
    assert d["properties"]["git"]["properties"]["force_push"]["const"] is False
    assert d["properties"]["authority"]["properties"]["self_validation"]["const"] is False

def test_file_event_archive_declares_recursion_boundary():
    p=ROOT/"docs/r5/file-protocol/CANONICAL_FILE_EVENT_ARCHIVE_V1.md"
    t=p.read_text(encoding="utf-8")
    assert "LEDGER_DERIVED_METADATA" in t
    assert "COMMIT_A" in t and "COMMIT_B" in t
