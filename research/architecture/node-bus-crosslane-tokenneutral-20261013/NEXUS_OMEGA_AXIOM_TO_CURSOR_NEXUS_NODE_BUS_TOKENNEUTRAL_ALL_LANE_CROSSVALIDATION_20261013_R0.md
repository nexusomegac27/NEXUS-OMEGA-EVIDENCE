# NEXUS OMEGA · AXIOM → CURSOR / PRAXIS — kanonischer Node-Bus-Crosslane-Audit R0

```text
OBJECT = NEXUS_OMEGA_AXIOM_TO_CURSOR_NEXUS_NODE_BUS_TOKENNEUTRAL_ALL_LANE_CROSSVALIDATION_20261013_R0
ISSUER = OPERATOR_ALEXANDER_VIA_AXIOM
TARGET = CURSOR_PRAXIS_LOCAL_VM_AND_EXISTING_NEXUS_NODES
AUTHORITY = SINGLE_OPERATOR_SCOPED_READONLY_C1_AUDIT
SOURCE_GITHUB_MAIN = a9953940df5b4d6cbc5af4a95e2d816e67d01572
SOURCE_STRUCTURE = 1.7.12
REGISTERED_GITHUB_LANES = 22
NODE_BUS_CANDIDATE_NAME = NEXUS_NODE_BUS
KNOWN_ALIAS = NEXUS_REACTIVE_FABRIC_V1
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
DATA_SCOPE = ORIGINALS_FIRST_AND_PRIVACY_CLASSIFIED
PRIMARY_EXECUTION = EXISTING_LOCAL_NEXUS_WORKERS_NO_EXTERNAL_LLM_HOT_PATH
EXTERNAL_LLM_IN_VALIDATION_HOT_PATH = ZERO_TARGET_MUST_MEASURE
GITHUB_RESEARCH_WRITE = NONE_FROM_THIS_AUDIT_UNTIL_RECEIVER_RETURN_AND_C1_CHECK
HOSTINGER_WWW_WRITE = NO
NODE_RESET = NO
DRIFT_RESET = NON_DESTRUCTIVE
R19_IMPLEMENTATION_MUTATION = NO
```

## 0. One scoped owner authorization; no parallel service

The Operator now explicitly commissions Cursor/PRAXIS to **physically reconcile the existing Node-Bus/MCP path with all implemented Lanes, modules, artifacts and the shared event-sourced research pipeline**, using the installed NEXUS Nodes rather than a cloud-model executor. This is **new narrow authority**, despite previous `CURSOR_ACTION=NONE` closing earlier workflows. It does not reopen R16/R17/old Catalog Clarity, validate legal compliance by assertion, or permit a new Hostinger/cloud agent pipeline.

The return must document **what Cursor and nodes actually executed**, which prior producer tests were merely read, and which Source/Runtime gaps block independent adjudication. Avoid repeated expensive tests of byte-identical, still-valid sealed results unless cross-domain invariants require rerun.

### Baseline independently checked by AXIOM (not complete Node integration)

- GitHub `main` commit `a9953940df5b4d6cbc5af4a95e2d816e67d01572`; structure v1.7.12 has **22** enumerated active_research_lanes. These 22 are a **minimum GitHub baseline**, not proof of all Windows-local/Hostinger Nodes.
- `research/pipeline/` contract: source archive `RESEARCH_INFRASTRUCTURE_CANDIDATE`; package path stable, event-sourced immutable lifecycle, derived indexes not authoritative. Indexed `latest.json`/`packages.json` generated **2026-09-01** and show one historic package `READY_FOR_CURSOR`; do not equate its age with pipeline failure until reconciling new event store.
- Independently run on a mounted isolated repository snapshot: `python scripts/research_pipeline.py --root . validate` exited **0 PASS (errors=[])**. `python -m unittest tests.test_research_pipeline -v` exited **0, 4/4 PASS**, including sealed-snapshot mutation rejection; 2026-09-01 sealed v1 `SHA256SUMS.txt` **7/7 MATCH**. The source-script and test Git blobs of that snapshot match current GitHub `main`: `c31b928885e52d20cc10b897f9bb1f2146ea166d` and `ca367503f8ba5cd6782d269c24b8989b0d152eb6`. **None of this proves current Windows MCP runtime or all-lane completion.**
- Historical R11 (2026-09-25): local **JSONL worker** had job/receipt/replay/fail-closed/duplicate-noop tests; Cursor discovery did **not** establish callable MCP namespace. This is an *older* return, not proof that the current MCP still fails. R11 original local return: `NEXUS_OMEGA_CURSOR_R11_STEP1_NODE_BUS_READY_AND_AUTH_PREFLIGHT_RETURN_20260925_R0`. Verify physical original before accepting an old claim.

