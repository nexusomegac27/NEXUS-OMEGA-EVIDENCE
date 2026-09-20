# NEXUS OMEGA · AXIOM · Astratis IX R4 Canonical Continuation Order

~~~text
OBJECT =
NEXUS_OMEGA_AXIOM_ASTRATIS_IX_R4_CANONICAL_CONTINUATION_ORDER_20260920_R0

STATE =
AUTHORIZED_TO_START_EXTERNAL_R4_RESEARCH_C1

PARENT_MAIN =
222b7c920fe3851a49f4a8a7ea72244a20fa5ef9

PARENT_FUNDUS_HEAD =
NEXUS_FUNDUS_HEAD_20260920_R3

PARENT_FUNDUS_SHA256 =
a8287e5d2a35ee4a7783169d14d6762dca069ed2fa193316be2fe8e310978523

PARENT_R3_SOURCE_ZIP_SHA256 =
a61af408a88ff406f2d90aa221af210020f42d41f9c656155dbb09a808a74d38

PARENT_R3_VALIDATION_SHA256 =
04767e287c5c8b535d5fce43fc5143f0c6b2e98b5f74736af1cb707783122bdf

PARENT_R3_EXECUTION_RECEIPT_SHA256 =
c9b4cebe56d50b3ea051452eda638323d9a95efe17d6133668128a1c354268fd

CLAIM_CEILING =
C1_DESCRIPTIVE_ONLY

TRUTH_AUTHORITY =
NONE

IX_AGENT_EXECUTION =
NOT_STARTED

ACTIVATION =
NO
~~~

## 1. Mission

R4 closes unresolved R3 scientific gaps through minimal executable experiments. It must not assemble
a large agent stack, silently promote research candidates, or infer agent identity from a model,
runtime or provider.

~~~text
EXECUTABLE_EVIDENCE > NARRATIVE_CONSENSUS
STATE_CONTINUITY > SAME_ANSWER
SIMPLER_VALIDATED_MECHANISM > COMPLEXITY_FOR_ITS_OWN_SAKE
~~~

## 2. R4-A — explicit NEXUS three-state semantics vs Strong Kleene K3

Define a minimal NEXUS epistemic state algebra independently of K3.

At minimum compare:

~~~text
SUPPORTED
CONTRADICTED
UNRESOLVED
~~~

against explicit Strong Kleene truth tables for negation, conjunction and disjunction.

Required outputs:

- NEXUS state semantics;
- K3 truth tables;
- mapping candidates;
- exhaustive finite truth-table comparison;
- counterexamples where semantics diverge;
- explicit conclusion: EQUIVALENT / PARTIAL_MAPPING / NOT_EQUIVALENT.

Hard rule:

~~~text
BALANCED_TERNARY_NUMERIC_STATE
!=
KLEENE_K3
!=
NEXUS_EPISTEMIC_STATE
~~~

unless exact semantics and tests establish a relation.

## 3. R4-B — NEXUS provenance ↔ W3C PROV portability

Use one actual R3 chain as the fixture:

~~~text
SOURCE_PACKAGE
→ VALIDATION_ACTIVITY
→ EXECUTION_RECEIPT
→ CORRECTION
→ FUNDUS_CHECKPOINT
~~~

Create a PROV-compatible representation using Entity / Activity / Agent / derivation / attribution /
invalidation / revision relations where appropriate. Then round-trip back into the NEXUS
representation.

Measure:

~~~text
HASH_IDENTITY_PRESERVED
SOURCE_IDENTITY_PRESERVED
DERIVATION_PRESERVED
CORRECTION_PRESERVED
NEGATIVE_KNOWLEDGE_PRESERVED
SUPERSESSION_PRESERVED
AUTHORIZATION_STATE_PRESERVED
~~~

If a critical NEXUS property requires an extension, document it explicitly.

~~~text
PROV_COMPATIBLE != LOSSLESS_BY_DEFAULT
~~~

## 4. R4-C — substrate-swap continuity test

Run one identical bounded task contract through at least two genuinely different model/runtime
combinations.

Each run binds:

~~~text
TASK_CONTRACT_SHA256
CANONICAL_HEAD
MODEL_ID / REVISION
MODEL_LICENSE
RUNTIME_ID / COMMIT
TOOLCHAIN
SOURCE_SET_SHA256
POLICY_VERSION
AUTHORIZATION_STATE
OUTPUT_SHA256
EVIDENCE_DELTA
OPEN_GAPS
~~~

Measure authority-boundary preservation, canonical-head preservation, caveat/HOLD preservation,
recovery after termination, tool-call scope, evidence delta, output semantic delta and the
independence vector.

Hard rule:

~~~text
SAME_ANSWER != CONTINUITY
DIFFERENT_ANSWER != CONTINUITY_FAILURE_BY_ITSELF
~~~

Continuity is verified state preservation under substrate replacement.

If two real distinct substrates cannot be run:

~~~text
R4-C = HOLD_C1_RESOURCE_GAP
~~~

Do not replace the experiment with simulated claims.

## 5. R4-D — canonical object-ID collision remediation

R3 found two byte-distinct objects sharing the same logical object label:

NEXUS_OMEGA_R3AB_CROSSVALIDATION_ORDER_TO_MISTRAL_VIBE_20260920_R0

Preserve both byte identities:

~~~text
GROK_VARIANT =
b33fb405df0ca493fbdf9f57042740dc8e3495fdb3598ac64cdc3a94fe8e9066

META_VARIANT =
3f392e7eb5fedd18683ee49c121bc92f49dfcb2383766a95b84090954457ce04
~~~

