# R39 Source-Exact Repair — 2026-11-22 C1

CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
CLAIM_PROMOTION = NO

This package binds the Cursor SOURCE_EXACT_REPAIR after AXIOM adjudication of the offline thaw return (ZIP 4800 / d92757a6…).

## Material repairs

1. Counts: suite counts.by_status PASSED_EXPECTED=26, SOURCE_GAP=39 (status field = un_status). Prior EXEC/RESULT text claiming 0 pass is superseded for tip only; original offline ZIP preserved.
2. Comment ID: AXIOM thaw comment on Issue #387 is 7081295152 (not 7081297152).
3. Sources: X13-R1 successor PY/RESULTS/MANIFEST + 65 public-safe per-ID receipts + SOURCE_GAP taxonomy.

## Non-claims

- SOURCE_EXACT_INDEPENDENT_REPLAY = PENDING (AXIOM rehash of this PR)
- PHYSICAL_OPPO_CAPTURE = NOT_AUTHORIZED
- BODYTWIN_VALIDATED = NO
- Expert E01/E05/E06/E08/E16 returns = NOT_INVENTED
- PRIVATE PR #40 original X13 6237B = PRESERVED_UNCHANGED (not redistributed here)

## Parent

- PR #389 OPEN DRAFT head e5f67d9456103ccdefe401feb945dd1e5376eb86
- Issue #387 repair order comment 7081988854
- Issue #386 expert Stage0 comment 7081989435