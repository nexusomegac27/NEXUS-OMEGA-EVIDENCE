# AXIOM Alpha-Node — R10 actual-source-byte gate V2 (C1, 2026-10-30)

OBJECT: NEXUS_OMEGA_ALPHA_R10_SOURCE_BYTE_GATE_V2_20261030_R0
DECISION: TESTED_IMPROVEMENT_C1_ISOLATED_SCAFFOLD_CANDIDATE
CLAIM_CEILING: C1_DESCRIPTIVE_ONLY
PINNED_MAIN_BEFORE: 5e044225bece1cc0d9ce1944ce77043bf4d4bcf2
PREDECESSOR_PR: 215
PREDECESSOR_ISSUE93_RECEIPT: 6520594552
R10_PR115_MERGE_AUTHORITY: NONE
PRODUCTION_INTEGRATION: NO

## OBSERVE / ORIGINAL_BYTES / PROVENANCE

The GitHub API readback returned main 5e044225bece1cc0d9ce1944ce77043bf4d4bcf2, with parent a04d9874f19a04101d8e106809c6b0f6d58feb0b. The prior C1 R10 registry-gate report, original candidate and frozen evaluator were fetched at this pinned main. The prior candidate's source_bytes_rehashed and source_blob_rehashed values are boolean fields supplied inside the caller's claim, rather than results computed from actual source bytes. This is an evidence-boundary weakness, not a demonstrated production exploit.

The real registry docs/governance/EXTERNAL_AGENT_WRITE_SLOTS_V1.json was retrieved at pinned main, Git blob 1fabcab7f556e83621a3676ddfb3d11cdd964b55, exactly 2,178 UTF-8 bytes and SHA-256 d257be3faef8336e30f688d440758b051d93dd2a29ece693882af4ed8e463e7c (independently recalculated from copied exact JSON bytes). The external actor allowlist is empty and default is DENY. No registry write or external registration occurred.

R10 PR #115 was read as OPEN / NOT_MERGED, with zero discussion comments and zero review threads at this cutoff. The owner-mediated ACK assertion is retrievable at the R10 head dab7c59070d67e7e2a244bd6d05db9a4d37460e3 under research/r10/biocomputing-independent-experts-20261016/returns_20261016/R10_EXTERNAL_RECEIVE_ACK_ASSERTION_20261016.txt, Git blob 4e31f92be1f673f49a2c27e570b5849e754cca78. Its title and text claim independent receipt; this is not an independently authenticated receiver. The R10 original manifest remains pinned to 539d4bb33d2ba2c4895713c1bc437ece0743eeea, 4,588 bytes, SHA-256 7e026d579e4a0c6062203c3c6ca9b720301e5cf87b86a4c4052b0351233fd6cc, as established in the preceding report. No new external expert original was established.

## NEGATIVE HYPOTHESIS / PINNED BASELINE

A caller could set the old candidate's source_bytes_rehashed and source_blob_rehashed fields to true without supplying the alleged source file. The old gate cannot itself distinguish that assertion from a completed independent rehash. The new candidate MUST refuse those caller-controlled fields, require a local source file, calculate its byte count, SHA-256 and canonical Git blob SHA-1, and compare all three against separately supplied immutable pins before any review-eligibility result.

Falsifier: a same-length one-byte source mutation with unchanged pins must fail, as must an altered blob pin, changed byte-count pin, injected rehash flags, unpinned registry mutation, or forged allowlist. The positive control must remain descriptive, not promote authenticated actor, independent ACK or scientific execution.

## ISOLATED CANDIDATE / SEPARATE EVALUATOR

New candidate alpha_r10_source_byte_gate_v2_20261030.py (5,963 UTF-8 bytes, SHA-256 c6cb1c5106397c24c1529db13d5d3c27daa45699b1313133666d67fe09f36842, Git blob 0bd02f9872994aea374853161e0f22bbf85c4164) accepts --source, --registry and --claim local files plus independently supplied immutable pins. It verifies the actual source byte length, SHA-256 and Git blob, and refuses caller-provided rehash booleans. It performs no GitHub authentication or network access and writes no files.

Independent frozen black-box subprocess oracle frozen_alpha_r10_source_byte_oracle_v2_20261030.py (6,961 UTF-8 bytes, SHA-256 55cd7e52b19cdfc494a0af6137f807a1395ac2f026db45608e30f9116b924717, Git blob 4310f4af91fda89a60d884ab9ea3800fba400fc0) was committed BEFORE the candidate on the same isolated branch. The exact local candidate and evaluator returned 24/24 PASS, including same-length source mutation, truncation, append, false source SHA, false Git blob, false byte count, duplicate JSON keys, NaN, caller-injected allowlist, self-asserted rehash fields, empty registry, unregistered actor, and a synthetic future allowlisted-actor positive control.

A separate local integration probe ran the candidate with the ACTUAL pinned 2,178-byte registry, a clearly SYNTHETIC 34-byte source and independently calculated source pins: exit 0, registry MATCH, source bytes/SHA-256/Git blob MATCH, actor eligibility NOT_ESTABLISHED. This does not claim the real 4,380-byte R10 ACK was passed through the new Python candidate end-to-end. The real R10 source was read via the GitHub connector, not locally materialized into this test.

| Comparable quality dimension | V1 | V2 |
| --- | --- | --- |
| Rehash status originates in caller's claim | Yes | Rejected as invalid field |
| Source file required and byte-hashed by gate | No | Yes |
| Source Git blob computed from bytes | No | Yes |
| Same-length mutated source with unchanged pins | Not evaluable without source file | Rejected, 1/1 synthetic |
| Independent frozen subprocess oracle | 20/20 synthetic V1 | 24/24 synthetic V2 |
| Real registry consumed by Python candidate | Not run in V1 report | 1/1 actual registry + synthetic source |
| Authenticated external actor / independent receiver ACK | NOT_ESTABLISHED | NOT_ESTABLISHED |

Reproduce from this directory:
```bash
python frozen_alpha_r10_source_byte_oracle_v2_20261030.py alpha_r10_source_byte_gate_v2_20261030.py
```

The source SHA-256 and blob pins are trusted inputs; the gate does not prove that a pin belongs to the claimed commit, nor that a self-reported actor_origin is genuine. Its eligibility result is only ELIGIBLE_FOR_SEPARATE_AUTHENTICATION_ONLY. Full real R10 source integration and external independent GitHub authentication remain separate tests. No production integration, runtime, Hostinger, WWW or PR #115 mutation.

## DECISION / PUBLICATION

This iteration selects ONE candidate: source-byte self-assertion removal. Existing research/r16/axiom-alpha-node-c1-adaptation-20261012/ receives three additive research files (frozen evaluator, candidate, report); no structure migration or historical overwrite. The final PR/main readback and Issue #93 receipt are separate post-publication steps; this report is not evidence of their future success.

Project-wide autonomous handoff success rate and complete-publication-readback rate remain NOT_COMPUTABLE because the authenticated denominator of all eligible attempts, including failures, is absent. The synthetic tests are not an operational success-rate numerator.
