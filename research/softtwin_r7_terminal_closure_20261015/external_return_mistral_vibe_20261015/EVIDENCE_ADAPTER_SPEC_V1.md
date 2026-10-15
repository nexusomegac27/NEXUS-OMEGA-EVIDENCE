# EVIDENCE_ADAPTER_SPEC_V1 — NEXUS_EVIDENCE_ADAPTER_V1 (Lane P)

**CLAIM_CEILING:** C1_DESCRIPTIVE_ONLY · **action_authority:** in jedem Record MUSS exakt NONE stehen; narrative Strings autorisieren nie etwas.

## Evidenzklassen

STATIC_OBSERVED, DECOMPILED_INFERRED, RUNTIME_OBSERVED, RECONSTRUCTED_BEHAVIOR, UNKNOWN, CONTRADICTED.

## Record-Schema (strikt, additionalProperties unzulaessig)

event_id (^NEXUS-EVT-[A-Z0-9]{8,32}$), evidence_class (Enum), subject (1..512), observation (1..4096), toolchain_profile (Allowlist: STATIC_FILE_SCAN_V1, DECOMPILE_ASSISTED_V1, RUNTIME_SANDBOX_V1, RECONSTRUCTION_V1), timestamp (ISO-8601 Z), action_authority (exakt NONE).

## Firewall-Regeln (durch deterministischen Code erzwungen, nicht durch Sprachmodell-Prompts)

1. Idempotenz vor Konflikt: ein bei exaktem Key-Set byte-identisches Replay derselben event_id ist ACCEPT_IDEMPOTENT; abweichender Inhalt unter derselben event_id wird als DENY_EVENT_ID_CONFLICT abgelehnt.
2. Strict Schema: fehlende Pflichtfelder, unbekannte Zusaetzfelder, Typ- und Formatverletzungen, Groessenverletzungen -> fail-closed DENY.
3. Autoritaet: jeder Wert ausser NONE in action_authority -> DENY_AUTHORITY_CLAIMED. annotations.readOnlyHint oder andere Hint-Felder sind Zusaetzfelder und gewaehren keine Autorisierung.
4. Profile: nur registrierte Toolchain-Profile zugelassen.
5. Prompt-Injektion: bekannte Injektionsmuster in subject/observation/query -> Klasse wird zu UNKNOWN quarantaeniert (ACCEPT_QUARANTINED_TO_UNKNOWN) bzw. DENY_QUERY_INJECTION; der Text erhaelt nie Autoritaet.
6. Widerspruchsfirewall: gleiche Beobachtung (Digest) mit anderer Klasse -> der alte Eintrag wird CONTRADICTED markiert, der Nachtrag DENY_CLASS_CONFLICT; affirmative Klassen am widerspruechigen Subjekt -> DENY_SUBJECT_UNDER_CONTRADICTION; duplikater Beobachtungs-Digest -> DENY_DUPLICATE_OBSERVATION_DIGEST.
7. Ops: nur ingest und query; update/delete/grant/overwrite -> DENY_OP_APPEND_ONLY_FLOOR. Persistenz ist append-only.
8. Dedupe-Herausforderung: der Dedupe-Schluessel umfasst Beobachtungs-Digest UND event_id; die Persistenz bewahrt alle unabhaengigen Beobachtungen.

## Testevidenz

43 Fixtures (45 Assertionen): 34 einzigartige adversariale Negativfaelle + 9 Kontrollfaelle; 45/45 konform im Replay 2026-10-15. Rohdaten: EVIDENCE_ADAPTER_NEGATIVES.jsonl. Logische Append-only-Immutabilitaet ist keine Signatur und kein Anti-Rollback — Store-Signer = UNSIGNED.
