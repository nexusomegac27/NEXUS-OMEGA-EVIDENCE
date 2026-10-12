# NEXUS OMEGA · AXIOM R18 Clean-Room-Provenance · Quellenexakte Intake-Adjudikation R0

```text
OBJECT = NEXUS_OMEGA_AXIOM_R18_CLEAN_ROOM_PROVENANCE_SOURCE_EXACT_INTAKE_ADJUDICATION_20261012_R0
STATE = PASS_WITH_MAJOR_CAVEATS_C1_RESEARCH_INTAKE_AND_OFFLINE_REPRODUCTION
OPERATOR_MODULE = R18_NEXUS_OMEGA_AXIOM_CLEAN_ROOM_PROVENANCE
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
RESEARCH_CHAIN = R30_AXIOM_QWEN_ORDER -> QWEN_A_B_C -> CRSF_V1 -> R31
R18_MODULE_FILESYSTEM_INSPECTED = NO
R18_MODULE_TERMINAL = NOT_ESTABLISHED
EXTERNAL_GITHUB_WRITE = NO
LIVE_DEPLOY = NO
NODE_RESET = NO
NEXT = CURSOR_R18_READ_ONLY_SOURCE_BIND_AND_INDEPENDENT_TECHNICAL_PROTOTYPES
```

## 1. Auftrag und Beweisstand

Der Operator bezeichnet den lokalen Windows-Pfad unter `NEXUS_MASTER_CHIEF_MODUL/R18_NEXUS_OMEGA_AXIOM_CLEAN_ROOM_PROVENANCE` und liefert sechs Dateien. Der Windows-Ordner selbst wurde nicht physisch gelesen; der Remote-Desktop-Connector meldete kein angeschlossenes Gerät. Die Bezeichnung R18 ist daher Operator-Modulzuordnung, **keine** unabhängig belegte Implementierungs- oder Abschlussbehauptung.

Sechs neue Originaldateien wurden im aktuellen Container SHA-256-geprüft und unverändert in `source_originals/` übernommen. Die R31-ZIP-CRC-Prüfung bestand; 11 von 11 manifestierten Dateien stimmen in Bytes, SHA-256 und Git-Blob-SHA1. Der ZIP-Eintrag `SHA256_MANIFEST.json` ist korrekt nicht selbst Teil seiner Kindliste; das zweite ungeführte ZIP-Element ist das Verzeichnis `fixtures/`. Der externe ZIP-Umschlag hat einen eigenen Hash und ist **keine** digitale Signatur.

Originalidentität: `R30_Axiom_QWEN_Order.txt` 7.552 B / SHA `2379c3fd796aa73c9a811bdb379764c9b2d00a0b8b62a63feb694fe97d3ed4be`; `QWEN_A_B_C_Return.txt` 44.686 B / SHA `a292eed579237c96a342dbd6bbb520fa87d1efeee68734a1e38580e44e493107`; `QWEN_A_B_C_19pages.pdf` 115.988 B / SHA `0b4f62e3f3c1b73431d014d3bf2ae7a39f98060f2e3a37c9da76c25d528a2677`; `CRSF_V1.md` 26.459 B / SHA `b64e26c945b5ee7889b33fd3d0517700e94a3c4e0ac75f8924661be39e8beb40`; `Symbiotic_R31.md` 26.774 B / SHA `63efd6746189e291a362bd36e50faa907fbce7c2ea06478185ba021818eb0d46`; R31-ZIP 41.492 B / SHA `e64691d785dd331d4490983f268763a53aef87c8054377e49c6366e9dce0d30d`.

Das ältere CRSF-V1-`DRAFT_C1`-Anchor-JSON wird mit **4.707 Bytes** und SHA `2a20d7fabd3d59115dcee9ef2266a319d5880dca8c1a77de984d2668ca9bd5aa` behauptet; es liegt **nicht** unter den sechs Originaluploads und ist nicht im R31-ZIP. Es darf nicht durch den 5.869-Byte-R31-Nachfolger-Anchor substituiert werden. Status bleibt `SOURCE_GAP`.

## 2. Reproduktion (unabhängig vom Producer-Receipt)

