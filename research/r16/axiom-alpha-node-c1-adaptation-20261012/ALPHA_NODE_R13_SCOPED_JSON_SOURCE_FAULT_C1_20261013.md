# AXIOM Alpha-Node R13 — scoped malformed JSON containment (C1 candidate)

OBJECT = NEXUS_OMEGA_AXIOM_SCOPED_JSON_SOURCE_FAULT_R13_20261013_R0  
STATE = TESTED_IMPROVEMENT_CANDIDATE_NOT_INTEGRATED  
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY  
AUTHORITY = NEXUS_OMEGA_OPERATOR_DIRECT_C1_RESEARCH_PUBLICATION_20261012_R0  
BASE_MAIN = d355400dabed3c280e1fce5030cab69ea099428b  
MAIN_GUARD_BLOB_SHA1 = fe51de53a905a6c6ac5f8b999cbb34bed327a59d  
MAIN_GUARD_SHA256 = 7a948f92e54cf23538d368175950502222112b89833b95b335af3da4a10d5809  
PREDECESSOR = NEXUS_OMEGA_AXIOM_FUTURE_SOURCE_METADATA_R12_20261013_R0  
PREDECESSOR_ZIP_SHA256 = 17e1b53c9f0201a86568bb2d757d2a00d875a9a1e4fd4c2204e8630319896e4a  
PREDECESSOR_SCRIPT_SHA256 = 871156f9b4688ca0bb2bfe0632ed274d51abba9bd1e3656d88d5c9c977e3c659  
ISOLATED_CANDIDATE_SCRIPT_SHA256 = a47b3a07bb7d82ed8bce3efb5398f5298e0d6d6f57dd79f6571a53fb84c0c439  
FROZEN_INDEPENDENT_BLACKBOX_EVALUATOR_SHA256 = 1c4fb85ed379ca2bdd496ec8c21ae8d0c6613a5343559e772117bf2b2790af37

## Negative hypothesis and bounded patch

R12 globally aborts the continuity audit when *one* package manifest or derived index is syntactically malformed, contains duplicate JSON keys or invalid UTF-8. This hides otherwise accessible package/event observations. R13 adds scoped `PACKAGE_MANIFEST_PARSE_ERROR` and `DERIVED_INDEX_PARSE_ERROR` INTEGRITY findings and continues to other sources. The repository structure contract remains fail-closed. No corrupted source is accepted as valid.

## Frozen independent tests

The corrected R13 black-box evaluator was frozen **before** the candidate patch. Its nine synthetic cases cover malformed syntax, duplicate keys and invalid UTF-8 in both source classes; malformed structure-contract fail-closed; normal positive control; read-only byte preservation. Baseline R12: **2/9**. R13: **9/9**. Seven additional cases pass. The earlier preliminary evaluator v0 had a fixture-directory placement error; it was preserved as INVALID_ORACLE and replaced *before* any candidate change; no post-candidate evaluator adjustment.

Historical regression suite: **16/16**. Prior frozen R2/R4–R12 suites: **82/82**. Frozen historical R3: **0/5** due to pre-existing same-day 09:00 event vs pinned 00:00 observation-time contradiction. R13 does not alter the R3 oracle or claim integration readiness.

Falsifier: Any malformed single package/index that prevents unrelated event/package observations, is silently accepted, yields exit 0 with `--fail-on-integrity`, or mutates input bytes refutes the scoped-containment claim. This is synthetic test evidence only; no external acceptance or runtime integration.

## Scope and custody

Artifact class: isolated C1 research/scaffold candidate, existing `research/r16/axiom-alpha-node-c1-adaptation-20261012/` lane. No new pipeline root, source rewrite, runtime/Hostinger mutation, new worker, secret, model-weight change, rights change, or claim promotion. Candidate implementation and frozen evaluator are available in the run's separately hashed R13 local evidence package; this note alone is **not** source-byte publication of those files. Until candidate and evaluator bytes are separately retrievable in GitHub, the evidence handoff remains incomplete. GitHub branch/PR/CI/main and Issue #93 receipt must be independently read back before any publication-success claim.
