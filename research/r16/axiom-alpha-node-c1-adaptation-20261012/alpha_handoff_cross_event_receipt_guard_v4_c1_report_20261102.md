# NEXUS OMEGA — Alpha-Node cross-event handoff receipt reuse guard V4 — 2026-11-02

```text
OBJECT=NEXUS_OMEGA_ALPHA_HANDOFF_CROSS_EVENT_RECEIPT_GUARD_V4_20261102_R0
DECISION=TESTED_IMPROVEMENT_C1_ISOLATED_PREPUBLICATION
CLAIM_CEILING=C1_DESCRIPTIVE_ONLY
PINNED_MAIN_BEFORE=0c6e9385ad4fb7fdd9a0ee384427460e568b2809
PREDECESSOR_PR=295
PREDECESSOR_ISSUE93_RECEIPT=6582097904
FROZEN_EVALUATOR_FIRST_COMMIT=6c01dc33652604aafc67a39b373f3084ce4db2d6
CANDIDATE_SECOND_COMMIT=da8a47316b5b7a669de9d0f720903e80b7995a24
PRODUCTION_INTEGRATION=NO
WWW_PARITY=NOT_ESTABLISHED
```

## OBSERVE / ORIGINAL_BYTES / PROVENANCE

Read GitHub's current main ref, actual AGENTS.md, GOVERNANCE.md, bootstrap, structure, operator direct C1 rule, Alpha-Node R0, Task Anchor V1, pipeline policy, Repository Steward V1, external writer registry and Issue #93. Pinned main was `0c6e9385ad4fb7fdd9a0ee384427460e568b2809`, parent `b650d9361b58bc6cc9235f97a68edf732336f4eb`; predecessor PR #295 was merged and latest Issue #93 receipt #6582097904. The inbox had 277 comments, latest all owner-authored; external actor allowlist remains empty.

The historical V1/V2/V3 originals were read at pinned main, copied without alteration and rehashed in a separate local process. SHA-256: V1 `560ea49f753fa1a1118b12526e837bdfa3a055dfabe87894f553a7f3b1d04fb9`; V2 `04ad66f90be63f173709627f14f5bd87f7577b2d810323ce6156f8829befc98e`; V3 `40485983568c9c0722abdf4817fb3ef4061d30de44235b7378358772860c85df`. These historical files are unchanged.

## NEGATIVE HYPOTHESIS / PINNED BASELINE

V3 refuses reuse of one URL across receipt roles **within** an event, but permits two distinct eligible events to cite the **same** handoff receipt URL. An actual shared handoff receipt does not by itself prove two distinct unattended handoffs. On a fixed two-event synthetic negative fixture, V3 returns `COHORT_DECLARED_ONLY, numerator=2, denominator=2`. This is a structural false acceptance, **not** a demonstrated real-world false handoff.

## ISOLATED CANDIDATE / INDEPENDENT TEST

Frozen independent Python evaluator first committed at `6c01dc33652604aafc67a39b373f3084ce4db2d6`: `frozen_alpha_handoff_cross_event_evaluator_v4_20261102.py`, 5,409 bytes, SHA-256 `f532b7a349b0d0ce59162d9f07e902cf2b22928d608002ac7a43eb45b2370036`, Git blob `9345844ad547b846b352620753e0cf20731bb9fc`. It was not modified after its first commit.

V4 candidate second committed at `da8a47316b5b7a669de9d0f720903e80b7995a24`: `alpha_handoff_cross_event_receipt_guard_v4_20261102.py`, 2,305 bytes, SHA-256 `16e797b4e60d5854c7aa3cd25a22511f0cd6e4e8273eb13dca097a7f62ed8b2a`, Git blob `b99a6fea864a660e46d73147200ce3ab674c85e8`. V4 verifies V3's original SHA-256 before importing it; V3 already verifies V2 and V2 verifies V1. V4 refuses to calculate a cohort rate if two **eligible, structurally supported** events reuse the same `handoff_receipt` URL. It does not require distinct triggers or evaluators across events.

A separate local Python process executed the frozen evaluator against byte-identical pinned V1–V3 and candidate V4: **14/14 expected cases PASS**; stdout 2,528 bytes, SHA-256 `b541f0081a0b1d0724b03b7aecd2edb11eaa08b27e6e0815221a67a77854b517`. Baseline synthetic duplicate = V3 `2/2 COHORT_DECLARED_ONLY`; V4 duplicate = `NOT_COMPUTABLE` with null numerator/denominator. Distinct handoff receipts = V4 `2/2 COHORT_DECLARED_ONLY`. Negatives include three-event reuse, missing evaluator, incomplete population, unknown eligibility, intra-event collision, malformed input and mutation of pinned V3 bytes. Excluded private/non-unattended events remain excluded. Reproduction from this directory:

```sh
python frozen_alpha_handoff_cross_event_evaluator_v4_20261102.py alpha_handoff_receipt_role_guard_v3_20261102.py alpha_handoff_cross_event_receipt_guard_v4_20261102.py
```

## FALSIFIER / SCOPE

Two distinct declared handoff URLs can still be invented, owner-authored, or represent the same real-world handoff. A single evaluator receipt may cover several legitimate events; V4 intentionally allows such sharing and still returns `COHORT_DECLARED_ONLY`. A legitimate batch handoff receipt covering multiple distinct events would also be conservatively refused without content-level disambiguation. No GitHub API receipt dereference, independent actor authentication, real unattended execution or project-wide 90% metric is established.

Project-wide real eligible-event numerator/denominator = `NOT_COMPUTABLE / NOT_COMPUTABLE`; project-wide publication readback rate = `NOT_COMPUTABLE`. No new productive handoff success counted.

## R10 PASSIVE OBSERVATION / PUBLICATION BOUNDARY

PR #115 remains open at `dab7c59070d67e7e2a244bd6d05db9a4d37460e3`; zero PR comments/reviews. Detached manifest at original immutable head `539d4bb33d2ba2c4895713c1bc437ece0743eeea` and current head returned identical Git blob `0c2ca57a40f519da45ce60b565e8aadb4c9b95df`, 4,588 UTF-8 bytes. Expected previously verified SHA-256 `7e026d579e4a0c6062203c3c6ca9b720301e5cf87b86a4c4052b0351233fd6cc`. No new independently authenticated R10 expert ACK or actual research execution established; owner-mediated reports are not external authenticated actors.

Only three additive files in the existing research lane; no historical rewrite, new worker, external actor registration, production integration, Hostinger/WWW change, Cursor dispatch or claim promotion. Publication remains conditional on actual PR checks, merge, main source readback and append-only Issue #93 receipt. `BLOCKED_LANE != BLOCKED_SYSTEM; DRIFT_RESET=NON_DESTRUCTIVE`.
