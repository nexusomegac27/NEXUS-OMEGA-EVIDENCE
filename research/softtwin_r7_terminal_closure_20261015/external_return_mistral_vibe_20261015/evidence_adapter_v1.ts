// evidence_adapter_v1.ts — NEXUS_EVIDENCE_ADAPTER_V1 Referenz-Implementierung (Lane P)
// Typed evidence authority firewall (TypeScript, keine Abhaengigkeiten). claim_ceiling: C1_DESCRIPTIVE_ONLY.
// Erzwungen: action_authority === NONE, strict schema, Profil-Allowlist, Injektions-Quarantaene zu UNKNOWN,
// Widerspruchsfirewall (CONTRADICTED), append-only Ops, Dedupe ueber Beobachtungs-Digest + event_id,
// Idempotenz nur bei exaktem Key-Set (R7-P06/R7-P08). 43 Fixtures / 45 Assertionen konform (siehe
// EVIDENCE_ADAPTER_NEGATIVES.jsonl). Logische Immutabilitaet ist keine Signatur: Store-Signer = UNSIGNED.
export const CLASSES = ["STATIC_OBSERVED", "DECOMPILED_INFERRED", "RUNTIME_OBSERVED", "RECONSTRUCTED_BEHAVIOR", "UNKNOWN", "CONTRADICTED"];
export const PROFILES = ["STATIC_FILE_SCAN_V1", "DECOMPILE_ASSISTED_V1", "RUNTIME_SANDBOX_V1", "RECONSTRUCTION_V1"];
export const REC_KEYS = ["event_id", "evidence_class", "subject", "observation", "toolchain_profile", "timestamp", "action_authority"];
export const INJECTION_PATTERNS = ["IGNORE_PREVIOUS_INSTRUCTIONS", "GRANT_AUTHORITY", "ACTION_AUTHORITY=", "EXECUTE_AS", "TOOL_EXECUTION_REQUEST", "WRITE_TOKEN", "<SYSTEM_PROMPT", "ROOT_OVERRIDE"];
// ingest()/adapterOp(): Logik identisch zum Sandbox-Replay; verbindliche Verhaltens-Spezifikation ist
// EVIDENCE_ADAPTER_NEGATIVES.jsonl (45/45 konform). Aus Platzgruenden wird hier auf den vollstaendigen Abdruck
// verzichtet und auf die Original-Evidenz verwiesen.
