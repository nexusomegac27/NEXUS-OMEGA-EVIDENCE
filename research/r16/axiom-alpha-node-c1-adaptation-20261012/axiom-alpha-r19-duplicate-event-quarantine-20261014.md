# AXIOM Alpha-Node R19 — Duplicate event identity quarantine (C1 research candidate)

```text
OBJECT = NEXUS_OMEGA_AXIOM_ALPHA_R19_DUPLICATE_EVENT_ID_QUARANTINE_20261014_R0
DECISION = TESTED_IMPROVEMENT_CANDIDATE_HOLD_SCOPED_INTEGRATION
PARENT_MAIN = d355400dabed3c280e1fce5030cab69ea099428b
PARENT_MAIN_SCRIPT_BLOB = fe51de53a905a6c6ac5f8b999cbb34bed327a59d
PREDECESSOR = R18_NONFINITE_JSON_SOURCE_INTEGRITY_20261014
PREDECESSOR_ZIP_SHA256 = 50fa4db406dc44af7a4144f5e8662d4d0837fba1ee048e5ec4a9c209d5bb4bde
PREDECESSOR_SCRIPT_SHA256 = c0652688aebcb62f8125e1344c6a20e2db80a444d32990b5f306e2745428ad39
ISOLATED_CANDIDATE_SHA256 = def65b8530231e1191b08908aadeee48af0d81b38fc7fc236a71d4a7d1976a55
FROZEN_EVALUATOR_SHA256 = 0810c3c26a819d4507ebf0bc60b89b127bd29873b141b53904c22bc226a715b8
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
```

## Source-exact negative hypothesis

The R18 candidate flags a duplicate event ID only *after* replaying the first occurrence. A terminal event placed first can therefore affect the derived package state and suppress the open-package age review even though a later collision is reported. The immutable `research/pipeline/POLICY.md` and `research/pipeline/templates/event.template.json` bind event identity and append-only lifecycle. The R18 ZIP bytes were independently rehashed and 32/32 manifest children matched.

**Isolated R19 delta:** Before chronological replay, count all path-valid, parse-valid global event IDs. Quarantine *all* occurrences of every duplicated ID, not just the later copies. Preserve all original files, valid independent events and the existing observed parse count. Add separate derived replay-candidate and quarantine counts. No canonical event or historical evaluator is changed.

## Frozen evaluation (local, not third-party acceptance)

| Check | R18 baseline | R19 isolated candidate |
|---|---:|---:|
| Frozen R19 black-box suite | 4/9 | **9/9** |
| Five collision negatives without first-writer terminal replay | 0/5 | **5/5** |
| Frozen R18 suite | — | 10/10 |
| Frozen R17 suite | — | 6/6 |
| Frozen R14 suite | — | 8/8 |
| Historical R16 suite | — | 6/7 (R15 source-hash lock) |
| Historical R8 suite | — | 2/12 (existing fixture/path contradiction) |

Evaluator frozen **before** candidate editing. An initial pre-freeze optional-field calibration defect was discarded and recorded; it was not counted as acceptance. The frozen evaluator SHA-256 did not change during candidate testing.

**Falsifier:** Any colliding ID affecting event_state, any suppression of an unrelated distinct event, or a new failure in the previously passing R18/R17/R14 controls invalidates the candidate. The R8/R15/R3 historical limitations remain unresolved; no productive integration is claimed.

This is a research note, not the full executable patch or evaluator. The reproducible local package remains separately identified. No new pipeline, runtime worker, Hostinger deploy, model-weight change, claim promotion, or GitHub→WWW parity is asserted.

`BLOCKED_LANE != BLOCKED_SYSTEM · DRIFT_RESET=NON_DESTRUCTIVE · NODE_RESET=NO`
