# AXIOM Alpha-Node — fixed file-metadata anchors V4 · 2026-11-02 · C1

```text
OBJECT=NEXUS_OMEGA_ALPHA_PUBLICATION_COHORT_FILE_ANCHOR_V4_20261102_R0
DECISION=TESTED_IMPROVEMENT_C1_ISOLATED_SCAFFOLD_BRANCH_CANDIDATE
CLAIM_CEILING=C1_DESCRIPTIVE_ONLY
PINNED_MAIN_BEFORE=558dd66d4dd733236b628d0cd0894d96554db176
PREDECESSOR_PR=286
PREDECESSOR_ISSUE93_RECEIPT=6570267138
FROZEN_ORACLE_FIRST_COMMIT=df8673f49f175e4e8933874cd4266f8e3ae88280
CANDIDATE_SECOND_COMMIT=f11a06c0bbc20584eef6c0f6d3f43de17324e96b
PRODUCTION_INTEGRATION=NO
WWW_PARITY=NOT_ESTABLISHED
```

## Original bytes, authority, source and isolation

Governed by root AGENTS.md, GOVERNANCE.md, operator direct C1 research publication rule, Task Anchor Norm V1, Repository Order Law V1 and the R16 Alpha-Node C1 adaptation contract at pinned main. Owner-only additive files under the existing R16 research lane. No new root, worker, runtime, ruleset, evaluator replacement or source rewrite.

Historical cohort manifest at immutable main `558dd66d4dd733236b628d0cd0894d96554db176`:
`research/r16/axiom-alpha-node-c1-adaptation-20261012/alpha_publication_cohort_census_274_283_20261102.json`.
Source bytes: **19,301 ASCII bytes**, SHA-256 **`8f835b1dd27472702ee0aad0e2c5c5fc3e9d467d4d7423518ba3cb4c41e3191c`**, Git blob **`2f4dbfa8b05a073d5fd939b5fc779a2734f65fdd`**. SHA-256 independently recomputed over fetched original text using a locally executed JS SHA-256 implementation checked against the standard `abc` test vector; Git blob separately supplied by GitHub Contents. This verifies this manifest's bytes, not the original 36 files again.

V3 predecessor: `alpha_publication_cohort_middle_edge_guard_v3_20261102.py`, Git blob `1ffc190d0b49bc11b38baf27aefb3f3a8ea16d13`. The V3 report explicitly documented acceptance of co-forged file SHA-256 and blob fields. The new V4 is a **standalone JS snapshot guard** with 36 fixed file-path, byte-count, SHA-256 and Git-blob metadata anchors copied from the independently retrieved immutable cohort manifest. It does not replace or modify V1–V3.

## Negative hypothesis and independent test contract

Hypothesis: V3 structural checks can accept a coherent manipulation of a file's declared SHA-256 and both declared Git-blob fields, or an altered positive byte count. An independently frozen file-metadata reference should detect this **manifest drift**.

The separate JS oracle was committed **before** V4 code at `df8673f49f175e4e8933874cd4266f8e3ae88280`, blob `9af180cbdb0083677600de859e2dc8a2a25b8be6`, SHA-256 `d3dcb4690b165e2bff59743036f9689eb2547cff7a3be4194b53208616a646aa`, 3837 bytes. The V4 candidate was committed later at `f11a06c0bbc20584eef6c0f6d3f43de17324e96b`, blob `faccc2c6000d41bcb131ac79f61bd016a8af24ab`, SHA-256 `886983f30c503207f8da36c52a0fa9202aa1233976aaa8788fdcbd5dbd167f9a`, 12215 bytes. The evaluator was not edited to fit the candidate.

Actual frozen-oracle execution in a separate JS evaluation function on the fetched real manifest:

| Predeclared fixture class | V3 structural mirror | V4 candidate |
|---|---:|---:|
| Actual pinned manifest accepted | 1/1 | 1/1 |
| 36 co-forged file hash/blob negatives rejected | 0/36 | **36/36** |
| 36 altered byte-count negatives rejected | 0/36 | **36/36** |
| Three existing regression negatives rejected | 3/3 | **3/3** |
| Total expected oracle outcomes | 76/76 | **76/76** |

The baseline here is an independently written JS translation of the source-visible V1–V3 structural contract; it is **not** a fresh execution of the original Python V3 module. The candidate itself was executed as its actual JS source with the frozen oracle against the actual GitHub manifest and 75 derived fixtures. No third-party scientific evaluator, production E2E, or live API execution of V4 occurred.

**Falsifier executed:** regenerate the candidate's trusted reference anchors from a jointly falsified manifest. The resulting forged reference/candidate pair accepts the altered data. Thus V4 detects drift relative to its separately frozen metadata, **not** malicious upstream sources, coordinated reference compromise, original-file byte authenticity, GitHub actor identity or project-wide event completeness.

## Measured effect and decision

Within this **explicitly bounded historical PR #274–283 cohort**, the 72 new negative mutations went from **0/72** detected by the structural mirror to **72/72** by V4. No real automated Handoff was created or counted. The original 36-file provenance receipts remain historical and are not silently revalidated by static field comparison.

`PROJECT_WIDE_AUTOMATION_RATE=NOT_COMPUTABLE`; `PROJECT_WIDE_PUBLICATION_READBACK_RATE=NOT_COMPUTABLE` because authenticated full numerators and denominators remain unavailable. `UNAUTHORIZED_WRITES_OBSERVED_IN_THIS_RUN=0` is only an observation of performed actions, not a global zero-incident certification.

Scientific decision: `TESTED_IMPROVEMENT_C1_ISOLATED_SCAFFOLD` subject to PR CI, actual main readback and append-only Issue #93 receipt. This file is a branch candidate until those events are independently observed.

R10 remains a read-only side observation: PR #115 OPEN; pinned detached manifest 4,588 bytes, SHA-256 `7e026d579e4a0c6062203c3c6ca9b720301e5cf87b86a4c4052b0351233fd6cc`, Git blob `0c2ca57a40f519da45ce60b565e8aadb4c9b95df` verified on original head. Operator-mediated expert texts exist, but independent GitHub receiver ACK and actual expert execution are not authenticated. No R10 merge, external registration or biological experiment.

Reproduction: in an isolated JS environment, load the frozen oracle and V4 module (CommonJS exports), parse the historical JSON manifest at the pinned commit, then call `oracle.run(manifest, candidate.evaluate)`. No network call is made by the candidate. No secrets, runtime or WWW writes.
