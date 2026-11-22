#!/usr/bin/env python3
"""R41 P5 — classify external expert materials by origin / auth / independence."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

OUT = Path(__file__).resolve().parent / "PROVENANCE_CLASSIFICATION.json"

# Bound from AXIOM R40→R41 handoff + Folder X R40 sealed prior (no invention of missing bytes)
RECORDS = [
    {
        "source": "Stage-1_E01_E16",
        "auth_class": "PARTIAL_MANIFEST_REFERENCE",
        "independence": "NOT_INDEPENDENTLY_REGISTERED",
        "quorum_eligible": False,
        "status": "3_OF_14_REFERENCED_MANIFEST_FILES_PRESENT_AND_CHECKED",
        "scientific_role": "METHODS_CONTRIBUTION_ONLY",
        "caveat": "DOES_NOT_FORM_EXPERT_QUORUM",
    },
    {
        "source": "AutoClaw_X14",
        "auth_class": "ZIP_CRC_AND_FILE_HASH_MATCH_REPORTED",
        "independence": "OFFLINE_SIMULATION_AND_COUNTEREXAMPLES",
        "quorum_eligible": False,
        "status": "ZIP_CRC_PASS_6_OF_6_FILEHASH_MATCH_AXIOM_STATED",
        "scientific_role": "OFFLINE_SIMULATION_COUNTEREXAMPLES",
        "caveat": "DOES_NOT_FORM_EXPERT_QUORUM",
    },
    {
        "source": "Grok",
        "auth_class": "ADVISORY_CROSSVALIDATION_REPORT_RECEIVED",
        "independence": "ADVISORY_ONLY",
        "quorum_eligible": False,
        "status": "REPORT_RECEIVED",
        "scientific_role": "ADVISORY_SOURCE_AND_METHOD_CONTROL",
        "caveat": "DOES_NOT_FORM_EXPERT_QUORUM",
    },
    {
        "source": "Mistral_Vibe",
        "auth_class": "READBACK_REPORT_RECEIVED",
        "independence": "GITHUB_CONTINUITY_CONTROL_ONLY",
        "quorum_eligible": False,
        "status": "READBACK_REPORT_RECEIVED",
        "scientific_role": "GITHUB_CONTINUITY_CONTROL",
        "caveat": "DOES_NOT_FORM_EXPERT_QUORUM",
    },
    {
        "source": "R41_MAXI_ZIP_CLAIMED",
        "auth_class": "CLAIMED_PACKAGE",
        "independence": "N_A",
        "quorum_eligible": False,
        "status": "SOURCE_GAP",
        "claimed_bytes": 15516,
        "claimed_sha256": "a903a4598bb2b0a5482d20f06694b7687a51058ee078e98250fe39cbb4dbdbc5",
        "local_status": "ABSENT_AT_CURSOR_INTAKE",
        "scientific_role": "ORDER_TRANSPORT_CLAIM",
        "caveat": "ISSUE_395_ALONE_AUTHORIZES_P0_SCOPE_ZIP_BYTES_NOT_INVENTED",
    },
    {
        "source": "GitHub_Issue_395",
        "auth_class": "PUBLIC_ISSUE_OPEN_READBACK",
        "independence": "OPERATOR_AXIOM_ORDER_SURFACE",
        "quorum_eligible": False,
        "status": "OPEN_VERIFIED_RECEIPT",
        "scientific_role": "SOURCE_AUTHORITY_FOR_R41_IMPLEMENTATION_ORDER",
        "caveat": "NOT_PHYSICAL_CLEARANCE",
    },
]


def main() -> int:
    quorum_count = sum(1 for r in RECORDS if r.get("quorum_eligible"))
    receipt = {
        "object": "R41_PROVENANCE_CLASSIFICATION",
        "recorded_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "claim_ceiling": "C1_DESCRIPTIVE_ONLY",
        "independent_expert_quorum": False,
        "quorum_eligible_count": quorum_count,
        "records": RECORDS,
        "law": "UNREGISTERED_OR_COPIED_CONTRIBUTIONS_DO_NOT_FORM_QUORUM",
        "verdict": "PASS_CLASSIFICATION_NO_QUORUM_CLAIM",
    }
    text = json.dumps(receipt, indent=2, ensure_ascii=False) + "\n"
    OUT.write_text(text, encoding="utf-8")
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    print(json.dumps({"verdict": receipt["verdict"], "sha256": digest, "path": str(OUT)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
