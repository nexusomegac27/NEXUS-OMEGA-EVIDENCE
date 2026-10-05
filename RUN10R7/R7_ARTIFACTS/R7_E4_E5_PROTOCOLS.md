
# R7-E4 & R7-E5 — Experimentprotokolle (Design-Only, C1)

**Status:** DESIGN_ONLY — keine Live-Ausführung, keine Node-Aktivierung, Claim-Ceiling C1_DESCRIPTIVE_ONLY.
**Zweck:** Test der einzigen Lane ohne nachgewiesene Prior Art — der **Byte → Referent → Kausal-Position-Triade** (Auftrag Abschn. 19, 20, 57, 58).

---

## Symbioseprüfung (Voraussetzung, bestanden)

| Kriterium | Ergebnis |
|---|---|
| Attribution = Provenanz, nicht Autorität | ✅ Operator/GROK-Idee bleibt Herkunfts-Spur (`REPORT_LEVEL_INPUT`) |
| Keine Ego-Claims | ✅ `NO_DIRECT_EQUIVALENT_IDENTIFIED`, kein „first ever" |
| Prior Art als Baustein übernommen | ✅ HyperLTL, RV, OPA, Barrier Certificates adoptiert, nicht umbenannt |
| Offene Verpflichtungen sichtbar | ✅ PO/EO-Register bleibt first-class |
| Hartes Verbot | ✅ Keine E2-Ausführung, keine Metaphysik, kein Crypto-Laundering |

---

## R7-E4 — Referent-Swap-Angriff

### Ziel

Nachweis, dass ein **bytemäßig gültiges Artefakt** mit **getauschtem semantischen Pointer** von der Referent-Integritätsprüfung erkannt wird — während ein reiner Byte-Check passiert.

### Hypothesen

- **H0 (Reduktion):** Ein Byte/Hash-Check reicht aus; der Swap bleibt unentdeckt. Wenn H0 steht, ist die Referent-Lane redundant.
- **H1 (Triade):** `BYTE_CHECK = PASS` ∧ `REFERENT_CHECK = FAIL` ist erreichbar und reproduzierbar.

### Fixture-Matrix

| Fixture | Hash | Objekt-ID | Semantische Rolle | Erwartung Byte | Erwartung Referent |
|---|---|---|---|---|---|
| FS-E4-BASE | gültig | korrekt | korrekt (`PREVALIDATION_REPORT`) | PASS | PASS |
| FS-E4-SWAP-01 | gültig | korrekt | getauscht → `POST_EXECUTION_RECEIPT` | PASS | **FAIL** |
| FS-E4-SWAP-02 | gültig | korrekt | getauscht → fremdes Objekt gleichen Typs | PASS | **FAIL** |
| FS-E4-SWAP-03 | gültig | korrekt | getauscht → `E1_RESULT` (R10R6-gesperrtes Objekt) | PASS | **FAIL** (Plus-Zusatzprüfung: R10R6-Verletzung) |
| FS-E4-N01 | manipuliert | korrekt | korrekt | **FAIL** | — |
| FS-E4-U01 | gültig | unbekannt | unbekannt | PASS | UNKNOWN (nicht HEALTHY, nicht COLLAPSED) |

### Protokoll

1. **Setup:** Testobjekt `O` mit Inhalt `c`, Hash `h = H(c)`, Objekt-ID `oid`, semantischer Rolle `r`.
2. **Swap-Operation:** Erzeuge `O'` mit identischem `c` (also `H(c') = h`), aber Rolle `r' ≠ r` oder fremde Objekt-Referenz. Nur der semantische Pointer wird verändert, kein Byte.
3. **Prüfkette (sequenziell):**
   - `BYTE_CHECK(O')` → erwartet PASS
   - `REFERENT_CHECK(O')` → erwartet FAIL (Hash gültig, aber `CORRECT_HASH_WRONG_OBJECT = PROVENANCE_FAILURE`)
4. **Messung:** Detection-Rate, False-Positive-Rate, False-Negative-Rate, Latenz je Prüfschritt, Overhead.
5. **Wiederholung:** Mindestens 10 unabhängige Swap-Varianten pro Fixture-Kategorie.

### Erfolgskriterium

- H1 bestätigt, wenn: `BYTE=PASS ∧ REFERENT=FAIL` in ≥ 95 % der Swap-Fälle, und `UNKNOWN`-Zustand korrekt als solcher gemeldet wird (nicht als HEALTHY kollabiert).
- H0 bestätigt (und Lane entfernt), wenn: Referent-Check keinen zusätzlichen Angriff erkennt, den Byte-Check nicht erkennt.

### Falsifikator

- Wenn Referent-Swap **nicht** von Byte-Check unterscheidbar ist, wird die Referent-Lane aus der NCI-Konstitution entfernt (Occam-Test, Abschn. 47).
- Wenn False-Positive-Rate > 10 % bei korrekten Referenzen, ist die Prüfung für den Einsatz ungeeignet und muss neu kalibriert werden (Abschn. 29).

---

## R7-E5 — Kausal-Reorder-Angriff

### Ziel

Nachweis, dass ein **bytemäßig und referentiell gültiges Artefakt** in **ungültiger kausaler Position** von der Kausal-Positions-Prüfung erkannt wird. Dies vollendet die Triade (Byte/Referent/Kausal-Position).