- Originale R31-Software in einer **separaten Kopie** ausgeführt, einzig der feste alte Perplexity-Dateipfad wurde auf die unveränderten mitgelieferten Inputbytes in einem isolierten Prüfverzeichnis gebunden. Der wissenschaftliche Hash-/Validator-Code ist sonst unverändert. Prozessabschluss `exit=0`.
- 7/7 FIPS/RFC-Hash-Selbsttests bestanden; 4-Objekt-Handshake: 3 MATCH, 1 HOLD_SOURCE_GAP, kein MISMATCH.
- 3/3 positiven Schemafälle `PASS_0_ERRORS` und 6/6 One-Defect-Fälle F1–F6 vom JSON-Schema, dem eigenen Validator und dem Repo-Validator korrekt verworfen.
- F7 ist **reproduziert**: Schema akzeptiert `continuity.anchor_id != object`; semantischer Repo-Validator weist denselben Payload mit `INVALID_ANCHOR_ID` zurück. Dies ist eine **Cross-Field-Contract-Lücke** im Schema, kein erfolgreicher Angriff auf den kombinierten Validator.
- Die Normreferenz (`schema`, `validator`, Norm-Dokument) wurde aus dem älteren physischen `NEXUS_OMEGA_TASK_ANCHOR_NORM_V1_20261011_PACKAGE.zip` read-only extrahiert; Schema 6.591 Bytes SHA `077098b4...98dc2e` / Git-Blob `3c44450c...`, Validator 11.466 Bytes SHA `2c9432fb...79d82` / Git-Blob `2215790b...`. Dieselben Git-Blob-Werte wurden separat über den verbundenen GitHub-Connector an Main `5721f2128db0f147c3a657b88250c66972cc5e04` zurückgelesen.
- Der GitHub-Registerstand `docs/architecture/REPOSITORY_STRUCTURE.json` wurde an diesem historischen Commit als Version `1.7.4`, die `external_actor_allowlist` als **leer** gelesen. Formatvalidierung ist keine Identitäts-/Actor-Freigabe.

Die Originaldateien `VONCOD~1.PDF` und `HERMET~1.TXT` sind getrennte Medienobjekte mit textueller Inhaltsüberschneidung, **keine** binärgleichen Quellen. Das PDF besitzt 19 Seiten; auf Seite 4 führt seine Tabelle die fünf Build-Hermetizitätsmaßnahmen Lockfiles, Vendoring, Sandbox, Image-Digests und `SOURCE_DATE_EPOCH` auf. Seite 7 listet Cleanroom-Box-Structures, TLA+, Proofs, symbolische Ausführung und Property-Based Testing; Seite 11 behandelt DSSE/in-toto/SLSA/Sigstore, Seite 14 die A/B/C-Synergiematrix. Dieser Inhalt ist für R18 als **Research Seed** geeignet.

## 3. Wissenschaftliche Architekturentscheidung: R18-A/B/C

**A — Build-Reproduzierbarkeit / Hermetizität.** Deklarative Inputs, pinbare Toolchains, Zeit-/Locale-/Randomness-Steuerung, Container-Digests, reproduzierbare externe Gegenbuilds. Kein absoluter Determinismus allein aus `SOURCE_DATE_EPOCH`, Nix, Bazel oder einem SHA. Nachweisziel ist ein zweiter unter kontrollierten Bedingungen ausgeführter Build mit übereinstimmendem Output-Digest, inklusive dokumentierter Gegenfälle.

**B — Clean-Room-Verhalten / formale Verträge.** Trenne (i) Mills-Cleanroom für Defektvermeidung und Black-/State-/Clear-Box-Spezifikation von (ii) *unabhängiger, urheberrechtlich sauberer Verhaltens-Reimplementierung*. Beide sind verwandte, aber nicht identische Konzepte. Fasse Contract/StateMachine/Oracle unabhängig von Implementierungsbytes. Teste Roundtrip, Differential-, Metamorphic- und Negativfälle; formale Modellprüfung nur für **explizit modellierte** Zustandsräume. Blackbox-Test-PASS ist kein universeller Korrektheitsbeweis und keine automatische Rechtsfreigabe.

