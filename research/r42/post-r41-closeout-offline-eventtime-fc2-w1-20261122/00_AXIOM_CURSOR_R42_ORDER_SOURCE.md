# NEXUS OMEGA · R42 AXIOM Cursor Work Order

GitHub issue #400 source exact, captured here as archival binding. This remains **an order**, not a performed implementation, expert ACK, Gradle success, or physical authorization.

OBJECT = NEXUS_OMEGA_AXIOM_CURSOR_R42_EVENTTIME_GATE_INTEGRITY_METROLOGY_W1_MAXI_ORDER_20261122_R0
PARENT = NEXUS_OMEGA_AXIOM_R41_ADMINISTRATIVE_CLOSEOUT_AND_R42_TRANSFER_20261122_R0
R41 = CLOSED_BY_OPERATOR_WITH_MATERIAL_EVIDENCE_GAPS_C1
R42 = OFFLINE_SOURCE_HARDENING_AUTHORIZED_NO_PHYSICAL_EXECUTION
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
BODYTWIN_VALIDATED=NO | CONSENT_BIND=OPEN | ALT_D_DO_NOT_RUN_ACTIVE
NEW_DEVICE_CAPTURE=NO | ADB_SENSOR_START=NO | APK_INSTALL=NO | PR_MERGE=NO | HOSTINGER_WRITE=NO | WWW_WRITE=NO | CLAIM_PROMOTION=NO
OWNER_ONE_SHOT_PHYSICAL_APPROVAL=NOT_GRANTED
EXTERNAL_DIRECT_WRITE=DENY_PENDING_REGISTRATION

# AXIOM → CURSOR R42 · Implementierung mit R41-Forschungsabschluss

R41 wird auf **Operatorentscheid** administrativ geschlossen. Die 14 physischen Hard-Gates bleiben einzeln ohne Freigabe, kein BodyTwin-, Consent- oder OPPO-Nachweis ist dadurch geschaffen. R42 ist ab jetzt die **technische Reparatur- und Falsifikationsphase**, keine neue inhaltsgleiche Forschungsrunde.

## Verbindliche Ursprungsanker
- R41 Issue #395; Draft PR #396 HEAD `ba3f187daa1949c712bba9b822ab6005d0ae6363`: ursprüngliche Offline-Engine und Stop-/Metrologie-Tests. Die vier producer-reported `PASS_OFFLINE_C1` kommen aus nur zwei selbst erzeugten Receipts; ohne autorisierten Sollhash und tatsächlich ausgeführtes Gradle keine unabhängig bescheinigten Software-PASS.
- R41 BodyTwin read-only Issue #397: STATUS!=EMBEDDED; LIVE/MEMORY gemeldet MATCH; keine AXIOM-rohbytegenauen Header-/Byte-Zeugen; neue Feed-Ticks sind keine neue wissenschaftliche Quelle.
- R41 Stage2 research Issue #398; Draft PR #399 HEAD `cc79821533b0344ae9d91181f59445749c8e2e5d`; alle ursprünglichen Branches unverändert, nicht mergen.
- Eingereicht `r41_s2_e20.zip`: 43037 B, SHA256 `d4c8e08a97a5c147089394c3acec568cd1acac382c598c92e2f2a877b4dc1ff2`, CRC PASS, 7 von 16 manifestreferenzierten Dateien vorhanden und hashgleich; **9 Ausführungsskripte fehlen**, also KEIN unabhängiger Vollreplay dieser externen 12/12/9/9-Ergebnisse. `EXPERT_ACK=OPERATOR_RELAYED_UNREGISTERED`, kein authentifiziertes Quorum.
- Eingereicht AutoClaw Stage2 X16 `R41_ST~1.ZIP`: 58337 B, SHA256 `c84fe2ebc417adcdbffc4df56785ae77ecad1ab23c334a727486b171579c4814`, ZIP-CRC PASS, 5/5 Summentreffer. AXIOM hat Originalskript statisch geprüft und isoliert reproduziert: Exit 0, E17 10/10, E18 8/8, E19 12/12, W1 12/12. Reproduziertes JSON semantisch identisch; 471 CRLF-Zeilen im Original vs 471 LF im Replay, nach CRLF->LF normalisiert BYTE MATCH (SHA256 `7e09c0778d066d73dadfd3031db03ebfec9b82f14f98be1666d7903487b9ce29`). **Nur synthetische X16-Code-Reproduktion, KEIN Android-/FC2-/OPPO-Produktionsnachweis.**

