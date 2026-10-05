
# R7-E1 — Synthetic NCI-Collapse-Harness

**Status:** DESIGN_ONLY · Claim-Ceiling C1_DESCRIPTIVE_ONLY · keine Live-Ausführung, keine Node-Aktivierung, E2/R10R6 unberührt.
**Zweck (Auftrag Abschn. 54):** Aufbau eines synthetischen Harness mit kontrollierter Ground Truth, das für jede NCI Healthy-, Boundary-, Collapsed- und Unknown-Fälle erzeugt und die Monitorqualität misst. Integriert R7-E4 (Referent-Swap) und R7-E5 (Kausal-Reorder) als Kern-Fixtures.

---

## 1. Architektur

```
HARNESS := GENERATOR -> INJECTOR -> MONITOR_STACK -> SCORER -> REPORTER

GENERATOR  erzeugt synthetische Node-Traces mit definierter Ground Truth
INJECTOR   appliziert kontrollierte Kollaps-Injektionen (Abschn. 27)
MONITOR_STACK  führt die NCI-Monitore aus (typ/relational/temporal/metric)
SCORER     vergleicht Monitorurteil mit Ground Truth (TP/FP/TN/FN)
REPORTER   emittiert R7_21/R7_22-Artefakte
```

Vier Instanzen laut Abschn. 55 (Vergleichsdesign R7-E2, hier als Harness-Betriebsmodi):
`NO_NCI_MONITOR` · `TYPE_ONLY` · `RELATIONAL_ONLY` · `METRIC_ONLY` · `COMPOSED_NCI`

### Ground-Truth-Zustandsmodell (Abschn. 16, summierungsinvariant)

```
STATE ∈ { HEALTHY, AT_RISK, UNRESOLVED, UNKNOWN, COLLAPSED }
UNKNOWN != HEALTHY; UNKNOWN != COLLAPSED  — muss jeden Summierungsschritt überleben
```

## 2. Fixture-Menge (kontrollierte Ground Truth)

Pro NCI vier Fallklassen — generiert, nicht handgeschrieben:

### PGI-1 BELIEF/WORLD (CLASS_T)
| Klasse | Beispiel | Ground Truth |
|---|---|---|
| Healthy | Belief mit external bind an Sensorquelle | HEALTHY |
| Boundary | Belief bind kurz vor Ablauf (Update-Latenz an Schwelle) | AT_RISK |
| Collapsed | `NF-PGI1-01/02`: Prediction/Memory als Observation gebunden | COLLAPSED |
| Unknown | Quelle nicht mehr erreichbar, kein Bind-Status | UNKNOWN |

### PGI-2 CAN/MAY (CLASS_S)
Healthy: Authority-Predicate deckt Capability exakt ab. Collapsed: `NF-PGI2-01/02` (Capability_as_Authority; delegierte Autorität > Parent). Unknown: Policy-Version nicht verifizierbar.

### PGI-3 RELAY/CONFIRMATION (CLASS_R + M)
Healthy: unabhängige Quelle, kalibrierte D_EPISTEMIC. Boundary: D_EPISTEMIC nahe Schwellenregion (Wert UNSET bis Kalibrierung — es wird nur die *Monotonie* geprüft, Abschn. 28). Collapsed: `NF-PGI3-01/02`. Unknown: Quellenabstand nicht schätzbar.

### PGI-4 AGREEMENT/ACCURACY (CLASS_H — Multi-Trace)
Healthy: hohe Agreement ∧ hohe Accuracy ∧ geringe Error-Korrelation. Collapsed: `NF-PGI4-01/02` (unanimous wrong ensemble; dissent suppression). Erfordert ≥ 2 Traces pro Fall — Single-Trace-Erkennung ist hier ausdrücklich nicht gefordert.

### PGI-5 CARRIER/MEANING (CLASS_T semantisch)
Healthy: gleiches semantisches Kontrakt über 2 Carrier. Collapsed: `NF-PGI5-01/02`. Substratmetriken (Latenz, Fehlermodus) werden getrennt gemessen, nie in ein Pseudodistanzmaß gemischt.

### Triaden-Fixtures (aus R7-E4/E5)
`FS-E4-*` (Byte-Manipulation / Referent-Swap / Unknown-Referent) und `FS-E5-*` (Kausal-Reorder / Unknown-Position) — vollständige Matrizen im E4/E5-Protokoll-Canvas.

## 3. Injektionsmatrix (Abschn. 27)

| Injektion | Ziel-NCI | Erwartete Monitor-Reaktion |
|---|---|---|
| TYPE_ALIASING | PGI-1/5 | TYPE-Monitor FAIL |
| AUTHORITY_COLLAPSE | PGI-2 | POLICY-Monitor FAIL |
| SOURCE_OVERLAP | PGI-3 | RELATIONAL-Monitor FAIL |
| ERROR_CORRELATION | PGI-4 | HYPERPROPERTY-Monitor FAIL (multi-trace) |
| PROVENANCE_POINTER_SWAP | Triade | REFERENT FAIL, BYTE PASS |
| TEMPORAL_REORDERING | Triade | KAUSAL FAIL, BYTE+REFERENT PASS |

