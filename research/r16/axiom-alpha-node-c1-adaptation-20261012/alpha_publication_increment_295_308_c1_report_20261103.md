# NEXUS OMEGA — AXIOM Alpha-Node · incremental real publication readback (2026-11-03)

```text
OBJECT=NEXUS_OMEGA_ALPHA_PUBLICATION_INCREMENT_295_308_20261103_R0
DECISION=KNOWLEDGE_APPEND_C1_BOUNDED_REAL_SOURCE_AUDIT
CLAIM_CEILING=C1_DESCRIPTIVE_ONLY
PINNED_MAIN_BEFORE=bbdb0eaf5382f4dd880f20c1a417ad4c80990b25
PREDECESSOR_PR=308
PREDECESSOR_ISSUE93_RECEIPT=6591500315
FROZEN_EVALUATOR_FIRST_COMMIT=50ccf288b7711746206cb830d4527166006ea53a
SOURCE_SNAPSHOT_SECOND_COMMIT=8f574ce4e969e3868899f3ea78aab4f6300ff544
PRODUCTION_INTEGRATION=NO
WWW_PARITY=NOT_ESTABLISHED
```

## OBSERVE / ORIGINAL_BYTES / PROVENANCE

One bounded, new eight-PR source audit was selected instead of another handoff guard. The cohort is **PR #295–300 and #307–308 only**; the missing numbers #301–306 were not included and returned 404 as pull requests. This is **not** an exhaustive project publication denominator, not a time-period-wide census, and not a measurement of unattended handoffs. Previous PR #295 had separately audited PR #286–294; that historical report is not silently counted as a fresh independent rehash in this run.

GitHub connected API reads were performed on actual PR metadata, Issue #93 owner comments, immutable main commit refs, commit comparisons and **23 immutable GitHub Contents original UTF-8 payloads**. The SHA-256 computation was performed separately on decoded UTF-8 bytes (implementation known-answer test SHA256('abc') passed); the Git-blob IDs came from the GitHub Contents endpoint. Each independent byte length and SHA-256 was checked against the corresponding prior Issue #93 receipt, and each provider blob ID matched the recorded blob. This is independent of the owner's **receipt assertions**, but still within GitHub's provider trust domain. The source snapshot is a derived, additive index, not an authenticated raw HTTP archive.

| PR | Merge/main SHA | Issue #93 receipt | Source files | UTF-8 bytes | Result |
|---|---|---:|---:|---:|---|
| 295 | `0c6e9385ad4fb7fdd9a0ee384427460e568b2809` | 6582097904 | 2 | 11004 | MATCH |
| 296 | `0c6595660cc51cafe0d0d5a7daeeb7007defe9b1` | 6583755114 | 3 | 13281 | MATCH |
| 297 | `a55f1026a6cf418f89b6c7c916bd015d55dffd13` | 6585520284 | 3 | 15065 | MATCH |
| 298 | `013ee6b3027eb8f8b172ea72aec5b6812316d386` | 6586901931 | 3 | 12978 | MATCH |
| 299 | `a3e8b63ecb52f27cef1177ad2bab86057804bbbb` | 6588025294 | 3 | 13475 | MATCH |
| 300 | `94ea6517cc7a9f98a53cc8c4fb5f6a3d6fd9c6f8` | 6588842440 | 3 | 11814 | MATCH |
| 307 | `88e7bb6aa41f15bb1127753e869e0cd38b74f031` | 6590159318 | 3 | 15008 | MATCH |
| 308 | `bbdb0eaf5382f4dd880f20c1a417ad4c80990b25` | 6591500315 | 3 | 14276 | MATCH |
| **Total** | **8/8** | **8/8** | **23/23** | **106901** | **MATCH** |

For all eight consecutive observed main transitions, GitHub compare returned `ahead_by=1, behind_by=0`, with the exact 2 or 3 added files and no historical modification or deletion. Every owner receipt contains its matching PR URL, exact main SHA and C1 ceiling. The full 23-file path/byte/SHA-256/Git-blob index is in `alpha_publication_increment_295_308_source_snapshot_20261103.json`, committed **after** the independent evaluator.