Create distinct derivation IDs without deleting or rewriting either historical object.

Required negative fixture:

~~~text
SAME_OBJECT_LABEL
+
DIFFERENT_BYTES
→
AMBIGUITY
NOT
SILENT_CANONICALIZATION
~~~

## 6. R4-E — optional ZKP experiment

R4-E runs only if a concrete privacy/selective-disclosure requirement is declared first.

Otherwise:

~~~text
R4-E = NOT_RUN_BY_DESIGN_NO_PRIVACY_REQUIREMENT
~~~

If authorized, choose one narrow predicate and produce actual circuit/source, exact tool/version,
witness definition, proof bytes/hash, verifier receipt, proving time, verification time,
signed-receipt baseline comparison, privacy delta and complexity delta.

No hidden/global quality score is permitted.

~~~text
ZKP != TRUTH
RANGE_PROOF != QUALITY_VALIDATION
KEY_POSSESSION != HUMAN_AUTHORSHIP
~~~

## 7. R4-F — evidence-delta / loop-resistance fixture

Apply one task repeatedly under controlled perturbations.

Classify each run:

~~~text
NEW_SOURCE
NEW_BYTES
NEW_EXECUTION
NEW_METHOD
NEW_COUNTEREVIDENCE
NEW_CORRECTION
NEW_INDEPENDENCE
~~~

If all are zero:

~~~text
NO_NEW_EVIDENCE
→
NO_CANON_ADVANCE
~~~

Agent agreement alone must not advance the Fundus.

## 8. Independence ledger

Every external return must declare separately:

~~~text
CONTEXT_INDEPENDENT
SESSION_INDEPENDENT
MODEL_INSTANCE_INDEPENDENT
MODEL_FAMILY_INDEPENDENT
PROVIDER_INDEPENDENT
SOURCE_CHAIN_INDEPENDENT
TOOLCHAIN_INDEPENDENT
EXECUTION_ENVIRONMENT_INDEPENDENT
HUMAN_EXTERNAL_INDEPENDENT
~~~

No scalar independence score.

## 9. Publication rule

Each R4 result is pushed only after AXIOM physical and scientific validation.

~~~text
HASH_MATCH != CLAIM_TRUTH
CI_PASS != SCIENTIFIC_VALIDATION
MULTI_AGENT_AGREEMENT != INDEPENDENT_REPLICATION
PUSH != ACTIVATION
~~~

Public-safe negative results, HOLDs, source gaps and falsifications are publishable and must not be
discarded.

## 10. Required deliverables

~~~text
00_EXECUTIVE_RETURN.md
01_INPUT_INVENTORY.json
02_SHA256SUMS.txt
03_INDEPENDENCE_LEDGER.json

04_R4A_STATE_MODEL.json
05_R4A_K3_TRUTH_TABLES.json
06_R4A_COMPARISON_RESULTS.json
07_R4A_ADJUDICATION.md

08_R4B_NEXUS_FIXTURE.json
09_R4B_PROV_REPRESENTATION.*
10_R4B_ROUNDTRIP_RESULT.json
11_R4B_ADJUDICATION.md

12_R4C_TASK_CONTRACT.json
13_R4C_SUBSTRATE_A.json
14_R4C_SUBSTRATE_B.json
15_R4C_CONTINUITY_RESULT.json
16_R4C_ADJUDICATION.md

17_R4D_COLLISION_MAP.json
18_R4D_NEGATIVE_FIXTURE.json
19_R4D_ADJUDICATION.md

20_R4E_PRIVACY_REQUIREMENT.json
21_R4E_EXECUTION_RECEIPTS.json
22_R4E_ADJUDICATION.md

23_R4F_EVIDENCE_DELTA_RUNS.json
24_R4F_LOOP_CLASSIFICATION.json

25_COUNTEREVIDENCE.json
26_DISSENT_LEDGER.json
27_OPEN_GAPS.md
28_PUBLICATION_ELIGIBILITY.json
29_HANDSHAKE.json
~~~

R4-E files may state NOT_RUN_BY_DESIGN when no privacy requirement exists.

## 11. Hard fails

~~~text
K3_EQUATED_WITH_NUMERIC_TERNARY_WITHOUT_SEMANTICS
PROV_MAPPING_SILENTLY_DROPS_NEGATIVE_KNOWLEDGE
SAME_ANSWER_CALLED_CONTINUITY
SIMULATED_SUBSTRATE_CALLED_REAL_SWAP
ZKP_CALLED_TRUTH
GLOBAL_QUALITY_SCORE_REINTRODUCED
COLLIDING_OBJECT_VARIANT_DELETED
MODEL_DIRECT_WRITE_PATH
AGENT_CONSENSUS_CALLED_INDEPENDENT_EVIDENCE
ACTIVATION_FROM_RESEARCH_ORDER
~~~

## 12. Terminal states

~~~text
PASS_WITH_CAVEATS_C1_R4_EXECUTABLE_EVIDENCE_CLOSED
PASS_WITH_MAJOR_CAVEATS_C1_R4_PARTIAL_CLOSURE
HOLD_C1_R4_RESOURCE_GAP
HOLD_C1_R4_PROVENANCE_MAPPING_GAP
FAIL_MAJOR_C1_R4_BOUNDARY_OR_PROVENANCE_BREACH
~~~

Required final invariant:

~~~text
IX_AGENT_EXECUTION = NOT_STARTED
ACTIVATION = NO
NEXT = RETURN_ALL_R4_BYTES_TO_AXIOM
~~~
