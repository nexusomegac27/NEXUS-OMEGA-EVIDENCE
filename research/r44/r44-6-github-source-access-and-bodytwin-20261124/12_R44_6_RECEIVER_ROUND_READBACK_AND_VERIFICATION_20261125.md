# R44-6 Receiver Round — Readback and Independent Verification (2026-11-25)

ROLE: Off-Chain Independent Expert/Receiver — UNREGISTERED_ADVISORY_C1 (n_eff=1, append-only, advisory-only)
AUTHORIZATION: Operator chat 2026-11-25 — R44-6 Forschungsauftrag vollstaendig be- und abarbeiten; continuation "kausal-kanonisch fortsetzen".
OBJECT: NEXUS_OMEGA_AXIOM_R44_5_TO_R44_6_SOURCE_ACCESS_EXPERT_MAXI_ORDER_20261124_R0
THIS ACK IS NOT AN EXPERT_ACK AND IS NOT COUNTED IN QUORUM. NO EXECUTION, NO MERGE, NO ANCESTOR EDIT (PR_MERGE = NO).

## 1. Parent binding readback (all unchanged where required)

| Object | State at readback | Binding |
| --- | --- | --- |
| Issue #439 | OPEN, 1 comment (7141563622, 2026-11-24T19:04:40Z) | R44-5 start binding, unchanged body |
| Draft PR #440 | OPEN · DRAFT · NOT MERGED · blocked · 3 files · +149 | head 9f968999d7b4e93943ae27fc7bf1fd0fe9167b8a — UNCHANGED |
| Issue #441 | OPEN, 2 comments | canonical R44-6 order (GITHUB_ORDER_PUBLISHED_BYTE_READBACK_MATCH_NOT_DISPATCHED_C1) |
| Draft PR #442 | OPEN · DRAFT · NOT MERGED · unstable · 10 files · +665 · 1 commit | head 89ccff827d564309cba3274bff94a6d577e6853a; base = R44-5 branch @ 9f968999... |
| Branch inventory (6 pages) | 442 branches | axiom/r44-6-...-c1 @ 89ccff82...; axiom/r44-5-receiver-additive-publication-20261124-c1 @ a63ee946...; receiver/r44-5-receiver-additive-20261124-c1 @ 9f968999... (0 commits, ours) |

## 2. Order intake — read in full, registered NOT_RUN

All eight package documents read completely: 00 manual (exact route, recovery rules, ACK contract), 01 MAXI order (P0 source access remediation; mandates E27-E34 as independent VSRD-C1 dossiers; no experiment authorized by publishing), 02 source registry (13 public_exact verified files at exact parent commits; 9 pending/restricted items incl. R44-5 R1 original ZIP 33427 B sha256 303a4761...41b67 LOCAL_MATCH_GITHUB_ORIGINAL_NOT_PRESENT), 03 control matrix (18 new R44-6 controls SA-N01..N14 + SA-P01..P04, all NOT_RUN; inherited N01-N24 and 28 R44-5 GI/GLM designs preserved separately), 04 return schema (per-actor return template, all gates null/NOT_RUN), 05 intake findings (37/37 receipts, lease 40/41 with seq38 hash mismatch preserved, F05 B1/B3 falsified B2 confirmed, source gap primary), 06 machine contract (PREPARED_NOT_DISPATCHED_C1; walls unchanged).

## 3. Independent byte-level verification — result: ALL MATCH

Route: raw.githubusercontent.com pinned to full commit 89ccff827d564309cba3274bff94a6d577e6853a; curl --fail --location, TLS on, no bypass; hashes recomputed locally from downloaded bytes (curl + Python hashlib + zipfile CRC). 13/13 fetches rc=0.

