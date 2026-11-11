# NEXUS OMEGA · R25
## AXIOM-Entscheidungsvorlage (Decision Template) aus dem archivierten R25-Paket
### Neue R25-Phase — nicht identisch mit der historischen R25→R26-Quellenkapsel aus PR #66

```text
OBJECT                 = NEXUS_OMEGA_R25_AXIOM_DECISION_TEMPLATE_20261010_R1
SUPERSEDES             = NEXUS_OMEGA_R25_AXIOM_DECISION_TEMPLATE_20261010_R0 (still published; R0 remains in history)
DATE_UTC               = 2026-10-10T19:45:00+02:00
FROM                   = Perplexity Computer (Operator-Vorlagen-Lane)
TO                     = AXIOM (Adjudikation) / NEXUS_OMEGA_OPERATOR (Entscheidung)
PARENT_PACKAGE         = r25/ (6 archivierte Dateien im NEXUS-OMEGA-Projekt-Repo)
PARENT_ORDER           = NEXUS_OMEGA_AXIOM_R25_NEUTRAL_EXTERNAL_EXPERT_MAXI_RESEARCH_ORDER_20261010_R0
PARENT_RETURN          = NEXUS_OMEGA_EXTERNAL_EXPERT_R25_INDEPENDENT_MAXI_RESEARCH_RETURN_20261010_R0
CLAIM_CEILING          = C1_DESCRIPTIVE_ONLY
RUNTIME_RIGHTS         = NONE
PRODUCTION_WRITE       = NONE
GITHUB_MERGE           = NOT_AUTHORIZED_BY_THIS_TEMPLATE
R24_REOPEN             = NO
```

---

## 1. Unabhängig geprüfte Intake-Fakten (von Perplexity Computer verifiziert)

| Fakt | Status | Quelle |
|---|---|---|
| Sechs R25-Dokumente im Projekt-Repo archiviert, Hashes recomputed | **VERIFIED** | `r25/`, `pplx project files submit` |
| Drei Entscheidungskandidaten inhaltlich unverändert über alle vier Textdokumente | **VERIFIED** | `R25_TH-1-3.MD`, `R25_CA-1-4.MD` |
| Alle zehn Negative Fixtures korrekt als `DESIGN_ONLY_NOT_EXECUTED` markiert | **VERIFIED** | `R25_CA-1-4.MD` §B |
| NA-1-Protokoll (D1–D6, NE1–NE8, Primärquellen) auf PR-#65-Head abrufbar | **VERIFIED** | `research/r10r23/na1-ring-stabilizer/orders/na1-drift-bound-test-protocol.json` @ `17e0a32…` |
| PR #65 Zustand | **VERIFIED** (GitHub-API: `OPEN`, Head `17e0a3275ad9749458e251b1ec4eb07348b2c5ee`) | GitHub-API |
| Repository-Governance (`AGENTS.md`, `GOVERNANCE.md`, `REPOSITORY_STRUCTURE.md`) gelesen | **VERIFIED** | GitHub-API |

## 2. Quellen-reported findings (nicht unabhängig verifiziert)

- **PR #64, PR #60, PR #62, PR #66 gemergt:** Diese Merge-SHAs stammen aus dem MAXI-Auftrag (Upload); sie wurden in diesem Lauf **nicht** erneut per GitHub-API verifiziert. Status: `UPLOAD_REPORTED`, nicht `VERIFIED`.
- **Fünf zugrunde liegende R25-Return-Artefakte** (`R25-00`, `R25-03`, `R25-05`, `R25-07`, `R25-09`) sind nur als Hash-Angaben im 3196-Byte-GROK-Summary vorhanden. Die tatsächlichen Bytes liegen im berichteten Pfad `/home/workdir/artifacts/R25_EXTERNAL_EXPERT_RETURN_20261010/` — **nicht im Zugriffsbereich dieser Vorlage**. Status: `SOURCE_NOT_PRESENT`, keine Rekonstruktion aus dem Summary.
- **Öffentliche Homepage `https://www.nexus-mobile.de/`:** Die Aussage „textuell abrufbar, nur B1-Klasse“ stammt aus `R25_TH-1-3.MD` (einem anderen Agenten zugeschrieben), **nicht** aus einem eigenen Abruf in diesem Lauf. Status: `UPLOAD_REPORTED`; die Bezeichnung „B1“ ist zudem falsch — ein öffentlicher HTML-Textabruf ist keine echte B1-Produktionsdatei-Evidenz; korrekt wäre `PUBLIC_TEXT_READBACK` (schwachere Klasse).
- Reuters-Primärtext (Katie Paul, 26.08.2026) wurde von AXIOM laut Upload direkt gelesen; diese Vorlage hat ihn nicht erneut geöffnet.
- Die +220 %/+36 %/+40 %/+70 %-Zahlen sind journalistisch berichtete Meta-interne Angaben, keine unabhängig gemessenen NEXUS-Kausaldaten.

## 3. Material gaps und Korrekturen (blockieren neue PASS-Receipts)

