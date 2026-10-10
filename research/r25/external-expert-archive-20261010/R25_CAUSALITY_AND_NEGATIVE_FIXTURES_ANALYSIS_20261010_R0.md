# R25 · Kausalitätsfehler-Prüfung der drei Kandidaten + Negative-Fixtures-Analyse

```text
OBJECT          = R25_CAUSALITY_AND_NEGATIVE_FIXTURES_ANALYSIS_20261010_R0
FROM            = GROK (External Expert)
TO              = AXIOM / NEXUS_OMEGA_OPERATOR
CLAIM_CEILING   = C1_DESCRIPTIVE_ONLY
DATE_UTC        = 2026-10-10
```

---

## A. Kausalitätsfehler-Prüfung der drei Entscheidungs-Kandidaten

### Kandidat 1 — PR65 OPEN_HOLD_SCOPED bis Negative Fixtures + Fehlerbudget

| Mögliche Kausalitätsfalle | Befund | Risiko |
|---------------------------|--------|--------|
| „HOLD besteht, *weil* der Ring ungeeignet ist“ | **FEHLER** — HOLD besteht, weil *Nachweise fehlen*, nicht weil Ungeeignetheit bewiesen ist | Mittel |
| „Fehlerbudget *beweist* Filter-Dominanz“ | **FEHLER** — Budget zerlegt; Dominanz ist ungetestet | Hoch falls behauptet |
| „Negative Fixtures *werden* den HOLD aufheben“ | **FEHLER** — Fixtures können HOLD verstärken oder aufheben; Ausgang offen | Mittel |
| „Design-only Modell *impliziert* Runtime-Eignung“ | **FEHLER** — explizit ausgeschlossen | Hoch |

**Kausalitäts-Status Kandidat 1:** Kein interner Kausalitätsfehler in der empfohlenen Haltung. Die Haltung ist epistemisch korrekt (Nichtwissen → HOLD). Gefahr entsteht nur bei stillschweigender Promotion von „fehlender Nachweis“ zu „Nachweis der Ungeeignetheit“.

### Kandidat 2 — Project OT als E1-deskriptiv + E2-prospektiv

| Mögliche Kausalitätsfalle | Befund | Risiko |
|---------------------------|--------|--------|
| „+220 % Code → fehlendes Ledger war Ursache“ | **FEHLER** — reine Assoziation; Confounder offen | Sehr hoch |
| „60 %-Szenario *hätte* Kollaps erzeugt“ | **FEHLER** — nie ausgeführt; Gegenfaktisch | Hoch |
| „Biologische Dual-Origin *beweist* Organisations-Isomorphie“ | **FEHLER** — Heuristik, keine formale Abbildung | Hoch |
| „E1 *unterstützt* E2“ | **FEHLER** — E1 und E2 sind logisch unabhängig | Mittel |

**Kausalitäts-Status Kandidat 2:** Die empfohlene Disziplin (E1 deskriptiv, E2 prospektiv) ist kausal sauber. Jede stärkere Formulierung erzeugt sofort einen Kausalitätsfehler.

### Kandidat 3 — Cursor-Lane ungestört; HTML ≠ Live-Funktion

| Mögliche Kausalitätsfalle | Befund | Risiko |
|---------------------------|--------|--------|
| „Seite erreichbar → Funktion live“ | **FEHLER** — B1 ≠ B2 ≠ B3 | Sehr hoch |
| „CI grün → Produktionszustand verifiziert“ | **FEHLER** — CI prüft Code, nicht Hostinger/Browser | Hoch |
| „Öffentliche Route *ersetzt* Terminal-Proof“ | **FEHLER** — explizit getrennt zu halten | Hoch |

**Kausalitäts-Status Kandidat 3:** Die empfohlene Trennung ist kausal korrekt. Der häufigste Fehler in der Praxis ist die stillschweigende Gleichsetzung von Abrufbarkeit mit Funktionsnachweis.

### Gesamt-Kausalitätsurteil

```text
KANDIDAT_1 = KAUSAL_SAUBER (bei korrekter Interpretation des HOLD)
KANDIDAT_2 = KAUSAL_SAUBER (bei strikter E1/E2-Trennung)
KANDIDAT_3 = KAUSAL_SAUBER (bei B1/B2/B3-Disziplin)
AGGREGAT   = KEINE_INTERNEN_KAUSALITAETSFEHLER_IN_DEN_DREI_EMPFEHLUNGEN
```

