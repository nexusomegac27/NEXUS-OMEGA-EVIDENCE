# NEXUS OMEGA – Canonical Validation of QWEN Inputs

**Status:** `CANONICAL_BASELINE_ACCEPTED_WITH_CLAIM_DOWNGRADES`  
**Validiert durch:** Manus AI · **Datum:** 1. September 2026  
**Scope:** ausschließlich die Dateien „Architekturvergleich für NEXUS_AGENTENSYSTEME“ und „GitHub anhand der Claim-Kette“

## 1. Ergebnis

Die beiden Dateien sind in der VM vorhanden, lesbar und technisch intakt. Die TXT-Datei ist gültiger UTF-8-Text; die PDF-Datei ist ein lesbares PDF 1.7 mit 50 Seiten im A4-Format. Ihre Inhalte sind thematisch stark überlappend und bilden gemeinsam die **kanonische Arbeitsgrundlage** für den CLAUDE-CODER-Auftrag.

Die Grundlage wird jedoch nicht ungeprüft als vollständig verifiziert übernommen. Mehrere Aussagen des QWEN-Materials sind **Hypothesen, Überdehnungen oder Quellen-/Begriffsfehler**. Kanonisch übernommen werden deshalb Architekturfragen, Claim-Kettenstruktur, Negativtestlogik und die Forderung nach unabhängiger Provenance. Nicht kanonisch übernommen werden unqualifizierte Aussagen über OIDC, Axiom-Adjudikation, GitLab Orbit, GitLab Duo/MFA und vermeintliche „Fälschungssicherheit“.

| Datei | VM-Befund | SHA-256 |
|---|---|---|
| `Architekturvergleich für NEXUS_AGENTENSYSTEME.txt` | UTF-8, 114 Zeilen, 52.537 Bytes, CRLF | `247e73e8177162836c52d3ff9fe3cb3cc7923f3b8b4f5a53dc2774e4caaf9718` |
| `GitHub anhand der Claim-Kette.pdf` | PDF 1.7, 50 Seiten, A4, 275.542 Bytes | `b59943630c287a0cb9384fc0001441a83caf6c0db06abc291dddc913b51d759a` |

## 2. Technische Validierung

Die PDF-Datei wurde in der VM mit `pdfinfo` und `pdftotext` verarbeitet. Es konnten 124.999 Zeichen in 1.833 extrahierten Textzeilen gelesen werden. Die PDF-Textstruktur und die TXT-Datei zeigen dieselbe zentrale Untersuchung, jedoch nicht dieselbe Dateirepräsentation; beide Hashwerte sind daher eigenständig zu führen. Ein identischer Inhalt darf nicht behauptet werden, solange kein byteweiser oder normalisierter Inhaltsvergleich mit definiertem Transformationsprotokoll erfolgt ist.

Die PDF enthält ein umfangreiches Quellenregister mit mehr als 400 Einträgen. Dieses Register ist nicht automatisch ein validiertes Quellenverzeichnis. Es enthält offizielle Dokumentation, Blogposts, Foren, Social-Media-/Werbeseiten, sekundäre Beiträge und offensichtlich irrelevante Treffer. Der CLAUDE-CODER muss jede tragende Behauptung erneut gegen Primärquellen prüfen.

## 3. Kanonisch akzeptierte Architekturthese

Die Untersuchung darf weiterhin als Vergleich zweier Evidenzpfade geführt werden:

```text
A = GitLab Ultimate + GitLab Duo + MCP + GitLab Orbit
B = AXIOM + Cursor + GitHub
```

Die belastbare Fragestellung lautet nicht, welche Gruppe „moderner“ oder „sicherer“ ist. Sie lautet, welche Architektur unter konkret definierten Bedingungen die Claim-Kette besser **nachweist, begrenzt, reproduziert und gegen Umgehung testet**.

Die Claim-Kette bleibt:

