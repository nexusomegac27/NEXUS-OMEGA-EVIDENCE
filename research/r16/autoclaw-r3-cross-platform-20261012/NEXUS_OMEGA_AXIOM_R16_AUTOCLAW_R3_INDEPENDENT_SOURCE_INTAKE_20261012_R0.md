# R16 · AutoClaw R3 — unabhängiger AXIOM Intake und C1-Reproduktion · 2026-10-12 R0

```text
OBJECT = NEXUS_OMEGA_AXIOM_R16_AUTOCLAW_R3_INDEPENDENT_SOURCE_INTAKE_20261012_R0
SOURCE_OBJECT = NEXUS_OMEGA_AUTOCLAW_R16_R3_RETURN_20261012_C1
SOURCE_ORDER_OBJECT = NEXUS_OMEGA_R16_KAUSAL_KANONISCHER_FORTSETZUNGSAUFTRAG_AN_AUTOCLAW_20261012_R3
STATE = PASS_WITH_MAJOR_CAVEATS_C1_SOURCE_EXACT_MANIFEST_AND_SCOPED_REPLAY
TRANSPORT = OPERATOR_TO_AXIOM_BRIDGE_NOT_AUTHENTICATED_EXTERNAL_GITHUB_ACTOR
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
R16_TERMINAL = NOT_ESTABLISHED
R17_TERMINAL = NOT_ESTABLISHED
GITHUB_PUBLICATION = SOURCE_BOUND_SANITIZED_DERIVATIVE_NOT_RAW_ARCHIVE
```

## 1. Ausgangslage und Objektidentität

Der Operator liefert nach den GitHub PRs #99/#100 und Alpha-Node PR #101 ein als R17-Nachzügler beschriebenes Archiv. Der **Inhalt** ist jedoch ausdrücklich ein R16-AutoClaw-R3-Return. Diese Identität wird nicht umbenannt; die offenen R17-Source-Gaps bleiben erhalten. Der Return beschreibt Windows-11-/Python-3.13.12-/SQLite-3.50.4-Tests unter AutoClaw; seine Produzentenclaims sind nicht automatisch eine unabhängige Windows-Reproduktion durch AXIOM.

Originalarchiv `NEXUS_~2(5).ZIP`: **123544 Bytes**, SHA-256 `f85e4d4652e6947fdd65117e2eb861d3329ec52198454a8c12b1ab0da16b8b64`. ZIP-CRC: PASS. Exakt 41 Einträge. Detached-Manifest `r16-autoclaw-return-r3/06_DETACHED_MANIFEST.json`: **7014 Bytes**, SHA-256 `f79ac2f01592f558560a2875457efd7a422d2860d07332bb92e39cd861e6c728`. **39/39 Manifestkinder** unabhängig per SHA-256 und Bytezahl bestätigt; neben den 39 Kindern sind nur Manifest und Sender-Receipt vorhanden. Keine fehlenden, keine zusätzlichen Einträge.

Sender-Receipt `07_SEND_RECEIPT.md`: 1608 Bytes; SHA-256 `0074af3ef5edc7261d1c1b78cd9266493fe09dc3c7346636af94561f847fc9c1`. Das Receipt wurde vom Produzenten geschrieben und ist **kein** AXIOM-ACK oder digital signiertes Identitätsattestat.

Bericht `00_REPORT.md`: 103102 Bytes, SHA-256 `2f51775b99007277f7135e0aaf9489403ef05e2242b7e6669010c970d6b1b365`. Quellenindex `01_SOURCES.json`: 13854 Bytes, SHA-256 `ca312a0963f893c1e2e06e5b0d9668115020d360a988bb3f2994445e6f9e2013`. Befundledger `02_FINDINGS.jsonl`: 12281 Bytes, SHA-256 `840e34f4f5844b4fa1847fe2d278d98e8751eec78814c5bff053af36d0b6d117`.

