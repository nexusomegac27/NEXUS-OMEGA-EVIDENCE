# NEXUS OMEGA · R25
## NF-05 und NF-06 — Vorregistrierungs-Entwurf (Preregistration Draft)
### Design-only · nicht ausgeführt · keine Runtime-Freigabe

```text
OBJECT                     = NEXUS_OMEGA_R25_NF05_NF06_PREREGISTRATION_DRAFT_20261010_R0
DATE_UTC                   = 2026-10-10T19:50:00+02:00
FROM                       = Perplexity Computer (Design-only-Lane)
TO                         = AXIOM / NEXUS_OMEGA_OPERATOR
PARENT_SPEC                = research/r10r23/na1-ring-stabilizer/orders/na1-drift-bound-test-protocol.json @ 17e0a3275ad9749458e251b1ec4eb07348b2c5ee (PR #65, OPEN_HOLD_SCOPED)
STATUS                     = PREREGISTRATION_DRAFT_WITH_UNRESOLVED_FIELDS
DESIGN_ONLY_NOT_EXECUTED  = TRUE
EXECUTION_AUTHORIZATION    = NONE
RUNTIME_RIGHTS             = NONE
PRODUCTION_WRITE           = NONE
GITHUB_MERGE               = NOT_AUTHORIZED
```

---

## 0. Wichtiger Hinweis

Dies ist ein **Vorregistrierungs-Entwurf** (`PREREGISTRATION_DRAFT_WITH_UNRESOLVED_FIELDS`), keine abgeschlossene, eingefrorene Vorregistrierung. Mehrere modellkritische Parameter und Schwellen sind im NA-1-Protokoll als `pass_criteria_proposal_operator_adjudicable` markiert und **noch nicht vom Operator/AXIOM final adjudiziert**. Die Ausführung bleibt untersagt, bis AXIOM die offenen Felder benennt und die Vorregistrierung explizit einfriert.

## 1. Bezug zum NA-1-Protokoll (source-exakt)