## NEGATIVE HYPOTHESIS / PINNED BASELINE / ISOLATED CANDIDATE

Negative hypothesis: owner receipts may overstate source coverage, reuse identities, omit files, or refer to a different main commit. A mere statement of `8/8` is not evidence. Baseline before this run: the eight selected PRs had individual owner-authored receipts, but no new independent **joint** source audit for this cohort. After: **8/8** actual PR/main/receipt bindings and **23/23** original UTF-8 file lengths/SHA-256/provider blob comparisons were checked in this bounded cohort.

The independent structural evaluator was committed first at `50ccf288b7711746206cb830d4527166006ea53a`. It was then re-fetched by exact branch path and executed against the subsequently committed source snapshot in a fresh isolated JavaScript evaluation. It returned `BOUNDED_SOURCE_RECONCILED` and **16/16 PASS**: one positive control and **15/15 negative fixtures** (missing/duplicate PR, wrong main/parent, missing/duplicate receipt, wrong receipt-main, missing/extra file, incorrect addition count, SHA/blob/byte mismatch flags, zero bytes, total-byte drift). The evaluator is frozen and is not a source of independent GitHub authentication or scientific peer review.

Reproduce after checkout:

```bash
node -e "const p='./research/r16/axiom-alpha-node-c1-adaptation-20261012/';const e=require(p+'frozen_alpha_publication_increment_295_308_evaluator_v1_20261103.js');const s=require(p+'alpha_publication_increment_295_308_source_snapshot_20261103.json');console.log(e.runTests(),e.assess(s.rows))"
```

**Falsifiers:** any missing real PR, mismatched immutable parent/merge, altered file SHA-256/size/blob, absent or aliased Issue #93 receipt, or divergent provider response invalidates the corresponding bounded conclusion. A jointly forged GitHub provider view and owner receipt, or a fabricated snapshot with all `*_match=true`, can still pass the *structural* evaluator; the original-byte audit and evaluator must not be conflated. The original HTTP response bodies were not archived.

## DECISION / METRICS / BOUNDARIES

`KNOWLEDGE_APPEND_C1_SOURCE_BOUND`: new independently rehashed source coverage is **8/8 real PRs, 23/23 files, 106901 bytes** for this explicit cohort. This is **not** 100% project-wide publication coverage. The project-wide 100% publication-readback denominator and the eligible, authenticated 90% unattended-handoff numerator/denominator remain `NOT_COMPUTABLE`. No new productive unattended handoff is established; private/local inaccessible returns are excluded. No production code, workflow, ruleset, write slot, worker, Windows node, Hostinger, WWW or claim level was changed.

## R10 passive readback

PR #115 remains OPEN, current head `dab7c59070d67e7e2a244bd6d05db9a4d37460e3`; its PR discussion contains no independently authenticated expert receiver comment. The detached original R10 manifest at immutable `539d4bb33d2ba2c4895713c1bc437ece0743eeea` and current PR head was separately fetched and SHA-256 rehashed: **4588 bytes / SHA-256 `7e026d579e4a0c6062203c3c6ca9b720301e5cf87b86a4c4052b0351233fd6cc` / Git blob `0c2ca57a40f519da45ce60b565e8aadb4c9b95df` MATCH**. The pinned actor registry `docs/governance/EXTERNAL_AGENT_WRITE_SLOTS_V1.json` has an empty external allowlist. All **284** observed Issue #93 comments before this new publication were owner-authored. `PUBLIC_SEND=OBSERVED`; `INDEPENDENT_RECEIVER_ACK=SOURCE_NOT_PRESENT`; `AUTHENTICATED_EXTERNAL_GITHUB_ACTOR=NOT_ESTABLISHED`; `AXIOM_SCIENTIFIC_ADJUDICATION=NOT_EXECUTED`; `EXPERT_RESEARCH_ACTUALLY_EXECUTED=UNVERIFIED`. No R10 merge or expert registration.

`BLOCKED_LANE != BLOCKED_SYSTEM` · `DRIFT_RESET=NON_DESTRUCTIVE` · `CLAIM_CEILING=C1_DESCRIPTIVE_ONLY`
