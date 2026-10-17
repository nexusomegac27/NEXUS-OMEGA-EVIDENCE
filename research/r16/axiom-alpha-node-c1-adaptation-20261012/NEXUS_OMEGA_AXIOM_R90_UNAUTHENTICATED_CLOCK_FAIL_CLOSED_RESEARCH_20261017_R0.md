# NEXUS OMEGA · AXIOM Alpha-Node R90 — unauthenticated clock fail-closed C1

```text
OBJECT = NEXUS_OMEGA_AXIOM_R90_UNAUTHENTICATED_CLOCK_FAIL_CLOSED_RESEARCH_20261017_R0
CLASS = ISOLATED_EXTERNAL_VALIDATOR_CANDIDATE
PREDECESSOR = NEXUS_OMEGA_AXIOM_R89_SOURCE_VARIANT_IDENTITY_GUARD_RESEARCH_20261017_R0
TECHNICAL_BASELINE = R88_CURRENT_ASOF_WINDOW_GUARD_20261017_R0
PINNED_MAIN = d355400dabed3c280e1fce5030cab69ea099428b
MAIN_PROTECTED = YES
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
R10 = PASSIVE_READBACK_ONLY
```

## OBSERVE / source provenance

GitHub `main` was read at immutable commit `d355400dabed3c280e1fce5030cab69ea099428b`. Governing files: `AGENTS.md` blob `f24f7cf557927016860279b65d0725275e6270a9`, `GOVERNANCE.md` blob `b630b62eb9800e2f57b6c86318c72faadb29c23b`, Alpha-Node contract blob `f8adcf6df22bba526c17dbff72b7ad494b42c63e`. R88's GitHub branch report at commit `92526a26a67a89dd70bb68fbb26d5be27ec6ef01`, blob `82f7f9c75943ae0ccb33db2ae941b78b1c144ec6`, itself states that a source string is not independent clock authentication. Its separately archived candidate code was fetched from the local R88 ZIP: 18010 bytes, SHA-256 `32c5342223f69d7ccc8ef5a6db4df5197ec1cba5088257f76ca26eece3d483d1`. This ZIP is a locally mounted predecessor, NOT a GitHub main object. R89 is an artifact-variant identity guard; R90 does not overwrite it.

## NEGATIVE HYPOTHESIS

A producer-controlled `trusted_time_readback()` can return arbitrary `utc` and `source` strings, including `authenticated=true` or a plausible SHA. R88 checks syntax and freshness but can emit a numerical *current* 30-day success rate while declaring `asof_source_authentication=EXTERNAL_READER_CONTRACT_NOT_VERIFIED_HERE`. A reader-provided label cannot prove independence. In an actual deployment, this risks a misleading 90% claim.

## ONE ISOLATED CANDIDATE

R90 changes only the external research candidate's `audit_current_30day()` behavior to **fail closed** when there is no separately validated clock adapter. The present isolated code has no such adapter; therefore **no current numerical KPI is permitted**. The historical `audit()` remains unchanged. This is a conservative C1 guard, not a production integration. A later separately reviewed authenticated time/inventory adapter is required to restore current numerical KPIs. Do not make the candidate certify its own clock oracle.

## FROZEN EVALUATOR / FALSIFIER

Frozen before implementation: `frozen_r90_clock_provenance_evaluator.py` SHA-256 `471a0f54c5a899591e4a98378788718df1c7d4e920385be82ec1ecd9c89df639` (12 synthetic fixtures). On the same fixtures, R88 predecessor: 0/12 PASS, with **6/12 unauthenticated fixtures emitting a numeric current ratio**. R90 candidate: **12/12 PASS, 0/12 numeric**. Deliberately faulty R90 self-attestation mutant: 11/12 PASS. Historical independent regression: R83 18/18, R84 18/18, R85 24/24, R86 16/16, R87 15/15 = **91/91 PASS**. These are local synthetic checks, not an external scientific acceptance.

FALSIFIER: any numeric current KPI emitted without independently authenticated clock and inventory provenance; any historical `audit()` regression failure; or an observed valid authenticated adapter being falsely claimed by this candidate (none was available). The R88 current-KPI test suite's previously permitted synthetic numerical ratios are intentionally **not** preserved; this is a stricter safety contract, not a backward-compatible production change.

## DECISION / PUBLICATION BOUNDARY

`TESTED_IMPROVEMENT_CANDIDATE`; independent production clock verification, real 30-day inventory denominator, GitHub merge, WWW parity and operator-visible 90% achievement are NOT_ESTABLISHED. No R10 expert receiver ACK, Cursor dispatch, Hostinger operation, runtime mutation, source overwrite, model self-modification, or claim promotion is implied. Public C1 research report only; no candidate code is integrated into a running node. If branch/PR creation or Issue #93 receipt fails, preserve explicit `HOLD_SCOPED_PUBLICATION` and read back actual main.
