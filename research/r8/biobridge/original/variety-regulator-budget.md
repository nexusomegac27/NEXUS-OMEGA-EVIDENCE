# NEXUS//OMEGA — Variety Regulator Budget (Ashby's Law)

**OBJECT** = `21_VARIETY_REGULATOR_BUDGET.md`
**CLAIM_CEILING** = C1_DESCRIPTIVE_ONLY
**TRUTH_AUTHORITY** = NONE
**RUNTIME** = FROZEN_OFFLINE_TESTING
**PARENT** = 20_COMPATIBILITY_MATRIX.json

---
## 1. Ashby's Law Formal Application

> Only variety can destroy variety. Only variety in the regulator R can force down variety in the system S.

### Mapping

- **System Variety V(S)** = |D| = Produkt aller erlaubten Zustände in D1..D4 + concurrent work-lane Zustände X/Y
  - D1: 3 serialisations
  - D2: ≤3 concurrent semver versions
  - D3: 2 routing choices
  - D4: 3 compression profiles
  - X/Y lanes: 2^N Kombinationen unabhängiger Mutationen
  - → V(S) ≈ 3*3*2*3 * lane_combinations ≈ 54 * lane_factor

- **Regulator Variety V(R)** = Unterscheidungen die K + INCOMPATIBILITY_LEDGER + Microtrigger + friction delta machen können
  - K1: 5 microtrigger Symbole
  - K2: SHA-256 Match/Mismatch (2 Zustände, aber 2^256 Adressraum)
  - K3: Authority check PASS/FAIL (2)
  - K4: negative-evidence preserved / not (2, aber second ist FAIL)
  - K5: compatible / HOLD / FAIL (3)
  - Ledger: unbounded, aber strukturiert
  - → V(R) >> V(S) wenn korrekt implementiert

### 2. Regulator Budget Rules (C1)

1. **Coverage Rule**: Für jedes erlaubte Element d ∈ D muss mindestens ein beobachtbares r ∈ R existieren: ledger entry, friction delta, oder HOLD/? . Wenn zwei d1≠d2 gleiches r erzeugen → Kollaps oder Verbot (Regulator-Blindheit).

2. **Resource Pressure Rule (F12)**: Unter resource pressure sinkt V(R) (Ledger kann nicht mehr schreiben, Cache evicted). Pflicht-Checkpoint `;` stellt V(R) wieder her bevor Compaction V(S) reduziert. Wenn V(R) < V(S) nach Compaction → mandatory HOLD.

3. **Silent Corruption Rule**: Silent corruption = Zustand wo V(R) < V(S) und System absorbiert Differenz ohne HOLD/FAIL. Verboten. Muss zu ? oder ! eskalieren.

4. **Concurrency Cap**: D2 semver ≤3 concurrent versions. Begründung Ashby: Mehr als 3 erhöht V(S) über praktisch haltbares V(R) für offline testing. Erhöhung erfordert formale Erweiterung von V(R) (mehr Ledger-Kapazität, explizite friction logs).

### 3. Friction Logging & Measurement

```
friction(X,Y) = |bytes_X - bytes_Y| + |claims_X Δ claims_Y| + incompatibility_ledger_entries(X,Y)
B_incompatibility = friction + control_bytes_for_handling
```

Jeder HOLD (?) muss friction loggen. Jeder FAIL (!) muss ledger entry loggen.

### 4. Efficiency Measurement Protocol (closes G2)

```
C_t = B_control + B_references + B_dereferenced + B_incompatibility
```

- **B_control**: microtrigger bytes (1 byte each) + session headers (≤16 bytes). Gemessen pre/post transduction pro Fixture.
- **B_references**: 32 bytes per SHA-256 hash. Nur Referenzen im Control-Plane.
- **B_dereferenced**: Bytes tatsächlich aus CAS geholt beim first miss. Cache hit = 0. Gemessen im CAS Layer.
- **B_incompatibility**: Bytes + Claims für HOLD/FAIL Handling + ledger entries. Kontinuierlich gemessen, nicht nur bei F21.

**Baseline**: pure state-push = voller Zustand jedes Mal (inkl. provenance).

**Acceptance Bounds (C1 Vorschlag)**:
- Aggregate ΣC_t über Fixture-Suite muss ≥40% Reduktion vs baseline zeigen
- Dabei 100% provenance bits erhalten
- 100% negative-evidence events erhalten
- Full final-state recoverability (hash-verified)
- Statistik: mean + worst-case reporting, kein smoothing, keine Ausreißer-Entfernung ohne HOLD

**Status 49.56%**: PROJECT_CLAIM. Ohne Original-Baseline und Original-CAS nicht reproduzierbar. Plausibilität theoretisch gegeben, empirisch offen. Diskrepanzpflicht eingehalten.

### 5. Dobzhansky-Muller Budget Interaktion

X und Y dürfen unabhängig innerhalb D evolvieren solange kompatibel mit K. Wenn X∩Y ∉ K-kompatibel → Hybrid-Inkompatibilität. Regulator muss diese mit V(R) erkennen. Wenn nicht erkennbar (weil D Mutation K umgeht) → K verletzt → FAIL. Das Budget muss daher genug V(R) für alle erlaubten X/Y Paare vorhalten.

Regel: `No D mutation may reduce V(R) below threshold required to detect incompatibility with any other allowed D mutation.`

### 6. Terminal Seal

```
OBJECT = 21_VARIETY_REGULATOR_BUDGET.md
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
K = INVARIANT
D = BOUNDED
V(R) >= V(S) REQUIRED
RUNTIME = FROZEN
```
