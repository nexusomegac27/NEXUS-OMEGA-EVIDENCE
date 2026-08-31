# AXIOM Research Handoff — M50GRN Artefaktprüfung

**Datum:** 2026-08-31  
**Ersteller:** Manus AI  
**Zielrolle:** AXIOM  
**Claim Ceiling:** `C1`  
**Claim Promotion:** `false`  
**Publication Status:** `PENDING_OPERATOR_CONFIRMATION`

## 1. Gegenstand und Prüfgrenze

Gegenstand dieser Prüfung ist ausschließlich das vom Operator angehängte äußere Archiv `M50GRN~1.ZIP`. Es wurde zuerst physisch gebunden, danach passiv entpackt und anschließend in einer getrennten Build-Kopie statisch und technisch geprüft. Enthaltene Programme wurden nicht aus dem Originalarchiv heraus ausgeführt. Die im Archiv enthaltene Datei `attachments/NEXUS_~1.ZIP` wurde als inneres Quellpaket separat behandelt.

Die kanonische fachliche Grundlage ist der im Artefakt enthaltene und bytegenau verifizierte NEXUS-OMEGA-Live-Stand `NEXUS-OMEGA-FRAMEWORK-LIVE-20260831-R0` sowie die darin referenzierte R2-Forschungsbasis. Diese Grundlage wird nicht durch die vorliegende Prüfung rückwirkend verändert oder wissenschaftlich aufgewertet.

## 2. Physische Identität und zentrale Feststellung

Das äußere Operator-Archiv besitzt **2.598.531 Bytes** und SHA-256 `51ae10b55d1f6cfa7f4ed4aa85ecf4dc3d1e451ee31a7ecc50d48c30febd5487`. Die im eingebetteten `SOURCE-MANIFEST.json` deklarierte Paketbindung bezeichnet dagegen das innere `attachments/NEXUS_~1.ZIP` mit **212.788 Bytes** und SHA-256 `c8ad4fa891580c5983a88caf807bddefb1c77616e298c3c15fb70bb38fbd4864`. Das innere Paket stimmt mit seiner Deklaration überein; das äußere Paket ist ein anderes Objekt.

Damit liegt kein Beweis vor, dass das Manifest die äußere Operator-Lieferung bindet. Es liegt vielmehr eine nachvollziehbare **zweistufige Paketstruktur** vor: äußeres Zustellpaket und inneres NEXUS-Quellpaket. Diese Unterscheidung ist material und wird als `FAIL_MAJOR` für eine einstufige Package-Identity-Behauptung klassifiziert. Sie ist kein Grund, die 16 korrekt gebundenen Evidence-Dateien oder den inneren Quellstand zu verwerfen.

| Objekt | Bytes | SHA-256 | Status |
|---|---:|---|---|
| Äußeres Operator-Archiv `M50GRN~1.ZIP` | 2.598.531 | `51ae10b55d1f6cfa7f4ed4aa85ecf4dc3d1e451ee31a7ecc50d48c30febd5487` | physisch gebunden, nicht im eingebetteten Package-Feld referenziert |
| Inneres `attachments/NEXUS_~1.ZIP` | 212.788 | `c8ad4fa891580c5983a88caf807bddefb1c77616e298c3c15fb70bb38fbd4864` | `MATCH` zur Manifest-Deklaration |
| `public/evidence/SOURCE-MANIFEST.json` | 4.549 | `23fd323a0b24668b59e8e8561a58d5b6872f06453a21257a3b8b940c5d6e8bf8` | physisch vorhanden; Selbstbindung nicht unabhängig berechnet |
| Eingebettete Evidence-Bindings | 16 Dateien | jeweils `MATCH` | byte- und SHA-256-genau |

## 3. Technische Validierung

Die vorhandene JavaScript-Suite enthält 195 Tests. In einer isolierten Build-Kopie bestanden **187 Tests**, während **8 Tests** im Grok-PWA-Branding-Pfad scheiterten. Die Fehler betreffen Erwartungen an injizierte `og:title`-, `og:image`-, Head- und Streaming-Branding-Werte; sie zeigen eine Inkonsistenz zwischen Testannahmen und dem aktuell gebauten NEXUS-OMEGA-Branding, nicht automatisch einen Fehler der NEXUS-Evidenzschicht. `tsc --noEmit` bestand. ESLint scheiterte an einem `no-empty`-Fehler in `src/lib/app-data/client.server.ts:214:13`; zusätzlich wurde eine ungenutzte Disable-Direktive in `src/lib/auth/use-current-user.ts:59:3` gemeldet.

Die Installation mit `npm ci` war auf dem Originalstand nicht reproduzierbar, weil `package.json` und `package-lock.json` nicht synchron sind. Eine separate Build-Kopie wurde mit `npm install --ignore-scripts` hergestellt; das Originalartefakt blieb unverändert. Diese Reparatur ist nur eine Prüfmaßnahme und kein kanonischer Lockfile-Fix.