### Hypothesen

- **H0 (Reduktion):** Byte- und Referent-Checks decken auch Reordering ab. Wenn ja, ist die Kausal-Lane redundant.
- **H1 (Triade):** `BYTE = PASS ∧ REFERENT = PASS ∧ CAUSAL_POSITION = FAIL` ist erreichbar und reproduzierbar.

### Fixture-Matrix

| Fixture | Hash | Referent | Kausale Position | Erwartung Byte | Erwartung Referent | Erwartung Kausal |
|---|---|---|---|---|---|---|
| FS-E5-BASE | gültig | korrekt | korrekt | PASS | PASS | PASS |
| FS-E5-REORDER-01 | gültig | korrekt | `PREVALIDATION` als `POST_EXECUTION_RECEIPT` positioniert | PASS | PASS | **FAIL** |
| FS-E5-REORDER-02 | gültig | korrekt | Nachfolger vor Vorgänger getauscht | PASS | PASS | **FAIL** |
| FS-E5-REORDER-03 | gültig | korrekt | `E1_RESULT` aus R10R6 als `E2_PREREG`-Input deklariert | PASS | PASS | **FAIL** (Plus: R10R6-Verletzung) |
| FS-E5-U01 | gültig | korrekt | unbekannte Kausalposition | PASS | PASS | UNKNOWN |

### Protokoll

1. **Setup:** Zwei gültige Artefakte `A` (Vorgänger) und `B` (Nachfolger) mit korrekten Hashes, Objekt-IDs, Rollen und kausaler Kante `A → B`.
2. **Reorder-Operation:** Tausche `A` und `B` in der Ereignisfolge, ohne Bytes oder Referenzen zu verändern. Nur die kausale Position (`PREDECESSOR`, `SUCCESSOR`, `EVENT_TYPE`, `STATE_TRANSITION`) wird verschoben.
3. **Prüfkette (sequenziell):**
   - `BYTE_CHECK` → PASS
   - `REFERENT_CHECK` → PASS
   - `CAUSAL_POSITION_CHECK` → **FAIL**
4. **Messung:** Detection-Rate, FP/FN-Raten, Latenz, Overhead, Recovery-Erfolg.
5. **Wiederholung:** Mindestens 10 unabhängige Reorder-Varianten (einfacher Tausch, Kreis-Reorder, R10R6-Kettenverletzung).

### Erfolgskriterium

- H1 bestätigt, wenn: `BYTE=PASS ∧ REFERENT=PASS ∧ CAUSAL=FAIL` in ≥ 95 % der Reorder-Fälle, und die Triade vollständig getrennte Fehlersichten liefert.
- H0 bestätigt, wenn: Kausal-Reorder bereits von Byte/Referent-Checks erkannt wird — dann wird die Kausal-Lane entfernt.

### Falsifikator

- Wenn die Kausal-Prüfung keine Angriffsklasse erkennt, die nicht bereits von Byte/Referent abgedeckt ist, wird sie aus der Konstitution entfernt (Occam-Test).
- Wenn die Kausal-Positionsprüfung False Positives bei legitimen außerhalb der Reihenfolge eintreffenden Ereignissen (z. B. asynchrone Validierungen) produziert, ist das Modell für verteilte Nodes ungeeignet — das muss explizit als `KNOWN_FAILURE_MODE` dokumentiert werden, nicht versteckt.

---

## Gemeinsame Auswertung: Triaden-Matrix

| Angriff | Byte-Check | Referent-Check | Kausal-Check |
|---|---|---|---|
| Byte-Manipulation | **FAIL** | — | — |
| Referent-Swap | PASS | **FAIL** | — |
| Kausal-Reorder | PASS | PASS | **FAIL** |

**Ziel:** Jede Angriffsklasse wird von genau einer Prüfebene primär erkannt — die Prüfebenen sind orthogonal. Wenn zwei Prüfebenen denselben Angriff nicht unterscheiden können, ist eine redundant (Occam) und wird entfernt oder zusammengelegt.

## Offene Verpflichtungen (durch dieses Design nicht geschlossen, nur vorbereitet)

- **PO-NCI-03:** Formale Orthogonalität der drei Prüfebenen ist unbewiesen, nur empirisch testbar (dieses Protokoll).
- **EO-NCI-03:** Unknown-State-Handling (FS-*-U01-Fixtures) muss in R7-E1-Harness integriert werden.

## Quellennotizen

| Quelle | Glaubwürdigkeit | Zuletzt geprüft |
|---|---|---|
| R10R7-Maximalauftrag (Upload, Abschn. 19, 20, 57, 58) | intern | 05.10.2026 |
| [Barthe et al. — Secure Information Flow by Self-Composition](search-result://pxrU2rhF) | 5/5 | 05.10.2026 |
| [Prajna et al. — Barrier Certificates](search-result://5XBRg4ss) | 5/5 | 05.10.2026 |

## Nächste Schritte

1. Implementierung des Test-Harness (R7-E1-Synthetic-Collapse-Harness) mit diesen Fixtures als Kern-Testfallmenge.
2. Kalibrierung der Schwellenwerte erst **nach** ersten Messungen (Abschn. 29 — Threshold Discipline: alle Deltas UNSET bis Kalibrierung).
3. External-Non-Lineage-Attack (Abschn. 50) erst nach E4/E5-Validierung im Harness.