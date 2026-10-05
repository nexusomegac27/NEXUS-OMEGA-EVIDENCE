
{
  "schema_set": "R10R7_SCHEMA_V0_1",
  "claim_ceiling": "C1_DESCRIPTIVE_ONLY",
  "note": "Design artifacts. Thresholds UNSET until calibration (Threshold Discipline). Certificate means CHECK_EXECUTED_WITH_THIS_RESULT, never absolute truth.",

  "separation_certificate_schema": {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "R7_13_SEPARATION_CERTIFICATE",
    "type": "object",
    "required": ["nci_id", "nci_version", "node_id", "constitution_hash", "monitor_hash", "policy_hash", "distinction_class", "predicate", "verdict", "valid_from", "verifier"],
    "properties": {
      "nci_id": { "type": "string", "pattern": "^NCI-[A-Z0-9]+(-[A-Z0-9_]+)?$" },
      "nci_version": { "type": "string" },
      "node_id": { "type": "string" },
      "constitution_hash": { "type": "string" },
      "monitor_hash": { "type": "string" },
      "policy_hash": { "type": "string" },
      "distinction_class": { "type": "array", "minItems": 1, "items": { "enum": ["CLASS_T", "CLASS_R", "CLASS_C", "CLASS_S", "CLASS_M", "CLASS_H", "CLASS_TEMP"] } },
      "predicate": { "type": "string" },
      "metric_if_any": { "type": ["string", "null"] },
      "threshold_if_any": { "type": ["number", "null"], "comment": "UNSET until calibration" },
      "threshold_source": { "type": ["string", "null"] },
      "observed_value_if_any": { "type": ["number", "null"] },
      "uncertainty": { "type": ["object", "null"] },
      "trace_pointers": { "type": "array", "items": { "type": "string" } },
      "provenance_pointer": { "type": ["string", "null"] },
      "valid_from": { "type": "string", "format": "date-time" },
      "valid_until": { "type": ["string", "null"] },
      "verifier": { "type": "string" },
      "verdict": { "enum": ["HEALTHY", "AT_RISK", "UNRESOLVED", "UNKNOWN", "COLLAPSED"] },
      "parent_certificate": { "type": ["string", "null"] }
    },
    "additionalProperties": false,
    "invariants": {
      "no_collapse_of_axes": "verdict UNKNOWN must never be summarized to HEALTHY or COLLAPSED",
      "no_crypto_laundering": "hash match does not imply verdict HEALTHY"
    }
  },

  "proof_obligation_schema": {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "R7_14_PROOF_OBLIGATION",
    "type": "object",
    "required": ["po_id", "claim", "obligation_type", "formal_or_empirical", "current_status", "blocks_what", "does_not_block_what", "closure_criterion"],
    "properties": {
      "po_id": { "type": "string", "pattern": "^PO-[A-Z0-9]+(-[A-Z0-9_]+)?$" },
      "claim": { "type": "string" },
      "obligation_type": { "enum": ["FORMAL_PROOF", "EMPIRICAL_TEST", "CALIBRATION", "PRIOR_ART_REVIEW"] },
      "formal_or_empirical": { "enum": ["FORMAL", "EMPIRICAL"] },
      "current_status": { "enum": ["OPEN", "IN_PROGRESS", "CLOSED", "EXPIRED", "REJECTED"] },
      "evidence": { "type": "array", "items": { "type": "string" } },
      "counterevidence": { "type": "array", "items": { "type": "string" } },
      "blocks_what": { "type": "array", "items": { "type": "string" } },
      "does_not_block_what": { "type": "array", "items": { "type": "string" } },
      "closure_criterion": { "type": "string" },
      "expiry": { "type": ["string", "null"] }
    },
    "additionalProperties": false,
    "invariants": {
      "no_silent_closure": "status CLOSED requires non-empty evidence and closure_criterion met",
      "no_works_well_closure": "no obligation may close because the system operates well (Elegance Trap)"
    }
  },

  "registered_obligations_v0": [
    { "po_id": "PO-NCI-01", "claim": "Constitution rules compile to monitors without hand-written duplication", "formal_or_empirical": "FORMAL", "status": "OPEN", "blocks_what": ["NCI_COMPILATION (Abschn. 21)"] },
    { "po_id": "PO-NCI-02", "claim": "Monitors separate HEALTHY_EQUALITY from COLLAPSE", "formal_or_empirical": "FORMAL", "status": "OPEN", "blocks_what": ["R7-E1 harness validity"] },
    { "po_id": "PO-NCI-03", "claim": "Byte/Referent/Causal checks are orthogonal", "formal_or_empirical": "EMPIRICAL", "status": "OPEN", "blocks_what": ["Triade]"], "does_not_block_what": ["PGI classification"] },
    { "po_id": "EO-NCI-01", "claim": "Direct symbiosis reduces human-mediated transport error", "formal_or_empirical": "EMPIRICAL", "status": "OPEN", "blocks_what": ["Direct-Symbiosis lane promotion"] },
    { "po_id": "EO-NCI-02", "claim": "NCI composition does not cause excessive false blocking", "formal_or_empirical": "EMPIRICAL", "status": "OPEN", "blocks_what": ["COMPOSED_NCI mode selection"] },
    { "po_id": "EO-NCI-03", "claim": "Unknown-state handling survives harness summarization", "formal_or_empirical": "EMPIRICAL", "status": "OPEN", "blocks_what": ["R7-E1 pass criterion"] },
    { "po_id": "EO-NCI-04", "claim": "Harness TP/FP/FN/latency within success criteria", "formal_or_empirical": "EMPIRICAL", "status": "OPEN", "blocks_what": ["PASS_C1 terminal state"] }
  ]
}
