# M9 Crosswalk — AXIOM canonical vs MANUS local aliases

STATUS = OPEN_REQUIRED_BEFORE_TEST_ADOPTION
SILENT_CREDIT = PROHIBITED
SOURCE = PR427/04_R43_FOUR_HARD_CONTRADICTIONS_B01_B04.md + Cursor C1 inspect

| ID | AXIOM canonical object | MANUS local alias (report) | Equivalence |
|----|------------------------|----------------------------|-------------|
| M9-01 | same-mount independent Gaussian sensors → added Fisher info | Android timebase / SensorEvent.timestamp | NO |
| M9-02 | correlated Gaussian joint model | generic biomechanical observations | NO |
| M9-05 | units 1 vs 1e6 / eps_rank misclassification | batching/sleep/receiver time | NO |
| M9-07 | prior-only likelihood nullspace | MHEALTH grouping and split protocol | NO |
| M9-08 | no double count of shared prior | independent evaluator heldout/cost | NO |
| M9-09 | biased CRB shrinkage counterexample | signature trust and role | NO |
| M9-10 | reference-oracle feature leakage | public BodyTwin event witness | NO |
| M9-13 | selective risk-vs-abstention costs | MHEALTH/FDA grouping | NO |
| M9-16 | original frozen primary vs posthoc sensitivity | crypto attestation | NO |

RULE = MANUS_LOCAL_M9_ALIAS ≠ CANONICAL_M9_PASS
NEXT = NEW_CANONICALLY_INDEXED_RECEIPTS_OR_NOT_RUN