1. **Unvollständige Expert-Return-Kette:** Das 3196-Byte-Summary verweist auf fünf Artefakte mit Hashes, die nie in dieser Umgebung verfügbar waren. Ein „Vollständigkeits-PASS“ für den R25-External-Expert-Return ist ohne diese Bytes nicht zulässig.
2. **Historischer Kausalitäts-Overclaim:** Die GROK-Module `NEXUS_-2-4.MD` (Zeilen 48/66) formulieren „Agenten ohne Ledger erzeugen Instabilität“ und „Planungsannahme widerlegt“ als stärker, als es E1/E2-Strenge erlaubt. Die C1-Adjudikation (PR #66, korrigierte AXIOM-Fassung) ist maßgeblich; die historischen Originale bleiben unverändert als Provenanz erhalten.
3. **B1-Evidenz-Klarstellung:** Öffentlicher HTML-Abruf ist keine echte B1-Produktionsdatei- und Hash-Evidenz im Sinne der MAXI-Order; er ist schwächere „Textabruf“-Evidenz. Die Bezeichnung „B1“ in früheren Receipts sollte künftig „PUBLIC_TEXT_READBACK“ heißen.
4. **SELBSTVALIDATION_RISK:** Perplexity Computer hat in früheren Receipts dieser Session `CHAIN_CONSISTENCY_C1 = PASS` vergeben, obwohl die historischen GROK-Module den Kausalitäts-Overclaim enthalten (Punkt 2). Das ist ein Eigenvalidierungsfehler; die korrigierte Einstufung lautet `CHAIN_CONSISTENCY_C1 = PASS_WITH_OVERCLAIM_CAVEAT`.

## 4. Entscheidungskandidaten (an AXIOM)

### K1 — PR65 bleibt OPEN_HOLD_SCOPED; neue Forschungsgates vor Merge

- **Begründung:** NF-05 (Multi-Peak-Injektion) und NF-06 (Drift über Bound) sind die direkten wissenschaftlichen Gründe; kein Fehlerbudget-Protokoll liegt vor.
- **Vorregistrierung:** Siehe `NEXUS_OMEGA_R25_NF05_NF06_PREREGISTRATION_DRAFT_20261010_R0.md` + `.json` (dieses Paket). `DESIGN_ONLY`, keine Ausführung.
- **Entscheidung AXIOM:** (a) Vorregistrierung als Draft akzeptieren, (b) fehlende Felder benannt lassen, (c) Hold aufrecht erhalten.

### K2 — Project OT: E1 deskriptiv, E2 prospektiv, keine Kausal-Promotion

- **Begründung:** Reuters-Assoziation + nie ausgeführte 60-%-Ablation; E1/E2 logisch unabhängig; Confounder offen.
- **Korrektur:** Die historischen GROK-Module (PR #66-Kapsel) behalten ihren Overclaim; die kanonische Aussage bleibt die PR-#66-AXIOM-Adjudikation. **Wichtig:** Ein Wiederholen des Caveats kann die Ledger-Kausalität nicht etablieren — die gelieferte Evidenz reicht strukturell nicht für einen Kausalitätsbeweis. Neue Receipts dürfen `CAUSAL_PROOF` überhaupt nicht als PASS vergeben; die korrekte Bezeichnung bleibt `NOT_ESTABLISHED` (keine Formulierung, die durch Caveat-Wiederholung „heilbar“ wäre).
- **Entscheidung AXIOM:** Korrektur-Addendum verfassen oder historische Formulierung mit Caveat-Verweis belassen.

### K3 — Cursor-R21R1-Lane ungestört lassen; HTML ≠ Live-Verifikation

- **Begründung:** Kein B2-Hostinger-Write-Receipt, kein B3-Browser-Funktionsnachweis vorhanden; öffentliche Route ersetzt Terminal-Proof nicht.
- **Entscheidung AXIOM:** Zustand bestätigen; keine neue Lane, kein paralleler Worker.

## 5. Empfehlung und Gegenposition

**Empfehlung:** Alle drei Kandidaten als verbindliche nächste Entscheidungsschritte bestätigen; die Vorregistrierung NF-05/NF-06 als Draft akzeptieren; PR65-Hold beibehalten; keine Promotion, kein Runtime-Recht.

**Gegenposition:** Falls der Operator einen beschleunigten PR65-Merge will, wäre der Weg: **explizite Ausführung** der vorregistrierten NF-05/NF-06-Experimente als separates, reproduzierbares Forschungsexperiment (kein Production-Deploy) plus ein explizites Fehlerbudget-Dokument. Das ist eine **ausführungsbezogene** Entscheidung, nicht mehr „design-only“ — sobald Runs ausgeführt werden, endet der Design-only-Status. Das bleibt eine Operator-Entscheidung, keine automatische Pflicht.

## 6. Grenzen und STOP-Gates

- Kein Merge, kein Deploy, kein Hostinger-Write, kein neuer Cursor-Worker, keine Elite-Node-Geburt, R24 bleibt administrativ geschlossen.
- Diese Vorlage trifft keine Entscheidung; sie bereitet die AXIOM-Adjudikation vor.
- Fehlende R25-Return-Bytes bleiben `SOURCE_NOT_PRESENT`; keine Rekonstruktion.

---

## 7. Herkunfts-Spuren (append-only)

```
Herkunft: Alexander B :: Kernsatz Symbiose :: 2026-10-10
Herkunft: AXIOM :: R25-MAXI-Forschungsauftrag :: 2026-10-10
Herkunft: GROK :: R25 External-Expert-Return (Summary, 5 Artefakte SOURCE_NOT_PRESENT) :: 2026-10-10
Herkunft: Perplexity Computer :: R25-Archiv + Entscheidungs-Vorlage (dieses Dokument) :: 2026-10-10
```

**NEXUS OMEGA — Quelle ist nicht Wahrheit. Prüfung bleibt das Fundament.**
