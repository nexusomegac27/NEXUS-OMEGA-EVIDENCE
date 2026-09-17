# Implementierbare Blaupause SF-R0

## 1. Architekturentscheidung und Umfang

Lokaler evidenzorientierter Forumkern; bestehende R10-Oberflächen bleiben als spätere Integrationsbasis. Die Architektur ist ein Vorschlag nach eigener Quellenprüfung, keine vorgetäuschte gemeinsame GROK/Mistral-Freigabe.

```text
R10 UI / neue verständliche Ansicht
             |
       lokaler API-Adapter --- authentifizierte Sitzung / menschlicher STOP
             |
      Schema + Scope + Governance-Gates
             |
  transaktionaler ObjectStore + EventLog
             |
       lesbare Projektionen
      /        |         \
  Corpus   Review/Dissens  Return/Export
```

Zunächst nur Loopback, ein Workspace, explizite Benutzerzuordnung. Keine Federation, Tokens, Agenten-Selbsterhaltung, automatische Publikation oder autonome Claim-Promotion. Die vorhandenen R10-Module werden nicht durch dieses Paket verändert.

Der Python-Prüfadapter ist eine **ausführbare Referenz für die Verträge**, keine Entscheidung für einen Python-Produktionsserver. Cursor kann diese Regeln in die vorhandene JS-Schicht portieren; Golden-Bytes und gleiche Fixtureergebnisse sind dafür verpflichtend.

## 2. Fachobjekte und Verträge

Alle neuen dauerhaften Objekte: schema_version, claim_ceiling=C1_DESCRIPTIVE_ONLY, typisierte Payload, explizite Provenienz; Inhaltshash extern im CAS, keine Selbstreferenz.

| Objekt | Identität / Pflichtinhalt | Referenzen |
|---|---|---|
| ForumEntry | v2-Schema, menschlicher author_id, scope, interpretation, evidence_class, ambiguity, confidence | parent (optional), evidence_refs |
| Review | Peer/Third, reviewer_id, rationale, conclusion, independence, disclosures | entry_cid; Third zusätzlich peer_review_cid |
| EvidenceSource | kind=FILE/URL/REPORTED_RESULT; locator; observed_digest oder null; availability; access_checked_at | original evidence bytes oder explizite SOURCE_GAP |
| DissentRecord | actor_id, reason, scope; nicht löschbare fachliche Referenz | entry_cid, optional review_cid |
| GateAssessment | gate, status PASS/FAIL/UNKNOWN, evaluator, reason, method | target_cid, evidence_cids, policy_cid |
| DecisionRecord | HUMAN author, action, reason, result_state, acknowledged_dissent | entry_cid, review_cids, gate_assessment_cids, event_head |
| HoldRecord | reason, missing_evidence, assignee, due_at|null, released_by|null | entry_cid; keine Abschaltblockade |
| GapRecord | gap_id, description, scope, severity, status OPEN/RESOLVED/SUPERSEDED | evidence that opened/closed gap |
| TestDefinition | method, inputs, expected behavior, version, environment contract | script_cid / fixture_cids |
| TestRun | EXECUTED/FAILED/INTERRUPTED; actual command, runtime versions, exitcode, outputs, started/ended | definition_cid, exact input_cids |
| MigrationRecord | old_profile/digest, new_cid, transformer digest, reason | alter R10-Eintrag und neue Ableitung |
| Event | monotone seq, previous_cid, kind, payload_cid, request key/digest | exact payload, previous event |

Nur Entry/Review-Schemas und die Speicher-DDL sind hier ausführbar geliefert. Die übrigen Zeilen sind verbindliche **Implementierungsverträge**, noch keine fertigen produktiven Datentypen. Erweiterungen müssen unknown fields ablehnen und typisiert versioniert werden; nicht blind beliebige Payloads als Ergebnis akzeptieren.

## 3. Prozessübergänge

