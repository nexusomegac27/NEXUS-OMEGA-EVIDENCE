# NEXUS OMEGA · R25
## NF-05 und NF-06 — Vorregistrierungs-Entwurf R2 (Preregistration Draft)
### Design-only · nicht ausgeführt · keine Runtime-Freigabe

```text
OBJECT                     = NEXUS_OMEGA_R25_NF05_NF06_PREREGISTRATION_DRAFT_20261010_R2
DATE_UTC                   = 2026-10-10T20:30:00+02:00
FROM                       = Perplexity Computer (Design-only-Lane)
TO                         = AXIOM / NEXUS_OMEGA_OPERATOR
SUPERSEDES                 = R0, R1 (beide bleiben in der Historie)
PARENT_SPEC                = research/r10r23/na1-ring-stabilizer/orders/NA1_RING_STABILIZER_SPEC_AND_DRIFT_BOUND_PROTOCOL_20261010_R0.md @ 17e0a3275ad9749458e251b1ec4eb07348b2c5ee (PR #65, OPEN_HOLD_SCOPED)
PARENT_SPEC_SHA256         = 6b2bda7e700bf219fc9e7609da7d60b6c4079b0766caf51bb5d82629f31c4c11
STATUS                     = PREREGISTRATION_DRAFT_WITH_UNRESOLVED_FIELDS
DESIGN_ONLY_NOT_EXECUTED  = TRUE
EXECUTION_AUTHORIZATION    = NONE
RUNTIME_RIGHTS             = NONE
PRODUCTION_WRITE           = NONE
GITHUB_MERGE               = NOT_AUTHORIZED
```

---

## 0. Wichtiger Hinweis

Dies ist ein **Vorregistrierungs-Entwurf** (`PREREGISTRATION_DRAFT_WITH_UNRESOLVED_FIELDS`), keine abgeschlossene, eingefrorene Vorregistrierung. Die Ausführung bleibt untersagt, bis AXIOM die offenen Felder benennt und die Vorregistrierung explizit einfriert. **R2 ersetzt R0 und R1**, die in der Historie verbleiben.

## 1. Bezug zum NA-1-Spezifikations-Markdown (R1-Reparatur-Emission, abgerufen 2026-10-10)

Die vollständige Spezifikation wurde jetzt abgerufen (11 483 Bytes, SHA-256 `6b2bda7e…`). Die fehlenden Modellparameter sind **source-exakt dokumentiert** (nicht mehr unresolved):

### 1.1 Mathematische Minimalform (NA-1 §3, source-exakt)

```text
State: N ∈ {32, 64} Units auf dem Ring, θ_i = 2πi/N; Aktivierungen r_i ≥ 0

Update-Regel (pro Zeitschritt):
  h_i(t+1) = Σ_j W_ij · r_j(t) − g_inhib · max_j r_j(t) + I_ext(θ_i, t)
  r_i(t+1) = max(0, h_i(t+1))    # bzw. tanh-Cap; beide dokumentieren
  W_ij     = w0 + w_exc · cos((θ_i − θ_j)/2)^p

Globale Inhibition (Δ7-Analog) über den Max-Term; exakte Funktionsform ist frei,
muss aber im Test-Report fixiert sein.

Readout (PVA): θ̂(t) = atan2(Σ_i r_i · sin θ_i, Σ_i r_i · cos θ_i)

Ingress-Semantik:
  I_ext = 0 → Persistenz des Bumps (Form bleibt)
  I_ext = external_witness → Verschiebung, keine Neuerzeugung

Provenance-Doppelfeld (Pflicht): predicted_state + last_external_witness + filter
```

**Verbleibende unresolved Modellparameter** (Werte nicht in NA-1 spezifiziert, müssen im Test-Report fixiert werden): `w0`, `w_exc`, `g_inhib`, `p`, `timestep`, Aktivierungsform (max(0,·) vs. tanh-Cap), Rauschprozess-Definition, Konvergenz-Kriterium, Seed-Generierungsschema.

### 1.2 NF-05 ≙ NE-1 (MULTIPEAK_INJECTION)

NA-1 §5 definiert: „zwei Bumps injizieren → mehr als ein Peak nach Relaxationszeit = Fail." Die **Relaxationszeit ist nicht numerisch definiert** — sie muss vor dem Run festgelegt werden (unresolved).

### 1.3 NF-06 ≙ NE-4 + NE-8 + D-3 + D-6

- **NE-4** (`NO_INPUT_120S_DRIFT+HOLD_LAST_BASELINE`): „Replay mit realen OMM-Lücken ≥ 120 s → gemessene Drift überschreitet dokumentierten Bound = Fail."
- **NE-8** (`FILTER_STALENESS`): „Staleness-Flag bei Bound-Überschreitung → kein STALE-Flag trotz nachgewiesenem Bound-Bruch = Fail."
- **D-3** (nur 120 s): Mittelwert ≤ 1 Bin (2π/N), p99 ≤ 3 Bins.
- **D-6** (separat): SGP4-Eigenpropagationsfehler für 120 s dokumentiert und als klein gegenüber Filter-Bound ausgewiesen (filter-intern vs. Modellfehler getrennt).

## 2. NF-05 — Multi-Peak-Injektion (Preregistration Draft R2)

### 2.1 Hypothese und Fail-Kriterium (source-exakt)

- **H0:** Kollaps auf genau einen Peak innerhalb der Relaxationszeit.
- **H1 (Fail):** Mehr als ein Peak nach Relaxationszeit (NE-1, source-exakt).

### 2.2 Injektionsbedingungen (unresolved)