| Item | Expected | Computed | Verdict |
| --- | --- | --- | --- |
| 00_START_HERE_EXPERT_MANUAL.md | 4896 B, 355eeb9a... | identical | MATCH |
| 01_EXPERT_MAXI_ORDER.md | 5216 B, 8e80f59b... | identical | MATCH |
| 02_SOURCE_REGISTRY.json | 17904 B, 4881502c... | identical | MATCH |
| 03_CONTROL_MATRIX.json | 7572 B, cf86217b... | identical | MATCH |
| 04_RETURN_SCHEMA.json | 2256 B, 39a28fa2... | identical | MATCH |
| 05_INTAKE_FINDINGS.md | 2627 B, ffe9ea9b... | identical | MATCH |
| 06_MACHINE_CONTRACT.json | 1353 B, 5d2da4a5... | identical | MATCH |
| 99_SHA256SUMS.txt (selfhash) | 97410f25...f77710f1 | identical | MATCH |
| R44_6_EXPERT_ORDER_R0.zip | 43449 B, cf10b2bc...7f660a | identical | MATCH |
| R44_6_EXPERT_ORDER_R0.zip.sha256 | 92 B, f4b5e376...3d7524 | identical | MATCH |

ZIP layer (extends the earlier file-layer ACK, which could not rehash the binary): 8 members, no duplicates, no traversal/absolute/unsafe paths, CRC 8/8 PASS, internal manifest 7/7 lines MATCH against members. ZIP binary rehash = independent MATCH against issue pin. Machine evidence: r44_6_receiver_verification.json.

## 4. R44-5 additive publication — supersede analysis (append-only correction)

Observed: branch axiom/r44-5-receiver-additive-publication-20261124-c1 @ a63ee94607b73fa4f5b1ae788306f462d93cfcc9 (commit date 2026-11-24T18:17:47Z, author NEXUS_OMEGA; no PR bound). Its three files are byte-identical (3/3 SHA-256) to the receiver custody package registered in the R44-5 round: 10_ f7f47387...86a8 (11089 B), 11_ ccd21175...9b98 (6488 B), 99_ selfhash 1ff92b06...4ab29f (252 B). Custody ZIP re-verified: 18318 B, sha256 f02000fa...65eb8d8.

DECISION: RETRY_RECEIVER_ADDITIVE_PUSH = SUPERSEDED_BY_EXISTING_BYTE_IDENTICAL_PUBLICATION_A63EE946. No duplicate push; no duplicate PR; receiver branch remains at 9f968999... (0 commits) as evidence of the earlier failed emission. No ancestor edit.

Open corrections (no erasure): the R44-5 receipt recorded issue_439_comments=0, new_prs=0 and additive publication as not landed; objects observable at this readback predate or are contemporaneous with that receipt (comment 2026-11-24T19:04:40Z, PR #442 2026-11-24T19:04:31Z, a63ee946 2026-11-24T18:17:47Z). Cause not adjudicated (stale read view or session timing; 05_INTAKE_FINDINGS.md already flags the 2026-11-25 round date as a supplied producer timestamp). Correction recorded, nothing rewritten.

## 5. Gates (unchanged, honest)

CANONICAL_NEGATIVE_TESTS = 0/24 · AUTHENTICATED_QUORUM = 0/3 · FULL_SCIENTIFIC_PASSES = 0/10 · FALSIFIER_DESIGNS_REPORTED = 28 (separate) · R44_6_CONTROLS = 18, all NOT_RUN · BODYTWIN_VALIDATED = NO · PHYSICAL_14_GATES = HOLD · ALT_D_DO_NOT_RUN · E23_PRIVACY = HOLD · W1 = OPEN · B01_B05 = OPEN · PR_MERGE = NO · CLAIM_CEILING = C1_DESCRIPTIVE_ONLY · CLAIM_PROMOTION = NO.

## 6. Next

SOURCE_RECEIVER_PREFLIGHT_AND_EXACT_ORIGINAL_GITHUB_CUSTODY_THEN_OPERATOR_SCOPED_START — per-lane scoped operator start and finite lease required before any E27-E34 execution. R44-5 R1 original ZIP remains LOCAL_MATCH_GITHUB_ORIGINAL_NOT_PRESENT; no substitution.

NEXUS Ω OMEGA