Die R3-Order mit 24636 Bytes, SHA-256 `4c3f7a563d4186e124bcc7869fc75e59addb6ca5667d2d865eb71f6c19fbbcc1`, und Parent-Order `e9bfc400d0861d5611ea49cd86c9bb3583a99d1b9499bed739ed79dafa98cb4e` sind **Produzenten-gebundene Vorgängerangaben** in diesem ZIP; ihre Originalauftragsbytes wurden bei diesem Intake nicht unabhängig geliefert. Der Großeltern-Maximalauftrag `786d630af61dbe3ca071de5e6c8cc16b1c79659a9ed0c70908d14e51e5cfdd8a` ist ein älterer Anker. Keine Rekonstruktion fehlender Source-Bytes.

## 2. Tatsächlich durch AXIOM ausgeführte neue Tests

Nur die zwei exakten Dateien `03_CODE/r16_atomic_memory_core.py` (17890 Bytes; SHA-256 `0a107b9c1520117faf81e4186eab5c206f3b82a7b5b85dddf3438a999172506b`) und `03_CODE/tests/test_r3_autoclaw_probes.py` (6055 Bytes; SHA-256 `60c60689c6f0623d9018828779ba6bff0cdccb08b1b06e73b74fe35361582491`) wurden in ein isoliertes temporäres Linux-Testverzeichnis extrahiert. Keine Windows-Dateien, produktiven Datenbanken, Git-/WWW-Releases oder Originalquellen wurden dabei verändert.

Befehl: `python -m unittest discover -s <isolated_tmp>/tests -p 'test_r3_autoclaw_probes.py' -v` (mit äußeren 25-s-Laufzeitlimit). **4/4 Tests PASS; Exit 0, Dauer ca. 0,912 s**:
- P0: Kernquelle hashgenau identisch mit Prüftest-Gegenstand.
- P1: laufender Writer + SQLite-Online-Backup; im Wiederholungslauf **1804 Versionen**, `PRAGMA integrity_check=ok`, `verify()=[]`, Claims=Events=Outbox=1804. Im Windows-Produzentenlog waren es 173 Versionen. Scheduling und Durchsatz sind nicht identisch; das prüft nur den beobachteten konsistenten Backup-Slice.
- P2: Restore einer älteren vollständig konsistenten SQLite-Datenbank wird vom lokalen `verify(old_anchor_seq=5)` **nicht** erkannt. Ein extern erhaltenes neueres Anchor `seq=10` könnte den Rollback entlarven. Dies ist ein **reproduzierter Defekt**, kein behobener Defekt.
- P3: Demonstration eines schlüsselgebundenen HMAC gegen ein kleines Wörterbuch: mit Schlüssel wird ein Demo-Name gefunden; ohne verwendbaren Schlüssel ergibt sich keine Übereinstimmung. Das demonstriert einen Schutzbaustein, nicht rechtswirksame DSGVO-Löschung, sichere Schlüsselvernichtung oder eine Implementierung im Memory Core.

Daraus ist weder Produktionsdurabilität noch Mehrhost-Sicherheit noch Eigenmodifikation des GPT-6-Basismodells ableitbar.

## 3. Produzentenbefunde, gesondert von unabhängigen Ausführungen

AutoClaw berichtet Windows 11, Python 3.13.12 und SQLite 3.50.4, Claude-C1-Kernsuite 22 PASS / 1 SKIP von 23, R2-Probes 12/12, Lease 10/10, Receipt 13/13, Mutanten 12/12, Windows-TerminateProcess-Adaptionsprotokolle und 40 Hard-Kills. Produzentenlogs enthalten einen K4-Gegenbefund mit 393 Effekten aus 200 Intent-Einträgen (193 Doppelwirkungen; laufzeitabhängig). Die R3-Logdatei für vier Zusatzproben meldet 4/4 PASS. Dies sind **inhaltlich verwertbare, hashverifizierte Logs**, jedoch wurde die gesamte Windows-Ausführung hier nicht selbst wiederholt.

