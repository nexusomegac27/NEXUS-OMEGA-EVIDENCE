# 03 — Programm B: Kausale Autorität — Replikation und Gegenbefunde

Klasse aller eigenen Befunde: **LOCAL_VERIFIED_SYNTHETIC** (lokale SQLite/Dict-Kernel, keine Kryptografie,
keine Prozessisolation, keine echten externen Effekte). Quellen: `src/r45_9_expert_probes.py`,
`results/results_own_probes.json`, `results/results_axiom_replication.json`.

## B0 — Replikation der AXIOM-Referenz (Pflicht nach §12.B)

| Kriterium | Gepinnt (08_SQLITE_RESULT.json) | Eigener Lauf | Urteil |
|---|---|---|---|
| exactly_one_commit | 100/100 | **100/100** | REPRODUCED |
| budget_overruns | 0 | **0** | REPRODUCED |
| checks (13 Kontrollfälle) | 13/13 | **13/13, alle Werte identisch** | REPRODUCED |
| sqlite_version | 3.46.1 | 3.53.1 | ENV-DIFF (einziger JSON-Diff) |

## B1 — Eigene Gegenbefunde (über die 13 AXIOM-Kontrollen hinaus)

| # | Gegenprobe | Methode | Ergebnis | Bedeutung |
|---|---|---|---|---|
| B1.1 | Crash **vor** Commit | Kindprozess mit `os._exit(9)` zwischen INSERT und COMMIT (echter Prozess-Tod, keine simulierte Exception) | Readback `ABSENT`, `integrity_check=ok` | Journal-Rollback hält; keine Teilzustände. **Neu** gegenüber AXIOM („no real crash“) |
| B1.2 | Crash **nach** Commit, vor ACK | Kindprozess committet, stirbt vor ACK | Readback `VERIFIED_MOCK`, `integrity_check=ok` | Das UNKNOWN-Fenster ist durch unabhängiges Readback auflösbar — das Muster überlebt Prozess-Tod. **Neu** |
| B1.3 | Lock-Starvation | `BEGIN IMMEDIATE` gehalten, zweiter Writer mit timeout 0,05 s | `sqlite3.OperationalError('database is locked')` — **kein** `DENIED` | Versagensmodus ist eine Ausnahme, kein Vertragswert. In der Produktarchitektur muss Lock-Timeout explizit auf `DENIED`/`UNKNOWN` abgebildet werden (Gap G08) |
| B1.4 | Zwei-Ressourcen-Partialfehler | Commit auf db1 erfolgreich, injizierter Fehler vor Commit db2 | db1 `COMMITTED`, db2 `ABSENT` | Nichtatomarität über Ressourcen konkret demonstriert (nicht nur behauptet): lokale SQLite-Transaktion ≠ verteilte Atomarität (Gap G09) |
| B1.5 | Erweiterte Wächter | float `1.0`, `2**64`, negative/bool/NaN-Zeit, unbekannter Grant, `body=None`, Ablaufgrenze ±1 | 9/9 wie erwartet (`DENIED`; `expiry-1` → `COMMITTED`) | Wächterkette robust über die AXIOM-Kontrollen hinaus |
| B1.6 | Vokabular-Lücke | Schnittmenge Sandbox-Ergebnisse vs. `05_CONTRACT.json` `authority.result` | 5 Terme nur in der Sandbox (`ABSENT`, `COMMITTED`, `DUPLICATE`, `HOLD_MISMATCH`, `VERIFIED_MOCK`), 2 nur im Vertrag (`VERIFIED_EFFECT`, `VERIFIED_NO_EFFECT`) | **Neuer Integrationsbefund**: vor R46-1 ist eine explizite Abbildungstabelle Pflicht (Gap G10), sonst semantische Drift |

## B2 — Zehn Gegenprobenklassen (Order §2.1) als RED/GREEN

Methode: **RED** reproduziert in einem ungehinderten Modell die Defekt-Outcomes der Referenzmodelle
(GEMÄSS Order-Tabelle); **GREEN** zeigt, dass ein explizit bindender Kernel (Grant-Hash über
Ressourcenzustand, Aktion, Kosten, Lease-Ablauf, Epoche) jeden Pfad blockiert. Dict-Kernel, bewusst
ohne DB: die Proben prüfen Adjudikations-Semantik, nicht Speicherung.

| Klasse | RED (ungehindert) | GREEN (gebunden) |
|---|---|---|
| 1 Kosten nach Freigabe erhöht (GLM) | `RECEIPT` (Defekt reproduziert) | `DENIED` |
| 2 Boolean als Kostenwert (GLM) | `RECEIPT` | `DENIED` |
| 3 NaN als Kostenwert (GLM) | `RECEIPT` | `DENIED` |
| 4 Unendlich als Kostenwert (GLM) | `RECEIPT` | `DENIED` |
| 5 Settlement ohne Effekt (GLM) | `SETTLED` | `DENIED_NO_EFFECT` |
| 6 Abgelaufene, nicht aufgelöste Reservierung (GROK) | `BUDGET_BLOCKED` | `DENIED_RESERVATION_EXPIRED` + explizite Reconciliation mit Audit → Budget frei |
| 7 Gleichzeitige Änderung von Request und Grant (GROK) | `RECEIPT` | `DENIED` |
| 8 Veränderte Lease-Ablaufzeit im Grant (GROK) | `RECEIPT` | `DENIED` |
| 9 Veränderte Ressource bei unverändertem Receipt-Hash (GROK) | `VERIFIED_EFFECT` | `HOLD_MISMATCH` |
| 10 Settlement ohne unabhängige Beobachtung (GROK) | `SETTLED`, Readback `UNKNOWN` | `DENIED_UNOBSERVED_SETTLE` |

**RED 10/10 reproduziert · GREEN 10/10 blockiert.** Interpretation: Die §2.1-Tabelle der Order ist als
Defektklasse belastbar; ein Kernel mit expliziter Aktions-/Payload-/Lease-Bindung deckt alle zehn Pfade
ab. Das ist eine synthetische Prüflogik an einer modellierten Ressourcengrenze — kein Angriff auf und kein
Nachweis über das produktive NEXUS-System.

## B3 — Nicht behoben (bleibt offen, append-only)

- Reale Kryptografie, Prozessisolation, Stromausfall unter Last, vollständige Produktionsvermittlung: **nicht geprüft**.
- TLC: **NOT_RUN** (tla2tools nicht vorhanden; Installation laut Order verboten).
- Die beiden GLM-Vordiagnostiken (3360/24718, 49152/413952) bleiben **SOURCE_GAP** (erzeugende Artefakte nie übertragen).
- 156 Sequenzen / 4.096 Kombinationen: nur als *LOCAL_VERIFIED_INPUT* aus dem GLM-Return übernommen, nicht neu gerechnet.