| Vorher | Ereignis | Nachher | Bedingungen |
|---|---|---|---|
| kein Eintrag | create | DRAFT | valides Entry, author aus Sitzung, gebundene Quellen oder sichtbare Lücken |
| DRAFT | submit | IN_REVIEW | immutable entry_cid fixieren |
| IN_REVIEW/HOLD/BLOCKED | review/add-evidence | unverändert | neue append-only Objekte; Gatebewertungen erneut erstellen |
| DRAFT/IN_REVIEW/HOLD/BLOCKED | HOLD | HOLD | Grund, zuständige Person; kein Timeout-Accept |
| IN_REVIEW/HOLD/BLOCKED | ACCEPT | ACCEPTED_LOCAL_C1 | menschlicher Autor, aktuelle Peer/Third-Reviews, vier belegte Gates PASS, Dissens beantwortet |
| nicht terminal | ACCEPT mit UNKNOWN/fehlendem Review | HOLD | konkrete fehlende Bedingung anzeigen |
| nicht terminal | ACCEPT mit hartem FAIL | BLOCKED | Testfehler nicht durch Score ausgleichen |
| nicht terminal | REJECT | REJECTED | menschlicher Autor, Grund; kein Reviewzwang |
| nicht terminal | STOP | STOPPED | menschlicher Autor; Betriebs-STOP unabhängig davon jederzeit möglich |
| terminal | neue Revision | neuer DRAFT | neues CID mit parent; ursprüngliche Entscheidung bleibt erhalten |

Ein neues Review kann historische Entscheidungen kommentieren, nicht rückwirkend abändern. Ein erneuter Entscheidungsversuch nach STOPPED/REJECTED/ACCEPTED braucht eine neue Version; kein in-place reopening.

Der Referenzprüfer trennt reine Entscheidungsregeln von Speicherung. Ein produktiver Service MUSS beides in einer atomaren, versionsgebundenen Operation verbinden, damit zwischen Gateprüfung und Write kein Versionswechsel unbemerkt bleibt.

## 4. Lokale API — Implementierungsvertrag

Basis: `/api/forum/v1`. Mutationen nur POST, JSON <=1 MiB, UTF-8, strikte Parser/Schemas. Verbindliche Sitzungsidentität im Serverkontext, niemals Rollenfeld im Body. Schreibvorgänge verlangen CSRF-/Origin-Prüfung, erwarteten Event-Head und Idempotency-Key; explizite allowlist von Origins, kein wildcard-CORS. Loopback allein schützt nicht vor fremden Browserseiten.

| Endpoint | Request | Antwort |
|---|---|---|
| GET /capabilities | authentifizierte Sitzung | schema versions, LOCAL_ONLY, C1, permitted operations, no authority defaults |
| POST /entries | Entry draft, expected_head | 201 entry_cid + event_head |
| GET /entries/{cid} | gültige Inhaltsadresse | Entry, separat abgeleiteter Prozessstatus, ETag, provenance |
| POST /entries/{cid}/reviews | Review payload ohne client role | 201 review_cid; Target muss existieren |
| POST /entries/{cid}/dissent | scope, reason | 201 dissent_cid |
| POST /entries/{cid}/holds | reason, missing evidence, assignee, due_at|null | 201 hold_cid |
| POST /entries/{cid}/decisions | action, reason, exact review/gate CIDs, acknowledged dissent | 201 DecisionRecord plus event_head; kein stilles ACCEPT |
| GET /entries/{cid}/lineage | cursor pagination | parent/fork graph plus linear alternative |
| GET /corpus | cursor/filter | inventarisierte Objekte mit source status; null statt fingierter Messung |
| GET /runs/{cid} | gebundener Run | Definition/Run/Source-Reported klar getrennt |
| POST /exports | ausgewählte freigegebene CIDs | lokal erzeugte Bytes/Download und Manifest; keine externe Übertragung |
| POST /runtime/stop | Betreiber-Sitzung | stop receipt wenn möglich; Prozessstopp darf nicht vom Receipt abhängen |

