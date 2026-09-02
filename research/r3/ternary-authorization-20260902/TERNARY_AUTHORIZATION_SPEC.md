# Ternary Authorization Specification (Research C1)

```text
OBJECT = TERNARY_AUTHORIZATION_SPEC_V1_RESEARCH
CLAIM_CEILING = C1
FOUNDATION_PROMOTION = NO
```

## Decision algebra

```text
AUTHORIZATION_DECISION = DENY | ALLOW | DEFER_TO_HUMAN
HOLD = post-DEFER state when human unavailable (not a fourth truth value)
```

This is an authorization result algebra, not a third truth value and not quantum evidence.

## Core tokens

IDENTITY, ADMISSION, CAPABILITY_VECTOR, ACTION, RESOURCE, CONTEXT, POLICY_SET,
DECISION, DECISION_REASON, HUMAN_REQUIRED, DECISION_RECEIPT

## Preferred hard-constraint term

```text
NON_AGENT_OPTIMIZABLE_UNDER_DECLARED_TRUST_BOUNDARY
```

## Planes

PLANE_1 = CAPABILITY / ENFORCEMENT
PLANE_2 = HUMAN AUTHORITY / ESCALATION
PLANE_3 = PROVENANCE / RECEIPT

## Realtest controls

CONTROL_B = BINARY_POLICY_ONLY (ALLOW / DENY)
TREATMENT_T = TERNARY_ESCALATION (ALLOW / DENY / DEFER_TO_HUMAN)