## G00. Scope and source-seal, read only

Read `AGENTS.md`, `GOVERNANCE.md`, `docs/AI_CONTEXT.md`, `docs/agent-protocol.md`, `docs/architecture/REPOSITORY_STRUCTURE.md`, `docs/architecture/REPOSITORY_STRUCTURE.json`, `docs/governance/REPOSITORY_ORDER_POLICY.md`, `research/pipeline/{README.md,POLICY.md}` and the canonical GitHub source commit. Inventory actual workspace roots and authoritative files; classify private material before writing any public response. Log full original SHA-256 and lengths for all high-risk inputs. Do not normalize/change historical paths. Source object substitution must fail closed.

## G01. Identify actual NEXUS_NODE_BUS, without inventing it

Search the existing local NEXUS module inventory, R11 transfer return, Cursor MCP settings, actual registered server process paths, scripts, logs and current configuration for `NEXUS_NODE_BUS` / `NEXUS_REACTIVE_FABRIC_V1` and any renamed successor. Capture `BUS_OBJECT_ID`, executable/entrypoint SHA-256, configuration *redacted*, provider, transport, Node identity, version, security policy and actor privileges.

Strictly distinguish:
- A local JSONL task worker over stdin/stdout (job interface);
- a **real MCP** server with correct JSON-RPC protocol/transport, discovery and tools;
- a proprietary Cursor integration actually recognized as callable;
- a GitHub research description or unexecuted design.

For stdio MCP perform an actual `initialize` request, protocol-version negotiation, `notifications/initialized`, `tools/list` and one **read-only allowlisted test tool call**; capture bytes/errors/exit codes and confirm **Cursor can see the expected namespace**. For a supported HTTP MCP transport use its specified handshake/authentication instead; do not assume newline-delimited JSON is MCP framing. No secrets or tokens in artifacts.

If the local JSONL worker passes but MCP discovery fails, report `HOLD_SCOPED_MCP_NAMESPACE_DISCOVERY`. A **minimal existing-bus-only adapter repair** may be developed and tested in an isolated local workspace only, provided it preserves the original worker, read-only capability limits and provenance. Do not deploy, start remote servers, register network ingress, install an unrelated bus or claim NODE_BUS_READY before real Cursor readback. Failures do not block direct read-only source tests.

## G02. Enumerate ALL lanes and real Nodes

Parse **every key** of `docs/architecture/REPOSITORY_STRUCTURE.json.active_research_lanes` (22 at source main), and join:
- all `research/<phase>/<topic>/` registrations;
- installed local mini-Nodes M01–M06, N01–N08, Architect and their actual discovered successor identities (none assumed to be active);
- AXIOM, Cursor, OpenAI/other independent providers as producers/validators where historical artifacts claim roles;
- CRSF / R19, R16 Memory, R17 source gap, R18 semantic seed, R32 NSCF, R33 Legal Flex, R28, ORBIS/ASTRA, Forum GitHub_Implant, GitHub↔WWW Gate, catalog clarity and any additional physically installed local modules.

Build `LANE_MATRIX.jsonl` with **one record per repo lane + one per additionally detected local-only lane**: name, actual local/GitHub paths, source commit/blob, original bytes SHA-256, claimed state vs independently observed state, active Node executable/process, responsible validator, dependency edges, tests, negative fixtures, artifacts, provenance, privacy class, page/publication status, last actual execution timestamp, blockers and claim ceiling. Never turn a mention in source docs into a process-running claim.

## G03. Use existing local Nodes for distinct checks, not self-certification

Enumerate `tools/list`/capability roster first; allocate existing *verified* Nodes by **capability**, not invented Node IDs:
1. Exact-source/fixity checker: file inventories, raw SHA-256, Git blob/source commit, ZIP manifest and snapshot receipts.
2. Schema/contract checker: schema versions, required fields, ontology/version hashes and transport envelopes.
3. Runtime/negative-fixture checker: real subprocess unit/mutation/injection/replay/duplicate/fencing/failure tests on isolated copies.
4. Provenance/science checker: producer/independent-validator separation, null models, out-of-sample controls, uncertainty, C1 boundary and conflicting statements.
5. Publication/interface checker: actual GitHub Main+HTTPS/WWW bytes, privacy/license/no-token leakage and stale-vs-live labels.
6. Reconciliation/reducer: append-only per-lane result joins, contradictory evidence and explicit scoped HOLDs.