Beide Fixtures sind im NA-1-Protokoll (PR-#65-Head `17e0a32…`) bereits vorgezeichnet:

- **NF-05 ≙ NE-1 (MULTIPEAK_INJECTION):** `inject_two_bumps_expect_collapse_to_one`, Fail-Kriterium `more_than_one_peak_after_relaxation_time`.
- **NF-06 ≙ NE-4 + NE-8 (NO_INPUT_120S_DRIFT + FILTER_STALENESS):** `replay_with_real_omm_gaps_120s_plus`, Fail-Kriterium `measured_drift_exceeds_documented_bound`; sowie `staleness_flag_when_bound_exceeded`, Fail-Kriterium `no_STALE_flag_despite_proven_bound_breach`.

**Offene mapping-Frage (unresolved):** NF-06 überschneidet sich mit D3 (`filter_internal_drift_120s`) und D6 (`drift_source_attribution`). Die genaue Zuordnung „NF-06 = NE-4 ∨ NE-8 ∨ D3 ∨ D6“ muss vor dem Einfrieren geklärt werden; dieser Entwurf behandelt sie als **eine zusammengefasste Drift-Bound-Prüfung** mit Unterfallen.

## 2. Gemeinsame Modellannahmen (angepinnt an NA-1)

```text
MODEL_CLASS       = RING_ATTRACTOR_1D_C1
N_UNITS           = {32, 64}
STATE             = circular_phase_theta
READOUT           = POPULATION_VECTOR_AVERAGE
INGRESS_NO_INPUT  = BUMP_PERSISTENCE
INGRESS_WITNESS   = BUMP_SHIFT_NOT_CREATION
PROVENANCE_DUAL_FIELD = [predicted_state, last_external_witness, filter]
CLAIM_CEILING     = C1_DESCRIPTIVE_ONLY
```

**Nicht-Axiome (explizit):** Bump-Einzigkeit, Rauschrobustheit, `BUMP_PERSISTENCE`, externe Shift-ohne-Neuerzeugung. Diese sind Test-Hypothesen, keine bewiesenen Eigenschaften.

## 3. NF-05 — Multi-Peak-Injektion (Preregistration Draft)

### 3.1 Ziel und Hypothese

Prüfen, ob das 1-D-Ringmodell bei Injektion zweier gleichstarker Aktivitäts-Peaks nach definiertem Relaxationsfenster auf genau einen Peak kollabiert.

- **H0 (Nullhypothese):** Kollaps auf genau einen Peak innerhalb des Relaxationsfensters.
- **H1:** Mehr als ein Peak bleibt bestehen (Fail-Kriterium `MULTI_PEAK`).

### 3.2 Injektionsbedingungen (Entwurf, unresolved)

| Parameter | Wert | Status |
|---|---|---|
| Anzahl injizierter Peaks | 2 (symmetrisch um θ_inject platziert, z. B. θ_inject ± π/4) | Entwurf |
| Peak-Amplitude (relativ zur Ein-Peak-Baseline) | 1.0 (identisch) und 0.8 (asymmetrisch) | Entwurf |
| Peak-Breite (Rausch-σ) | aus Baseline-Run übernehmen, nicht neu wählen | Entwurf |
| Injektionszeitpunkt | t = 0, nach vollständiger Konvergenz eines Referenz-Bumps | Entwurf |
| Relaxationsfenster | 2 × (Bump-Umlaufzeit aus Baseline), mindestens 1000 Integrationsschritte | Entwurf |
| Zufalls-Seeds | 100 unabhängige deterministische Seeds pro Bedingung (wie NA-1 `runs_per_cell`) | Entwurf |

### 3.3 Peak-Zählregel (zirkulär, unverzichtbar)

Peaks werden über lokale Maxima des Population-Vektors `r(θ, t)` gezählt:

1. Berechne `r(θ_i, t)` auf dem zirkulären Gitter.
2. Finde lokale Maxima: `r(θ_i) > r(θ_{i-1})` und `r(θ_i) > r(θ_{i+1})` (zirkuläre Indizes, `θ_{N} = θ_{0}`).
3. Ein lokales Maximum zählt als Peak, wenn:
   - `r(θ_i) ≥ PROMINENCE_THRESHOLD` (z. B. 0.3 × max_t `r`), und
   - der zirkuläre Abstand zum nächsten zählenden Peak ≥ `MIN_SEPARATION_BINS` (z. B. `floor(N/8)`).
4. **Prominence- und Separations-Schwellen sind unresolved** — sie müssen vor dem Einfrieren von AXIOM/Operator festgelegt werden, nicht aus Explorationsdaten nachträglich.

### 3.4 Metriken (vorregistriert)

- `n_peaks(t)` über das Relaxationsfenster (Zeitreihe).
- `n_peaks_final` = `n_peaks(t_relax)`.
- Kollapszeit `t_collapse` = erster Zeitpunkt, an dem `n_peaks = 1` und bleibt.
- Amplitudenverhältnis `max(r) / r_baseline` bei `t_relax`.

### 3.5 Fail-Closed-Verhalten

- `n_peaks_final > 1` → `MULTI_PEAK` Reject, HOLD-Trigger für PR65.
- `n_peaks_final = 1` → **kein Beweis** der Ein-Peak-Eigenschaft im Allgemeinen; nur für die getestete Parameter-/Seed-Region. Das ist wichtig: „Multi-Peak korrekt erkannt/abwesend“ ≠ „Single-Bump-Eigenschaft bewiesen“.

### 3.6 Gegenhypothese / Grenze

Nichtlineare globale Inhibition kann in bestimmten Parameterbereichen (hohe Inhibition, enge Anregung) selbst Mehrfach-Oszillationen oder Bistabilität erzeugen. Ein negatives Ergebnis bei NF-05 ist kein Beleg für generelle Ungeeignetheit des Ringmodells, nur für die getestete Region.

## 4. NF-06 — Drift über Bound (Preregistration Draft)

### 4.1 Ziel und Hypothese

Prüfen, ob die zirkuläre Drift des Bump-Zentrums über definierte `T_out`-Fenster ohne externen Witness den deklarierten Bound überschreitet.

- **H0:** `d_circ(t0, t0 + T_out) ≤ BOUND` für alle `T_out ∈ {30, 120, 300, 3600} s`.
- **H1:** `d_circ > BOUND` für mindestens ein `T_out` (Fail-Kriterium `DRIFT_EXCEEDED`).

### 4.2 Definitionen (source-exakt aus NA-1)

```text
d_circ(a, b)    = |atan2(sin(a - b), cos(a - b))|
BOUND (Vorschlag) = 1_bin = 2π / N   (für mean)
                    3_bins             (für p99)
T_out-Grid      = {30, 120, 300, 3600} s
Runs pro Zelle  = 100 (unabhängige deterministische Seeds)
I_ext           = 0 (kein externer Witness während T_out)
Startzeitpunkt  = nach vollständiger Bump-Konvergenz (Baseline-Run)
```

**BOUND ist ein `pass_criteria_proposal_operator_adjudicable`** — dieser Wert ist ein Vorschlag, kein eingefrorener Standard. AXIOM/Operator müssen ihn vor dem Einfrieren bestätigen.

### 4.3 Trennung: Detektor-Eingabe vs. wissenschaftliche Messung

- **Detektor-Eingabe (künstlich, Testzweck):** bewusst über-Bound liefernde Simulationssignale, um das Fail-Closed-Verhalten des STALE-Flags zu prüfen (NE-8-Anteil).
- **Wissenschaftliche Messung:** tatsächlicher Modell-Drift ohne Injektion, verglichen mit dem deklarierten Bound.

Diese zwei Ebenen dürfen nicht vermischt werden. Der Detektor-Test prüft die Flag-Logik; die Messung prüft das Modell.

### 4.4 Metriken (vorregistriert)

- `circular_mean_drift(T_out)`, `circular_std_drift(T_out)`.
- `p95`, `p99` der Drift-Verteilung pro Zelle.
- `bump_amplitude_ratio(T_out)` (Persistenz-Proxy).
- Skalierungs-Check: `std`-Wachstum vs. `sqrt(t)` (diffusiv) oder subdiffusiv — **messen, nicht annehmen** (NA-1-Vorgabe).
- `STALE`-Flag-Auslösung bei Bound-Überschreitung (NE-8).

### 4.5 Fail-Closed-Verhalten

- `mean_drift > 1_bin` oder `p99_drift > 3_bins` → `DRIFT_EXCEEDED`, HOLD-Trigger.
- `STALE`-Flag nicht gesetzt, obwohl Bound nachweislich überschritten → `FILTER_STALENESS` Reject (NE-8).
- Keine Behauptung absoluter Orbitgenauigkeit ohne externe Ground-Truth; keine Behauptung, dass 120-s-Filter-Drift SGP4/TLE-Restwerte dominiert (D6 bleibt getrennt zu prüfen).

### 4.6 Grenzen

- Ohne externe Wahrheitsquelle ist nur eine Sensitivitäts- und Modellvergleichsanalyse zulässig, keine absolute Genauigkeitsaussage.
- Die Trennung von Filter-Drift, SGP4-Modellfehler und Quellen-Epochenfehler erfordert ein separates Fehlerbudget-Dokument (nicht Teil dieser Vorregistrierung).

## 5. Freeze- und Change-Control-Regeln

1. **Keine post-hoc-Schwellenänderungen:** Alle Schwellen (Prominence, Separation, BOUND, T_out-Grid) sind nach dem Einfrieren unveränderbar.
2. **Änderungen nur als neue Version:** Änderungen erhalten eine neue `R<N>`-Version und einen `supersedes`-Verweis; die alte Version bleibt auffindbar (Repository-Governance, Append-only).
3. **Unresolved-Felder-Liste:** Vor dem Einfrieren müssen folgende Felder von AXIOM/Operator final adjudiziert werden:
   - `PROMINENCE_THRESHOLD` (NF-05)
   - `MIN_SEPARATION_BINS` (NF-05)
   - `BOUND_mean`, `BOUND_p99` (NF-06)
   - Exakte Zuordnung NF-06 ↔ NE-4/NE-8/D3/D6
   - Peak-Amplitudenverhältnisse und Relaxationsfenster (NF-05)
4. **Kein Ausführungsstart ohne explizites Freeze:** Bis dahin gilt `PREREGISTRATION_DRAFT_WITH_UNRESOLVED_FIELDS`.

## 6. DESIGN_ONLY_NOT_EXECUTED — Bestätigung

```text
NF05_STATUS  = PREREGISTRATION_DRAFT_NOT_EXECUTED
NF06_STATUS  = PREREGISTRATION_DRAFT_NOT_EXECUTED
EXECUTION    = NOT_STARTED
RUNTIME_RIGHTS = NONE
PRODUCTION_WRITE = NONE
```

Kein Run, kein Log, kein Output wurde in diesem Entwurf erzeugt oder behauptet.

---

## 7. Herkunfts-Spuren (append-only)

```
Herkunft: Alexander B :: Kernsatz Symbiose :: 2026-10-10
Herkunft: GROK :: NA-1-Ring-Stabilizer-Spezifikation + Drift-Bound-Protokoll (PR #65) :: 2026-10-10
Herkunft: Perplexity Computer :: NF-05/NF-06-Vorregistrierungs-Entwurf (dieses Dokument) :: 2026-10-10
```

**NEXUS OMEGA — Quelle ist nicht Wahrheit. Prüfung bleibt das Fundament.**
