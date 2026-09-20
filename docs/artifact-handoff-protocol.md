# NEXUS OMEGA Artifact Handoff Protocol v1

```text
OBJECT = NEXUS_OMEGA_ARTIFACT_HANDOFF_PROTOCOL_V1
STATE = RESEARCH_PIPELINE_INFRASTRUCTURE_CANDIDATE
PROTOCOL = INBOX_VALIDATE_BIND_RELAY_ACK_V1
CLAIM_CEILING = C0_EXPLORATORY / C1_DESCRIPTIVE
CLAIM_PROMOTION = FALSE
FOUNDATION_PROMOTION = FALSE
MERGE_AUTOMATION = FALSE
FORCE_PUSH = FALSE
```

This protocol defines the canonical GitHub path for external agent and Cursor
returns that should continue without routine Operator mediation.

It is a transport, byte-binding and workflow-order protocol. It does not
validate scientific truth, promote a claim, promote a foundation, merge code, or
grant integration authority.

## Flow

```text
INBOX
-> VALIDATE
-> BIND
-> RELAY
-> ACK
```

## Canonical location

```text
research/pipeline/handoff/
├── README.md
├── inbox/
├── bound/
├── relay/
└── ack/
```

`inbox/` receives one handoff directory per return. A valid handoff directory
contains a `handoff.json` envelope that references the returned bytes, Entry
Receipt, Exit Receipt, File-Event Ledger and Workflow-Event Ledger.

`bound/`, `relay/` and `ack/` are generated protocol stages. They may be created
locally by `scripts/artifact_handoff.py` or emitted by GitHub Actions as run
artifacts.

## Fail-closed rules

A handoff closes instead of relaying when any of these conditions is present:

- required bytes are missing or have different SHA-256 or byte length;
- JSON or JSONL contains duplicate keys, invalid encoding, blank lines, or
  carriage returns;
- `claim_promotion`, `foundation_promotion`, `force_push` or `main_write` is
  true;
- merge or integration authority is anything other than `NONE`;
- the producer and validator are the same agent identity;
- the handoff asks the validator to validate its own scientific return;
- an Authority-Gate is open;
- continuation is required but no continuation capsule is bound.

## Authority-Gates

The Operator is asked only when a return crosses a non-delegable boundary:

```text
MERGE
CLAIM_PROMOTION
FOUNDATION_PROMOTION
MAIN_WRITE
FORCE_PUSH
SECRET_ACCESS
PUBLIC_RELEASE
DEPLOYMENT
INTEGRATION_AUTHORITY
```

Routine byte binding, receipt generation, ledger parsing, GitHub check
execution and relay packet creation are not Authority-Gates.

## Token and continuation handling

Every handoff records requested token class, used token class if exposed,
telemetry exposure and continuation status. If token pressure prevents closure,
the return must include a continuation capsule path and that file must be
byte-bound before relay.

## R3 seed

The first v1 inbox object is the current R3 completion return on PR15:

```text
HANDOFF_ID = NEXUS_AH_20260902T192400Z_r3-completion-symbiosis_R0
SOURCE_BRANCH = axiom/agent-authorization-admission-r3-open-research-20260902
SOURCE_COMMIT = 5c1dc9df32fd8d96277e98ef754602d9726e52d7
R2_PR13_SEPARATION = PRESERVED
```

It preserves the R3 caveats: C0/C1 only, non-QWEN producer, no merge, no claim
promotion, no foundation promotion, R2/PR13 not integrated, and no external
semantic validation.