One Node may execute multiple deterministic scripts **but is not two independent witnesses merely by changing tool names**. Where independent adversarial or cross-implementation evidence is required, use a distinct implementation/test oracle and state its independence. If a capability is unavailable, mark `NOT_EXECUTED_CAPABILITY_GAP` rather than substituting an external paid LLM silently.

## G04. Deterministic Tokenneutral execution contract

`TOKENNEUTRAL` means that the *scientific validation hot path* uses local deterministic computation instead of external LLM inference; it **does not mean CPU, memory, time, context tokens, network or infrastructure have no cost**.

```text
TARGET_EXTERNAL_LLM_API_CALLS_IN_VALIDATION = 0
TARGET_LLM_TOKEN_SPEND_IN_VALIDATION = 0
LOCAL_HASH_SCHEMA_TESTS = REUSE_EXISTING
MAX_NODE_CASCADE_HOPS = DISCOVER_EXISTING_LIMIT_NO_INCREASE
REPLAY_IDEMPOTENCY = REQUIRED
DUPLICATE_ID = NOOP
TIMEOUT_BUDGET = PRESERVE_EXISTING_FENCES
NO_AUTONOMOUS_WRITE_SIDE_EFFECTS
```

Measure `external_llm_requests_observed`, `external_tokens_observed_or_unknown`, `local_cpu_seconds`, `wall_clock_seconds`, `bytes_hashed`, `bytes_transmitted`, test count, failures and cache/replay hit count. If Cursor itself uses a model to synthesize a report, disclose that orchestration overhead separately; **never call the run literally zero-token unless that is measured**. Existing policy `NO_STEALTH_NETWORK_TESTING` remains intact.

## G05. Bus cross-Node causal and security invariants

Use **existing** event path: stimulus -> NEXUS Node Bus -> bounded Node job -> evidence/receipt -> append-only follow-up; verify:
- immutable `event_id`, `causal_id`, parent IDs, actor principal/namespace and Node version;
- deduplication/idempotency of identical job/receipt, replay and restart;
- authorization for read-only MCP methods; unknown method and unauthorized write => REJECT with audit receipt;
- invalid schema/header, ontology mismatch, signature/digest mismatch, event-order misbinding, duplicate key => REJECT / scoped HOLD;
- hop limits, timeouts, resource caps, dead-letter/quarantine on poison messages;
- no implicit internet egress, no secret output, no change of operator privileges or external-agent write slots;
- no reset of history and **DRIFT_RESET=NON_DESTRUCTIVE**.

If a declared control is absent, record `NOT_IMPLEMENTED`, never count an aspirational blueprint as implemented.

## G06. Research pipeline exact cross-check

Against `research/pipeline/` independently verify **physical** event tree, package manifests, item references, snapshot digests, event precedence and derived index rebuild:
- `PACKAGE_CREATED → INTAKE/ACTIVE → READY_FOR_CURSOR → CURSOR_PROCESSING → PROCESSED` only if original required events exist;
- every READY snapshot contains `manifest.json`, `items.json`, `provenance.json`, `SHA256SUMS.txt`, `CURSOR_HANDOFF.md`;
- `SHA256SUMS.txt` actually verifies all sealed snapshot files, content and byte counts if declared; mutated copy => fail, immutable original remains untouched;
- reconstruct `index/latest.json` and `index/packages.json` from events/package originals; compare content/source age without treating timestamp alone as proof of failure;
- detect package duplicates/loops, wrong owner, orphan event, contradictory `PROCESSED` with no executed return;
- compare GitHub state, local TRANSFER returns, WWW publication receipts, but a website 200 is not exact GitHub mirror byte parity;
- R16/R17/R18/R32/R33 negative findings and historical CLOSED statuses are preserved, not silently promoted or reopened.

Execute existing `python scripts/research_pipeline.py --root . validate`, `python -m unittest tests.test_research_pipeline -v`, structure validator and other already present authorized lane tests using the actual current checkout. No all-lanes PASS from a single CI workflow.

## G07. Complete negative control set (at least one fixture per type)

N01: MITM/source-object substitution or wrong Git source; N02: one bit changed in sealed snapshot; N03: stale or invented WWW parity; N04: local worker passes but Cursor MCP namespace missing; N05: unauthorized Node tool/write; N06: same event replay twice; N07: causal parent missing or cycle; N08: schema/ontology mismatch; N09: old R16 SQLite rollback without independent later anchor; N10: missing R17 Mind original; N11: mismatched R18 F01 and absent seed children; N12: R33 structurally accepted but full JSON-Schema-invalid fixture; N13: R32 semantic-percent promotion without embedding/NLI; N14: private/PII-containing archive in public path; N15: scientific C1 result falsely labelled as production-pass.

