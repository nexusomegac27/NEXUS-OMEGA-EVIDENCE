# NEXUS OMEGA R17 · Reproduktion der isolierten Forschungsprüfung (18.10.2026)

**Zweck:** eine synthetische Integritätsprüfung, kein autonomer Agent oder ausführungsberechtigter R18-Loop. Kein Quantum-Circuit, keine echten externen Identitäten, keine Operatorratifizierung.

## Teste unter CPython 3.13+ (stdlib-only)

```bash
python -m unittest -v test_r17_integrity_guard_frozen.py
```

Erwartetes Ergebnis: `Ran 20 tests`, `OK`, Exit 0. Der Test wurde als eigener Dateistand vor dem Kandidaten geschrieben und gehasht (SHA256 in `synthetic_test_receipt.json`). Beide Dateien entstammen demselben AXIOM-Forschungsprozess — also **nicht** einer unabhängigen wissenschaftlichen Auditoreninstanz.

**Negative Mutation:** Lege den Inhalt von `mutant/r17_integrity_guard.py` als isolierte `r17_integrity_guard.py` neben die unveränderte Testdatei; er weicht nur dadurch ab, dass die Prüfung der Proof-Level-Reihenfolge zu `True` vereinfacht wird. Erwartet: 18/20; Tests 08 und 09 müssen scheitern; Exit 1. `mutant_failure_stdout.txt` dokumentiert den tatsächlichen Lauf.

## Veröffentlichungs- und Beweisgrenzen

- `role_ratified=True` im Test ist ein erfundener Fixture-Wert. Das Programm bestätigt **keine Operator-Signatur**.
- `evaluator_independently_attested=True` ist kein tatsächlich authentifiziertes Konto und keine reale Prozessisolation.
- `FORMAL_PROOF` als Zeichenkette ist **kein Proof-Artefakt**, Lean-Audit oder Beweis einer quantenmechanischen Identität.
- `verify_ledger` kann Änderung und Suffixlänge nur im Zusammenhang mit bereits extern bekannten Checkpoints/Counts entdecken. Es implementiert kein unveränderliches Storage und keine sicheren Retention-Rechte.
- Primary web sources wurden inhaltlich online geprüft. Raw-Body-Hashes/HTTP-Header fehlen: `primary_source_audit_partial.json` markiert korrekt `PARTIAL`.
- **Keine** Produktionsfreigabe, keine `C2`, kein Hostinger/GitHub-Merge, kein Experiment an Menschen, keine neue Actor-Registry, kein Quantum Runtime-Resultat.

## Paket

`manifest.json` enthält SHA256 und Größen jeder anderen veröffentlichten Paketdatei. SHA256 des ZIP selbst wird separat nach dessen Schließung ausgewiesen; `manifest.json` schließt sich selbst aus der Manifestliste aus.
