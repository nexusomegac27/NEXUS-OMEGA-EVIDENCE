# Artifact rollout preparation

```text
OBJECT = NEXUS_OMEGA_ARTIFACT_ROLLOUT_PREP_SURFACE_V1
STATE = SEPARATE_ROLLOUT_PREPARATION_C1
PROTOCOL = PR15_ARTIFACT_HANDOFF_ROLLOUT_PREP_V1
```

This directory is the separate rollout-preparation surface for validated
artifact handoff chains. It packages readiness, operator-gate state and
continuation handling without executing a merge, main write, release,
deployment, claim promotion or foundation promotion.

```text
plans/      rollout-preparation plans
receipts/   generated readiness, gate, ack and workflow-event receipts
```

The current seed rollout is:

```text
NEXUS_RO_20260902T204500Z_pr15-artifact-handoff_R0
```

It is bound to PR15 head
`ab4081133ad9d37d6a3ae3fce2c838ef1d6eea9a` and the handoff seed
`NEXUS_AH_20260902T192400Z_r3-completion-symbiosis_R0`.
