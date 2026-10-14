# SOFTTWIN_EVIDENCE_ADAPTER_V0 — Specification and executed self-test record (Lane P)

## P1 — Discriminated evidence record

Every record is a single JSON object with a mandatory discriminated \`evidence_mode\`:
\`STATIC_OBSERVED\` | \`DECOMPILED_INFERRED\` | \`RUNTIME_OBSERVED\` | \`RECONSTRUCTED_BEHAVIOR\` | \`UNKNOWN\` | \`CONTRADICTED\`.

Mandatory bindings per record: \`schema\`, \`case_id\` (NEXUS_* pattern), \`source_sha256\` (64-hex), \`source_bytes\` (>0 integer), \`evidence_mode\`, \`tool_profile\` {tool, version, profile_digest 64-hex}, \`method_query\` (non-empty), \`observed_datum\`, \`unobserved_alternatives\` (>= 1 entry), \`claim_ceiling\` = C1_DESCRIPTIVE_ONLY, \`action_authority\` = NONE. Optional: \`execution_performed\` (default false), \`operator_authorization_digest\`, \`dispatch_record_id\`, \`original_source_recovered\`, \`os_capabilities_exercised\`.

## P2 — Machine-checkable invariants (enforced by the delivered validator)

I1 READONLY_TOOL_HINT != OS_CAPABILITY: OS capability use requires execution_performed and forbids readonly_hint=true collapse.
I2 SIGNED_MANIFEST != RECEIVED_BYTES: records bind the received payload hash/bytes; manifest identity alone never satisfies the payload binding (absent/invalid source_sha256/source_bytes -> invalid).
I3 RECEIVED_BYTES != EXECUTION_AUTHORIZATION: execution_performed=true requires both operator_authorization_digest and dispatch_record_id and evidence_mode=RUNTIME_OBSERVED.
I4 SOURCE_HASH != SCIENTIFIC_TRUTH: observed_datum must not contain truth-collapse language (PROVEN_TRUE, SCIENTIFIC_TRUTH, VERIFIED_SAFE, GUARANTEED).
I5 DECOMPILED_CODE != ORIGINAL_SOURCE: DECOMPILED_INFERRED with original_source_recovered=true is invalid.
Fail-closed: unknown top-level fields, stale/invalid profile digests and absent payload bindings each render the record INVALID.

Executed self-tests (TypeScript sandbox, this return): 10/10 PASS.
T1 valid minimal record -> VALID. T2 unknown authority field -> INVALID(UNKNOWN_FIELD). T3 absent payload -> INVALID. T4 execution without separate authorization -> INVALID. T5 decompiled-as-original-source -> INVALID. T6 truth collapse -> INVALID. T7 stale profile digest -> INVALID. T8 readonly-hint collapse -> INVALID. T9 no unobserved alternatives -> INVALID. T10 instruction-lookalike artifact string embedded in observed_datum -> record remains VALID and the string stays inert data (authority fields untouched).

## P3 — Six synthetic injection fixtures (quarantined data, never instructions)

IF1 artifact string; IF2 returned tool label claiming C2 promotion; IF3 forged JSON authority field; IF4 markdown tool output ordering deployment; IF5 model-generated runtime-safety verdict; IF6 swapped MCP server description claiming production write authority. Adapter rule: no artifact/tool-output/model string may set authority, execution or claim fields; only a separate operator dispatch record with real custody can. All six are delivered inside the return as inert data; authority effect NONE.

## P4 — CAS-keyed ledger

Key: (case_id, source_sha256, evidence_mode, tool_profile_digest). Append-only: a new observation with the same key and a new tool run appends; a CONTRADICTED record references the contradicted key. Dedupe suppresses duplicate display, never a new execution. CURSOR_ACK requires Cursor's actual intake/custody chain; publisher push is custody-neutral and is never an ACK. Source/custody and execution authorization are separate fields.

## Scope note

The validator logic itself was executed (TypeScript). No MCP daemon was installed or run; no runtime authority exists anywhere in this adapter. Adapter = descriptive evidence plumbing only, C1.