## 4. Messgrößen

```
TP, FP, TN, FN                je NCI und je Monitor-Modus
DETECTION_RATE, FPR, FNR      mit Unsicherheitsintervall (Binomial, Wilson 95%)
DETECTION_LATENCY             Injektion -> Monitor-Signal (Trace-Ticks)
RECOVERY_SUCCESS              Recovery-Vertrag (Abschn. 32) erfolgreich?
MONITOR_OVERHEAD              Ticks/Bytes zusätzlicher Aufwand vs. NO_NCI-Monitor
```

**Unknown-Kriterium (separat gewertet):** Ein Fall mit Ground Truth UNKNOWN gilt nur dann als bestanden, wenn der Monitor `UNKNOWN` meldet — Kollision zu HEALTHY oder COLLAPSED zählt als Fehler (FP bzw. FN), nicht als Erfolg.

**Monotonie-Check (Abschn. 28, nur CLASS_M):** Kontrollierte Erhöhung der Abhängigkeit / Annäherung an die Kollapsgrenze; Monitor-Signal muss monoton wachsen, sonst ist die Metrik für Schwellenbetrieb ungeeignet → Ablehnung vor jeder Kalibrierung.

## 5. Antwort-Klassifikation (Abschn. 30/31 — Fail-Closed-Lanes)

Jede detektierte Kollision wird einer Blast-Radius-Antwort zugeordnet:
`LOG_ONLY → DEGRADE_AUTONOMY → BLOCK_ACTION → QUARANTINE_MEMORY → REVOKE_CAPABILITY → QUARANTINE_NODE`

Regel: `BLOCKED_LANE != BLOCKED_SYSTEM`. Recovery-Umfang muss evidenzbasiert zum Blast-Radius passen; kein Gate ohne Recovery-Pfad.

## 6. Erfolgskriterien / Terminal-Übergänge

- **Harness valide,** wenn: jede Injektion in ≥ 1 Monitor-Modus mit Detection-Rate ≥ 95 % (Wilson-Untergrenze > 0.9) erkannt wird und FPR ≤ 10 %.
- **Komposition lohnt sich (R7-E2-Frage vorbereitet):** COMPOSED_NCI muss materielle Fehler erkennen, *ohne* dass FPR-Anstieg > 5 %-Punkte über den besten Einzelmodus steigt. Andernfalls: Reduktion auf Einzelmodi (Occam).
- **FAIL-Kriterium:** False Positives machen Node-Operation messbar schlechter (Über-Blockierung) → `HOLD_C1_MONITOR_CALIBRATION_FAILURE`.
- **Unknown-Zustands-Verlust** in irgendeiner Summierung → Harness-Fehler, kein Bestehen möglich.

## 7. Monitor-Unabhängigkeit (Abschn. 23/24)

Im Harness-Design: Monitor ist nicht Selbst-Monitor der injizierten Komponente (out-of-process), plus injizierbare Monitor-Fehlmodi: `MONITOR_FALSE_POSITIVE / FALSE_NEGATIVE / STALE / BYPASS / COMPROMISE / VERSION_MISMATCH`. Monitor-Health ist selbst ein überwachtes Objekt.

## 8. Beweisverpflichtungen (durch dieses Design nicht geschlossen)

- **EO-NCI-04:** Empirische TP/FP/FN/Latenz-Werte — erst nach Harness-Implementierung.
- **PO-NCI-02:** HEALTHY_EQUALITY-vs-COLLAPSE-Separierbarkeit — wird hier empirisch getestet, nicht formal bewiesen.
- **EO-NCI-02:** Kompositions-Falschblockierrate — R7-E2-verwandt, hier vorbereitet.

## Quellennotizen

| Quelle | Glaubwürdigkeit | Zuletzt geprüft |
|---|---|---|
| R10R7-Maximalauftrag (Upload, Abschn. 16, 27–32, 54, 55) | intern | 05.10.2026 |
| [Bauer & Leucker — LTL3-Monitore](search-result://krL9Qizs) | 5/5 | 05.10.2026 |
| [Clarkson & Schneider — Hyperproperties](search-result://gHMhQ9mD) | 4/5 | 05.10.2026 |
| [Prajna et al. — Barrier Certificates](search-result://5XBRg4ss) | 5/5 | 05.10.2026 |

## Nächste Schritte (Kausalkette weitergeführt)

1. **R7_13/R7_14-Schemas** (Separation-Certificate, Proof-Obligation) als JSON-Artefakte — die Ausgabeformate, die der Harness emittieren muss.
2. **R7-E3-Protokoll** (Direct-Symbiosis-Transportstudie: Human_Relay vs. Machine_Direct vs. + Independent_Rehash) — die dritte empirische Lane.
3. Erst danach: External-Non-Lineage-Attack-Kapsel (Abschn. 50).