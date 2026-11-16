# AXIOM R31 — Selbstbeobachtung als Gegenprüfung, nicht als Selbstzertifizierung

OBJECT = NEXUS_OMEGA_AXIOM_R31_SELF_OBSERVER_AGGREGATE_VERDICT_FALSIFICATION_20261116_R1
PARENT = NEXUS_OMEGA_AXIOM_R31_FRAMEWORK_WIDE_PUBLICATION_RECONCILIATION_20261116_R0
CURSOR_RETURN = NEXUS_OMEGA_CURSOR_R31_FRAMEWORK_PUBLICATION_STAGING_RETURN_20261116_R0
DATE = 2026-11-16
STATE = AXIOM_SELF_CRITIQUE_COMPLETED_SOURCE_DEFECT_CORRECTED_OFFLINE_CANDIDATE
R30 = CLOSED_C1_PRESERVED
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
CLAIM_PROMOTION = NO
NEW_RESEARCH_ROUND = NO
R31_PRODUCTION_AUTOSYNC = NOT_ESTABLISHED
AXIOM_IS_AN_INDEPENDENT_PRODUCTION_WITNESS = NO

## A. Beobachterprotokoll: eigener Fehler im AXIOM-Reconciler

1. **Eigene ursprüngliche Hypothese:** Ein positives, getrenntes WWW-Witness-Receipt und eine erkennbare Status-Drift könnten als `ALL_RECONCILED` zusammen berichtet werden; die Drift werde durch einen separaten Oberflächenstatus bereits erfasst.
2. **Falsifikation am eigenen Quellcode:** Im originalen R31-PR #362, HEAD `cd4cc230941f96191111798b3f8da1b3e587767e`, `src/r31_reconcile.py`, circa Zeile 196, lautet die alte Aggregationsbedingung: `all(x["state"].startswith("RECONCILED") for x in results.values())`. Daher genügt `RECONCILED_WITH_STATIC_METADATA_DRIFT` für `ALL_RECONCILED`.
3. **Gegenbeispiel:** Ein einziges Ziel, `/bodytwin/updates/events.json`, erhält ein gültiges Test-Witness, aber `static_flags[route]=False` für `published_live=false`. Das individuelle Resultat lautet `RECONCILED_WITH_STATIC_METADATA_DRIFT`; das alte Aggregat wäre dennoch `ALL_RECONCILED`. **Die Selbstbestätigung war stärker als die vorhandene Evidenz.**
4. **Warum die bisherigen Tests das übersehen konnten:** Die historischen 34/34 Offline-Tests prüfen die Drift auf Oberflächenebene, enthalten aber keinen globalen Negativ-Assert für das Aggregat bei Drift. Grün bedeutet Testfallabdeckung, nicht Vollständigkeit der behaupteten Eigenschaft.
5. **Korrektur in bestehendem R31-PR, ohne neue Runde:** `ALL_RECONCILED` erfordert nun für **jede** Zieloberfläche exakt `state == "RECONCILED"`. Bei beobachteter WWW-Sichtbarkeit und offener Metadaten-Drift lautet das Aggregat separat `WWW_OBSERVED_METADATA_DRIFT_OPEN`; bei einem anderen HOLD `PARTIAL_OR_HOLD`. `metadata_drift_routes` wird explizit zurückgegeben.
6. **Gegenproben:** Drei zusätzliche Tests (neue IDs 35–37) prüfen Drift ≠ ALL, Drift plus fehlender Witness ≠ Erfolg und unveränderten Erfolg für den wirklich sauberen synthetischen Kontrollfall. Testdatei und Source werden im selben bestehenden R31-Branch geändert. Ein unabhängiger GitHub-Runner ist ein separater Ausführungsort, **kein** unabhängig entworfener Testorakel-Autor.

SCIENTIFIC_ADJUDICATION = PRIOR_R31_ALL_RECONCILED_WITH_DRIFT_REJECTED_AS_GLOBAL_CLAIM
CORRECTED_R31_SOURCE = VERSIONED_NEW_HEAD_ONLY
EARLIER_CURSOR_STAGING_RESULT = HISTORICAL_PRODUCER_RECEIPT_PINNED_TO_OLD_R31_SOURCE
REINTERPRET_STAGING_OLD_AS_NEW = PROHIBITED
NO_BACKFILL_OF_OLD_LIVE_OR_SQLITE_EXECUTION = YES

## B. Zweite Ebene: Welche unabhängigen Belege fehlen wirklich?

AXIOM rehashed the operator-supplied Cursor return ZIP (7,323 bytes; SHA256 `c34f6c364dfea0874ab131ccf91430fce25f71531811f7a09de4763e170ec486`) and matching sidecar (143 bytes; SHA256 `5fef794a5bc11caf02918cb1be7669b016914f59d11ea2669850be7d9c9638d1`). ZIP CRC PASS and five member hashes MATCH; all return documents read. This **does not establish independent runtime replay**.