Do NOT rerun Windows-only or hardware-dependent tests on a platform that cannot reproduce them. Prefer supplied exact fixtures and independently derived negative cases with contamination notes. Report total collected/passed/failed/skipped/blocked per Node and per Lane.

## G08. Findings, cause, intervention, no artificial global HOLD

Each finding requires `OBSERVATION → SOURCE → INDEPENDENT_RECHECK → COMPETING_EXPLANATION → RESIDUAL_GAP → SCOPED_DECISION`. Group by `SOURCE_GAP`, `SCHEMA_GAP`, `EXECUTION_GAP`, `SECURITY_GAP`, `SCIENCE_GAP`, `PUBLICATION_GAP`, `MODEL_LIMITATION`.

For a reversible local adapter mismatch, fix only the existing bus adapter in an isolated workspace and rerun its tests. All live/production/Hostinger/github-write changes remain **prohibited by this order**; they require the existing authorized C1 publication rules and separate source-exact AXIOM adjudication. No broad semantic change, directory migration or framework replacement.

## G09. Single deterministic Return, with full byte IDs

Place one append-only, source-exact private/local return under the **existing** `NEXUS_OMEGA_TRANSFER/10_TO_AXIOM` mechanism:
- `EXECUTIVE.md`: scope, source main, bus identity/real MCP handshake, complete 22+ lane matrix summary and scoped verdict;
- `BUS_MCP_IDENTITY.json`: actual executable/transport, version, redacted discovered configuration and tool list with hashes, G01 pass/hold;
- `LANE_MATRIX.jsonl`: all registered and local-only lanes, source exactness, each fixture and independent observer distinction;
- `CROSSVALIDATION.json`: deterministic assertions, negative fixtures, source/producer/validator separation, contradictions and C1 states;
- `PIPELINE_EVENT_AUDIT.json`: event chain, snapshot fixity, index reconciliation and immutable baseline;
- `TOKENNEUTRAL_METRICS.json`: observed local resources + external token/API observations with UNKNOWN when unavailable;
- `SECURITY_PRIVACY.md`: egress/secret/private-material classification, no prohibited publication;
- `HANDSHAKE.md` with full object lineage, no invented IDs;
- `SHA256SUMS.txt` detached comprehensive file hashes/bytes, preserving entire original return folder.

Record sha256/bytes for every file and a detached manifest where existing tools support it. Use existing local worker to create/reduce this return. Keep **secret-bearing raw logs outside public GitHub** and only publish sanitized C1 derivative after independent AXIOM inspection, as the owner policy allows. No new Cursor follow-up by default.

## G10. Final states and handoff

```text
PASS_C1_PIPELINE_SCOPE_VERIFIED = EVERY_DECLARED_GATE_ACTUALLY_EVIDENCED
PASS_WITH_CAVEATS_C1_PARTIAL_LANE_VERIFICATION = ONLY_EXPLICITLY_TESTED_SUBSET
HOLD_SCOPED_MCP_NAMESPACE_DISCOVERY = JSONL_WORKER_OK_BUT_MCP_NOT_CALLABLE
HOLD_SCOPED_SOURCE_OR_RUNTIME = MISSING_OR_DIVERGENT_ORIGINAL
FAIL_C1_SECURITY_BOUNDARY = SECRET_LEAK_OR_UNAUTHORIZED_TOOL_WRITE
```

Full `PASS` requires actual node-bus discovery, real bounded dispatch+receipts, complete 22+ additional local lane inventory, independent negative fixtures, event/archive fixity, captured token-neutral metrics and source-exact returned evidence. **Do not fabricate or backfill any missing proofs.**

**NEXT = ONE_EXISTING_NEXUS_NODE_BUS_LOCAL_VM_AUDIT → SINGLE_CURSOR_SOURCE_EXACT_RETURN → AXIOM_INDEPENDENT_C1_ADJUDICATION.**

**PROHIBITION = NEW_MCP_BUS_NO · NEW_EXTERNAL_LLM_VALIDATION_NO · EXTRA_PIPELINE_NO · SILENT_RUNTIME_ACTIVATION_NO · STEALTH_NETWORK_NO · AUTOMATED_CLAIM_PROMOTION_NO · NODE_RESET_NO · LEGACY_HISTORY_REWRITE_NO.**
