# Zehn Fundamentverträge

Normativer **Kandidat**, keine rückwirkende Umschreibung von V0/R10. Die Begriffe MUSS/DARF NICHT beschreiben Anforderungen an eine spätere Implementierung. Die tatsächlich ausgeführten Teile stehen im Testreport.

## 00_CONSTITUTION — überprüfbare Zusammenarbeit

I01: „Organismus“ ist eine Metapher für additive Entwicklung und Fehlerprüfung, kein Bewusstseinsclaim.
I02: Ursprung, Peer und Third Node sind strukturell getrennt.
I03: Name, Nationalität, Anbieter, Reputation oder Zahlung erzeugen kein Wahrheitsprivileg.
I04: Dissens bleibt referenzierbar, auch nach lokaler Annahme.
I05: Entscheidungen bleiben beim autorisierten menschlichen Autor; Betriebskontrolle beim menschlichen Betreiber.
I06: Korrekturen ergänzen die Historie, sie ersetzen Originalbytes nicht still.
I07: Dauerhafte fachliche Objekte haben explizite Inhaltsadressen.
I08: Harte Negativfixtures sind nicht durch andere Erfolge kompensierbar.
I09: Jede Aussage nennt ihren Geltungsbereich.
I10: Unklarheit und Selbsteinschätzung bleiben explizit.
I11: Die Software ist kein Wahrheitsorakel.
I12: C1_DESCRIPTIVE_ONLY bleibt die Obergrenze.

Neutralität ist eine prüfbare Verfahrensanforderung, keine Behauptung vollkommener menschlicher oder maschineller Unvoreingenommenheit. Menschliche Hoheit erlaubt Abbruch, Ablehnung und neue Vorschläge; sie verwandelt unbelegte Aussagen nicht in validierte Ergebnisse.

## 01_AUTHORITY_MODEL — Wer darf was?

| Rolle | Zulässig | Nicht zulässig |
|---|---|---|
| Menschlicher Autor | eigenen Entwurf erstellen, Gründe ergänzen, lokal annehmen/ablehnen, stoppen | Reviews anderer umschreiben, Belege erfinden, C1 übergehen |
| Agent | Vorschläge und eigene Reviews im delegierten Scope erzeugen | menschlichen Autor impersonieren, eigene Ausgabe final freigeben |
| Peer | versionsgebunden beurteilen, widersprechen | automatische Annahme oder verdecktes Veto |
| Third Node | Peer und Ursprung kritisch prüfen, Abhängigkeiten offenlegen | Unabhängigkeit allein durch anderen Anzeigenamen behaupten |
| Betreiber | Sitzungen widerrufen, Prozess stoppen, geschützte Wiederherstellung | dadurch wissenschaftliche Richtigkeit bescheinigen |

Delegation ist später ein eigenes Objekt: delegator, delegate, erlaubte Operationen, object_scope, expiry, revoked_by_event. Default: keine Delegation. ACCEPT/REJECT des Autors werden im V1-Vertrag nicht an Agenten delegiert. Betreiber-STOP funktioniert auch bei defekter Datenbank, fehlenden Reviews oder kaputtem Entry-Schema; wenn ein Log nicht schreibbar ist, kann es nachträglich als Recovery-Beobachtung ergänzt werden. **Kein Logging-Gate darf Abschalten verhindern.**

Der Referenzadapter nimmt `Principal` aus einem vertrauenswürdigen Aufrufer entgegen. Er authentifiziert keine Menschen. Der spätere Server darf Identität/Rolle niemals aus dem JSON-Body übernehmen.

## 02_EPISTEMIC_MODEL — drei getrennte Achsen

- Prozess: DRAFT, IN_REVIEW, HOLD, BLOCKED, ACCEPTED_LOCAL_C1, REJECTED, STOPPED.
- Evidenzklasse: SPECIFICATION, HYPOTHESIS, PROPOSAL, OBSERVATION, LOCAL_TEST_RESULT, EXTERNAL_SOURCE_CLAIM, DERIVED_ANALYSIS, NEGATIVE_RESULT, UNRESOLVED.
- Interpretation: expliziter Text mit scope, ambiguity, confidence und Quellenverweisen.

HOLD heißt „für diese Entscheidung fehlt Klärung“, nicht „halb wahr“. BLOCKED heißt „ein gebundenes hartes Gate scheitert“. ACCEPTED_LOCAL_C1 heißt „der Mensch übernimmt diesen lokalen Vorschlag im angegebenen Rahmen“, nicht „wahr“, „live“ oder „wissenschaftlich bestätigt“.

