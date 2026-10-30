# AXIOM Alpha-Node — independent source-authority pin V2 (2026-10-31)

```text
OBJECT=NEXUS_OMEGA_ALPHA_SOURCE_TRUSTED_PIN_V2_20261031_R0
DECISION=TESTED_IMPROVEMENT_C1_ISOLATED_CANDIDATE
CLAIM_CEILING=C1_DESCRIPTIVE_ONLY
PINNED_MAIN_BEFORE=209ae5f11c0bda7c4b5336fe51cb19c683758299
PINNED_MAIN_PARENT=167cd7672f701bf27b67f147568ce9cee00a2d59
PREDECESSOR_PR=226
PREDECESSOR_ISSUE93_RECEIPT=6534875643
TRUST_PIN_FIRST_COMMIT=808f57da150e3a660bec314768fd18840f114ba1
FROZEN_ORACLE_SECOND_COMMIT=6ab43ef07def68350b6080aa1d0d1df07266f85b
CANDIDATE_THIRD_COMMIT=477a70fe8c1d997025ffd22a85bd1385fd48e3c9
```

## Source and falsifiable negative hypothesis

The original 1,452-byte V3 source was retrieved from immutable commit `167cd7672f701bf27b67f147568ce9cee00a2d59` at `research/r16/axiom-alpha-node-c1-adaptation-20261012/alpha_handoff_commit_ref_binding_v3_20261030.py`. Independent local SHA-256 `425e60df8d363866b90924d739b237a051033def77d5b7d0bb71d63979fba0c3` and Git blob `73ef222f9117f566930390e60899d571ecc77402` matched the retrieved source. GitHub's commit API gave root tree `60b0fddfe38708d4de486e0355ff684e8eb12b98`; the separate recursive tree API returned an untruncated 916-entry projection containing the exact path as a regular `100644` blob with the same Git blob SHA and 1,452-byte size. The API is an asserted observation, **not** a cryptographically independent reconstruction of the full commit-tree ancestry.

**NEGATIVE_HYPOTHESIS:** V1 proves only consistency of locally accessible bytes with producer-supplied hashes. An adversary able to change both source bytes and its producer manifest can recalculate the SHA-256 and Git blob ID and still receive `LOCAL_SOURCE_BYTES_MATCH`. The V2 candidate must reject that same-length, self-consistently forged pair against an independently fixed, immutable witness without modifying the V1 predecessor.

## Frozen evaluator and independent baseline

The API-derived pin JSON was committed **first**, the black-box Python evaluator **second**, and the candidate **third**. The evaluator imports no candidate code and executes both versions via `python -S` subprocesses. It holds a predeclared independent expected pin digest, original source digest, original Git blob ID and expected tree projection. The candidate does not write to the evaluator, source or repository.

| Observable test | V1 predecessor | V2 candidate |
|---|---:|---:|
| Correct pinned original accepted | 1/1 | 1/1 |
| Same-length changed bytes + recomputed producer SHA-256/blob accepted | **1/1 (vulnerability)** | **0/1** |
| Independent black-box evaluator | Not applicable | **19/19 PASS** |
| Negative/malformed fixtures | Not applicable | **15/15 FAIL_CLOSED** |
| Altered pin rejected under frozen expected pin SHA | Not checked | 1/1 |
| Altered predecessor executable rejected | Not checked | 1/1 |
| Real source bytes / SHA-256 / blob | 1/1 MATCH | 1/1 MATCH |

The negative set also covers incorrect commit, path, digest, blob, byte length, repository, claim ceiling, source URL, duplicate JSON keys, nonfinite JSON, malformed JSON and symlink substitution. **FALSIFIER:** a self-consistent forged producer source/manifest is accepted against the unchanged independent pin, a valid original is rejected, or a changed pin or predecessor passes against the frozen expected digests.

## Artifact inventory and reproduction

- `alpha-source-trusted-pin-v2-20261031.json`: 832 bytes; SHA-256 `d1bf6a811f42c575a5d8c6506f6ae6f67edff514470406e691830419257563dc`; Git blob `eb6e457fdbb7b5ded6c649913e7bd4cc7b4f374d`.
- `frozen-alpha-source-trusted-pin-oracle-v2-20261031.py`: 5,643 bytes; SHA-256 `1202222fc40da41ea4310971bf48dd841186a4b98099b2048bc1e31ad3704d92`; Git blob `afb153a47778b60f7616aee57322fda2221251f3`.
- `alpha-source-trusted-pin-v2-20261031.py`: 5,353 bytes; SHA-256 `f65479c457b078db1b1b30b38d850127e4e30b7d9f34e781fe4f5b17c6017db5`; Git blob `720e62f84da217021302b180816858283ffd65fc`.

Reproduce from a checkout containing the original pinned source and predecessor:

```bash
python -S research/r16/axiom-alpha-node-c1-adaptation-20261012/frozen-alpha-source-trusted-pin-oracle-v2-20261031.py research/r16/axiom-alpha-node-c1-adaptation-20261012/alpha-source-trusted-pin-v2-20261031.py research/r16/axiom-alpha-node-c1-adaptation-20261012/alpha-source-byte-proof-v1-20261030.py research/r16/axiom-alpha-node-c1-adaptation-20261012/alpha-source-trusted-pin-v2-20261031.json .
```

## Epistemic and authorization boundaries

The **expected pin SHA-256 must come from an independently governed channel**. If an attacker controls both the pin and the expected digest, V2 cannot establish trust. It does not authenticate GitHub transport, independently reconstruct a Git commit/tree object, prove an expert's identity, authorize a write, or demonstrate scientific correctness. The improvement is a narrow fail-closed separation of producer assertions from a previously fixed source witness. All source/provenance claims are `C1_DESCRIPTIVE_ONLY`.

The repository's public-safe research lane is reused. No historical source, frozen evaluator after candidate, governance, branch rules, external actor registry, production/runtime, Hostinger, WWW or pipeline root was changed. This report is a C1 research candidate, not production integration. PR checks, exact immutable main readback and Issue #93 append-only receipt are separate postpublication gates.

## R10 passive watch and project metrics

R10 PR #115 remained OPEN at owner head `dab7c59070d67e7e2a244bd6d05db9a4d37460e3`, with no PR discussion, reviews or review threads; its original detached manifest was retrievable at immutable `539d4bb33d2ba2c4895713c1bc437ece0743eeea` as Git blob `0c2ca57a40f519da45ce60b565e8aadb4c9b95df` (4,588 characters in UTF-8). The 216 Issue #93 comments inspected before this iteration were all owner-authored. No new independently authenticated expert return was established; `PUBLIC_SEND=OBSERVED`, `INDEPENDENT_RECEIVER_ACK=NOT_ESTABLISHED`, `AUTHENTICATED_EXTERNAL_ACTOR=NOT_ESTABLISHED`, `AXIOM_SCIENTIFIC_ADJUDICATION=NOT_PERFORMED`, `EXPERT_RESEARCH_ACTUALLY_EXECUTED=NOT_INDEPENDENTLY_ESTABLISHED`.

The 90% handoff target and 100% project-wide readback target are **not measurable** without the complete authenticated denominator of eligible public handoff attempts and publications including failures. This run's synthetic security-test denominators must not be counted as real handoffs. `PROJECT_AUTOMATION_RATE=NOT_COMPUTABLE`, `PROJECT_FULL_READBACK_RATE=NOT_COMPUTABLE`, `WWW_PARITY=NOT_ESTABLISHED`.
