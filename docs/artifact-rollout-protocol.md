# NEXUS OMEGA Artifact Rollout Protocol v1

```text
OBJECT = NEXUS_OMEGA_ARTIFACT_ROLLOUT_PROTOCOL_V1
STATE = PR15_ARTIFACT_HANDOFF_ROLLOUT_PREP_C1
PROTOCOL = PR15_ARTIFACT_HANDOFF_ROLLOUT_PREP_V1
CLAIM_CEILING = C0_EXPLORATORY / C1_DESCRIPTIVE
ROLL_OUT_EXECUTION = FALSE
MERGE_AUTOMATION = FALSE
CLAIM_PROMOTION = FALSE
FOUNDATION_PROMOTION = FALSE
FORCE_PUSH = FALSE
```

This protocol prepares a complete, separate rollout package for a GitHub-hosted
artifact handoff chain. It is a readiness, packaging and gate-routing protocol.
It is not a merge, release, foundation promotion, claim promotion or
integration-authority grant.

## Flow

```text
PREPARE
-> VALIDATE
-> PACKAGE
-> AUTHORITY_GATE
-> ACK
```

The automated part stops at `AUTHORITY_GATE`. Any later merge, main write,
release, deployment, claim promotion, foundation promotion, force-push or
integration-authority step requires an explicit Operator receipt.

## Canonical location

```text
research/pipeline/rollout/
├── README.md
├── plans/
└── receipts/
```

`plans/` contains immutable rollout-preparation plans. `receipts/` contains
generated readiness receipts, authority-gate packets, acknowledgement receipts
and workflow-event ledgers.

## Fail-closed rules

A rollout-preparation plan fails closed when any of these conditions is present:

- required source bytes are missing or have different SHA-256 or byte length;
- JSON or JSONL contains duplicate keys, invalid encoding, blank lines, or
  carriage returns;
- execution is enabled before an Operator authority receipt exists;
- merge, main-write, force-push, release or deployment automation is enabled;
- claim or foundation promotion automation is enabled;
- self-validation is asserted;
- PR15/R3 source head or seed handoff identity is changed without a successor
  rollout plan;
- R2 and PR13 separation is weakened;
- token pressure requires continuation but no continuation capsule is bound.

## Authority-Gates

The rollout package can prepare material up to these gates, but cannot close
them:

```text
MERGE
MAIN_WRITE
FORCE_PUSH
PUBLIC_RELEASE
DEPLOYMENT
CLAIM_PROMOTION
FOUNDATION_PROMOTION
INTEGRATION_AUTHORITY
SECRET_ACCESS
```

Automated validation may mark a gate `PENDING_OPERATOR` or `NOT_REQUESTED`.
It may not mark a gate closed.

## PR15 seed rollout

The first v1 rollout-preparation object is bound to the PR15 artifact handoff
acknowledgement chain:

```text
ROLLOUT_ID = NEXUS_RO_20260902T204500Z_pr15-artifact-handoff_R0
PR15_HEAD = ab4081133ad9d37d6a3ae3fce2c838ef1d6eea9a
PARENT = 5c1dc9df32fd8d96277e98ef754602d9726e52d7
SEED_HANDOFF = NEXUS_AH_20260902T192400Z_r3-completion-symbiosis_R0
R2_PR13_SEPARATION = PRESERVED
```

This preserves the current C0/C1 ceiling and the rule that PR15 infrastructure
readiness does not authorize merge, claim promotion, foundation promotion,
release or deployment.
