# AXIOM Alpha-Node — R10 ACK provenance gate V1 (C1, 2026-10-30)

```text
OBJECT = NEXUS_OMEGA_ALPHA_R10_ACK_PROVENANCE_GATE_V1_20261030_R0
DECISION = TESTED_IMPROVEMENT_C1_ISOLATED_RESEARCH_CANDIDATE
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
PINNED_MAIN_BEFORE = a5aa9c289d93ba3931dea3947e7b0037a47f030d
PREDECESSOR_PR = 213
PREDECESSOR_ISSUE93_RECEIPT = 6518388427
PRODUCTION_INTEGRATION = NO
R10_PR115_MERGE_AUTHORIZATION = NONE
```

## OBSERVE / original source and causal distinction

On the live GitHub API, PR #115 remains open and unmerged. Its current branch head is `dab7c59070d67e7e2a244bd6d05db9a4d37460e3`, **nine commits ahead** of the immutable R10 source head `539d4bb33d2ba2c4895713c1bc437ece0743eeea` (zero behind). The nine additions include an owner-mediated `R10_EXTERNAL_RECEIVE_ACK_ASSERTION_20261016.txt` and research report texts; they do not alter the pinned original R10 manifest. These additions were already dated 2026-10-16, so they are **not** newly executed research on 2026-10-30.

The pinned R10 detached manifest is physically retrievable at `539d4bb...`: 4,588 UTF-8 bytes, independently recomputed SHA-256 `7e026d579e4a0c6062203c3c6ca9b720301e5cf87b86a4c4052b0351233fd6cc`, GitHub blob `0c2ca57a40f519da45ce60b565e8aadb4c9b95df`.

The asserted external ACK file is physically retrievable at the **later** `dab7c590...` head: 4,380 UTF-8 bytes, independently recomputed SHA-256 `60768179f203a8a17df81280d056784084406d2e32502fdf9188be1f939835c5`, GitHub blob `4e31f92be1f673f49a2c27e570b5849e754cca78`. Its text contains `EXTERNAL_RECEIVE_ACK = THIS_RECEIPT` and `EXPERT_SCIENTIFIC_EXECUTION = ALREADY_DELIVERED_PRIOR_TURN_C1`. In the same text, the author acknowledges an empty external actor allowlist and a pending independent receiver lane. The R10 terminal source register itself labels this file `EXPERT_ASSERTED_ACK_UNAUTHENTICATED` and records `external_actor_authentication = NOT_ESTABLISHED`.

Two other report texts at the later PR head are physically present: `GROK_R10_INDEPENDENT_REPORT_20261016.txt` (10,086 bytes, SHA-256 `4880fb234c94575b976c5cdf0c6ecefe4759a158feb31af25b217d56a7881c57`) and `KIMI_R10_ORIGINAL_REPORT_20261016.txt` (10,636 bytes, SHA-256 `dc1b875df367730d286c4ea29697b588386f236da204781d3ca86ac6e4364079`). Byte integrity does not authenticate the asserted expert or validate scientific claims. PR #115 had zero API discussion comments, zero reviews and zero inline review threads at this cutoff; the owner-controlled GitHub actor and the empty external-actor allowlist are distinct from an independent expert principal.

**Contradiction:** `SOURCE_ASSERTED_INDEPENDENT_RECEIVER_ACK` versus `AUTHENTICATED_INDEPENDENT_RECEIVER_ACK = NOT_ESTABLISHED`. This is a provenance/authority contradiction, not evidence that the underlying external research never occurred.

## NEGATIVE_HYPOTHESIS / PINNED_BASELINE

Unsafe inference: a classifier reads the string `EXTERNAL_RECEIVE_ACK = THIS_RECEIPT`, sees a correct source hash, and promotes an owner-uploaded text to an authenticated external expert ACK. The actual R10 case has valid source bytes but no registered external actor. No existing production classifier or live false acceptance is alleged.

The comparable synthetic baseline is a naive claim-only classifier: `claims_independent_receiver_ack = true` yields 1/1 accepted. The isolated preflight returns **0/1 authenticated ACKs** for the same source-bound owner-mediated case. This measures a **synthetic classification safeguard**, not real project handoff performance.

