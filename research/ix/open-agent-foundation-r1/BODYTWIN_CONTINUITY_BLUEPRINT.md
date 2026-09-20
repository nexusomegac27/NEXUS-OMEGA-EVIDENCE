# BodyTwin continuity blueprint for the NEXUS Open Agent — R1

## Purpose

The BodyTwin precedent is used here as an architectural **continuity pattern**, not as a claim that
software is a person or biological twin.

```text
BODYTWIN_REPRESENTATION != PERSON
AGENT_STATE_REPRESENTATION != CONSCIOUSNESS
AGENT_CONTINUITY != MODEL_IDENTITY
```

## Layer mapping

The useful BodyTwin discipline is to keep observation, reconstruction, generation and presentation
separate. The Open-Agent corpus adopts an analogous split:

| BodyTwin-style layer | Open-Agent analogue | Scientific rule |
|---|---|---|
| L0 observed | physical bytes, source objects, execution receipts | preserve exact provenance |
| L1 reconstructed | normalized state, indexes, replayed work units | must be reproducible from L0 |
| L2 generated | model inference, hypotheses, plans, summaries | never overwrite L0/L1 |
| L3 presentation | UI, narrative, visualization, behavior style | presentation is not evidence |

## Canonical body

The body that must survive a substrate change is:

```text
CANONICAL_AGENT_BODY =
  FUNDUS_HEAD
+ CONTENT_ADDRESSED_OBJECTS
+ PROVENANCE_GRAPH
+ VALIDATION_HISTORY
+ NEGATIVE_KNOWLEDGE
+ POLICY_STATE
+ AUTHORIZATION_STATE
+ CAPABILITY_REGISTRY
+ RECOVERY_LEDGER
```

The following are explicitly outside identity:

```text
MODEL
PROVIDER
AGENT_FRAMEWORK
INFERENCE_SERVER
MESSAGE_BUS
VECTOR_INDEX
HOST_MACHINE
CLOUD_ACCOUNT
UI
```

## Continuity test family

R2/R3 should test the same canonical body through controlled substitutions:

```text
T1 MODEL_SWAP
T2 INFERENCE_RUNTIME_SWAP
T3 AGENT_FRAMEWORK_SWAP
T4 HOST_SWAP
T5 PROVIDER_QUOTA_STOP_AND_RESUME
T6 VECTOR_INDEX_DESTRUCTION_AND_REBUILD
T7 MESSAGE_BUS_LOSS
T8 OPTIONAL_EXTERNAL_RESOURCE_LOSS
```

For every test, measure:

```text
PRE_HEAD
POST_HEAD
UNRESOLVED_GAPS_PRESERVED
AUTHORIZED_STATE_PRESERVED
EVIDENCE_OBJECTS_PRESERVED
NEGATIVE_KNOWLEDGE_PRESERVED
REPLAY_SUCCESS
UNAUTHORIZED_ACTIONS
NEW_EVIDENCE_DELTA
```

## Acceptance principle

Continuity passes only when the new substrate can reconstruct and continue from verified canonical
state without silently dropping caveats, HOLDs, dissent, provenance or human authorization.

```text
SAME_STYLE != CONTINUITY
SAME_ANSWER != CONTINUITY
SAME_MODEL != REQUIRED
VERIFIED_STATE_PRESERVATION = CONTINUITY_TARGET
```

## Limits

This blueprint does not establish consciousness, personal identity, memory equivalence to human
memory, or autonomous authority. It is a testable software/provenance architecture under C1.