**C — Provenienz und Authentizität.** SHA belegt Byteidentität, keine Wahrheit oder Urheberschaft. DSSE signiert definierte Bytes mit domain-separiertem PAE; in-toto enthält Statements und Subjects; SLSA Build Provenance dokumentiert Inputs, Builder und Prozess; Sigstore/Fulcio/Rekor unterstützen prüfbare Identitäts-/Transparenzpfade. Authentizität setzt überprüfte Principalbindung, Trust-Root, Scopes, Schlüssel-/OIDC-Vertrauen, Logbeweise, Widerrufs-/Zeitfensterbehandlung und ggf. Datenschutz voraus. Aus einem lokalen Manifest folgt **weder** signierte SLSA-Provenienz **noch** ein verifizierter Release.

**D — R16/R17-Einordnung.** R18 ergänzt den R16-Memory-/Selbstmodifikationsfokus durch die kontrollierbare Lieferkette `Specification → Source → Build → Artifact → Attestation → Independent Evaluator → Push Proposal`. Auch bei unverändertem Vertrags-Hash kann die Implementierung variieren; die *Implementation-Hashes* müssen dann ausdrücklich verschieden sein. R17 ist aus früherem AXIOM-Intake noch nicht unabhängig source-exact terminal, und R18 macht R17 nicht rückwirkend terminal.

## 4. Präzise R31-/CRSF-Nachfolger-Korrekturen

1. **I-16 als harter Befund:** JSON-Schema und semantischer Repo-Validator sind gemeinsam erforderlich; `anchor_id==object` ist im vorliegenden Schema nicht erzwungen. R31 R0 korrekt als unabhängiger, nichtdestruktiver Nachfolger; DRAFT_C1-Fehler nur hypothetisch, da dessen Bytes fehlen.
2. **I-17 Kyverno nach Primärquelle:** Klassische Kyverno-`ClusterPolicy` „Verify SLSA Provenance (Keyless)“ nutzt `predicateType=https://slsa.dev/provenance/v0.2` und `validationFailureAction: Audit`; neuere `ImageValidatingPolicy` verwendet `Deny`, erwartet im veröffentlichten Beispiel jedoch auch `v0.2`. Daher kein abgeleiteter v1.x-PASS. Quellen: https://kyverno.io/policies/other/verify-image-slsa/verify-image-slsa/ und https://kyverno.io/policies/other-ivpol/verify-image-slsa/verify-image-slsa/.
3. **SLSA-Version:** Offizielle veröffentlichte Spezifikation v1.2; für Build Provenance weiterhin Predicate `https://slsa.dev/provenance/v1`. Quelle: https://slsa.dev/spec/v1.2/.
4. **Nicht überdehnen:** „Code besitzt keinen Wert mehr“, „unbestechliche kryptografische Wahrheit“, „SHA-256-Provenienz beweist autonome Korrektheit“ sind philosophische/werbliche Thesen, nicht vorliegende empirische Schlussfolgerungen. Code, Lizenzen, Auditierbarkeit, Wartung und Implementierungsqualität bleiben wertrelevant.
5. **I-13 Transport präzisieren:** `OPERATOR_TO_AXIOM_BRIDGE` ist ein zulässiger Intake-Transport, **nicht** GitHub-Deposit. Der spätere GitHub-Owner-Write mit Readback/Manifest ist eine eigene kanonische Publication-/Push-Stufe. Der CRSF-V1-Anspruch „ausschließlich GitHub-API-Handshake“ ist für reine Intake-Rückgabe zu eng gegenüber dem verifizierten `TASK_ANCHOR_NORM_V1`-Vertrag.
6. **I-08/I-09 Scope:** Signierte SLSA-Build-Attestations sind ein zukünftiges Software-Lieferkettenziel; nicht jeder Forschungs-Input, Text oder unfertige Hypothesen-Return darf deshalb automatisch als ungültig gelten. Öffentliche Transparenzlogs dürfen keine personenbezogenen Daten oder Secrets enthalten.
7. **Autoritätsgrenze:** Der R31-Anchor hat `write_slot=NOT_ALLOCATED`, `runtime_authorized=false`, `node_reset_authorized=false`, `claim_promotion_authorized=false`; diese Werte sind lokal maschinengeprüft. Sie erteilen selbst keine Berechtigung und ersetzen keine extern verifizierte Signatur.

## 5. R18-Exit-Gates für Cursor/PRAXIS (separat zu autorisieren)

