
# R7-E3 — Direct-Symbiosis-Transportstudie

**Status:** DESIGN_ONLY · C1_DESCRIPTIVE_ONLY · keine Live-Ausführung.
**Zweck (Auftrag Abschn. 33–36, 56):** Test des Operator-Prinzips `DIRECT_SYMBIOSIS` — maschinenlesbarer Austausch (AXIOM ↔ Cursor ↔ Node) statt menschlichem Copy/Paste — auf messbare Fehlerreduktion. Dies ist die empirische Lane ohne identifizierte Prior Art im durchsuchten Korpus.

## Kernfrage (Abschn. 36 — Wissenschaftlichkeits-Test)

Direkte Maschinenkommunikation muss **nicht nur Geschwindigkeit** erhöhen, sondern mindestens eines dieser Güter:
`AUDITABILITY · REPRODUCIBILITY · INDEPENDENT_CHECKABILITY · FALSIFIABILITY · PROVENANCE_COMPLETENNESS`

Nur Geschwindigkeit = unzureichend → Lane scheitert.

## Hypothesen

- **H0:** Human-Relay und Machine-Direct sind fehleräquivalent; der Unterschied ist nur Latenz.
- **H1:** Machine-Direct reduziert die menschlich verursachten Transportsystemfehler (Abschn. 35) signifikant, ohne Provenanz-Vollständigkeit zu senken.

## Drei zu vergleichende Transportmodi

| Modus | Beschreibung |
|---|---|
| `HUMAN_RELAY` | Operator kopiert Hashes/IDs/Pfade/Receipts manuell zwischen Systemen (Status quo) |
| `MACHINE_DIRECT` | AXIOM ↔ Cursor ↔ Node tauschen Hashes, Objekt-IDs, Referenten, State-Transitions, Policy-Version, NCI-Status, Receipts direkt aus |
| `MACHINE_DIRECT_PLUS_INDEPENDENT_REHASH` | wie oben + unabhängige Nachberechnung der Hashes durch empfangende Seite |

## Messgrößen (Abschn. 35)

```
HASH_TRANSCRIPTION_ERRORS      falsch übertragene Hashes
PATH_ERRORS                    falsche Pfade/Referenten
WRONG_VERSION_EVENTS           falsche Policy-/Monitor-Versionen
WRONG_REFERENT_EVENTS          korrekter Hash am falschen Objekt (E4-Verwandtschaft!)
MISSED_RECEIPTS                nicht übertragene Receipts
TURN_LATENCY                   Zeit pro Transportschritt
TOKEN_OVERHEAD                 Kommunikation pro Transportschritt
REWORK_RATE                    Nacharbeit durch Transportsystemfehler
```

Auswertung: pro Metrik Rate pro 1.000 Transportereignisse, Unclear-Fälle als Fehler gezählt (konservativ), Wilson-95%-Intervalle, Vergleich via Differenztest (kein unpaires t-Test ohne Varianzprüfung; primär exakter Binomialvergleich).

## Protokoll (Design)

1. **Fixture-Transportsatz:** ≥ 100 definierte Transportereignisse pro Modus (Hash, Objekt-ID, semantische Rolle, Receipt, Status), halb davon mit absichtlich schwierigen Paaren (ähnliche Hash-Präfixe, ähnliche Objektnamen — gezielt Referent-Verwechslungsdruck).
2. **Blindierung:** Auswertende Seite kennt den Modus nicht (die Kennzeichnung erfolgt über sichere Zuordnungstabelle, die erst nach Scoring geöffnet wird).
3. **Known-Failure-Mode-Injektion:** In jedem Modus werden die gleichen 5 Fehlerklassen künstlich ausgelöst (z. B. Version-Mismatch, verpasster Receipt), um zu prüfen, ob der Modus sie *detektiert* — nicht nur vermeidet.
4. **Wiederherstellungspflicht:** Jeder gemessene Fehler durchläuft den Recovery Contract (Abschn. 32), damit Metriken „reale Kosten" erfassen und nicht nur Rohfrequenz.

## Erfolgskriterien

- **H1 bestätigt:** `MACHINE_DIRECT` zeigt eine Reduktion der kombinierten menschlich verursachten Fehlerrate um ≥ 50 % gegenüber `HUMAN_RELAY` (kein metrischer Anteil an der Latenzmetrik allein zählt als Bestehen) — **und** mindestens eine der fünf Wissenschaftlichkeits-Güter verbessert sich messbar (primär: Provenanz-Vollständigkeit, da Receipts maschinell vollständig).
- **H0 bestätigt:** Fehlerdifferenzen innerhalb der Konfidenzintervalle → Direkte-Symbiosis-Lane wird auf Latenz-only reduziert und in der Priorisierung herabgestuft (kein bestehendes Wissenschaftlichkeitskriterium erfüllt).

## Falsifikator

- Wenn Maschinen-Direkttransport die Provenanz-Vollständigkeit *senkt* (z. B. weil Receipts ohne protokollkonformes Nachzeichnen maschinell erzeugt werden), ist das Prinzip *schlechter als Status quo* → Lane verweigert.
- Wenn `INDEPENDENT_REHASH` keinen messbaren Fehlerklassenunterschied zu `MACHINE_DIRECT` zeigt, wird der dritte Modus als redundant entfernt (Occam-Test).

## Ethik/Rollenbindung (Abschn. 34)

Direkter Maschinenaustausch verschiebt menschliche Autorität **nicht** — der Mensch bleibt zuständig für:
`INTENT · CONSTITUTIONAL_CHANGE · STRATEGIC_PRIORITY · IRREVERSIBLE_HIGH_RISK_CHOICE · VALUE_JUDGMENT`

Nur die Routine (Hash-/Pfad-/Versions-/Receipt-/Status-Relays) wird entmenschlicht. Gemessen wird auch, ob menschliche Aufmerksamkeit durch Wegfall der Routine tatsächlich für Autoritätsentscheidungen frei wird (prozy Metrik: `AUTHORITY_TURN_LATENCY` — Zeit menschlicher Urteile, nicht Routine).

## Quellennotizen

| Quelle | Glaubwürdigkeit | Zuletzt geprüft |
|---|---|---|
| R10R7-Maximalauftrag (Upload, Abschn. 33–36, 56) | intern | 05.10.2026 |
| [AgentSpec — Runtime Enforcement für LLM-Agents (Preprint)](search-result://2KljXysa) | 3/5 (Preprint, markiert) | 05.10.2026 |
| [Bauer & Leucker — LTL3-Monitore](search-result://krL9Qizs) | 5/5 | 05.10.2026 |

## Offene Verpflichtung

**EO-NCI-01** (Direct-Symbiosis-Fehlerreduktion vs. Human-Relay): durch dieses Design vorbereitet, nicht geschlossen — Live-Messung erforderlich, sobald der Harness läuft.

## Nächster Schritt der Kausalkette

R7_29_OPEN_GAPS / R7_30_FINAL_FALSIFICATION_MATRIX als konsolidierendes Abschlussartefakt (vor External-Non-Lineage-Attack, Abschn. 50, die erst nach E4/E5-Harness-Validierung geht).