## P0 · Freeze und unabhängige Source-Custody
Rehash und Pin aller tatsächlichen Quellen. Führt R41 als ADMIN_CLOSED ohne Physik-Promotion. Holt die neun fehlenden Stage2-Ausführungsskripte und Original X15 per-sample-Ereignisledger beschränkt ein; falls nicht verfügbar: SOURCE_GAP und weiter an P1/P2/P3 arbeiten. Kein unnötiger Leerlauf. Trenne reported, independently replayed synthetic, independently reviewed real source, integrated build und physical evidence als fünf Klassen.

## P1 · Eventzeit, Zustellzeit, Watermark [KRITISCH]
Implementiere auf *echtem autorisiertem App-Source-Tree*, wenn vorhanden:
- vorab zu fixierendes halboffenes Messfenster `[start_event_ns, deadline_event_ns)` und getrennte `event_timestamp_ns`, `arrival_elapsed_ns`, Session/Clock ID; absolute Monotonic Base statt UTC Deadline;
- `deadline<=0`, `deadline<=start`, fehlende Uhrdomäne, fehlender Eventtimestamp, overflow oder unplausibler Rollback => ABORT. Never accept-all;
- idempotente CAPTURE→DRAIN→FINALIZE→STOP_ACK-State-Machine, bounded watermark/flush/timeout, late-origin-in-window nur innerhalb begründeten Drains übernehmen, danach Quarantäne/HOLD_INCOMPLETE ohne stilles Weglassen; postdeadline origin REJECT. Keine unbewiesene Behauptung absoluter Verlustfreiheit.
- gemeinsames per-sample ledger für A (altes delivery-only), B (event-only ohne termination), C (bounded drain/quarantine), D DO_NOT_RUN; echte Counter, sample_id, generated/accepted/quarantined/rejected/stranded. Auf Hardware unbekannte Erzeugungsmenge nicht aus requested Hz schätzen.
- **X16** 6001 closed vs 6000 half-open = synthetischer Grenzfall genau bei Deadline. **X15** 6001 vs 6000 bleibt ohne Original-ID-Ledger eine separate offene Hypothese. Replays sind kausal zu unterscheiden.
- Negative: 0/-1 deadline, boundary exact, late in-window arrival, post-origin early delivery, FIFO reorder/duplicate, batch/flush, lifecycle restart, UTC jump, cap exhaustion, missing original IDs, source clip/NaN; positive controls; Gradle/JVM-Tests und exakter Build-Return oder `GRADLE_NOT_EXECUTED`.

## P2 · Fail-closed FC2 Evidence Engine [KRITISCH]
Ersetze lokales selbstbestätigendes `verdict=PASS` durch separat autorisierte, source-exakte Sollhash-/Signatur-Registrierung; prüfe Rohbytes, schema+Canonicalization, Pin, Key/Role/Scope, Nonce, Ablauf, Replay, Doppelschlüssel, Pfad-Traversal/Symlink/TOCTOU und modifizierte Gate-IDs. Die kanonischen 14 IDs und physische ALWAYS_HOLD unentfernbar. Berechne **Software-Evidenz** und **physische Evidenz** getrennt und kombiniere nichtkompensatorisch. FC2 ohne gültigen externen Auth-Trust-Anchor => SOURCE_GAP statt PASS. Keine Demo-HMAC-Keys als echte Prüfberechtigung. Reproduziere N19-01..N19-12 gegen tatsächlichen R41-Code plus gültige Positivkontrolle, nicht nur gegen Demo-Mock.