| Parameter | Status |
|---|---|
| Anzahl injizierter Peaks | 2 (source-exakt) |
| Relaxationszeit | **UNRESOLVED** — NA-1 nennt keine Zahl; muss festgelegt werden |
| Injektionsart (Addition vs. Ersetzung) | **UNRESOLVED** |
| Platzierung (symmetrisch um θ_inject) | **UNRESOLVED** (Vorschlag) |
| Peak-Amplitude / Peak-Breite | **UNRESOLVED** |
| Seeds | ≥100 deterministisch (NA-1-Grid) |

### 2.3 Peak-Zählregel (neu, muss vor Run eingefroren werden)

```text
Metric: Aktivitätsarray r_i(t)
Local maxima: r_i > r_{i-1} AND r_i > r_{i+1} (zirkulär, r_N = r_0)
Peak zählt, wenn:
  - Prominenz ≥ PROMINENCE_THRESHOLD (relativ zum lokalen Tal, nicht global max)
  - zirkulärer Abstand zum nächsten Peak ≥ MIN_SEPARATION_BINS
Plateau/Tie-Behandlung: UNRESOLVED
Null-Aktivitäts-Guard: UNRESOLVED
```

### 2.4 Fail-Closed-Verhalten

- Mehr als ein Peak nach Relaxationszeit → `MULTI_PEAK` Reject, HOLD-Trigger für PR65.
- Kollaps beobachtet ≠ generelle Ein-Peak-Eigenschaft bewiesen; Misserfolg ≠ generelle Ungeeignetheit bewiesen (nur getestete Region).

## 3. NF-06 — Drift-Bound-Prüfung (Preregistration Draft R2)

### 3.1 Definitionen (source-exakt)

```text
D-0: Drift = circ_dist(θ̂(t0+dt), θ̂(t0)) mit I_ext = 0 nach vollständiger Bump-Konvergenz
T_out-Grid: {30, 120, 300, 3600} s
Seeds: ≥100 deterministisch pro Zelle
```

### 3.2 Bound-Regel (wichtig — D-3 gilt nur für 120 s)

- **Für T_out = 120 s:** D-3 ist source-exakt (Mittelwert ≤ 1 Bin, p99 ≤ 3 Bins). Der Wert ist ein Kalibriervorschlag, kein biologisches Faktum.
- **Für T_out ∈ {30, 300, 3600} s:** **KEIN source-exakter Bound** — `NEW_PROPOSAL`, separat zu adjudizieren. **Keine bedingungslose aggregierte Ablehnungsregel** über alle T_out darf formuliert werden; die D-3-Formel gilt nur für 120 s.

### 3.3 D-6 ist separat

D-6 (SGP4-Eigenpropagationsfehler-Dokumentation, filter-intern vs. Modellfehler getrennt) ist eine **separate Pflicht**, kein Bestandteil der NF-06-Ausführung.

### 3.4 Detektor vs. Messung (getrennt halten)

- **Detektor-Test (NE-8):** bewusst über-Bound lieferndes Signal, um die STALE-Flag-Logik zu prüfen.
- **Wissenschaftliche Messung (D-0/D-3):** tatsächlicher Modell-Drift ohne Injektion.
- `BOUND_traj` (per-Trajektorie-Schwelle) ist unresolved; Equal-Bound-Verhalten unresolved.

### 3.5 Fail-Closed-Verhalten

- Gemessene Drift > dokumentierter Bound → `DRIFT_EXCEEDED` (NE-4).
- Kein STALE-Flag trotz nachweislichem Bound-Bruch → `FILTER_STALENESS` (NE-8).
- Keine absolute Orbitgenauigkeit ohne externe Ground-Truth; keine 120-s-Dominanz-Behauptung ohne D-6-Dokumentation.

## 4. Unresolved-Felder (vollständige Liste vor dem Freeze)

1. **Modellparameter:** `w0`, `w_exc`, `g_inhib`, `p`, `timestep`, Aktivierungsform, Rauschprozess, Konvergenz-Kriterium, Seed-Generierungsschema.
2. **NF-05:** Relaxationszeit (numerisch), Injektionsart, Platzierung, Amplitude/Breite, Peak-Zählregel (Prominenz, Separation, Plateau, Null-Guard).
3. **NF-06:** `BOUND_traj`, Equal-Bound-Verhalten, statistische Schätzer und Quantil-Regel, `NEW_PROPOSAL` für nicht-120-s-Bounds.

## 5. Freeze- und Change-Control-Regeln

1. **Keine post-hoc-Schwellenänderungen** nach dem Einfrieren.
2. **Änderungen nur als neue Version** (`R<N>`, `supersedes`-Verweis).
3. **Kein Ausführungsstart ohne explizites AXIOM-Freeze.**

## 6. DESIGN_ONLY_NOT_EXECUTED — Bestätigung

```text
NF05_STATUS  = PREREGISTRATION_DRAFT_NOT_EXECUTED
NF06_STATUS  = PREREGISTRATION_DRAFT_NOT_EXECUTED
EXECUTION    = NOT_STARTED
```

Kein Run, kein Log, kein Output wurde erzeugt oder behauptet.

---

## 7. Herkunfts-Spuren (append-only)

```
Herkunft: Alexander B :: Kernsatz Symbiose :: 2026-10-10
Herkunft: MISTRAL/VIBE :: NA-1-Ring-Stabilizer-Spezifikation R1 (PR #65, abgerufen) :: 2026-10-10
Herkunft: GROK :: R25 External-Expert-Return + Kausalitätsanalyse :: 2026-10-10
Herkunft: Perplexity Computer :: NF-05/NF-06-Vorregistrierungs-Entwurf R2 :: 2026-10-10
```

**NEXUS OMEGA — Quelle ist nicht Wahrheit. Prüfung bleibt das Fundament.**
