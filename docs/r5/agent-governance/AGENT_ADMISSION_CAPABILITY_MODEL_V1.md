# NEXUS OMEGA Agent Admission & Capability Model V1

```text
OBJECT = NEXUS_OMEGA_AGENT_ADMISSION_CAPABILITY_MODEL_V1
STATE = IMPLEMENTATION_CANDIDATE
CLAIM_CEILING = C1
DEFAULT_CAPABILITY = DENY
SELF_VALIDATION = PROHIBITED
```

## Purpose

Every external agent must receive the NEXUS standing instructions before substantive work and must operate under an explicit capability profile. `RANG_0..3` is a human-readable preset layer, not an epistemic hierarchy.

```text
RANG = PROFILE_ALIAS(CAPABILITY_VECTOR)
RANG != TRUTH_AUTHORITY
RANG != CLAIM_PROMOTION
```

## Machine capability axes

- `read_scope`
- `write_scope`
- `execute_scope`
- `network_scope`
- `tool_scope`
- `secret_scope`
- `validation_role`
- `subject_mutation`
- `git_branch_create`
- `git_commit`
- `git_push`
- `git_force_push`
- `git_pr_create`
- `git_approve`
- `git_merge`
- `canonical_memory_write`
- `final_path_write`
- `claim_promotion`
- `foundation_promotion`
- `deploy`

Any capability not explicitly granted is denied.

## Presets

- `RANG_0_OBSERVER`: read/orient only.
- `RANG_1_RESEARCHER`: research outputs only in an authorized research lane.
- `RANG_2_VALIDATOR`: may inspect and validate a bound subject; subject mutation prohibited.
- `RANG_3_PRODUCER`: may mutate only the explicitly authorized candidate surface; may not independently validate its own scientific output.

AXIOM, Cursor/PRAXIS and the human Operator are system roles, not external-agent ranks.

## Admission sequence

```text
STANDING_INSTRUCTIONS
→ CAPABILITY_PROFILE
→ ADMISSION_ENVELOPE
→ MACHINE_ENTRY_ACK
→ HASH/SCHEMA/CAPABILITY_CHECK
→ ADMITTED
```

Write-capable work remains on hold until the entry ACK binds the exact instruction/profile hashes and acknowledges the forbidden paths and self-validation boundary.

## File mutation duty

Every substantive agent-created filesystem/repository mutation must emit a canonical File Event after the resulting bytes are known. The event binds actor identity, task/order, operation, path, before/after raw-byte SHA-256, reason and Git result commit when applicable.

Ledger bookkeeping files are deterministic derived metadata and are excluded from recursive self-logging. This is the explicit recursion termination rule; it does not exempt substantive agent artifacts.

## Separation invariant

```text
PRODUCER_CONTEXT ∩ INDEPENDENT_VALIDATOR_CONTEXT = NO_SELF_VALIDATION
```

A producer may never gain validation authority merely by receiving a broader capability vector. A validator may never repair or mutate the subject it is independently validating.
