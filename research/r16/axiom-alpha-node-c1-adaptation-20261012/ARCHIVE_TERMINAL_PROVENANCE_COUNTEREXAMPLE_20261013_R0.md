# AXIOM Alpha-Node — terminal lifecycle provenance counterexample (C1, 2026-10-13)

```text
OBJECT = NEXUS_OMEGA_AXIOM_ARCHIVE_TERMINAL_PROVENANCE_R3_20261013_R0
DECISION = CONTRADICTION_APPEND_AND_PATCH_CANDIDATE_HOLD_SCOPED
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
RUNTIME_CHANGE = NONE
NODE_RESET = NO
DRIFT_RESET = NON_DESTRUCTIVE
```

## Pinned source and scope

Repository: `nexusomegac27/NEXUS-OMEGA-EVIDENCE`. Immutable parent main `d355400dabed3c280e1fce5030cab69ea099428b`. Original `scripts/archive_continuity_guard.py` Git blob `fe51de53a905a6c6ac5f8b999cbb34bed327a59d`, reconstructed byte-for-byte from the previous isolated R2 candidate by reverse-applying `main_to_r2.diff`; independent Git-blob recomputation MATCH, original main file 8,726 bytes, SHA-256 `7a948f92e54cf23538d368175950502222112b89833b95b335af3da4a10d5809`. The original main code is Apache-2.0 marked. Historical R1 invalid-state counterexample and R2 candidate are retained; neither is integrated.

Policy basis: `research/pipeline/POLICY.md` §12: PROCESSED requires a Cursor terminal processing event or explicitly authorized processor. Event schema `schema/research-pipeline-event-v1.schema.json` declares `event_type`, `actor`, `evidence_refs`, `prior_state` and `new_state`. These fields are *declared* provenance, not authenticated identity or independently verified return bytes.

## Independently frozen negative evaluation

One isolated, immutable-before-patch black-box oracle was written and SHA-256 pinned BEFORE modifying R2: `6f661685282f58f2ac87174fa62f5754737a4eb84392a4e7bbdbb010a52ffb55`. The fixture models a package ACTIVE since 2026-09-01, manifest claiming PROCESSED, and a subsequent PROCESSED event. Four negative variants: (1) `actor=AXIOM` despite `event_type=CURSOR_RESULT`; (2) `event_type=STATE_CHANGED` despite declared Cursor actor; (3) empty `evidence_refs`; (4) string rather than array `evidence_refs`. One positive control declares `event_type=CURSOR_RESULT`, `actor=CURSOR_PRAXIS`, and a nonempty evidence reference. The test also checks source byte preservation.

| Target | Frozen oracle | Existing 16 regression tests | Earlier frozen 9-case R2 oracle |
| --- | --- | --- | --- |
| Immutable main guard | 0/5 | baseline source, not rerun here | not claimed |
| Isolated R2 candidate | 0/5 | 16/16 (previous R2 evidence) | 9/9 (previous R2 evidence) |
| Isolated R3 patch candidate | **5/5** | **14/16** | **8/9** |

The R3 experiment adds a terminal-envelope gate: do not accept PROCESSED as an effective state unless a preceding event exists and `event_type=CURSOR_RESULT`, `actor` is `CURSOR` or `CURSOR_PRAXIS`, `claim_ceiling=C1`, and `evidence_refs` is a nonempty array of nonblank strings. Otherwise append `UNVERIFIED_TERMINAL_TRANSITION`, retain the previous open state, and preserve `AGING_OPEN_REVIEW` plus manifest/event mismatch. For a syntactically acceptable envelope, explicitly label `DECLARED_NOT_INDEPENDENTLY_AUTHENTICATED`—no proof of processor identity or actual result bytes.

**Important contradictory result:** R3 fails two older regression tests and one older frozen R2 test because those fixtures assume `PROCESSED` is valid without Cursor-result provenance. These historical oracles were **not modified**. This is a documented test-policy conflict, not a production-ready fix. The new oracle was frozen independently of R3 implementation but not externally peer-reviewed.

## Decision and falsifier

`CONTRADICTION_APPEND` is supported by the new negative fixture. `PATCH_CANDIDATE_HOLD_SCOPED` applies to the R3 code: do not merge it into `scripts/`, do not update an evaluator to self-approve, and do not mark packages PROCESSED merely because an actor string matches. A falsifier is a legitimate, fully evidenced Cursor terminal event rejected by the envelope gate, or a forged envelope accepted as independently authenticated. The former requires explicit policy/evaluator adjudication; the latter would invalidate any stronger provenance claim.

Publication of this research note alone changes no runtime, guard, validator, old fixture, website or source evidence. GitHub main and CI readback must be reported separately from this proposed research publication. WWW parity is NOT established without an independent HTTPS receipt.

## Target metrics (not attainment claims)

Global accessible authorized handoff denominator remains **not yet measured**; local/private unavailable handoffs are excluded, never counted as successes. In this iteration, the only candidate is R3, and zero productive code integrations are claimed. Publication success/readback must be measured against actual GitHub results, not this note.
