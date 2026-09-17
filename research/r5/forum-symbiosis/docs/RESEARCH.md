# Primärquellenabgleich — 2026-09-17

Die folgenden Quellen wurden für diese Synthese direkt aufgerufen. Sie belegen technische Konzepte, nicht die Gültigkeit von NEXUS. Keine aktuellen Versions-/Wartungsbehauptungen aus den Vorlagen ungeprüft übernommen.

| Quelle | Nachgelesener Punkt | Eigene Konsequenz |
|---|---|---|
| [IPFS: Content addressing](https://docs.ipfs.tech/concepts/content-addressing/) | CID trägt Format-/Hashinformationen; Datei-Hash und IPFS-Adressierung sind zu unterscheiden | Neuer lokaler Profilname; IPFS-Mapping später separat mit fixierter Codierung testen |
| [IPFS: Pin files](https://docs.ipfs.tech/how-to/pin-files/) | Aufbewahrung muss aktiv organisiert werden | Hashidentität ist kein Backup- oder Verfügbarkeitsbeleg |
| [RFC 8785](https://www.rfc-editor.org/rfc/rfc8785) | Kanonische JSON-Bytes benötigen präzise Regeln | Hier bewusst eingeschränktes eigenes Profil, **kein** unbelegter JCS-Kompatibilitätsclaim |
| [SQLite transactions](https://www.sqlite.org/lang_transaction.html) | Schreibtransaktionen und Konkurrenzkonflikte müssen behandelt werden | BEGIN IMMEDIATE, eindeutige IDs, atomarer CAS-/Event-Write; stale-head und Wiederholungsfälle testen |
| [W3C PROV overview](https://www.w3.org/TR/prov-overview/) | Herkunft lässt sich über Entitäten, Aktivitäten und beteiligte Akteure strukturieren | Eintrag/Review/Run getrennt; agent_id ist Herkunftsangabe, nicht Wahrheitsgewicht |
| [WCAG 2.2 contrast](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html) | Normaltext mindestens 4,5:1, Großtext 3:1; nicht auf Schwelle aufrunden | Tokenpaare numerisch prüfen; tatsächliche UI zusätzlich messen |
| [WCAG reflow](https://www.w3.org/WAI/WCAG22/Understanding/reflow.html) | Inhalte müssen bei schmalem Darstellungsbereich sinnvoll umbrechen | 320 CSS px, keine horizontale Pflichtnavigation; Tabelle alternativ linear anzeigen |
| [WCAG focus visible](https://www.w3.org/WAI/WCAG22/Understanding/focus-visible.html) | Tastaturfokus muss sichtbar bleiben | Echte Controls, sichtbarer Fokus und Rückgabe nach Dialogen |

Die Auswahl eines lokalen SQLite-Kerns, die konkrete HOLD-Regel und die Review-Gates sind **eigene Architekturentscheidungen**. Diese Quellen bestätigen weder „trinäre Überlegenheit“ noch wissenschaftliche Kontinuität oder institutionelle Anerkennung.

Weitere in Vorlagen genannte OSS-Projekte sind Discovery-Hinweise, nicht geprüfte Abhängigkeiten. Kein Code, kein Token-Layer und kein fremdes Telemetriesystem wird daraus übernommen. Bibliotheksauswahl, Version-Pinning und Lizenzprüfung gehören zum späteren Integrationslauf.
