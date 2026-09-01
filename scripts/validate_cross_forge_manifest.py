#!/usr/bin/env python3
import json
import re
from pathlib import Path

HEX40 = re.compile(r"^[0-9a-f]{40}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")

p = Path("cross_forge/manifest.json")
data = json.loads(p.read_text(encoding="utf-8"))

assert data["schema_version"] == "1.0.0"
assert data["claim_ceiling"] == "C1"
assert data["canonical_content_digest"] == "SHA256"
assert data["source_object_substitution"] is False
assert data["merge"] is False
assert data["deploy"] is False
assert data["claim_promotion"] is False

for value in (
    data["github"]["main_anchor"],
    data["github"]["active_pr_head"],
    data["gitlab"]["main_anchor"],
):
    assert HEX40.fullmatch(value), value

for value in (
    data["terminal_bundle"]["master_sha256"],
    data["terminal_bundle"]["repair_receipt_sha256"],
):
    assert HEX64.fullmatch(value), value

assert data["terminal_bundle"]["axiom_independent_rehash"] == "NOT_EXECUTED_SOURCE_BYTES_NOT_PRESENT"
assert data["cross_forge_state"] == "FOUNDATION_ONLY_REPLICATION_NOT_YET_ESTABLISHED"
print("CROSS_FORGE_MANIFEST_PASS")