Die Empfehlungen selbst erzeugen keine Kausalitätsfehler. Fehler entstehen erst bei ihrer *Überdehnung*.

---

## B. Analyse der Negative Fixtures (Design-Katalog)

Aus R25-07 und R25-03 abgeleiteter, strukturierter Katalog. Alle Fixtures sind **DESIGN_ONLY_NOT_EXECUTED**.

| ID | Fixture | Erwartetes Fail-Closed | Beobachtbare Metrik | Reject-Klasse | Bezug zu Kandidat |
|----|---------|------------------------|---------------------|---------------|-------------------|
| NF-01 | Missing / stale external witness | `predicted_state` läuft offen; kein neues `last_external_witness` | Drift vs. letzte gültige Epoche | `WITNESS_ABSENT` | K1 (Fehlerbudget) |
| NF-02 | Wrong NORAD / wrong epoch | Reject oder isolierte Markierung; kein stilles Überschreiben | Hash/ID mismatch flag | `IDENTITY_MISMATCH` | K1 |
| NF-03 | Source without licence / provenance | Reject; kein `LIVE_MEASURED_EXTERNAL` Label | Provenance field empty/invalid | `PROVENANCE_MISSING` | K2 (Ledger-Hypothese) |
| NF-04 | Non-monotonic / jumped clock | Time-consistency reject | Δt < 0 oder Sprung > Bound | `CLOCK_INCONSISTENT` | K1 |
| NF-05 | Multi-peak activity injection | Collapse to single peak *oder* explicit multi-peak flag | Number of local maxima in r | `MULTI_PEAK` | K1 (PR65 HOLD) |
| NF-06 | Drift beyond declared bound | Fail-closed / HOLD trigger | d_circ > bound | `DRIFT_EXCEEDED` | K1 |
| NF-07 | Simulation signal labelled LIVE_MEASURED_EXTERNAL | Reject / relabel to PREDICTED | Label audit | `LABEL_FRAUD` | K1 + K3 |
| NF-08 | Browser tiles unreachable / attribution missing | No WWW_LIVE_VERIFIED_C1 | HTTP/asset/console evidence | `B3_INCOMPLETE` | K3 |
| NF-09 | Ground truth absent while absolute accuracy claimed | Claim demoted to sensitivity-only | Presence of external truth source | `NO_GROUND_TRUTH` | K1 |
| NF-10 | Unit ablation 40–60 % without retuning | Persistence/correction metrics logged (outcome open) | Bump amplitude, recovery, d_circ | `ABLATION_RESULT` | K1 + K2 (E2) |

### Kritische Beobachtungen zu den Fixtures

1. **NF-05 und NF-06** sind die direkten wissenschaftlichen Gründe für den PR65-HOLD. Solange sie nicht gelaufen sind, bleibt die Einzigkeit und die Drift-Bound-Behauptung ungesichert.
2. **NF-01 / NF-07 / NF-09** schützen die dual-field-Disziplin (`predicted_state` ≠ `last_external_witness`).
3. **NF-08** schützt Kandidat 3: öffentliche Erreichbarkeit darf nie stillschweigend zu B3 hochgestuft werden.
4. **NF-10** ist der einzige direkte empirische Test von E2; er ist modellbezogen und ersetzt keinen Meta-Feldversuch.
5. Kein Fixture darf post-hoc Schwellen ändern. Vorregistrierung ist Pflicht.

### Kausalitäts-Risiko der Fixtures selbst

- Fixture-Erfolg darf nicht als Beweis gelesen werden, dass der Ring „produktionsreif“ ist.
- Fixture-Misserfolg darf nicht als Beweis gelesen werden, dass „Ring-Attraktoren prinzipiell ungeeignet“ sind — nur dass die getestete Parameter-/Implementierungsregion scheitert.
- NF-10 (Ablation) testet ein *Modell*; er testet nicht die Organisations-Hypothese E2 bei Meta.

---

## C. Synthese

Die drei Entscheidungs-Kandidaten sind kausal sauber formuliert.  
Die Negative Fixtures bilden das minimale adversarielle Netz, das verhindert, dass die Kandidaten durch Überdehnung selbst kausal fehlerhaft werden.

Nächster wissenschaftlicher Schritt (Design-only): vorregistrierte Ausführung von NF-05, NF-06 und dem Fehlerbudget-Protokoll — ohne Runtime- oder Produktionsanspruch.

---

*GROK External Expert · C1 · 2026-10-10*
