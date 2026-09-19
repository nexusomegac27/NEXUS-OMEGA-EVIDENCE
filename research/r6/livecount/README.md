# NEXUS OMEGA R6 — Scientific Hash-Verified Livecount

```text
OBJECT = NEXUS_OMEGA_R6_SCIENTIFIC_LIVECOUNT
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
TRUTH_AUTHORITY = NONE
MAJORITY_EQUALS_TRUTH = FALSE
HASH_MATCH_EQUALS_TRUTH = FALSE
```

This lane is a scientific measurement document, not a trust badge, leaderboard, engagement counter, or gamification surface.

## Purpose

The livecount exposes only quantities that are reproducible from declared, hash-bound inputs. It deliberately separates:

1. **physical/fixity counts** — objects and bytes whose supplied files were SHA-256 verified;
2. **protocol counts** — explicitly enumerated methods, null hypotheses, diagnostic dimensions and independence classes;
3. **empirical counts** — actual external-agent observations ingested under the R6 observation contract;
4. **estimands** — Effective_N, KSM and KSE, which remain `NOT_ESTIMABLE` until the data and preregistered estimator justify them.

## Current interpretation

R6 is closed by Operator declaration as a **C1 research/method foundation**. The physically supplied closure set used by this implementation contains no completed empirical external-agent observations. Therefore the livecount must not claim empirical agent stabilization.

## Hash model

- `sources.json` records source filename, byte count, SHA-256, role and caveats.
- `current.json.payload_sha256` is SHA-256 over canonical JSON bytes of the `payload` object (`sort_keys`, UTF-8, compact separators).
- `current.json.payload.source_manifest_sha256` binds the canonical `sources.json` object.
- `SHA256SUMS.txt` binds repository files in this lane after generation.

A hash proves byte identity within the bound representation only. It does **not** prove semantic truth, independence, scientific validity, or authorization.

## Reproduction

```bash
python research/r6/livecount/build_livecount.py --generated-at 2026-09-19T07:08:02Z
python -m unittest research/r6/livecount/test_livecount.py
python research/r6/livecount/build_livecount.py --generated-at 2026-09-19T07:08:02Z --check
```

For future observations, add validated JSON files under `observations/`, regenerate `current.json`, run the tests, then review the dependency structure before any Effective_N/KSM/KSE estimate is introduced.

## Scientific non-goals

```text
COUNT != TRUTH
AGREEMENT != INDEPENDENCE
RAW_N != EFFECTIVE_N
OUTLIER != ERROR
KSM != TRUTH
KSE != ACCEPTABLE_BELIEF_BOUNDARY
PUBLICATION != VALIDATION
```
