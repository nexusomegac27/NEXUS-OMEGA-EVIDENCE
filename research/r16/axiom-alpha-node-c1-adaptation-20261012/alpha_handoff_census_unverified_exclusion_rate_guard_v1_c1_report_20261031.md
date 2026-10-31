# AXIOM Alpha-Node — unauthenticated-exclusion rate guard V1 · 2026-10-31

```text
OBJECT = NEXUS_OMEGA_ALPHA_HANDOFF_CENSUS_UNVERIFIED_EXCLUSION_RATE_GUARD_V1_20261031_R0
DECISION = TESTED_IMPROVEMENT_C1_ISOLATED_SCAFFOLD_CANDIDATE
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
PINNED_MAIN_BEFORE = 03906d3c1cdc64fe6f1830808d18b765f90a830d
PINNED_MAIN_PARENT = b8e9a27e88f8806a72c2d7945337214ed884aec6
PREDECESSOR_PR = 238
PREDECESSOR_ISSUE93_RECEIPT = 6542349733
FROZEN_ORACLE_FIRST_COMMIT = 36ed59aabe9d90c16f2bf56bf3c393e8fabadc80
CANDIDATE_SECOND_COMMIT = 2595257d8245401a41aa800ed570ad3b83c60a3c
PRODUCTION_INTEGRATION = NO
WWW_PARITY = NOT_ESTABLISHED
```

## One candidate; material negative hypothesis

The already published isolated census V1.1 can output an **illustrative 100% handoff rate** for one synthetically successful handoff plus one synthetically failed handoff whose record is reclassified as `OUT_OF_SCOPE` with `NOT_AUTHORIZED` and a merely nonempty `evidence_ref`. It counts the exclusion but does not authenticate its justification. This is a **structural illustration risk**, not an observed NEXUS production falsification: V1.1 already marks every operational rate `NOT_COMPUTABLE_UNTIL_INDEPENDENT_API_SOURCE_AND_ACTOR_VERIFICATION`.

H0 / falsifier: a caller-controlled exclusion must not allow a numeric illustrative handoff **or publication** rate unless the exclusion provenance has been independently authenticated. A counterexample in which V1 guard still emits a number despite at least one unauthenticated exclusion falsifies this candidate. A false negative in the no-exclusion positive control also falsifies it.

## Original bytes and provenance

The owner GitHub `main` was read via the connected GitHub API at the exact 40-hex commit above. Governing files `AGENTS.md`, `GOVERNANCE.md`, the R16 Alpha adaptation contract, the Operator C1 direct-publication rule, the Task Anchor Norm and the default-DENY external actor registry were retrieved at that commit. Existing V1.1 was fetched from:

`research/r16/axiom-alpha-node-c1-adaptation-20261012/alpha_handoff_census_v1_1.py`

Its original source is **4,947 UTF-8 bytes**, SHA-256 `273401c8bc1e4fedaf2326674f76bcc35ee6135c0bae7ac5d682f92ae8418f20`, Git blob `d3115ce9d64d2b427a92aa9917246368b120f17c`. A byte-exact local copy was reconstructed and checked against **both** the Git blob formula and the independent SHA-256 digest before subprocess testing; this is not a substitute for actor authentication.

The evaluator was committed **before** the candidate, not modified to accept the candidate:

| Artifact | Bytes | SHA-256 | Git blob |
|---|---:|---|---|
| `frozen_alpha_exclusion_rate_oracle_v1_20261031.py` | 3,665 | `64d3d220e4a38a448b4aab9e412162ad787c1357174d6c6afaf33d4a4ad93794` | `e32ffefb3ea0977336efe2a74cfa539f2fc9c7d2` |
| `alpha_handoff_census_exclusion_guard_v1_20261031.py` | 1,283 | `297a09c45d91c7256d6280d52d5c634b16fcf2fa331f484ffd01dd8a71cb331c` | `fecb091d0459dc48ecd328309c7669cb2ae23491` |

All three sources were executed or inspected as local original bytes, without GitHub Actions secrets or remote runtime access. The new files are additive within the existing R16 research directory; no pre-existing file, evaluator, path, workflow, permission or branch rule was changed.

## Isolated independent-subprocess test

Reproduce from the R16 directory using Python standard library:

```sh
python frozen_alpha_exclusion_rate_oracle_v1_20261031.py alpha_handoff_census_v1_1.py
# observed: exit 1, AssertionError: unverified_exclusion_must_not_yield_100_percent
python frozen_alpha_exclusion_rate_oracle_v1_20261031.py alpha_handoff_census_exclusion_guard_v1_20261031.py
# observed: exit 0, {"oracle": "FROZEN_EXCLUSION_RATE_ORACLE_V1", "tests": 14, "passed": 14}
```

Baseline versus candidate: the synthetic `[success, out_of_scope_failed]` input produced **100% illustrative rate** under V1.1; the additive guard returns `rate_percent=null` and `rate_block_reason=EXCLUSION_SCOPE_NOT_AUTHENTICATED` while retaining `excluded_with_declared_reason=1`. No-exclusion `[success, failure]` remains 1/2 = 50% *illustrative only*. The frozen oracle checks 14 assertions: baseline denominator preservation, no-exclusion rates, unverified exclusions (including private), publication exclusions, source gaps, contradictory duplicates, duplicate JSON keys, nonfinite JSON, deduplication and explicit non-promotion. The baseline failure is preserved, not rewritten.

The candidate imports V1.1 without modifying it. It cannot authenticate exclusion sources; therefore it **suppresses both numerical illustrative rates whenever exclusions are present**, rather than claiming a verified denominator. No source claims, local/private returns or synthetic fixture outcomes are counted as actual automated NEXUS handoffs.

## Scientific and operational limits

The 14/14 is a **separate frozen technical subprocess oracle**, not independent external scientific validation. The guard does not prove event-ledger completeness, GitHub actor identity, exclusion eligibility, receipt independence, or a project-wide denominator. It does not turn a structurally complete publication into an independently verified byte readback. The complete authenticated 90%-handoff denominator and 100%-publication denominator remain `NOT_COMPUTABLE`.

R10 secondary source watch: PR #115 remained OPEN/UNMERGED at observation. Its current head `dab7c59070d67e7e2a244bd6d05db9a4d37460e3` differs from original pinned `539d4bb33d2ba2c4895713c1bc437ece0743eeea`; the detached manifest at both is 4,588 bytes and Git blob `0c2ca57a40f519da45ce60b565e8aadb4c9b95df`, with identical returned content. Issue #93 contained 228 comments, all owner-authored, and PR #115 discussion had zero comments. `PUBLIC_SEND=OBSERVED`; `INDEPENDENT_RECEIVER_ACK=NOT_ESTABLISHED`; `AUTHENTICATED_EXTERNAL_GITHUB_ACTOR=NOT_ESTABLISHED`; `AXIOM_SCIENTIFIC_ADJUDICATION=NOT_PERFORMED`; `EXPERT_RESEARCH_ACTUALLY_EXECUTED=UNVERIFIED`.

## Decision

`TESTED_IMPROVEMENT` is limited to reducing **unauthenticated-exclusion rate inflation in the isolated illustrative census**. This candidate is not a production integration and does not improve a measured operational handoff rate. No additional automation, worker, new root, registry update, Hostinger/WWW change, R10 merge, biological experiment, destructive reset or C1 promotion. Publication/CI/main/Issue-#93 receipts must be added only after actual GitHub API verification.
