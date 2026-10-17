# NEXUS OMEGA — AXIOM R101 · Portable Unicode normalization alias guard · 2026-10-17

```text
OBJECT = NEXUS_OMEGA_AXIOM_R101_PORTABLE_UNICODE_NORMALIZATION_GUARD_20261017_R0
STATE = TESTED_ISOLATED_PATCH_CANDIDATE_C1
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
MAIN_PIN = d355400dabed3c280e1fce5030cab69ea099428b
PREDECESSOR = R99_PORTABLE_DIRECTORY_CASE_COLLISION_GUARD_UNMERGED_CANDIDATE
PUBLICATION_CLASS = C1_PUBLIC_SAFE_RESEARCH_REPORT_ONLY
PRODUCTION_INTEGRATION = NO
```

## Original-byte source and challenge

The pinned main Git tree identifies `scripts/nexus_repository_steward.py` as Git blob `296c7dc67b40f28270c92512ca6f67f8ad25fc50`, 8,023 bytes. Its historical tests are blob `063365adf8d4e8738412b917df9ff1d69f44e808`, 4,445 bytes. The independently checked local R99 archive contains matching Git-blob bytes for both original files. R99's isolated candidate adds case-only *directory* collision detection but remains unmerged.

Negative hypothesis: Git paths containing canonically equivalent Unicode strings (NFC vs NFD) can remain distinct under `str.casefold()` yet alias on filesystems that normalize Unicode names. This can affect full filenames or ancestor directories even when their child basenames differ. The source can therefore pass a case-only portability check while not being portable across all target filesystems. This is a portability risk, **not** evidence of a real collision or compromised checkout.

## Frozen oracle, isolated implementation and controls

The separate 18-case deterministic evaluator was written and SHA-256 frozen **before** R101 implementation: `2aa254cf5e5eadeaf8057ed30cbd2bf46f46eedccbcfdd63f81442e81cac5da8`. It contains ten one-defect negative alias fixtures (NFC/NFD full filenames and nested directories, including mixed case) and eight controls (ASCII case-only, distinct accents, unrelated paths, single NFD names).

- Pinned main original: **8/18**.
- R99 unmerged candidate: **8/18**.
- R101 isolated candidate: **18/18**.
- Deliberately weakened R101 mutant (downgrades the integrity fault to advisory): **8/18**.
- R99's earlier frozen evaluator, R101 candidate: **14/14**.
- Historical main tests, R101 candidate with test path adjusted only: **12/12**.

R101's isolated extension computes NFC-normalized, case-folded keys for complete file paths and every ancestor prefix. Where distinct raw spellings collide *only after normalization*, it records `PORTABLE_UNICODE_NORMALIZATION_COLLISION` as an integrity fault **before reading source bytes**. Case-only faults remain under the R99 classification. Candidate SHA-256: `948bfa44e0db7cf8493cbbc9ed2cdf0b3c37e4e8af2d472b44f54142943555c5`.

**Falsifier:** Any tested pair of NFC/NFD-equivalent paths not flagged on both entries, or whose source bytes are read despite the ambiguity, invalidates the tested fail-closed claim. A distinct path pair falsely flagged invalidates the claimed control specificity. The mutant's ten negative failures confirm the evaluator is sensitive to the integrity/advisory distinction.

## Main census and limitations

At the pinned main tree: **501 Git blob entries**, 151 unique directory prefixes under a JavaScript NFC+lowercase preflight, with **zero observed normalized collisions in that preflight**. The census uses JavaScript lowercasing rather than Python full Unicode casefold and is therefore a *limited preliminary scan*, not a universal Unicode audit.

These are synthetic tests on the available Linux filesystem; no macOS/APFS or Windows/NTFS filesystem replay, external validator acceptance, CI integration, or live node validation is claimed. This research report does not install code. R101 builds on the **unmerged R99 candidate**, not on an authorized main implementation. The independent evaluator is code-separated and pre-frozen, not an independent third-party scientific acceptance.

## Decision and publication boundary

`TESTED_ISOLATED_PATCH_CANDIDATE_C1`: candidate is reproducible in isolation, but no main merge, runtime change, Hostinger write, device capture, external actor registration or claim promotion is authorized by this report. Executable candidate and frozen evaluator require separately verified repository transport before claiming GitHub availability.

30-day authorized public handoff success numerator = **UNKNOWN**; eligible denominator = **UNKNOWN**; 90% target = **NOT_COMPUTABLE**. No improvement in productive handoff rate is asserted. A GitHub research-report commit, if successful, is not a tested productive integration or WWW parity receipt.

R10 passive check: PR #115 remains OPEN_NOT_MERGED, head `dab7c59070d67e7e2a244bd6d05db9a4d37460e3`; zero PR reviews, zero PR issue comments, and 35 owner-authored comments in passive Issue #93. `PUBLIC_SEND=DOCUMENTED`; `INDEPENDENT_RECEIVER_ACK=SOURCE_NOT_PRESENT`; `AUTHENTICATED_EXTERNAL_GITHUB_ACTOR=NOT_ESTABLISHED`; `EXPERT_RESEARCH_ACTUALLY_EXECUTED=NOT_ESTABLISHED`.

`BLOCKED_LANE != BLOCKED_SYSTEM · DRIFT_RESET=NON_DESTRUCTIVE · EVIDENCE > AGREEMENT`
