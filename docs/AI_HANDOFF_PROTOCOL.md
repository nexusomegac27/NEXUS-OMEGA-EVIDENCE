# NEXUS OMEGA — AI Handoff Protocol

Use this protocol whenever responsibility moves between Operator, AXIOM, Cursor/PRAXIS, GitHub Copilot, or an external expert.

The objective is a contiguous causal chain that survives chat limits, session loss, model changes, and ephemeral execution environments.

## Required handoff object

Every material handoff should contain at least:

```text
OBJECT = <unique stable object id>
STATE = <current state>
DATE_UTC = <ISO-8601 if known>
FROM = <producer/sender>
TO = <recipient>
AUTHORITY = <explicit authority source>
CLAIM = C1_DESCRIPTIVE_ONLY
CLAIM_CEILING = C1
PREDECESSOR_OBJECT = <exact prior object id or NONE>
PHYSICAL_INPUTS = <list or NONE>
INPUT_REHASH = <MATCH/MISMATCH/NOT_ESTABLISHED>
WORK_EXECUTED = <concise exact description>
WORK_NOT_EXECUTED = <explicit list>
EVIDENCE_STATUS = <established/reported/not established>
UNCERTAINTY = <explicit gaps>
CLAIM_PROMOTION = FALSE
INTEGRATION_AUTHORITY = NONE
AUTO_FOLLOW_ON = NO
NEXT_ACTION = <one causal next step>
```

## Physical artifact rule

If an output file is material to validation, include:

```text
FILENAME
BYTES
SHA256
PHYSICAL_EXPOSURE = YES/NO
```

The receiver independently recomputes bytes and SHA-256. A producer-side hash is `REPORTED` until reproduced by the receiver.

## Epistemic state vocabulary

Prefer these exact terms:

- `MATCH`
- `MISMATCH`
- `SOURCE_NOT_PRESENT`
- `NOT_ESTABLISHED`
- `NOT_COMPUTABLE`
- `PASS`
- `PASS_WITH_CAVEATS`
- `FAIL_MAJOR`
- `HARD_FAIL`
- `HOLD`
- `OPERATOR_REPORTED`
- `AXIOM_VERIFIED`
- `EXTERNALLY_VALIDATED`

Do not use a stronger state when a weaker one is the only state supported by evidence.

## Producer / validator separation

```text
PRODUCER_RETURN != INDEPENDENT_VALIDATION
VALIDATOR_PASS != CLAIM_PROMOTION
```

A validator must inspect the actual object. If it receives zero required files, content validation is `NOT_COMPUTABLE`; it must not infer a pass from the producer's receipt.

## Session bootstrap

When a new AI session begins, the AI should say internally, in effect:

> Retrieve the durable repository context before relying on conversation memory.

Read:

1. `AGENTS.md`
2. `GOVERNANCE.md`
3. `docs/AI_CONTEXT.md`
4. this protocol
5. `index/v1/latest.json`

Then identify the latest applicable handoff object.

## No chat-order fallback

If repository/physical handoff evidence conflicts with chat chronology, preserve the conflict and prefer the physically/retrievably bound predecessor for evidence claims.

Chat remains useful for operator authorization and intent, but chat alone does not create byte provenance.

## Handoff quality gate

A handoff is complete only when another competent agent can answer all of these without guessing:

1. What exact object is being continued?
2. What is its predecessor?
3. Which bytes were actually received and verified?
4. What was executed?
5. What was not executed?
6. Which claims are established, reported, blocked, or not computable?
7. What authority is explicitly absent?
8. What single next action is allowed?

If any answer requires reconstruction from memory, the handoff is incomplete.

## GitHub transport convention

For nontrivial repository changes:

```text
BRANCH
-> COMMIT(S)
-> PR
-> REVIEW / VALIDATION
-> OPERATOR DISPOSITION
-> MERGE ONLY IF AUTHORIZED
```

Do not interpret a merged PR as scientific promotion.

## Artifact handoff inbox

When a return should be processed autonomously through GitHub, use the
repository inbox protocol instead of a free-form chat handoff:

```text
research/pipeline/handoff/inbox/<HANDOFF_ID>/handoff.json
```

The required order is:

```text
INBOX
-> VALIDATE
-> BIND
-> RELAY
-> ACK
```

`VALIDATE` is fail-closed and structure/byte-bound only. `BIND`, `RELAY` and
`ACK` are receipt stages, not semantic validation or authority promotion.