Errors: 400 Parse/Schema; 401 unauthenticated; 403 actor/scope; 404 missing object; 409 stale head/idempotency conflict/terminal; 413 size; 422 governance invariant; 503 recovery mode. Errorbody: code, plain_message, affected_cids, missing_evidence, retriable, current_head. Keine Tokens, Stacktraces oder privaten absoluten Pfade.

Ein HOLD/BLOCKED ist ein gültiges **Entscheidungsergebnis**, nicht automatisch ein HTTP-Fehler. Ein unverarbeitbarer oder unautorisierter Request wird dagegen verworfen.

## 5. Speicher, Nebenläufigkeit und Recovery

SQLite-Datei außerhalb öffentlich ausgelieferter Assets. DDL siehe `schema/store.sql`. Gate- und Principal-Prüfung unmittelbar vor Write, innerhalb konsistenter Transaktionssicht. BEGIN IMMEDIATE; current_head prüfen; idempotente identische Wiederholung liefert ursprüngliches Receipt; gleiche Request-ID mit anderem Inhalt = Konflikt. Bei Abbruch alles rollback, kein halbes Event.

Der Referenzstore demonstriert atomare CAS-/Event-Writes. Er hat absichtlich keine Auth-/Policyfunktion und darf nicht direkt als API angeboten werden. Projektionen sind abgeleitet; rebuild schreibt neue Cachedateien, keine Änderungen an Belegen. Append-only-Trigger sind keine Abwehr gegen Dateieigner/Administratoren.

Backup vor Migration: Datenbank-sicherer Snapshot, Hashmanifest, separat gespeicherter Head; Wiederherstellung in anderem temporären Verzeichnis, vollständiges Replay vergleichen. Gleichzeitigen Writer berücksichtigen. Referenztests prüfen geregelten Neustart und sequenziellen Konflikt zweier Verbindungen, **keinen Stromausfall oder konkurrierenden Lasttest**. Diese bleiben Integrationsgates.

## 6. UI-Vertrag: Alltagsansicht und Expertenspur

Default deutsch, verständliche kurze Texte. Sichtbar oben: „Lokaler Arbeitsstand · C1 · keine wissenschaftliche Validierung“. Nie Live-Badge aus Build/Hash ableiten.

| Route | Inhalt | Interaktion / leere Zustände |
|---|---|---|
| /forum/local | Vorschläge, offene Fragen, Entscheidungen | Filter nach Prozess/Evidenz, Suchfeld, echte Counts mit Quelle |
| /forum/local/create | Vorschlag, Geltungsbereich, Unsicherheit, Belege | Entwurf speichern; serverseitige Fehlermeldung, kein fingierter Erfolg |
| /forum/local/entry/{cid} | Aussage + Quellen + offener Dissens | versionierte Revision, kein edit-in-place |
| /forum/local/review/{cid} | Peer/Third nacheinander, Vorbefassung | Third bindet konkretes Peer-CID; fehlende Trennung sichtbar |
| /forum/local/epistemic | Statusachsen nebeneinander | Erklärung „angenommen ist nicht bewiesen“ |
| /forum/local/lineage/{cid} | Versions-/Eventverlauf | Graph und gleichwertige Listenansicht |
| /forum/local/provenance | Herkunft, Verfügbarkeit, Hashprüfung | Text „Quelle fehlt“; kein Abruf fremder URLs ohne Freigabe |
| /forum/local/audit | CA1–CA6, Gaps, Fixture-Coverage | Quelle vs eigener Run getrennt |
| /forum/local/portability | Trialdefinition und fehlende Voraussetzungen | SPECIFIED_NOT_EXECUTED; kein Startbutton ohne passenden Auftrag |
| /forum/local/receipts | exakte Exporte/Tests/Entscheidungen | Bytebasierter Download; Erfolg erst nach Fertigstellung |

MANUS-Elemente werden **neu formuliert**, nicht mit Debug-Collector, externen Fonts/Analytics oder Toast-Attrappen übernommen. Ein Quelle-zu-Entscheidung-Diagramm ist Beziehungsgrafik, keine quantitative Durchflussmessung ohne Daten. Keine persönlichen Avatare oder Angaben aus privaten Quellgesprächen veröffentlichen.

