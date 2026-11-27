# R46-4 · RETURN-STACK (GLM-Lane) — OPPO-Referenzmetrologie, Kalibrierung und Messunsicherheit für BodyTwin [C1]

Objekt: `NEXUS_OMEGA_VIBE_R46_4_REFERENCE_METROLOGY_EXPERT_RETURN_GLM_R1_20261127_R0`
Datum: 2026-11-27 · Autor: unabhängige Experten-Lane (GLM) nach AXIOM-Kanon
Antwort auf: `R46_4_EXTERNAL_OPPO_REFERENCE_METROLOGY_ORDER_R0` (Issue #476 / Draft-PR #477, HEAD f39aeeb2)

## Lesereihenfolge

1. `02_INPUT/R46_4_ORDER.txt` — unveränderte Kopie des AXIOM-Auftrags (Eingangsintegrität 12/12 gegen `99_SHA256SUMS.txt` des Order-ZIP geprüft).
2. `02_PREREG.md` — VOR Auswertung fixiertes Prüfprotokoll (Witness-Register W01–W35), SHA-256 `4f30fa5b8658db6b068a25033719de4ee26b57b6e43e8c107e60854863f0e55f`.
3. `03_WITNESSES_RUNNER.js` — deterministischer, reproduzierbarer Prüf-Runner (keine Zufallsquellen außer deklariertem LCG, Seed 20261127).
4. `04_RESULTS.json` — maschinenlesbare Runner-Ausgabe: **15/15 Checks PASS, `ALL_PREREG_CHECKS_PASS`**, 4 dokumentierte Prereg-Divergenzen (D01–D04, alle methodischer Natur, kein Ziel geändert).
5. `01_RETURN_REPORT.md` — Vollbericht in deutscher Sprache (Abschnitte A–E).
6. `05_EVIDENCE_FRAME.json` / `06_INTEGRATION_MATRIX.json` / `07_SOURCES.md` / `08_GATES_AND_HOLDS.json` / `09_RESOURCE_RECEIPT.json` / `10_LIMITATIONS.md`.
7. `99_SHA256SUMS.txt` — Prüfsummen aller Stack-Mitglieder (nicht über sich selbst).

## Kernresultat in einem Satz

Die R21-Parent-Aggregate (n=7014, M=9.832738001091458 m/s², S=0.009171945499113295 m/s², g0=9.80665) sind intern konsistent reproduzierbar; die AXIOM-Referenzwerte (μ, σ, t, Ratios, Schranken, ULP-Abstände, Ränge, Design-Konditionen, Dominanz-Simulation) wurden unabhängig nachvollzogen — die Signatur der Parent-Aggregate ist bis auf die dokumentierten Prereg-Divergenzen bestätigt, und die Behauptung „σ aus Betragsmomenten = Kalibrierung“ bleibt abgelehnt (W05, W19).

## Status

- Acceptance: `ALL_PREREG_CHECKS_PASS`
- Holds: unverändert übernommen (physische Kette 0/14, ALT_D ACTIVE, Ceiling C1_DESCRIPTIVE_ONLY, kein Cursor-Handoff bis R46-9-Closeout)
- Next: `R46_4_RETURN_FOR_AXIOM_ADJUDICATION`