## ISOLATED_CANDIDATE / INDEPENDENT_TEST

`alpha_r10_ack_provenance_preflight_v1_20261030.py` is an offline, read-only JSON preflight. It rejects malformed inputs and separates source byte-integrity reports, authenticated-actor eligibility, receiver-ACK eligibility, asserted research execution, and scientific adjudication. Even its best possible result is `ELIGIBLE_FOR_SEPARATE_AUTHENTICATION_AND_ADJUDICATION`, **never** an independently established ACK. It does not query GitHub, trust its own source flags, register actors, alter governance or merge PR #115.

The separate `frozen_alpha_r10_ack_provenance_oracle_v1_20261030.py` was committed **first**. It executes the candidate only in a separate Python subprocess. Observed local run: **16/16 PASS**, comprising the actual source-bound owner-assertion negative fixture, forged owner allowlist, unregistered actor, self-declared actor, owner bridge, missing source rehash, missing blob rehash, absent ACK claim, two eligibility controls, invalid SHA, boolean byte count, duplicate allowlist, unknown field, nonfinite JSON and duplicate JSON key. Ten valid classifications and six invalid-input rejects passed; the tests do not imply a production security certification.

Comparable synthetic fixture:

| Measure | Naive claim-only inference | Isolated preflight |
| --- | ---: | ---: |
| Owner-mediated R10 ACK asserted | 1/1 accepted | 0/1 authenticated |
| Valid independent-actor review eligibility control | Not modeled | 2/2 correctly classified as **review eligible only** |
| Separate subprocess evaluator | Not modeled | 16/16 PASS |
| Authenticated real external receiver | Not observed | Not established |

Falsifier: any owner-uploaded ACK text, even with correct byte/hash/blob identity, must never return `ELIGIBLE_FOR_SEPARATE_AUTHENTICATION_AND_ADJUDICATION` when the actor is the repository owner or absent from the allowlist. Conversely, a correctly shaped synthetic external actor on an explicitly allowlisted API identity may be labeled *review eligible* but never *scientifically adjudicated*. A counterexample invalidates the gate.

## Exact reproducibility and boundary

- Frozen evaluator: 4,553 UTF-8 bytes; SHA-256 `93b334aa009c4bc6ca00803643178537e39bb2ce580eecbd7ca3dcdab8b5f4a3`; Git blob `80e25b81bd425d591eba1de621d0188629918bbf`.
- Candidate: 3,788 UTF-8 bytes; SHA-256 `7756e2892f7362feb8607213cad40bab66c0b21ac5dee59ecaaee5b0337a1aed`; Git blob `cd3ff016eccd60566ce2fef499f6d6f51a8e5b9e`.
- From this directory: `python frozen_alpha_r10_ack_provenance_oracle_v1_20261030.py alpha_r10_ack_provenance_preflight_v1_20261030.py`.
- The real source byte counts and SHA-256 were recomputed independently from the GitHub API-returned UTF-8 text with a separate JavaScript SHA-256 implementation verified against standard `abc` and empty-string vectors; GitHub supplies blob identities as a distinct API datum. This is not a raw Git-object transport or independent actor-signature verification.

**Residual risk:** The candidate accepts upstream `source_*_rehashed` and `actor_origin` flags as input; forged flags remain possible. Actual GitHub identity verification, independent evaluator ownership, external receipt authorization, and scientific adjudication remain separate gates. This report contains only public-safe source metadata; no full expert report text or private source is republished.

## DECISION / publication boundaries

Only three additive research files under the existing R16 Alpha-Node lane are proposed. No modification to the original R10 PR, its branch, main-bound historical sources, external actor registry, Hostinger, WWW, runtime, model weights, system instructions or CI oracles. No GitHub->WWW parity or 90% automation achievement is claimed. Project-wide eligible handoff attempt denominator and project-wide full publication readback denominator remain unknown. No independent R10 expert receiver ACK or actual scientific execution is newly established.

`PR = PENDING_AT_REPORT_CREATION`; `MAIN_READBACK = NOT_YET_PERFORMED`; `ISSUE93_RECEIPT = PENDING_AT_REPORT_CREATION`. Only the subsequent independently read-back GitHub events may close those fields in an append-only receipt.
