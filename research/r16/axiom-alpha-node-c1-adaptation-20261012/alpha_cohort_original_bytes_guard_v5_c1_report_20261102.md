# AXIOM Alpha-Node — bounded cohort original-byte readback V5 · 2026-11-02 · C1

\`\`\`text
OBJECT=NEXUS_OMEGA_ALPHA_PUBLICATION_COHORT_ORIGINAL_BYTES_GUARD_V5_20261102_R0
DECISION=TESTED_IMPROVEMENT_C1_ISOLATED_SCAFFOLD_BRANCH_CANDIDATE
CLAIM_CEILING=C1_DESCRIPTIVE_ONLY
PINNED_MAIN_BEFORE=2fbce469dc8c66d33a4be14eacb97bac3b02b938
PREDECESSOR_PR=287
PREDECESSOR_ISSUE93_RECEIPT=6570434057
FROZEN_EVALUATOR_FIRST_COMMIT=e5f0179c14c75b55c056a2308968d8cdcb0485d6
CANDIDATE_SECOND_COMMIT=38693f830814aca81317f6f4f7a7ea7c92810ba6
PRODUCTION_INTEGRATION=NO
WWW_PARITY=NOT_ESTABLISHED
\`\`\`

## Authority, source and bounded negative hypothesis

Owner-governed research-only addition under the existing R16 Alpha-Node lane; root AGENTS.md, GOVERNANCE.md, direct C1 publication rule, Task Anchor Norm V1, Repository Order Law V1, research/pipeline archive and existing repository-steward governance remain unchanged. No new root, agent, runtime, write slot, evaluator replacement, model-weight update or historical source overwrite.

Source: \`research/r16/axiom-alpha-node-c1-adaptation-20261012/alpha_publication_cohort_census_274_283_20261102.json\` at immutable main \`2fbce469dc8c66d33a4be14eacb97bac3b02b938\`, 19,301 ASCII bytes, SHA-256 \`8f835b1dd27472702ee0aad0e2c5c5fc3e9d467d4d7423518ba3cb4c41e3191c\`, Git blob \`2f4dbfa8b05a073d5fd939b5fc779a2734f65fdd\`. The SHA-256 was previously independently recomputed in the V4 source report; the source was fetched and parsed again for this run. The V4 report and its fixed metadata anchors remain unchanged.

**Negative hypothesis:** V4's fixed metadata comparison can pass even if an unexamined source payload has changed, because it does not consume independently retrieved original payload bytes. A separate, fail-closed source-byte comparator should reject altered payload bytes against the pinned manifest, even when the caller forges its reported Git blob.

## Original GitHub source-byte audit, separate from candidate execution

A read-only GitHub Contents fetch was performed separately for each of the **36 original files** at its own historical PR #274–283 immutable merge commit, as listed in the pinned manifest. Each UTF-8 content response was re-encoded to bytes, its byte count and SHA-256 independently computed in a separate JS evaluation implementation, and the GitHub-provided blob SHA compared with the pinned manifest. The JS SHA-256 implementation was checked against the FIPS-known \`abc\` and empty-message vectors before the audit. This was an actual API readback of source contents, **not execution of the new Python V5 candidate against all 36 payloads**.

| PR | File reads | Byte count | Byte/SHA-256/Blob matches |
|---|---:|---:|---:|
| #274 | 5 | 18,197 | 5/5 |
| #275 | 5 | 17,910 | 5/5 |
| #276 | 5 | 15,317 | 5/5 |
| #277 | 3 | 10,864 | 3/3 |
| #278 | 3 | 12,692 | 3/3 |
| #279 | 3 | 13,777 | 3/3 |
| #280 | 3 | 13,674 | 3/3 |
| #281 | 3 | 12,381 | 3/3 |
| #282 | 3 | 18,997 | 3/3 |
| #283 | 3 | 19,520 | 3/3 |
| **Total** | **36** | **153,329** | **36/36** |

This is an explicitly bounded historical cohort. No private or locally unavailable file is counted. The GitHub provider remains a common upstream trust domain; matching a pinned GitHub commit does not establish an independent external witness.

## Isolated candidate and independent frozen evaluator

The frozen Python evaluator was committed **first** at \`e5f0179c14c75b55c056a2308968d8cdcb0485d6\`, Git blob \`c7fab1fe3242300d3588bb4f61ed807747cc5ac5\`, 3,697 bytes, SHA-256 \`3adf934b71efe59882d8e9a83d695308193006f67a5e431d98cb9d5a26685ea7\`. The candidate was committed **second** at \`38693f830814aca81317f6f4f7a7ea7c92810ba6\`, Git blob \`656cfc0ae9bcba2f9bece850aeea4bb60fe40bfc\`, 4,754 bytes, SHA-256 \`1c74eb1105d99e5e02b0c2bc049b92b771e270c215404c37760a1eeb2117a236\`. Both Git blobs were read back after their commits and matched the local source-byte identities.

The V5 comparator accepts an independently acquired \`(commit, path, base64 payload, GitHub blob)\` record per manifest file, pins the manifest SHA-256 by default, independently recomputes payload SHA-256, length and Git's \`blob <len>\\0<bytes>\` SHA-1, rejects duplicate/unknown/missing records, invalid base64 and mismatched commits, and emits \`FAIL_CLOSED\` without performing network or writes. It is an isolated tool candidate, **not a live GitHub API client**.

The frozen evaluator was executed unchanged against the actual candidate source in a separate Python subprocess: **11/11 expected outcomes**, including two positive controls, eight negative fixtures and one explicitly expected falsifier. Actual one-byte payload corruption, jointly forged payload/provider blob, missing and duplicate files, wrong immutable commit, invalid base64, forged manifest with fixed trusted anchor, and extra records all failed closed. The executed falsifier jointly forged manifest, payload, provider blob **and caller-supplied trusted manifest SHA-256**; this was **accepted**, as predeclared. The evaluator output was independently saved locally: 1,575 bytes, SHA-256 \`4f9bfc18ec2f7c104c86a6aff733a55dc19950a83831024b286ef2ac99e31fdf\`. No hidden test or third-party scientific review is claimed.

Reproduce offline:
\`\`\`bash
python research/r16/axiom-alpha-node-c1-adaptation-20261012/frozen_alpha_cohort_original_bytes_evaluator_v5_20261102.py research/r16/axiom-alpha-node-c1-adaptation-20261012/alpha_cohort_original_bytes_guard_v5_20261102.py
\`\`\`

## Before/after, limitations and decision

| Metric | V4 predecessor | V5 run |
|---|---|---|
| Source payloads read and rehashed in this run | Not executed by V4 static metadata comparator | **36/36, 153,329 bytes** independently rehashed via read-only GitHub API |
| Original source-byte validation within isolated comparator | Not implemented | Implemented, offline test **11/11** |
| Original Python V5 run over 36 live payloads | N/A | **NOT_EXECUTED**; JS API audit and Python synthetic tests are distinct |
| New real automated artifact handoffs | No evidence | **0 newly established** |
| Project-wide eligible handoff denominator | Unknown | **Unknown; NOT_COMPUTABLE** |
| Project-wide publication readback denominator | Unknown | **Unknown; NOT_COMPUTABLE** |

V5 reduces a specific **metadata-only inspection gap** in the bounded cohort, not the project-wide operational handoff error rate. The original V4 report's earlier 36-file audit is not erased; this run independently repeats the physical-byte checks rather than claiming the cohort had never been audited.

**Falsifier/trust boundary:** If an attacker controls both the manifest and the caller-supplied trust-anchor digest, the comparator accepts a consistent forgery. GitHub Contents, its returned blob, the pinned manifest, and the caller's authorization are not independently authenticated by this offline code. There is no live Python-to-GitHub HTTPS E2E, production integration, external actor authentication, WWW parity, or scientific claim promotion.

R10 side observation (not a second candidate): PR #115 remains OPEN; the detached original and current PR-head manifest were both read and independently hashed at **4,588 bytes / SHA-256 \`7e026d579e4a0c6062203c3c6ca9b720301e5cf87b86a4c4052b0351233fd6cc\` / Git blob \`0c2ca57a40f519da45ce60b565e8aadb4c9b95df\`**. PR discussion and reviews were empty at inspection; 268 Issue #93 comments were owner-authored. Owner-mediated expert-return bytes remain recognized, but independently authenticated receiver ACK, expert execution and scientific adjudication are **NOT_ESTABLISHED**.

**Decision at report creation:** \`TESTED_IMPROVEMENT_C1_ISOLATED_SCAFFOLD_BRANCH_CANDIDATE\`. PR CI, actual immutable main readback and append-only Issue #93 receipt are subsequent separate events. No source overwrite, new automation, Cursor dispatch, R10 merge, Hostinger/WWW write, runtime modification or C2 promotion.