Die zentrale A83-Implementierung bindet Rohbytes korrekt an `payload_bytes` und `payload_sha256` und dekodiert erst danach strikt als UTF-8. Der lokale Browser-Ledger bleibt jedoch eine lokale Persistenzdemonstration; die Siegelaktion ist kein GitHub-Publish. Die Stamp-Seite prüft die 16 eingebetteten Bindings, jedoch nicht die äußere Operator-ZIP und nicht die Selbstbindung des Source-Manifests.

## 4. Eigene Innovationen und Weiterentwicklungen

### Innovation A — Dual-Layer Package Identity

Jede Übergabe sollte zwei ausdrücklich getrennte Identitäten führen: `outer_delivery_object` für das tatsächlich eingegangene Operator-Artefakt und `inner_source_object` für ein eingebettetes Quellpaket. Beide erhalten eigene Bytezahlen, SHA-256-Digests, Medientypen und Locator. Eine Übereinstimmung des inneren Pakets darf nie als Übereinstimmung mit dem äußeren Lieferobjekt interpretiert werden.

Diese Erweiterung schließt den im vorliegenden Artefakt beobachteten Provenienz-Gap, ohne historische innere Hashes umzuschreiben. Sie ist mit dem bestehenden NEXUS-Prinzip `IDENTITY_MATCH != CONTENT_VALIDATION` vereinbar und bleibt auf C1 beschränkt.

### Innovation B — Self-Binding Manifest Envelope

Das Manifest sollte neben den Child-Bindings einen kanonischen `manifest_identity_sha256` über eine selbstreferenzfreie Identitätsprojektion führen. Damit wird sichtbar, ob die Liste der Bindings selbst unverändert ist. Der äußere Archiv-Digest wird als separates Feld gebunden; eine zirkuläre Selbstreferenz wird vermieden.

### Innovation C — Monotonic Evidence Gate Matrix

Für AXIOM sollte jeder Prüfpfad eine monotone Statusmatrix liefern: `SOURCE_NOT_PRESENT` darf nicht zu `MATCH` hochgestuft werden; `MATCH` darf nur nach unabhängigem Rehash gelten; `PASS_WITH_CAVEATS` darf nicht als `PASS` veröffentlicht werden. Die Matrix trennt dabei vier Achsen: Objektidentität, Struktur, Semantik und Unabhängigkeit. Ein hoher Identitätsstatus erzeugt keine wissenschaftliche Validität.

### Innovation D — Attestation-Ready GitHub Publication

Für eine spätere Veröffentlichung sollte das vorbereitete Paket als unveränderliches GitHub-Release mit eindeutigem Tag, Release-Asset und SHA-256-gebundenem AXIOM-Handoff veröffentlicht werden. GitHub beschreibt Artifact Attestations als Digest-Bindung eines Subjects an eine Provenienz-Aussage und stellt CLI-Verifikation bereit.[1] Für unveränderliche Releases werden Tag und Assets nach Veröffentlichung geschützt; zusätzlich kann eine Release-Attestation Tag, Commit-SHA und Assets binden.[2] Diese Plattformbeweise werden im NEXUS-Modell ausschließlich als Transport- und Provenienzbelege klassifiziert, nicht als wissenschaftliche Wahrheit.

## 5. Empfohlene nächste Schritte

| Gate | Erforderliche Aktion | Status |
|---|---|---|
| G0 | äußeres Archiv und inneres Quellpaket getrennt rehashen | erfüllt |
| G1 | 16 eingebettete Evidence-Bindings rehashen | erfüllt |
| G1 | Manifest-Selbstbindung unabhängig berechnen | offen |
| G2 | Branding-Testabweichungen und ESLint-Fehler separat beheben | offen |
| G3 | AXIOM führt unabhängigen Rehash des Handoffs und der Inputs durch | offen |
| G4/G5 | Hashgebundener Branch/PR und CI auf GitHub | noch nicht veröffentlicht |
| G6 | Operator bestätigt exakten Veröffentlichungsumfang | erforderlich |
| G7 | Nach Veröffentlichung Asset, Tag, Commit und Release-Attestation erneut verifizieren | offen |

## 6. Epistemischer Schluss

Der belastbare Schluss lautet: Das Artefakt enthält eine technisch nachvollziehbare, C1-begrenzte NEXUS-OMEGA-Gate-Anwendung und 16 korrekt gebundene Evidence-Dateien. Die äußere Operator-Lieferung ist jedoch nicht mit dem im eingebetteten Manifest bezeichneten `package` identisch. Die Prüfung ergibt daher `PASS_WITH_CAVEATS` für die innere Evidenz- und Gate-Struktur, aber `NOT_ESTABLISHED` für eine einstufige Gesamtpaket-Provenienz und für jede wissenschaftliche Claim-Promotion.

Eine GitHub-Veröffentlichung darf nur den hier beschriebenen Status und die konkreten Digests transportieren. Sie darf nicht behaupten, dass Hashes, Signaturen, Tests, Agentenübereinstimmung oder GitHub-Attestierungen wissenschaftliche Wahrheit oder Autorität erzeugen.

## Quellen

[1]: https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations "GitHub Docs: Using artifact attestations to establish provenance for builds"

[2]: https://docs.github.com/en/code-security/concepts/supply-chain-security/immutable-releases "GitHub Docs: Immutable releases"