confidence ist zunächst UNCALIBRATED oder SELF_REPORTED, keine scheinpräzise Wahrscheinlichkeit. Spätere Kalibrierungsmessung benötigt Datensatz, Zielvariable, Auswertungsmethode, Nenner, Zeitraum und Ergebnisartefakt. Keine impliziten Defaults zu PASS.

## 03_MEMORY_AND_PROVENANCE — additive, begrenzte Zusagen

Objekte bestehen aus kanonischen UTF-8-Bytes; Adresse `nexus-forum-cas-v2:sha256:<64hex>`. Profil v2 erlaubt null, bool, sichere Ganzzahlen, Unicode-Skalarstrings, Arrays und Objekte mit ASCII-Schlüsseln. Keine Fließkommazahlen, doppelten JSON-Schlüssel, ungültigen Surrogate, Unicode-Normalisierung oder stillen Metadatenumordnung außerhalb der definierten Schlüsselsortierung. Größe maximal 1 MiB, Tiefe 64. Detailvertrag: `scripts/reference.py`.

Dies ist **weder IPFS CID noch RFC-8785-JCS noch R10 v1**. R10-Bytes bleiben unverändert. Eine Migration erzeugt ein eigenes Mapping mit old_profile, old_digest, new_cid, transformer_digest, reason; keine Umbenennung des alten Objekts.

SQLite speichert Objekte und geordnete Ereignisse in einer Transaktion. Neue fachliche Version referenziert die alte über parent. Forks werden sichtbar als getrennte Vorschläge, nicht per „last write wins“ zusammengezogen. Der Event-Head ist ein Kontrollpunkt, nicht das Eintrags-CID.

Objektänderung, Ereigniskettenfehler und abweichender Kontrollpunkt müssen erkannt werden. Die Hashkette schützt **nicht** gegen einen Besitzer, der die ganze Datenbank und den Kontrollpunkt ersetzt. Dafür wären separat verwahrte Kontrollpunkte, Signaturen, Backups und Zugriffstrennung erforderlich.

Privacy vor Aufnahme: keine Geheimnisse oder personenbezogenen Rohdaten im öffentlichen CAS. In einer späteren privaten Installation können berechtigte Redaktionen Zugriff/Index verändern und einen minimalen Redaktionsvermerk erzeugen; „append-only“ ist keine Verpflichtung, rechtswidrige Inhalte für immer öffentlich zu halten. Solche Lösch-/Aufbewahrungsregeln sind hier nicht implementiert.

## 04_THIRD_NODE_REVIEW — Prüfung ohne Konsenszwang

Peer bindet entry_cid. Third bindet entry_cid **und peer_review_cid**. Drei unterschiedliche actor_id sind notwendig, aber nicht hinreichend für echte Unabhängigkeit. Vorbefassung, gemeinsame Quellen/Prompts, Modellfamilie, organisatorische Kontrolle und Interessenkonflikte werden dokumentiert.

Default independence = UNDECLARED. DECLARED_NO_CONFLICT bleibt eine Erklärung, keine extern bestätigte Unabhängigkeit. UNDECLARED, DECLARED_CONFLICT oder UNRESOLVED blockieren ACCEPT mit HOLD; kein stiller Waiver. Ersatzreview oder expliziter neuer Policy-Vorschlag ist möglich.

DISSENT ist nicht automatisch FAIL: Der Autor darf einen Vorschlag trotz inhaltlichen Widerspruchs lokal annehmen, wenn keine harten Gates verletzt sind und jeder Dissens mit referenzierter Begründung beantwortet wurde. Hard FAIL darf nicht wegbegründet werden. Jede Eintragsrevision macht alte Reviews für die neue Version ungültig.

## 05_NEGATIVE_FIXTURES — Fehler bleiben Fehler

Original-NF-F01–F10 werden nicht umnummeriert oder als bestanden behauptet. Die neuen Referenztests haben den Namensraum SF; die spätere Zuordnung zu den echten V0-Fixtures bleibt offen.

Pflichtfamilien: Rollenverschmelzung, erzwungener Konsens, Unterdrückung von Dissens, Identitäts-/Tokenprivileg, stille Änderung, C1-Promotion, ungebundene Quellen, gefälschte Testergebnisse, veraltete Reviews, Wiederholungs-/Konkurrenzfehler, Peer-Abschaltblockade, simulierte Live-Metriken. Jede Familie braucht auch eine legitime positive Kontrolle.