```text
EXISTS
→ ENTITLED
→ ENABLED
→ CONFIGURED
→ EXECUTED
→ RECEIPT-VERIFIED
→ INDEPENDENCE-QUALIFIED
→ AXIOM-ADJUDICATED
```

`AXIOM-ADJUDICATED` ist dabei ein NEXUS-Zielzustand und nicht ohne Weiteres ein natives Feature einer kommerziellen Axiom- oder MCP-Integration. Das muss CLAUDE-CODER ausdrücklich prüfen.

## 4. Kritische Claim-Downgrades

| QWEN-Aussage / Richtung | Kanonischer Status | Korrekte Forschungsformulierung |
|---|---|---|
| „Duo“ als etablierter MFA-Anbieter innerhalb GitLab Duo | `SEMANTICALLY_AMBIGUOUS` | GitLab Duo und Cisco Duo/MFA strikt trennen; keine Identitäts- oder MFA-Eigenschaft ohne Primärquelle annehmen. |
| Orbit als organisatorisches Framework | `CORRECTION_REQUIRED` | GitLab Orbit als Beta-/Knowledge-Graph-/SDLC-Analysefläche prüfen; nicht als Kultur- oder Managementframework behandeln. |
| OIDC bindet jede Agentenaktion/Commits kryptografisch an den Benutzer | `OVERCLAIMED` | OIDC bindet bestimmte Token-Ausgaben und Workload-Identitäten; daraus folgt nicht automatisch, dass jede Agentenaktion oder jeder Commit signiert ist. |
| OIDC Subject Claims seien „immutable“ im Sinn unveränderbarer Benutzerhandlung | `OVERCLAIMED` | Unveränderlichkeit, Issuer, Audience, Subject-Semantik, Token-Lebensdauer und Vertrauensmodell konkret prüfen. |
| OIDC sei ein fälschungssicherer Receipt für Agentenaktionen | `NOT_ESTABLISHED` | OIDC ist Identitäts-/Workload-Authentisierung; ein NEXUS-Receipt benötigt zusätzlich Subject-Hash, Event, Job, Artefakt und Verifikation. |
| GitHub hosted runner + GitLab Runner als normale Architektur A | `CONFUSED_TOPOLOGY` | GitLab Runner, GitHub-hosted runner und Cross-Forge-Execution separat modellieren. |
| SLSA beweise fachliche Wahrheit | `REJECTED` | SLSA/Attestation belegt Provenance-Eigenschaften, nicht semantische oder wissenschaftliche Korrektheit. |
| Axiom MCP ermögliche native AXIOM-Adjudikation | `NOT_ESTABLISHED` | MCP kann Datenzugriff ermöglichen; Adjudikation setzt ein definiertes Regelwerk, Datenmodell, Receipt-Verfahren und unabhängige Entscheidungsgrenze voraus. |
| Provider-Trennung bedeute Unabhängigkeit | `REJECTED` | Provider-, Runner-, Scanner-, Ruleset-, Modell- und Source-Copy-Kopplung separat ausweisen. |
| lokale Reproduktion sei Hosted-CI-PASS | `REJECTED` | `LOCAL_REPLAY`, `GITHUB_CI` und `GITLAB_CI` getrennt als Resultate führen. |
| ein grüner Status sei ein Beweis | `REJECTED` | Status ist eine providerlokale Beobachtung; Receipt- und Origin-Prüfung ist erforderlich. |

## 5. Quellenhygiene-Befund

Die Dokumente enthalten brauchbare Primärquellenhinweise, aber auch zahlreiche schwache oder themenfremde Quellen. Für den CLAUDE-CODER gelten deshalb folgende Beweisregeln:

