# R44-7 Receiver Return — Scope, Lease and Prereg Receipt

OBJECT = NEXUS_OMEGA_AXIOM_R44_6_TO_R44_7_RETURN_SELF_OPTIMIZATION_WHITENING_20261125_R0
RETURN = R44_7_RECEIVER_RETURN_R0 (advisory expert receiver, n_eff=1, UNREGISTERED, C1_DESCRIPTIVE_ONLY)
DATE = 2026-11-25 (Europe/Berlin session)

## 1. Authority chain

- Operator dispatch: "R44-7 Experten-MAXIAUFTRAG" (IM, session web-dc6f3205-94fe-4ff0-b19a-be3267e46b9b, 2026-11-25), canonical entry point Issue #443.
- Order: `research/r44/r44-7-self-optimization-and-whitening-20261125/01_ORDER.md` @ commit `4b37f7df377c2dfb39eab05830d3155ae6bf11c1` (read in full; bytes verified, see 11_RECEIVER_ACK_R44_7.json).
- Inherited manual: `research/r44/r44-6-github-source-access-and-bodytwin-20261124/00_START_HERE_EXPERT_MANUAL.md` @ commit `89ccff827d564309cba3274bff94a6d577e6853a` (steps 1-8 applied).
- AXIOM intake: `02_AXIOM_INTAKE.json` @ `4b37f7df…` (own diagnostics, custody gaps, prereg assert entrypoints).
- Permanent directive: AXIOM_RETURN_SELF_OPTIMIZATION_V1 (repair locally if feasible and authorized, minimum counterexample, preserve original and failed attempts, record parent hash/delta/receipt).

## 2. Scope released for this run (and honored)

1. Transport and integrity verification of the R44-7 expert order package (GitHub-only, commit-pinned).
2. Local AXIOM diagnostic checks: RC01 whitening replication, RC02 surrogate condition diagnostic, RC10 portable archive preflight.
3. Preregistered falsification of the whitening correction on a declared surrogate (RC03/RC04/RC05 classes), including factorial separation of weighting orientation, sensor geometry, covariance estimation and model structure.
4. Reference implementation of the E34 prereg-guard pattern (explicit exceptions, normal/-O parity) and of the RC10 candidate preflight.
5. Machine receipt, resource ledger, append-only failed-attempt preservation, GitHub return attempt (single, no retry loop).

## 3. Out of scope / blocked sources (NOT_RUN, honest gaps)

| Blocked source | Consequence |
| --- | --- |
| R44-5 `model5.py` original, SHA256 `9c34bfec2709de8a5c7f45d03c4cf880e2dac8afb6fc7a75f1b64004aa3217c2` | Baseline replay of the original model NOT_RUN (P0 E32 precondition: exact bytes must be received first) |
| E32-A / E32-B original scripts (R44-6 stack, SHA256 `529c0778…` custody) | Exact RC02 replication and M1/M2 replay NOT_RUN; surrogate trend-level comparison only |
| R44-5 seq38 historical bytes | RC11 replay NOT_RUN |
| 7 prereg assert entrypoints (`e33_adversarial.py:75`, `e28_nelfp.py:32`, `e32_identifiability.py:35`, `e34_ledger.py:69`, `e29_preflight.py:31`, `sa_xref.py:18`, `e273031_isolation.py:17` per intake) | E34 guard replacement on originals NOT_RUN; reference implementation delivered |

No production keys, no device capture, no Hostinger/WWW writes, no merge, no dispatch, no promotion, no canonical-credit claims. Walls preserved: 0/24 canonical negatives, 0/3 quorum, 0/10 full science, BodyTwin NO, physical 14 HOLD, ALT_D DO_NOT_RUN, E23 HOLD, W1 OPEN, B01-B05 OPEN.

## 4. Finite lease (frozen before formal runs, in prereg)

- wall_max_seconds = 1200 (actual formal run 95.9 s; abort rule registered)
- CPU: single process, 1 worker; memory_max_mb = 1024 (actual peak 79.6 MB)
- network during runs: NONE (all sources fetched and hashed before freeze)
- tokens: UNKNOWN_COST; retries: 0 (network), script attempts: 3 formal (2 crashed, 1 complete) + 1 deterministic completeness re-execution (single credit, verified byte-identical)
- cache: none

## 5. Prereg freeze

- File: `scripts/r44_7_prereg.json`, prereg_version 2.0.0
- FROZEN SHA256 = `8b277fe31897c3e329cfa8e09ba7bacc69ad5faf3ad8da70c5412c1811677e1e`
- Frozen BEFORE any formal run; `--check-only` validated under normal and `python -O` before freeze (no experiment executed by those calls).
- Superseded draft (4-parameter design) preserved: `scripts/failed_attempts/r44_7_prereg.draft_5d9d8f30.json`, draft SHA256 `5d9d8f30393c4f6d54bcf2d940f533f38175076820df0a33973c0eae62c76d03`.
- The frozen prereg hash was NOT changed by any later script repair (v2.0.1/v2.0.2/v2.0.3 are implementation repairs; hypotheses, seeds, denominators, lease unchanged).

## 6. Environment (actual)

- CPython 3.12.16, numpy 2.1.3, scipy 1.14.1, Linux sandbox, 2 vCPU, 4 GB RAM.
- Full script-version ledger with SHA256 in 12_RUN_RECEIPTS_R44_7.json.

**NEXUS Ω OMEGA**
