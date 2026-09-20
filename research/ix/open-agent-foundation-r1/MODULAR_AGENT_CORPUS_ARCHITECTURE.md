# Modular NEXUS Agent Corpus Architecture — R1

## Status

```text
STATE = RESEARCH_FOUNDATION_C1
IX_EXECUTION = NOT_STARTED
ACTIVATION = NO
PRODUCTION_STACK = NOT_SELECTED
```

## 1. Continuity body

The NEXUS agent body is defined independently of any model/runtime:

```text
NEXUS_AGENT_BODY
├── F0 CONSTITUTION / GOVERNANCE
├── F1 CANONICAL CHECKPOINTS
├── F2 EVIDENCE / SOURCE OBJECTS
├── F3 METHODS / CODE / TESTS
├── F4 NEGATIVE KNOWLEDGE
├── F5 OPERATIONAL MEMORY / RECOVERY
├── CAPABILITY REGISTRY
└── AUTHORIZATION STATE
```

F4 is first-class: failed methods, rejected assumptions, loop patterns, source substitutions,
overclaims, HOLDs and non-reproducible results must remain discoverable.

## 2. Adapter boundary

All replaceable computation sits outside the continuity body:

```text
                 ┌───────────────────────────┐
                 │  CANONICAL NEXUS BODY     │
                 │ evidence / policy / state │
                 └─────────────┬─────────────┘
                               │ contracts
       ┌───────────────────────┼────────────────────────┐
       │                       │                        │
 MODEL ADAPTER          TOOL/PROTOCOL ADAPTER     RUNTIME ADAPTER
       │                       │                        │
 open weights /         MCP / A2A / local         llama.cpp /
 proprietary opt.       tools / peer nodes        vLLM / LocalAI
```

No adapter owns canonical identity.

## 3. Suggested research modules

These are **candidate interfaces**, not a selected stack:

- **Core state:** content-addressed files + SQLite/DuckDB-compatible index.
- **Retrieval acceleration:** Qdrant/pgvector-class vector indexes; rebuildable from canonical objects.
- **Model runtime:** llama.cpp, vLLM, LocalAI, or equivalent adapters.
- **Open-weight model:** Qwen3/Granite-class candidates; model cards and exact licenses bound per experiment.
- **Agent-framework adapter:** smolagents/AutoGen/OpenHands-class candidates; optional.
- **Tool protocol:** MCP-compatible boundary.
- **Agent protocol:** A2A-compatible boundary where inter-agent transport is needed.
- **Durable work:** append-only atomic work-unit ledger; Temporal is an optional implementation candidate.
- **Messaging:** NATS-class optional bus; never source of truth.
- **Workload identity:** SPIFFE/SPIRE-class candidate.
- **Policy:** OPA-class candidate.
- **Secrets:** OpenBao-class candidate for distributed deployments.
- **Sandbox:** Firecracker-class candidate for Linux microVM isolation where justified.
- **Supply chain:** in-toto + Sigstore/cosign + SLSA-compatible provenance.
- **Observability:** OpenTelemetry-compatible events/metrics/traces.

## 4. Atomic work-unit contract

Every long-running action must be resumable across provider/runtime failure.

Minimum work unit:

```text
WORK_UNIT_ID
PARENT_UNIT_ID
TASK_CONTRACT_SHA256
CANONICAL_HEAD
INPUT_SET_SHA256
METHOD_SHA256
EXECUTOR_CLASS
START_STATE
OUTPUT_SET_SHA256
VALIDATION_STATE
OPEN_GAPS
NEXT_ACTION
```

A quota stop therefore becomes:

```text
EXECUTION_PAUSE
```

not work loss.

## 5. Recovery invariant

A substitute runtime may continue only after verifying:

1. canonical head;
2. parent work unit;
3. input hashes;
4. task contract;
5. authorization state;
6. unresolved caveats.

```text
MODEL_FAILOVER != CANON_RECONSTRUCTION
```

## 6. Evidence-delta gate

An agent response does not advance the canon merely because it is new text.

```text
EVIDENCE_DELTA =
NEW_BYTES
+ NEW_SOURCE
+ NEW_EXECUTION
+ NEW_METHOD
+ NEW_COUNTEREVIDENCE
+ NEW_CORRECTION
+ NEW_INDEPENDENCE
```

If all terms are zero:

```text
NO_NEW_EVIDENCE
=> NO_CANON_ADVANCE
```

This gate is mandatory for multi-agent loop resistance.

## 7. External resources

Federated resources are capability objects, never authority objects.

Each resource should bind:

```text
RESOURCE_ID
RESOURCE_TYPE
UPSTREAM
LICENSE
OPENNESS_VECTOR
AUTH_REQUIRED
RATE_LIMIT
COST_CLASS
DATA_PROVENANCE
REPRODUCIBILITY
TRUST_BOUNDARY
FAILOVER
TERMS_SNAPSHOT
```

SatNOGS, CERN Open Data, volunteer-compute networks and public cloud datasets are examples of
resource classes, but none are foundational dependencies.

## 8. BodyTwin analogy boundary

The reusable BodyTwin principle is continuity under replaceable rendering/execution substrates:

```text
BODYTWIN REPRESENTATION != PERSON
AGENT BODY != MODEL
```

The analogy grants no personhood, mental state, biological claim or truth authority.

## 9. R2 falsification targets

R2 should try to break the foundation:

- remove the preferred model and resume on another runtime;
- terminate a provider session mid-work-unit;
- rebuild retrieval indexes from canonical objects;
- replay from a known checkpoint without chat history;
- corrupt one source object and require hash-fail closure;
- deny one capability by policy without blocking unrelated lanes;
- run the same task through two framework adapters and measure evidence delta;
- simulate a quota limit and verify zero scientific state loss.

Success is not “the agent answered.” Success is continuity of verified state with preserved caveats.