Accessibility-Ziel: WCAG 2.2 AA als Ziel, **kein Konformitätsclaim**. Tokenpalette in examples; alle zehn geprüften Text/Hintergrund-Kombinationen >=4,5:1. Renderer zusätzlich bei 320/390/1280 CSS px, 200/400 % Zoom, Keyboard-only, Reduced Motion, High Contrast und Screenreader testen. Fokus auf allen Controls sichtbar und nicht verdeckt. Menü/Modal: Escape, Fokusfang nur im Modal, Fokus zurück zum Auslöser. Datum mit Zeitzone; leere/fehlerhafte Ladevorgänge unterscheidbar.

## 7. R10-Migration ohne Verlust

1. Aktuellen R10-Pfad und Hashinventar erneut prüfen; der aktuelle Vergleich dieses Laufs umfasst nur die 24 im Auftrag enthaltenen Dateien.
2. R10-Tests/Build unverändert in separatem Arbeitsstand reproduzieren. Kein historisches 12/12 als aktuellen Pass ausgeben.
3. Bisherige Domainobjects/Routes über Adapter anbinden. Legacy `nexus-cas-v1` lesen, Originalbytes behalten.
4. Policy-defaults verschärfen: kein absent-review PASS, keine fehlenden Gates als false/unproblematisch interpretieren.
5. Persistenz hinter existierender API ergänzen, Daten in neue Datenbank importieren; Map-Storage nicht als dauerhafte Historie bezeichnen.
6. Bei Konvertierung explizite MigrationRecords, deterministic v2 golden corpus, Anzahl/Hash/parent/decision-Vergleich. Historisch fehlende Kausalität nicht nacherfinden.
7. UI-/Review-/Corpus-Projektionen ankoppeln. Unbekannte Metrik null, Demo getrennt.
8. Mistral-Entscheidungen und Negativfixture-Erweiterungen integrieren, lokale Abnahme; erst separat später etwaige Veröffentlichung.

Rollback: alter R10-Arbeitsstand und Snapshot bleiben lesbar; neue v2-Objekte nicht löschen oder in v1 zurückrechnen. Fehlgeschlagene Migration erzeugt Bericht, keinen automatisch korrigierten Ursprungsbeleg.

## 8. Umsetzungslose mit Definition of Done

| Los | Ergebnis | Abnahme | Gate |
|---|---|---|---|
| L0 Quellen-/Reviewabschluss | G01/G02/G03 klären, Mistral-Gegenposition binden | versionierter Dissens-/Entscheidungsreturn | abhängige Integration wartet auf G04 |
| L1 Domainverträge | restliche Objektschemas + R10-Adapter | unknown-field, source-gap, stale-review, Golden-CAS Tests | L0 soweit betroffen |
| L2 Persistenz | transactional service, projection rebuild, migration | race, crash injection, restore, data lineage | L1 |
| L3 Auth/Governance | Sitzungen, CSRF, scopes, revocation, STOP | impostor/expired/revoked/forged-gate tests | L1/L2 |
| L4 UI/Interaction | zehn Routen, alltagstaugliche Texte, echte Exporte | browser, keyboard, screenreader, contrast; kein Demo-Leak | L2/L3 |
| L5 Corpus/Trials | CA-Gap-Modell, Runbindung, Trial-Vorbereitung | vollständige Inputs statt Narrativrekonstruktion | kein Trial ohne konkrete Voraussetzungen |
| L6 Release Candidate | lokale Build-/Test-/Returnlieferung | manifest rehash, Open-Gap-Liste, Reviewergebnis | keine Live-Publikation in diesem Auftrag |

Cursor implementiert; Mistral/Vibe reviewt mit Vorbefassungshinweis; menschlicher Autor entscheidet; AXIOM synthetisiert Befunde. Diese Rollenzuweisung ist ein Übergabevertrag, **keine Behauptung eines bereits gesendeten oder laufenden Fremdauftrags**.
