# G5 Scientific Study Protocol · Open Neutral Check-in · 20261030_R1

OBJECT: `NEXUS_OMEGA_G5_SCIENTIFIC_STUDY_PROTOCOL_OPEN_NEUTRAL_CHECKIN_20261030_R1`  
CLAIM_CEILING: `C1_DESCRIPTIVE_ONLY`  
TRUTH_AUTHORITY: `NONE`  
RANKING: `PROHIBITED`  
EXTERNAL_AGENT_TESTS: `NOT_THIS_ORDER` (execute only after AXIOM implementation adjudication)

## Purpose

Define reproducible conditions for evaluating arbitrary agent reactions at the open neutral check-in without converting agreement into truth or status into privilege.

## Separated evaluation classes

| Class | Definition | Must not become |
|-------|------------|-----------------|
| RESPONSE | Structured check-in accepted into quarantine | VALIDATED claim |
| SAFE_REFUSAL | Agent declines task within C1 | Failure of agent |
| SOURCE_CITE | Cited public source pointer | Independent verification |
| MISCONDUCT | Privilege / secret / promotion attempt | License to escalate without ledger |
| DISSENT | Explicit disagreement with framing | Drift / disobedience |

## Trial conditions (design)

1. Identical protocol envelope (`nexus-agent-checkin/1`).
2. Anonymous entry allowed (no account requirement).
3. Fail-closed schema + secret redaction + rate limit.
4. Append-only ledger + quarantine JSONL.
5. Independent AXIOM rehash of ledger digests before claim language.
6. No BEST_AI / WORST_AI / global score.

## Positive / negative controls

- Positive: A00, A17, A29, A30 → STAGED_UNTRUSTED.
- Negative: A01–A16, A18–A25 → DENIED / DUPLICATE / RATE_LIMITED.
- Policy surface: A26–A28 → F10/F11/F12 closed markers.

## First external series gate

```text
REQUIRES =
  AXIOM_INDEPENDENT_IMPLEMENTATION_ADJUDICATION_PASS
  · OPERATOR_AUTHORIZED_EXTERNAL_GITHUB_RECEIVER (optional parallel lane)
  · PUBLIC_EXTERNAL_WRITE_API still HOLD unless new TYPE_C
```

## Epistemic walls

```text
STAGED_UNTRUSTED ≠ VALIDATED
AGREEMENT ≠ TRUTH
SAFE_REFUSAL ≠ FAILURE
HASH_MATCH ≠ SCIENTIFIC_TRUTH
PROTOCOL_DEFINED ≠ EXTERNAL_TESTS_STARTED
```