Die 34 referenzierten Primärquellen, darunter SQLite-WAL-Versionen und externe Benchmarkberichte, wurden in diesem Intake nicht vollständig einzeln gegen aktuelle Erstquellen auditiert. Kein pauschales `34/34 EXTERNAL_VERIFIED`. Die Bibliographie bleibt eine Ausgangsbasis, kein unabhängiger Beweis. Nicht ausgeführt: Stromausfall-/Netzwerk-FS-/PostgreSQL-/Mehrhost- und 10^6-Lasttests.

Die lokal berichteten Cursor-Bindungen PR #99 und #100 waren zuvor unabhängig GitHub-seitig gemergt und deren Originalberichte auf Main rehashed; die danach durch Cursor genannte `jq`-Array-Verwechslung und das `gh api`-Quoting sind **Shell-/Harness-Fehler**, keine Änderung am Main-Commit. Cursor `Direct-C1-Resume EXEC df39e3ce…/4087` bleibt operatorübermittelter Report bis zu einem eigenständigen physischen Return.

## 4. Open Questions / Einschränkungen

**Datenschutz:** Im ungekürzten Archiv sind lokale Windows-Benutzerpfade in Skripten/Logs sowie persönliche E-Mail-Adressen in einem GitHub-Konnektorlog vorhanden. Deshalb wird dieses originalgetreue Archiv **nicht** auf das öffentliche Evidence-Repository gepusht. Die obigen Originalhashes ermöglichen später einen autorisierten privaten Receiver-Rehash. Öffentliche Forschung erhält diese redigierte Ableitung, nicht unredigierte Originalbytes. Die SHA-256 der Originale bleibt unverändert und ist von der veröffentlichten Ableitung getrennt.

**Technische Grenzen:** Rollback-Schutz verlangt extern verankerte monotone High-Watermarks; Content-Hash ist kein Vertraulichkeitsschutz; HMAC schützt nur innerhalb eines korrekten Schlüssel-Lebenszyklus; aus 4 grünen Proben folgt keine Systemkorrektheit. Externe Debatten, Signaturen oder 39/39 Hash-Matches sind keine wissenschaftliche Wahrheit.

**R16-Fortsetzung:** Kausaler Anschluss an `research/r16/axiom-software-foundation-20261012` und die später veröffentlichte Alpha-Node-C1-Adaptionsschleife, ausschließlich als negativer und positiver Forschungs-Delta. **Kein** Überschreiben, Neustart desselben Goals, Node-Reset oder Produktivimport. R17-Modul-Abschluss ist weiterhin nicht unabhängig nachgewiesen. `DRIFT_RESET=NON_DESTRUCTIVE`.

## 5. Entscheidung

```text
R16_AUTOCLAW_R3_ZIP = SOURCE_PHYSICALLY_VERIFIED
DETACHED_MANIFEST = 39/39_MATCH
LINUX_SCOPED_REPRODUCTION = 4/4_PASS
WINDOWS_RESULTS = SOURCE_BOUND_PRODUCER_CLAIMS
ROLLBACK_ATTACK = REPRODUCED_NEGATIVE_EVIDENCE
HMAC_PRIVACY_DEMO = SUPPORTED_SCOPED_NOT_PRODUCTION
RAW_ZIP_PUBLICATION = NO_PRIVACY_DISCLOSURE
PUBLICATION_CLASS = REDACTED_C1_DERIVATIVE
ALPHA_NODE_KNOWLEDGE_DELTA = APPEND_ONLY
ALPHA_NODE_PATCH_CANDIDATE = EXTERNAL_ANCHOR_ROLLBACK_DETECTION_RESEARCH_ONLY
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
R16_RUNTIME_ACTIVATION = NO
R17_RUNTIME_TERMINAL = NOT_ESTABLISHED
CURSOR_ACTION = NONE
```