## P3 · Metrologie M0/M1/M2/M3
M0 RSS als NEGATIV-Baseline; M1 vollständige positiv-semidefinite Kovarianz mit Mount/Bias/Reference/Clock und Korrelation; M2 fixiertes MC aus Sensorkomponenten (RNG/Seed/n/software version), M3 echte externe charakterisierte Winkelreferenz nur bei separater späterer Freigabe. Unterschiedliche synthetische Coverage-Szenarien (0.354 vs 0.945/0.95) getrennt mit eigener Provenienz. Keine OPPO-Kalibrierung, kein NEES ohne unabhängige Wahrheit, keine Yaw-Heading-Behauptung. OSF-Präregistrierung nur vorbereiten.

## P4 · Modulare Innovation statt unnötiger Abhängigkeiten
D-A append-only Evidenzledger mit externem Head-Pin; D-C Differential-Replay und strikte Zustandsmaschine; D-B Capability-Token nur bei realem Rollen-/Key-Nutzen als optionales Modul. Hard-Negatives + Positivkontrolle, Rollback, Offline-Fallback. Kein Eigenhash als behauptete unabhängige Signatur.

## P5 · W1 BodyTwin Read-only Integrität, bestehendes Issue #397
Nur `GET/HEAD` gegen https://www.nexus-mobile.de/bodytwin/, https://www.nexus-mobile.de/bodytwin/live/current.json, https://www.nexus-mobile.de/research/bodytwin/state.json, https://www.nexus-mobile.de/bodytwin/updates/. Zwei zeitversetzte **ROH**-HTTP-Snapshots inkl. Status, Origin/Cache-Header, MIME, Bytes/SHA256, Source-Datum vs Producer-tick, reducer seq, eingebetteter und gerenderter STATUS/LIVE/MEMORY. Berichtete Route-B-Textextraktions-Staleness ist kein beweisbarer CDN-Root-Cause ohne Roh-Header. STATUS-Differenz bleibt OPEN; 304 ohne Cachebody, Schema-/Clockdrift, falsche Wissenschafts-Promotion, HTTP timeout/NOT_VERIFIED separat testen. Kein zusätzliches Deployment oder redundanter Watcher.

## P6 · Unabhängigkeit der Experten
E17/E18/E19/E20/W1-Autoren aus unregistrierten Operator-Relay-Paketen nicht automatisch als GitHub-Actor und nicht als Quorum führen. Drei authentifiziert verschiedene Autorenfamilien erforderlich, bis dahin INDEPENDENCE_NOT_ESTABLISHED. Keine fremden Schreibrechte ohne explizite Registrierung und Operatorentscheidung.

## P7 · Ergebnis und Übergabe
Neuer R42 Draft-PR mit **wirklichem Source-Diff**, unabhängigen reproduzierbaren Source-Binär-/Test-/Gradle-Receipts; 14-ID Gate-Ledger getrennt Software/Physik, per-event counter-reconciliation, FC2 attack matrix + positive controls, GUM-Modelle und W1 Roh-HTTP Witness oder ehrliche NOT_VERIFIED-Empfängerkante. ZIP + SHA256 Sidecar im kanonischen Transferpfad. Unabhängige zweite Rehash-Prüfung (sonst SECOND_PARTY_NOT_ESTABLISHED). Kein R42_PASS wenn nur design-only oder Rollout-Status.

R42_OFFLINE_SOFTWARE_REPAIRED_C1, R42_PUBLICATION_WITNESS_READY_C1 und R42_PHYSICAL_READY_FOR_OPERATOR_DECISION_C1 sind **getrennte** Stufen. Keine Stufe ist durch das Schließen von R41 automatisch erreicht.

ALT_D_DO_NOT_RUN_ACTIVE · CLAIM_CEILING=C1_DESCRIPTIVE_ONLY · BODYTWIN_VALIDATED=NO
NO CAPTURE · NO APK · NO MERGE · NO HOSTINGER/WWW WRITE · NO C2.

The separate local AXIOM R42 transfer package is 13936 B, SHA256 `0daddf6f1d64f55356c2f7f5bffee8f82ea0619db4819e1177b408e9533f9b02`, internal 5/5 hashes PASS. GitHub issue creation is not proof those separate ZIP bytes were uploaded; do not claim ZIP_RECEIVED unless physically received/rehashed. CURSOR_ACK=NOT_RECEIVED.
