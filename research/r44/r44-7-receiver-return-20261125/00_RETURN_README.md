# R44-7 Receiver Return — DELIVERY README

OBJECT = NEXUS_OMEGA_AXIOM_R44_6_TO_R44_7_RETURN_SELF_OPTIMIZATION_WHITENING_20261125_R0
RETURN = R44_7_RECEIVER_RETURN_R0
Actor = advisory expert receiver (n_eff=1, UNREGISTERED_ADVISORY_C1), C1_DESCRIPTIVE_ONLY
Parent order commit = 4b37f7df377c2dfb39eab05830d3155ae6bf11c1 (Issue #443)

## What this branch is

Scoped receiver return per inherited manual step 8 and the R44-7 order's no-retry rule. Text deliverables and machine receipts are pushed here; the authoritative handoff object is the full package ZIP with its SHA256 sidecar:

- `R44_7_RECEIVER_RETURN_R0.zip` — 93,663 B — SHA256 `1be1803c09e8a711df75d56b60972f57864b4a039d7badbc12de6b9f2fb04c08`
- sidecar pushed as `R44_7_RECEIVER_RETURN_R0.zip.sha256`
- internal manifest `99_SHA256SUMS.txt` covers 23 package files (incl. scripts/, failed_attempts/, 15_RC03_RESULTS.json). A branch/link/comment is NOT byte custody; the ZIP bytes are the handoff object. Binary ZIP upload is not possible from this lane; if the operator requires GitHub byte custody of the ZIP itself, the authorized publisher must upload it (DELIVERY request, no receiver retry loop).

## Files on this branch

- 10_SCOPE_LEASE_PREREG_RECEIPT.md — authority chain, scope, finite lease, prereg freeze
- 11_RECEIVER_ACK_R44_7.json — source receiver ACK (routes, bytes, hashes, blocked sources)
- 12_RUN_RECEIPTS_R44_7.json — run ids, script-version ledger, failed-attempt ledger, resource ledger, walls
- 13_RC01_RESULTS.json — exact RC01 replication (all six AXIOM values, rel diff 0.0)
- 14_RC02_RESULTS.json — surrogate condition diagnostic (H4 falsified; orientation-conditioning observation)
- 16_FALSIFICATION_REPORT.md — full scientific report, verdicts V1-V6
- 17_CONTRAST_ANALYSIS.txt — factorial contrasts (factor separation)
- 99_SHA256SUMS.txt — package manifest (23 entries)
- R44_7_RECEIVER_RETURN_R0.zip.sha256 — package sidecar

15_RC03_RESULTS.json (155,691 B) and all raw scripts are inside the ZIP only, bound by the manifest.

## Key results (C1 descriptive, surrogate-level, no canonical credit)

1. RC01 replicated exactly: original whitening orientation (L@r) is not the GLS objective; corrected (L.T@r) matches r^T W r to machine precision.
2. Preregistered falsification (20/20 cells, N=2000/cell, frozen prereg `8b277fe3…`): correction benefit is real but CONDITIONAL — +0.096..+0.112 joint coverage at narrow geometry, ~35% fewer invalid-CI abstentions, lower bias, faster convergence; REVERSAL (−0.258) at wide geometry with minimal (R=6) estimated covariance; single-replicate covariance is structurally invalid (abstain-all).
3. Factor separation: sensor geometry dominates (−0.42..−0.50); model structure is arm-symmetric (−0.25..−0.26); the historical undercoverage class cannot be attributed primarily to the whitening orientation.
4. Walls unchanged: 0/24, 0/3, 0/10, BodyTwin NO, no merge, no dispatch, no promotion.

**NEXUS Ω OMEGA**
