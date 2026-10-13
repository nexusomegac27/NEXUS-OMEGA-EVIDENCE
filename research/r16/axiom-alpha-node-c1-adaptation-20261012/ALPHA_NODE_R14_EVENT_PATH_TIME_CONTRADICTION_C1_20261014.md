# AXIOM Alpha-Node R14 — event path/time provenance contradiction (C1)

OBJECT = NEXUS_OMEGA_AXIOM_EVENT_PATH_TIME_BINDING_R14_20261014_R0  
STATE = CONTRADICTION_APPEND · TESTED_ISOLATED_CANDIDATE · HOLD_SCOPED_INTEGRATION  
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY  
AUTHORITY = NEXUS_OMEGA_OPERATOR_DIRECT_C1_RESEARCH_PUBLICATION_20261012_R0  
PINNED_MAIN = d355400dabed3c280e1fce5030cab69ea099428b  
MAIN_GUARD_BLOB_SHA1 = fe51de53a905a6c6ac5f8b999cbb34bed327a59d  
MAIN_GUARD_SHA256 = 7a948f92e54cf23538d368175950502222112b89833b95b335af3da4a10d5809  
PREDECESSOR = NEXUS_OMEGA_AXIOM_SCOPED_JSON_SOURCE_FAULT_R13_20261013_R0  
R13_ZIP_SHA256 = a99db9d8f65820ebfe778d740564ef348b634516ddae210094d74fbe6727116f  
R13_CHILD_HASHES = 38_OF_38_MATCH  
R13_CANDIDATE_SHA256 = a47b3a07bb7d82ed8bce3efb5398f5298e0d6d6f57dd79f6571a53fb84c0c439  
R14_ISOLATED_CANDIDATE_SHA256 = ceab09240f0af4cc19513987bf8070337109cb73b60d116d426e352d1603c8e8  
R14_FROZEN_EVALUATOR_SHA256 = 2d1a29d2cd9ec5e60c812f01e87babf6591a569d96d562f71e43e7e542e28338  
R14_EVIDENCE_ZIP_SHA256 = 2ca0824397b31584180a1d94abc084ea569719bf572d057740ba96f607c77b28

## One bounded hypothesis and isolated candidate

The canonical existing `research/pipeline/POLICY.md` and `research/pipeline/events/README.md` specify event paths `events/YYYY/MM/DD/<UTC_TIMESTAMP>_<EVENT_ID>.json`. The unintegrated R13 auditor can replay an event whose JSON `recorded_at_utc` contradicts the immutable path's date or timestamp, potentially falsely closing an open package. R14 checks the date partition and UTC filename timestamp before lifecycle replay, emits `EVENT_PATH_TIME_MISMATCH` with INTEGRITY severity and excludes mismatched records. It does not validate actor identity, signature, independent source fixity or filename/event-ID equality.

A separately written black-box evaluator was SHA-256 frozen **before** the R14 candidate change. Synthetic negative and positive fixtures: R13 **2/8**, R14 **8/8**; historical tests **16/16** on both. Source-byte read-only checks pass.

## Independent contradiction prevents integration

Previously successful frozen R2/R4–R13 suites: R13 **91/91**, R14 **81/91**. The **10** new failures all belong to frozen R8 (R13 **12/12**, R14 **2/12**). Its synthetic event files retain a fixed filename timestamp (for example `20261013T160000Z_E02.json`) while varying the JSON event timestamp (for example 00:04 UTC), contradicting the canonical path contract. No existing evaluator was modified, weakened or reclassified as passed. Historical frozen R3 remains **0/5** because of the earlier as-of timebase contradiction.

**Decision:** `HOLD_SCOPED_INTEGRATION`. R14 is a reproducible isolated counterexample/guard candidate, **not** a validated implementation, CI-integrated change, scientific approval or runtime deployment. The next independent adjudication must determine whether the path contract or R8 fixtures are authoritative for this use case; corrections must be append-only successors, never hidden oracle rewrites.

Falsifier: any mismatched path/time event silently replayed, valid UTC-equivalent event excluded, independent valid event lost, or source bytes mutated. Positive and negative cases, unchanged historical evaluators, diff and full logs are in the separately hashed R14 ZIP. **The GitHub note alone does not publish those ZIP/code/evaluator bytes.** No original evidence or production source was changed.

Scope: existing `research/r16/axiom-alpha-node-c1-adaptation-20261012/` lane, owner-controlled branch/PR only. No new pipeline, external actor slot, secret, node reset, Hostinger change, model-weight change, claim promotion or WWW parity assertion. Rolling 30-day eligible handoff numerator and denominator remain NOT_ESTABLISHED.
