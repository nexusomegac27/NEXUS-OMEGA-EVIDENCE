# 01 — Input Integrity (unabhängige Eingangsprüfung)

Alle Prüfungen in dieser Sitzung, lokal gerechnet (`sha256sum` / `zipfile.testzip` / Manifest-Vergleich).

## A. Orders (TXT)

| Artefakt | Bytes | SHA-256 | Prüfung |
|---|---:|---|---|
| R45-9-Order (AXIOMR~1.TXT) | 24.491 | `bef961ac1c6c0e24c4f3b29689602847ceeafc9254f60cee9f78c25f69e8f3d6` | MATCH gegen input_audit.json und Binding-Node des AUTO_CLAW-Stacks |
| R45-7-Order (NEXUSO~1.TXT) | 19.045 | `4856e44fd3302f0d5da396a351b44deca23872ce4f891c5390e293c2be2c9e27` | MATCH gegen GLM 01_HARD_STATUS.txt („Anhang 19.045 B“) |

## B. Empfangene Archive (CRC via `zipfile.testzip`)

| Archiv | Bytes | SHA-256 | CRC | Inhalt |
|---|---:|---|---|---|
| AUTOCL~1.ZIP (R45-9-Abschlussstack, AUTO_CLAW-Vorlage) | 111.172 | `debfb872bccaacaf8732e09be97bedb46d833af504ca932f231d55fc69c8fc7b` | PASS | 27 Dateien |
| AUTO_C~1.ZIP (R45-6-Konsistenzarchiv) | 75.697 | `c68a0725a62a8626b6dc99f5de0e60dba82e23c24facb2c709085b633b336c9b` | PASS | passt zur R45-7-Order §1 („75.697 B, CRC PASS“) |
| 202611~1.ZIP (GLM R45-7-Return R1) | 255.587 | `82094ad9557215a12e16e2068c5372ae8e9b021e9c102041de3741e0d7f7588c` | PASS | vollständiger GLM-Return inkl. Transfer-ZIP |

**Eingebettete Verifikationskette (202611~1.ZIP):** `transfer/R45_7_EXPERT_ORDER_R1.zip` =
35.883 B, `0ff1cee1d2b33447265161316671250316515e1cfd4d6db2addee06fa9de7985`, Sidecar MATCH — identisch
zur kanonischen R45-7-Order-Veröffentlichung.

## C. **Materieller Eingangsbefund — AUTO_CLAW-Stack unvollständig**

Der MANIFEST.json des empfangenen R45-9-Abschlussstacks deklariert **33** Dateien; das Archiv enthält **27**.

- 26/27 vorhandene Mitglieder: SHA-256 **MATCH** gegen MANIFEST.
- **7 deklarierte Mitglieder fehlen im empfangenen ZIP:** `r45_9_sqlite.py`, `results_independent.json`,
  `results_projection.json`, `results_sqlite.json`, `review.md`, `SHA256SUMS.txt`, `SOURCE_REGISTRY_R45_9.json`.
- Konsequenz: die im AUTO_CLAW-Stack berichteten Kernzahlen (SQLite 100/100, 37/37; Projektion 28/28) sind
  **aus den empfangenen Artefakten allein nicht reproduzierbar** — die Quellen fehlen. Dieser Stack allein hätte
  die Non-Vacuity-Anforderung verletzt. (Die Fehlenden sind kein Beweis gegen die Original-Laufumgebung; sie sind
  nur hier nicht nachweisbar. Diese Return umgeht das Problem, indem alle Kernzahlen **unabhängig neu ausgeführt** werden.)

## D. GitHub-Readback (via Plugin, authentifiziert als `nexusomegac27`)

| Objekt | Befund |
|---|---|
| Issue #463 | OPEN, Titel/Inhalt identisch zu AUTO_CLAW-Readback |
| Draft-PR #464 | OPEN · DRAFT · **NOT MERGED**, head `167196287c864696baebddca7832221d6854e1ce`, base `332de9892c9b57d7bcdf19721c6bbb8ee0e42159`, 14 Dateien, 607 additions |
| Kanonischer ZIP `R45_9_FINAL_EXPERT_INTEGRATION_FOUNDATION_R0.zip` | **byte-exakt von raw.githubusercontent.com geladen: 37.284 B, `d15876f268ad378f220bfb83b9f1ba2ffcc041aa40949b8665d37b8d52f57c55`** — MATCH Order §11, Sidecar, Issue #463, PR #464 |

Damit ist die RV2-Lücke des AUTO_CLAW-Audits („ZIP inventarisiert, nicht bytegenau heruntergeladen“) geschlossen:
die Kanon-Referenz ist in dieser Return **bytegenau verifiziert**, nicht nur inventarisiert.

## E. AXIOM-Sandbox-Quelle

`07_SQLITE_SANDBOX.py` (GitHub, byte-exakt geladen) und gepinntes Ergebnis `08_SQLITE_RESULT.json`:
Replikationslauf in dieser Umgebung → 100/100, 0 Budgetüberschreitungen, 13/13 Kontrollen; einziger
JSON-Diff zur gepinnten Datei: `sqlite_version` 3.46.1 → 3.53.1 (Umgebung, semantisch erwartet).