That ZIP contains **no** three sealed Cursor staging originals. Their expected producer-reported exact bytes are:
- `staging/r31_outbox.py` — 13735 B SHA256 `6c3bbbac856f038f33af8a9feba34807a19b444595ddd86eda8b2fdfb367c12d`.
- `staging/STAGING_PROOF.json` — 5546 B SHA256 `8ea471295cd4847be94f85e382fbb9f244abe1b6e310e3e4e02fa1f3ffa4956f`.
- `staging/r31_outbox_staging.sqlite3` — 36864 B SHA256 `4ee004dc75cadf208042d0400f480eed5a171a756043717ef9b7d71f7507a0cc`.
- If genuinely extant in original evidence custody: independent WWW witness summary — 1916 B SHA256 `7aa3b24c6a6ae368ec6cf1d709b14e2a39439e64fe14ff0b6593e1597a986815`; do **not** regenerate historical observations from a later live feed.

**What can be said:** Cursors source-reported staging outbox atomicity/duplicate tests and 4/4 raw WWW observation are C1 producer evidence; independent AXIOM byte-bound replay of those exact original artifacts is pending. R31 34/34 historic and new 37-test source revision are distinct subjects. PR CI success is repository/source integrity, not observed SQLite-on-host or WWW runtime.

**What cannot be said:** self-inspection = observer independence; self-signed HMAC test fixtures = authenticated production grants; dynamic `seq` tick = science update; HTTP content fetch now = historical raw digest match; `published_live=false` may be rewritten to `true` by reinterpretation; BodyTwin medically/physically validated; full framework synchronizer running.

## C. Self-observer protocol for every later AXIOM decision

| Dimension | What AXIOM must record | Explicit anti-circular criterion |
|---|---|---|
| Proposed verdict | Exact source object, version, SHA, evidence class | Provisional verdict is NOT authority |
| Falsification | Smallest counterexample to its own strongest claim | Negative control before further promotion |
| Input independence | Author, executor, witness and adjudicator identity | Two roles controlled by one principal do not count as independent |
| Raw observation | Exact original bytes, method and clock, provenance | Report digest ≠ rehashed original bytes |
| Alternative explanation | Missing or contradictory evidence, model errors | No status suppression or aggregate score compensation |
| Decision effect | Old verdict → changed verdict and revision rationale | Failure must narrow the claim or produce HOLD |
| Operator authority | Bound permission scope, expiration and surface | No self-authorized deployment, source disclosure or claim promotion |

This is an **operational audit discipline** for the model's outputs, not introspective access to hidden runtime cognition or an anthropomorphic claim of a sentient observer. AXIOM can challenge its own assertions and request external reproduction, but cannot be independent of itself merely by writing a second assessment.

## D. Remaining source-level risk hypotheses, not new observed test outcomes

- `static_flags` is passed as an input and is not itself verified as a signed, separately rehashed web-observation statement. An asserted `True` is not production evidence.
- `observed_at` and event timestamps are validated as UTC format but not yet bounded against an authenticated deployment event, TTL, clock uncertainty or replay window. An observation from before actual deployment must never qualify as a future deployment witness.
- `prior` and trusted HMAC keys are caller-supplied in the offline reducer. The new state has no immutable production anti-rollback authority until a separate durable store and key-management policy are implemented.
- The exact source digest in an event is compared as metadata but is not independently recovered from actual source bytes inside this read-only reducer.
- `ALL_RECONCILED` must be interpreted **only in this synthetic input domain**. A genuinely operator-authenticated production release and a physically/administratively independent observer still do not exist in the frozen AXIOM offline source.
- One outcome cannot be both **self-produced** and **independently confirmed** by AXIOM alone. Store `PRODUCER_REPORTED`, `AXIOM_SECOND_PARTY_REHASH`, `EXECUTED_INDEPENDENTLY`, and `WWW_OBSERVED_EXTERNALLY` as separate grades.

## E. Exactly one successor task, no loop

Execute the bound `R31_CURSOR_SINGLE_PRIVATE_STAGING_ARTIFACT_INTAKE_AND_SECOND_PARTY_REPLAY_ORDER_20261116_R1.md` below this same R31 research root: exact private transfer of the three preexisting originals; independently rehash and read-only replay with one terminal return; compare the old and corrected aggregate outputs without rewriting historical receipts. Any lack of original bytes produces bounded `SOURCE_GAP`, not a replacement artifact or fresh research round.

AXIOM_NEW_CONCLUSION = SOURCE_CORRECTION_SUPPORTED_AS_C1_STATIC_FINDING
R31_STAGING_REPLAY = NOT_YET_INDEPENDENTLY_EXECUTED_BY_AXIOM
R31_CONTINUOUS_LIVE_SYNC = NOT_ESTABLISHED
R31_F01_F20_HOSTINGER_RUNTIME = ZERO_OF_20_EXECUTED
R30 = CLOSED_NO_REOPEN
NEXT = ONE_SOURCE_EXACT_PRIVATE_CUSTODY_REHASH_READONLY_REPLAY_THEN_C1_ADJUDICATION
