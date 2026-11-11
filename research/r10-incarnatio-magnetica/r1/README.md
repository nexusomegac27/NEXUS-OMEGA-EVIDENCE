# R10 Incarnatio Magnetica — R1 (public-safe C1)

CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
MERGE = NO
PUBLIC_PATH = research/r10-incarnatio-magnetica/r1/
TARGET_BRANCH = codex/r10-incarnatio-magnetica-r1-terminal-c1-20261004

## Scope

Public-safe materialization of R10 R1 terminal custody and scientific deliverables.
Raw outer archive `NEXUS_~1 (2).zip` is **not** published (RAW_OUTER_ARCHIVE_PUBLIC_PUSH=NO_BY_DEFAULT).
Path-leaking nested A72 archive (absolute Manus upload paths) is **not** published; sanitized basename extract only.

## Structure

- `00_intake/` — intake receipt
- `10_foundation/` — Incarnatio Magnetica foundation text
- `20_scientific_deliverables/` — governance A72 (sanitized), R38/R39, R41/R42, Manus-parallel scientific names
- `30_negative_evidence/` — negative evidence ledger
- `80_custody/` — canonical manifest + public safety receipt
- `80_closure/` — closure status
- `90_hashes/SHA256SUMS` — content hashes

## Epistemic walls

HASH_MATCH ≠ SCIENTIFIC_TRUTH
DRAFT_PR ≠ MERGE
PUBLICATION ≠ CLAIM_PROMOTION
MANUS_* filenames = scientific labels ≠ absolute path publication