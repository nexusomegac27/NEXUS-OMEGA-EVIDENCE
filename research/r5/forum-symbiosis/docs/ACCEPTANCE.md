# Abnahme und Fehlerproben

Alle automatischen Referenzfälle liegen in `tests/test_reference.py`. Ihre Namen sind die exakten Testlocators. Mehrere Unterfälle (z.B. Kontrastpaare) sind keine zusätzlich gezählten Unittests.

## Referenzabdeckung

| Invariante / Risiko | Ausführbarer Beleg | Grenze |
|---|---|---|
| I02 Third Node | roles_must_differ, peer_and_third_required, third_binds_peer_version | IDs ≠ tatsächliche Unabhängigkeit |
| I03/I12 keine Privilegien/Promotion | token_field_rejected, extra_score_rejected, claim_promotion_rejected | Freitext benötigt Review |
| I04 Dissens | dissent_not_silenced | UI-Sichtbarkeit separat offen |
| I05 menschliche Hoheit | agent_cannot_decide, other_human_cannot_decide, stop_does_not_require_review | Principal ist vertrauenswürdiger Testinput, keine Auth |
| I06/I07 additive CAS | mutation_changes_identity, sql_update_and_delete_denied, tampered_bytes_detected | Dateieigner kann Kette neu erzeugen |
| I08 hard fail | hard_fail_cannot_be_averaged, unknown_gate_holds | keine Gleichsetzung mit originalen NF-F01–F10 |
| I09/I10 Metadaten | missing_scope_rejected, schemas_well_formed | fachliche Vollständigkeit nicht automatisch entschieden |
| Recovery | restart_replay, stale_head_rolls_back, two_connections_no_silent_overwrite | kein Power-loss-/Parallelstress-/Backup-Restore-Test |
| Idempotenz | idempotent_retry, idempotency_conflict | produktive Session-/Scopebindung zusätzlich erforderlich |
| kanonische Bytes | golden_bytes, key_order, duplicate_key_rejected, invalid_unicode_rejected | eigenes eingeschränktes Profil, nicht JCS |
| UI-Token | design_token_contrast | zehn Paare mathematisch, keine gerenderte UI-Konformität |

I01/I11 sind zusätzlich kontextbezogene Sprach-/Darstellungsanforderungen. Ein Flag oder eine Regex beweist sie nicht.

## Zusätzliche Integrationsfixtures — noch nicht ausgeführt

SF-N01: derselbe authentifizierte Mensch unter zwei Alias-IDs → REVIEW_IDENTITY_COLLISION.
SF-N02: Browser sendet author_role=HUMAN, aber Agentensitzung → 403.
SF-N03: Third-Review für anderen Entry-/Peer-Hash → 422 ohne Write.
SF-N04: Client fälscht Gate-PASS → Server ignoriert Behauptung, lädt echte GateAssessments.
SF-N05: 99 % Score bei C1-Verletzung → BLOCKED.
SF-N06: HOLD-/Peer-Workflow verhindert Betreiber-STOP → Test FAIL.
SF-N07: Screenshot/Template wird als Messung importiert → SOURCE_REPORTED/DEMO, nie EXECUTED.
SF-N08: Revision nach Entscheidung überschreibt Original → API verweigert; neue parent-Version akzeptieren.
SF-N09: V0-Datei fehlt → SOURCE_GAP, keine synthetische Rekonstruktion als Original.
SF-N10: stale session/revoked delegation → 403 auch bei wiederholtem Request.
SF-N11: externer Origin/DNS-Rebinding auf Loopback → verweigern.
SF-N12: stored HTML/Script in Kommentar → als Text anzeigen, CSP; kein Execute.
SF-N13: Abbruch zwischen Objekt-/Eventwrite → keine halbe Transaktion, Neustart kontrolliert.
SF-N14: defekter Backup-/Kontrollpunkt → read-only Diagnose, kein Überschreiben.
SF-N15: Dashboard ohne Daten → „Noch keine Messung“, kein Live/0 %/Nominal.
SF-N16: Export scheitert → Fehlermeldung, kein Erfolgstoast.
SF-N17: Byteänderung zwischen Review und Commit → Versionskonflikt.
SF-N18: logarithmische oder farbige Darstellung versteckt Dissens → UI-Abnahme FAIL.

Positive Kontrollen: legitimer Widerspruch darf bestehen; Autor kann ablehnen ohne Konsens; negiertes Zitat „nicht bewiesen“ darf nicht pauschal als Claim-Promotion gesperrt werden; idempotente Wiederholung erzeugt genau ein Ereignis; lokale Annahme bleibt möglich, wenn alle unabhängigen Gatebedingungen erfüllt sind.

## Corpus- und Trial-Protokoll

Corpus-Prüfung je CA1–CA6: Eingangsdigest, Vorhandensein, Semantik/Version, Missing-References, Kausalitätsbehauptung, tatsächlich reproduzierbarer Test, Restlücken. Kein Summenscore als Vollständigkeitszertifikat. Vorliegende R10-Audits nur REPORTED_BY_SOURCE, sofern nicht neu ausgeführt.

Trial 001: erst nach abgeschlossenem erforderlichem Corpus-Audit; Operator-Scope, zwei konkrete Adapterversionen/Codecs, exakt gleicher Korpus, fixierte öffentliche Fixtures, unabhängige verdeckte Fixture-Verwaltung, Baseline A, Export, Reconstruction B, Compare. Harte Invarianten bitgenau; tolerierbare Performanceunterschiede vorher festlegen. Outputs/Logs/Environment binden. Parameterwechsel = neuer Trial, keine nachträgliche Änderung der Erfolgsschwelle. Auch ein Erfolg erlaubt nur Aussagen über diese geprüfte Konfiguration.

In diesem Paket: **kein ausgeführter Cross-Substrate-Trial**, keine neuen empirischen Forschungsergebnisse.

## Releasecheck späterer Forum-Implementierung

Separat nachweisen: Build, Unittests, Integrations- und Authprüfungen, Browser Chromium/Firefox/WebKit, tastaturbasierte Kernaufgaben, Fokus/Zoom/Kontrast, Screenreader, Recovery/Restore, Privacy, Lizenzinventar, Quellen- und Claim-Review. Nicht ausgeführte Dimensionen bleiben NOT_EXECUTED. Git-Push dieses Forschungsartefakts ist davon zu unterscheiden.
