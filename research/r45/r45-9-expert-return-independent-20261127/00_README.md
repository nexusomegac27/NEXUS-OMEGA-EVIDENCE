# R45-9 Independent Expert Return — README

Autor: unabhängiger Experte (eigener Lauf, diese Sitzung) · 2026-11-27 · Claim Ceiling **C1_DESCRIPTIVE_ONLY**

Diese Lieferung ist der vollständige Dateistapel der R45-9-Expertenausführung (Serienabschluss der R45-Forschungsserie).
Sie wurde **unabhängig** erzeugt: die Rechenkerne wurden selbst implementiert, nicht aus dem AUTO_CLAW- oder
GLM-Stack kopiert; die Vorlagen dienten ausschließlich als gedankliche Strukturreferenz (Reihenfolge, Belegkettenformat).

## Inhalt

| Datei | Zweck |
|---|---|
| 01_INPUT_INTEGRITY.md | Bytegenaue Prüfung aller Eingänge (Orders, 3 ZIPs, GitHub-Readback, kanonischer ZIP **byte-exakt** geladen) |
| 03_COUNTERFINDINGS.md | Programm B — Replikation der AXIOM-Sandbox + eigene Gegenbefunde (echter Crash, Lock-Starvation, Zwei-Ressourcen-Nichtatomarität, Vokabular-Lücke, RED/GREEN der 10 Gegenprobenklassen) |
| 04_ACCEPTANCE_A.md | Programm A — Abnahmekriterien der Verarbeitungskette L0–L3 |
| 05_TDP_D.md | Programm D — Konsolidierung Temporal Dream Phase |
| 06_GAP_MATRIX_E.json | Programm E — IST/SOLL-Gap-Matrix, 24 Zeilen, 10 SOURCE_GAP, 0 STAGED/LIVE/PHYSICAL |
| 07_RETURN_STATUS.txt | HARD-Statusblock |
| src/ + results/ | Eigene Quellen und Ergebnisdaten (alle reproduzierbar) |
| contract/ | Datenvertrag-Prüfung + Golden Fixtures |
| RECEIPTS/ | SHA-verkettete Belegkette R00–R05 |
| WITNESSES/ | Zusammenfassende Zeugen je Ergebnisgruppe |
| RESOURCE_LEASE.json | Vollständige Ressourcenbilanz dieses Laufs |

## Kernbefunde in einem Satz

Die AXIOM-Sandbox reproduziert sich extern exakt (100/100 genau ein Commit, 13/13 Kontrollen, einziger
Unterschied die SQLite-Version), **aber**: ihr Versagungsverhalten bei Sperren-Verhungern ist eine Ausnahme
statt `DENIED`, ihr Ergebnisvokabular deckt sich nicht mit dem Vertrags-Enum, Zwei-Ressourcen-Atomarität
existiert nicht (konkret demonstriert), echte Prozess-Crashes sind beidseitig sauber (neu geprüft), und alle
zehn Gegenprobenklassen aus §2.1 der Order werden im ungehinderten Modell reproduziert (RED 10/10) und vom
explizit bindenden Kernel blockiert (GREEN 10/10).

## Grenzen

Keine Kryptografie, keine Prozessisolation, kein verteilter Effekt, kein TLC, kein physischer Sensor, kein
Live-Readback, E23 HOLD. Alles synthetisch, lokal, C1. `R46_1_IMPLEMENTATION_AUTHORIZATION = NOT_GRANTED`.
