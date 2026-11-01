# AXIOM Alpha-Node — Evidence-Reference Canonicalization Guard V4 — C1 — 2026-11-01

```text
OBJECT=NEXUS_OMEGA_ALPHA_HANDOFF_EVIDENCE_REF_CANONICAL_GUARD_V4_20261101_R0
DECISION=TESTED_IMPROVEMENT_C1_ISOLATED_SCAFFOLD_NOT_PRODUCTION_INTEGRATED
CLAIM_CEILING=C1_DESCRIPTIVE_ONLY
PINNED_MAIN_BEFORE=40125c80636b8d4b8cb62bb8671766d96784a846
PREDECESSOR_PR=268
PREDECESSOR_ISSUE93_RECEIPT=6558219684
FROZEN_EVALUATOR_FIRST_COMMIT=3a2532b07e6382c3cfb9ebc8f072d0e373916197
CANDIDATE_SECOND_COMMIT=e80d72fe3c02442dca0f464e29399d93127aa01a
STDOUT_THIRD_COMMIT=61a70531ca985094774d13633109056f385ddd95
PRODUCTION_INTEGRATION=NO
```

## Source-bound baseline and single negative hypothesis

The immutable V3 source is `research/r16/axiom-alpha-node-c1-adaptation-20261012/alpha_handoff_attempt_id_canonical_guard_v3_20261101.py` at pinned main `40125c80636b8d4b8cb62bb8671766d96784a846`: **3,920 bytes**, SHA-256 `297b26d3d2eb9164459ad3fa31333acd52fb0ed8c1f70e64f1241808b90fcd11`, Git blob `b79b70e92771700afba4f5c860471da09c2775ed`. Its local byte reconstruction matched both hashes exactly. It was not modified.

**Negative hypothesis:** V3 canonicalizes `attempt_id`, but `evidence_ref` only uses `.strip()` for uniqueness. It accepts noncanonical, padded, decomposed, or invisible-control evidence references, including semantically aliased references in one census. This can make provenance attribution ambiguous even though no real fraudulent handoff has been demonstrated.

**Single isolated V4 candidate:** require every `evidence_ref` to be nonempty, already trimmed, Unicode NFC, free of Unicode `Cc` and `Cf` code points, and unique after canonicalization. Preserve case sensitivity, valid composed Unicode, all V3 attempt-ID checks and the eligibility arithmetic. V4 imports the immutable V3 module from the same research directory. This is a conservative **synthetic structure guard**, not GitHub URL canonicalization, source authentication, or a claim of full census coverage.

## Independently frozen oracle and falsifier

The 17-case subprocess oracle was authored and committed **before** the V4 candidate. Its expected outcomes were fixed independently of the candidate. The evaluator was not edited afterward. It contains 7 positive/regression cases and 10 new negative fixtures.

| Executed comparison | Immutable V3 | Isolated V4 |
|---|---:|---:|
| Expected outcomes | 7/17 | **17/17** |
| New noncanonical-reference negatives rejected | 0/10 | **10/10** |
| Positive and regression cases | 7/7 | **7/7** |
| Real authenticated project-wide handoff denominator | NOT_COMPUTABLE | NOT_COMPUTABLE |

Negatives: a single padded reference, single NFD reference, zero-width joiner, embedded NUL, embedded newline, nonbreaking-space padding, trailing tab, embedded BOM, NFC/NFD alias pair and invisible-format alias pair. Positive controls preserve case-sensitive and NFC references. **Falsifier:** if any negative is accepted, a valid positive is rejected, or eligible failed attempts cease to count in the denominator, reject V4. No real event identity or coverage proof is asserted.

Reproduce from repository root:

```sh
python research/r16/axiom-alpha-node-c1-adaptation-20261012/frozen_alpha_handoff_evidence_ref_canonical_evaluator_v1_20261101.py research/r16/axiom-alpha-node-c1-adaptation-20261012/alpha_handoff_attempt_id_canonical_guard_v3_20261101.py
# expected exit 1; 7/17
python research/r16/axiom-alpha-node-c1-adaptation-20261012/frozen_alpha_handoff_evidence_ref_canonical_evaluator_v1_20261101.py research/r16/axiom-alpha-node-c1-adaptation-20261012/alpha_handoff_evidence_ref_canonical_guard_v4_20261101.py
# expected exit 0; 17/17
```

## Exact candidate and evaluator byte bindings

- Frozen evaluator: **3,634 bytes**; SHA-256 `3c75f831a8ec550d5a42b833c3b6412f8df6a7b79cfb574c2ee313b4087b8bc7`; Git blob `7f148ad411f0e4079142bd42fb70dd4a71e0eeee`.
- V4 candidate: **1,873 bytes**; SHA-256 `92f2fa54dd7cf441f03c179e2732dd1a69983977e93c2144c088cc720f7466a6`; Git blob `f78106128faf0f1af869958897fea315fa349cfc`.
- Original V4 evaluator stdout: **2,521 bytes**; SHA-256 `b4d3f5aaa2117627d5c8e9dd1df36d7ebf6f9c9b00eac531dfaffcfe50587782`; Git blob `4bf65f2afc81740d196f239e47f5c4cec43a5480`.
- Baseline local stdout (not published as an original): **2,610 bytes**; SHA-256 `b979df76b213f03c55402ac93e0e417e46276555d25e737c219cf81ace9bb91d`.

## Governance, R10, and publication gate

Authority was checked at pinned main against `AGENTS.md`, `GOVERNANCE.md`, the R16 Alpha adaptation contract, the operator-direct C1 publication order, the task-anchor norm, and repository order rules. This adds research files only to the existing R16 lane; it changes no historical file, registry, schema, workflow, pipeline root, secret, runtime, Hostinger, WWW, model weight, or claim ceiling.

Issue #93 had 249 comments at source readback, all owner-authored; R10 PR #115 was open with no independent review or comment in the checked connector read. `PUBLIC_SEND` is distinct from `INDEPENDENT_RECEIVER_ACK` and `EXPERT_RESEARCH_ACTUALLY_EXECUTED`. No independent R10 expert return was established. The R10 manifest is on the R10 PR branch, not main.

**Publication conditional:** a branch/PR is not a main publication. Require GitHub PR CI, immutable merge/readback, source file byte/SHA-256/blob comparison, and append-only Issue #93 receipt. The 90% project-wide automation rate and 100% project-wide readback rate remain `NOT_COMPUTABLE` without independently enumerated complete denominators. No WWW parity or production integration follows.