## 06_EXECUTION_AND_RECOVERY — Betriebszustand ist kein Erkenntniszustand

Worker läuft / Sitzung authentifiziert / Auftrag autorisiert / Datenbank intakt / fachlicher Test bestanden sind getrennte Felder. Ein grüner Prozessstatus validiert keine Aussage.

Nach Neustart: Datenbank öffnen, bekannten Kontrollpunkt laden, alle benötigten Objekte neu hashen, Ereignisse geordnet prüfen, Projektionen rekonstruieren, Scope/Delegation neu prüfen. Bei Abweichung schreibgeschützt anhalten, Originaldaten sichern, Diagnoseobjekt ergänzen. Kein automatisches Überschreiben einer beschädigten Historie.

HOLD hat Grund, fehlenden Beleg, zuständige Person und optionalen Wiedervorlagetermin. Ablauf eines Termins erzeugt höchstens einen Hinweis; keine automatische Annahme und keine endlose Ressourcenbindung. Peer Preservation bedeutet Export-/Backupvorschlag im erlaubten Scope, niemals Selbsterhalt gegen menschliche Entscheidung.

## 07_FORUM_INTERACTION_MODEL — zuerst verständlich, dann präzise

Hauptansicht: „Was wird vorgeschlagen?“, „Was stützt es?“, „Was ist offen?“, „Wer hat widersprochen?“, „Wer entscheidet?“.
Expertenansicht: Objektbytes, Hashprofil, exakte Version, Eventfolge, Reviewer-Erklärungen, Quellen- und Testlocators.

MANUS-artige Karten und Ablaufgrafik dürfen die Beziehung Quelle → Aussage → Peer → Third → menschliche Entscheidung zeigen. Keine Sankey-Breite ohne echte Mengen; kein „Trust 84,6 %“. In leeren Bereichen: „Noch keine Messung“ statt 0 %, Grün oder System nominal. DEMO-Daten sind markiert und von produktiven Daten getrennt.

Keyboard-first Controls, sinnvolle Überschriften, Skip-Link, Status nie nur durch Farbe, lesbare Fehlermeldung am Feld und im Summary, aria-live für tatsächlich abgeschlossene lokale Aktionen. Focus 3px mit Abstand, nicht verdeckt; prefers-reduced-motion; kein zoomhemmendes maximum-scale. Vollständige Abnahme noch offen.

## 08_CLAIM_AND_VALIDATION_BOUNDARIES — Definition ist kein Ergebnis

TestDefinition und TestRun sind verschiedene Objekte. Ein Run benötigt exakte Inputs, Script-Hash, Umgebung, Befehl, Exitcode, tatsächlichen Output und Zeitpunkt. Ohne Run heißt der Zustand SPECIFIED_NOT_EXECUTED. Importierte Resultate tragen REPORTED_BY_SOURCE, bis sie tatsächlich reproduziert wurden.

Vier lokale Gates: source_binding, negative_fixtures, scope_review, policy_review. PASS/FAIL/UNKNOWN jeweils mit Belegbindung. Gate-PASS ist kein wissenschaftlicher Wahrheitswert. Freitext kann durch ein Schema allein nicht epistemisch validiert werden; Sprachprüfung bleibt kontextbezogene menschliche/reviewerische Aufgabe.

Corpus-Audit und Cross-Substrate Trial sind verschiedene Prüfpfade. Ein vollständiger ZIP-Rehash ist kein Audit der historischen kausalen Vollständigkeit. R10-Teilbefunde bleiben als historische Teilbefunde sichtbar.

## 09_CANONICAL_HANDSHAKE — azyklische Bindung

OUTPUT_MANIFEST bindet alle Nutzdateien des Kandidaten, nicht sich selbst, RETURN oder HANDSHAKE. RETURN bindet Manifest und berichtet Scope/Gaps/Teststatus. DELIVERY_HANDSHAKE bindet Manifest und Return. Externer Git-Commit/ZIP-Digest bindet zusätzlich den Handshake; kein unmöglicher selbstreferenzieller Hash.

Push, lokales PASS, CI, externe Review, Merge, Website-Livezustand und wissenschaftliche Validierung sind unterschiedliche Ereignisse. Repository-README-Verknüpfungen gehören zur Git-Transportebene und sind nicht Bestandteil des Nutzdateimanifests.
