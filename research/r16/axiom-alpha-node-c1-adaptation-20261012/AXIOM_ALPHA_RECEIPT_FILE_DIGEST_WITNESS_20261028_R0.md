# NEXUS OMEGA · AXIOM Alpha-Node · Receipt file-byte witness · 2026-10-28 R0

OBJECT=NEXUS_OMEGA_AXIOM_ALPHA_RECEIPT_FILE_DIGEST_WITNESS_20261028_R0
STATE=TESTED_IMPROVEMENT_C1_ISOLATED_RESEARCH_ONLY
CLAIM_CEILING=C1_DESCRIPTIVE_ONLY
PREDECESSOR_ISSUE93_RECEIPT=6463634536
PINNED_MAIN_BEFORE=259aa1bfa0019903268f71f72fc0dc458137a1ad
PRODUCTION_STEWARD_CHANGED=NO


## Original provenance and falsification

The immutable main above and prior Issue #93 receipt 6463634536 bind PR #167. Existing alpha_issue93_main_commit_witness_v4_20261027.py (Git blob 732bd83253a48eedb5f3107727be3f6f57661140) checks caller-supplied commit file-set and Git blob ID syntax, but does **not** recompute original-file SHA-256 or Git blob SHA-1. This is a scoped capability gap, not evidence of an incorrect historical receipt.

**Negative hypothesis:** a forged receipt SHA-256, substituted original bytes, changed commit blob or omitted file can evade metadata-only comparison. **Falsifier:** if the predecessor already independently hashes source bytes, or the new candidate accepts any one-defect fixture, the incremental improvement claim fails.

## Frozen evaluator, isolated candidate and results

- Frozen evaluator frozen_receipt_file_digest_evaluator_v1_20261028.py: **4625 bytes**, SHA-256 3da82354c24dc2961ed20ef839f2b420c04db6e4723ee4c0a6e6491c9e4062c8, Git blob 1428ec4c20063dac82fd6d8d578d7ba3b41e587c. It was committed first, on branch commit 9caeeb1f2788beea1c5d58d5ebf8f6a0dae51e3d.
- Candidate alpha_receipt_file_digest_witness_v1_20261028.py: **4899 bytes**, SHA-256 5ac7c5fd88b78c80e502bd01a4bc7fcbfd810179672486dec408ea9ac5617a9b, Git blob 5523bea43be23d96b37432b7147183818ab58c81. Committed second on 1fc05757f42fb743fc01da21bf62381bccad0781.
- Isolated Linux/Python 3.13.5 black-box subprocess evaluator: **16/16 PASS**. Two one-defect negative mutants, disabling SHA-256 and Git-blob comparison respectively: **14/16 PASS** each, two expected failures each.
- Targeted synthetic three-file input: previous metadata-only witness independently rehashes **0/3 file byte streams**; new witness independently checks **3/3** byte counts, SHA-256 and Git-blob SHA-1. This is fixture-scoped detection coverage, not a project handoff automation rate.

The evaluator does not import candidate functions. Positive controls include UTF-8 and binary bytes; negatives include content/hash/blob/length tampering, missing and duplicate paths, noncanonical base64, traversal and malformed JSON. The evaluator is versioned separately, **not** externally third-party validated.

## Scope and remaining gates

The witness accepts caller-supplied API snapshots and original-byte base64. It has no network or write operation and **cannot authenticate GitHub source origin, actor, Issue comment, actual main tip, pagination, CI or scientific validity**. Its output explicitly marks api_origin_authenticated=false, live_main_verified=false, receipt_authenticity_verified=false. Actual original GitHub source retrieval and readback are separate obligations.

Three additive files in the existing R16 Alpha-Node research lane only. No production Steward, governance, schema, ruleset, runtime, Hostinger, WWW, external actor registry or worker modification. PR checks, merge, actual-main readback and Issue #93 append-only receipt are separate pending gates, not asserted by this pre-merge report. Project-wide eligible handoff numerator/denominator: NOT_ESTABLISHED; 90%/100% targets: NOT_VERIFIED. R10: no new independently authenticated expert return in observed PR/Inbox discussions; EXPERT_RESEARCH_ACTUALLY_EXECUTED=NOT_ESTABLISHED.