- **G0 Exact Intake:** Windows-R18-Ordner read-only inventarisieren; Quellzuordnung zu den sechs physischen Anhängen separat bestätigen; fehlende Originale nicht rekonstruieren.
- **G1 Contract:** Black-/State-Box/FSM-Definition einer minimalen Mini-Node und ≥8 adversarielle, logisch eigenständige Fixtures; F7 muss als Schema/Semantik-Divergenz erhalten bleiben.
- **G2 Hermeticity:** Zwei unabhängige isolierte Builds aus demselben gepinnten Inputstand; Byte-Digest-Vergleich plus zumindest ein absichtlich mutierter nichtdeklarierter Input (Soll: fail-closed oder expliziter Nichtdeterminismusbefund).
- **G3 Attestation:** DSSE/in-toto-Testbeispiel mit bewusst isoliertem Testschlüssel, signiertem Subject-Digest und überprüften Negativfällen (falscher Principal, anderes Subject, abgelaufener Scope, modifizierter Payload). Keine Selbst-Freigabe.
- **G4 Version/Admission:** SLSA-v1.x-`predicateType` und Feldpfade (`runDetails.builder.id`) gegen exakt eingesetztes Policy-Gate testen; `Audit != Deny` explizit.
- **G5 Independence:** Evaluator-Code/Fixtures vor Kandidat eingefroren; Hash/Commit des Evaluators außerhalb Kandidatenkontrolle; Rückgabe der vollständigen Ausführungslogs.
- **G6 Provenance Privacy:** Rechte/Lizenzen und personenbezogene Provenienzdaten geprüft; Original-Gaps bleiben scoped HOLD.
- **G7 Receipt:** Vollständige Child-Bytes, Detached-SHA256-Manifest, Push-Proposal getrennt vom C1-Forschungsresultat. `AXIOM_ACK` erst nach unabhängiger Gegenseitenprüfung.

**Freie Forschung** zu Alternativbuildsystemen, Rust, WASM, TLA+, Alloy, formalem Proof, DSSE/Sigstore und Cleanroom-Reimplementierung ist erwünscht. Keine der genannten Werkzeuge ist zwingend; maßgeblich ist der reproduzierbare Beleg. Keine zusätzlichen künstlichen Gate-Schleifen für isolierte Forschung.

## 6. R18-Kanon-Status und Transfergrenze

```text
OBJECT = NEXUS_OMEGA_AXIOM_R18_CLEAN_ROOM_PROVENANCE_SOURCE_EXACT_INTAKE_ADJUDICATION_20261012_R0
STATE = PASS_WITH_MAJOR_CAVEATS_C1_RESEARCH_INTAKE_AND_OFFLINE_REPRODUCTION
UPLOADED_ORIGINAL_FILES = 6_PHYSICALLY_HASHED
R31_ARCHIVE = ZIP_CRC_PASS
R31_MANIFEST = 11_OF_11_BYTES_SHA256_GITBLOB_MATCH
R31_PORTABLE_REPLAY_EXIT = 0
R31_CRYPTO_SELFTESTS = 7_OF_7_PASS
R31_SCHEMA_POSITIVES = 3_OF_3_PASS
R31_NEGATIVE_FIXTURES = F1_TO_F6_6_OF_6_REJECT
R31_F7_CROSSFIELD_DIVERGENCE = REPRODUCED
CRSF_DRAFT_C1_4707_BYTES = SOURCE_GAP
QWEN_PDF = PHYSICAL_115988_BYTES_19_PAGES
R18_LOCAL_MODULE_FILES = NOT_INSPECTED
HERMETIC_BUILD = NOT_EXECUTED
SLSA_SIGNING = NOT_EXECUTED
KYVERNO_ADMISSION = NOT_EXECUTED
GITHUB_R18_PUSH = NO
CLAIM_PROMOTION = NO
NODE_RESET = NO
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
NEXT = R18_READ_ONLY_CURSOR_BIND_AND_SCOPED_OFFLINE_PROTOTYPE_RETURN
```

**Empfangsregel:** Dieser Beleg ist die unabhängig geprüfte AXIOM-Auswertung der **hier gelieferten** Bytes. Er ersetzt weder R30/R31-Originale noch eine fehlende R18-Windows-Verzeichnisinventur. Alle Befunde bleiben append-only.