| Quellenklasse | Verwendung |
|---|---|
| Offizielle GitLab-/GitHub-Dokumentation, API-Referenz, Release Note | Produktsemantik, Limits, Berechtigungen, Status und aktuelle Verfügbarkeit |
| SLSA, in-toto, Sigstore, CycloneDX, IETF/RFC, MCP-Spezifikation | Standards, Attestation, Token- und Protokollsemantik |
| Offizielle Axiom-/Cursor-Dokumentation | nur konkrete Axiom-/Cursor-Funktionen und Versionen |
| Issue Tracker/Forum | Known Issues und negative Evidenz, niemals alleinige Sicherheitsgarantie |
| Blogs, Social Media, Marketing, Aggregatoren | Discovery oder Kontext, nicht tragender Beweis |
| Such-Snippet | keine Evidenz |

Jede tragende Behauptung erhält URL, exakten Abschnitt, Abrufdatum, Versions-/Offering-Kontext, Claim-ID und Falsifikationstest. Bei fehlender Primärquelle lautet der Status `NOT_ESTABLISHED`.

## 6. Kanonische Validierungsregeln

Erlaubt sind nur Aussagen mit klarer Trennung zwischen `DOCUMENTED`, `OBSERVED`, `REPRODUCED`, `ATTESTED`, `INDEPENDENCE_QUALIFIED` und `ADJUDICATED`. Kein Dokumentationsbefund darf als konkrete Namespace-Aktivierung ausgegeben werden. Kein Hash Match beweist semantische Richtigkeit. Keine Human Attribution beweist unabhängige Validierung. Keine Auditspur ersetzt einen verifizierten Receipt.

Die erste harte Sicherheitsgrenze ist die Runner-/Tool-Governance. Wenn ein fehlender Runner-Eintrag auf Allow fällt, ist jede High-Integrity-Agentenausführung bis zur Kompensation `BLOCKED`. Setup-Scripts, unscoped Tokens, schreibfähige MCP-Tools, Policy-Root-Schreibrechte, Status-Relabeling, Self-Approval und Automerge bleiben verboten.

## 7. Kanonische Claim-Ceiling-Entscheidung

```text
CANONICAL_CLAIM_CEILING = C1
QWEN_RESULTS = INPUT_EVIDENCE_NOT_FINAL_TRUTH
ARCHITECTURE_COMPARISON = CONDITIONAL
GITLAB_ADVANTAGE = NOT_ESTABLISHED
GITHUB_ADVANTAGE = NOT_ESTABLISHED
OIDC_AGENT_RECEIPT = NOT_ESTABLISHED
AXIOM_NATIVE_ADJUDICATION = NOT_ESTABLISHED
ORBIT_CANONICAL_EVIDENCE = REJECTED
AUTOMATED_PUBLICATION = PROHIBITED_UNTIL_OPERATOR_GATE
AXIOM_FINAL_REVIEW = DOWNSTREAM_ONLY
```

Diese Einstufung ist die kanonische Grundlage, auf der CLAUDE-CODER weiterarbeitet. CLAUDE-CODER darf QWEN nicht „bestätigen“, sondern muss die überdehnten Claims entweder korrigieren, belegen oder verwerfen.

## 8. VM-Prüfprotokoll

```text
READABILITY_TXT = PASS
READABILITY_PDF = PASS
PDF_TEXT_EXTRACTION = PASS
SHA256_TXT = 247e73e8177162836c52d3ff9fe3cb3cc7923f3b8b4f5a53dc2774e4caaf9718
SHA256_PDF = b59943630c287a0cb9384fc0001441a83caf6c0db06abc291dddc913b51d759a
SEMANTIC_OVERLAP = HIGH
BYTE_IDENTITY = NOT_APPLICABLE / NOT_ESTABLISHED
SOURCE_REGISTER_QUALITY = MIXED
CANONICAL_ACCEPTANCE = WITH_CLAIM_DOWNGRADES
IMPLEMENTATION_PERFORMED = NO
GITHUB_MUTATED = NO
GITLAB_MUTATED = NO
AXIOM_INVOKED = NO
A90_M2_TOUCHED = NO
```
