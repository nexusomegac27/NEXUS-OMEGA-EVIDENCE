# NEXUS OMEGA – GitLab Ultimate / Duo Quartet Framework

**Ausarbeitungsstand:** 1. September 2026 · **Autor:** Manus AI · **Status:** Forschungs- und Architekturentwurf, nicht implementiert

> **Geltungsgrenze:** Diese Ausarbeitung verarbeitet die beiden Projektdateien als verbindliche Ausgangslage. Sie verändert keine Konten, Einstellungen, Repositories, Tokens, Agents, Flows, Pipelines, Merge Requests oder Experimente. Das laufende A90-M2-Lane und der vorhandene Cross-Forge-Zustand bleiben unangetastet.

## A. Executive Verdict

Die Vierparteienarchitektur ist **konzeptionell stärker** als GitHub + Cursor allein, aber nur unter einer strengen Rollen- und Evidenztrennung. GitLab liefert nicht deshalb unabhängige wissenschaftliche Evidenz, weil es ein zweiter Anbieter ist. Der Gewinn entsteht erst, wenn GitLab einen getrennten Runner-, Policy-, Scanner-, Audit- und Agentenpfad ausführt, der an exakt denselben versiegelten Bytes hängt und dessen Ergebnis nicht vom Produzentenprojekt oder von Cursor umgeschrieben werden kann.

Die beste Zielarchitektur ist daher nicht „vier gleichartige Validatoren“, sondern **drei operative Vertrauensdomänen plus ein epistemischer Adjudikator**: Cursor/Local VM, GitHub und GitLab führen aus; AXIOM preregistriert, ordnet Evidenz ein und adjudiziert. Cursor ist Orchestrator und Receipt-Builder, aber kein Ersatz für providerlokale CI. GitHub PASS bleibt GitHub PASS, GitLab PASS bleibt GitLab PASS, und beide werden nur als getrennte Belege in ein neutrales Reconciliation-Objekt aufgenommen.

| Entscheidung | Urteil | Begründung |
|---|---|---|
| Quartet statt Trio | **USE_NOW als Architekturprinzip** | Mehrere Fehler- und Anbietergrenzen, sofern die Rollen nicht kollabieren. |
| GitLab als unabhängige Forge | **ENABLE_AND_TEST** | GitLab CI, Policy-Projekt und Security-Scans können eine zusätzliche Durchsetzungsschicht bilden. |
| Cursor → GitLab MCP | **ENABLE_AND_TEST, read-only zuerst** | OAuth-basierte HTTP-Anbindung ist dokumentiert; Schreib- und Löschwerkzeuge bleiben deny. |
| GitLab Duo Agents/Flows | **RESEARCH_ONLY bis Sandbox-Nachweis** | Composite Identity begrenzt Rechte, erzeugt aber keine wissenschaftliche Unabhängigkeit. |
| Runner Governance | **Sicherheitskritischer Hard Stop** | Fehlende Runner-Regel fällt laut GitLab Known Issues auf Always Allow zurück. |
| Orbit | **RESEARCH_ONLY** | Beta/Experiment und punkt-in-Zeit-Analyse; nie Primärevidenz. |
| Policy Project | **ENABLE_AND_TEST** | Zentrale, vom Kandidaten getrennte Jobs sind technisch plausibel. |
| Native GitHub-Repo-CI in GitLab | **DEFER** | Kann Transport vereinfachen, schwächt aber die klare Repository- und Fehlerdomänentrennung. |
| Automerge | **DO_NOT_USE FOR NEXUS** | Zwei grüne Badges sind weder unabhängige Wahrheit noch Operatorfreigabe. |

## B. Current Trial Entitlement Matrix

Die offizielle GitLab-Dokumentation bestätigt einen 30-Tage-Ultimate-Trial. Für einen Free-Tier-Trial auf GitLab.com werden 24 GitLab Credits pro Nutzer genannt; sie gelten nur für die Trialdauer und werden bei Verbrauch nicht nachgeladen. Proxy-abhängige Funktionen, insbesondere externe Agents und direkte `/v1/proxy`-Aufrufe, benötigen einen Default-Duo-Namespace. Custom- und Foundational Agents/Flows sind von genau dieser Einschränkung laut Trial-Dokumentation nicht betroffen [1].

| Oberfläche | Trial-Aussage | Aktuelle NEXUS-Klassifikation |
|---|---|---|
| Ultimate-Grundfunktionen | Nahezu alle Ultimate-Funktionen laut Trial-Seite | Trial-entitled, aber einzelne Aktivierung prüfen |
| Duo Agent Platform | 24 Credits/Nutzer im Free-Tier-Trial | Credit-limited; Verbrauch messen |
| External Agents / Proxy | Default-Duo-Namespace erforderlich | Trial-restricted, nicht voraussetzen |
| Custom/Foundational Agents und Flows | Von der genannten Proxy-Einschränkung ausgenommen | entitlement prüfen, anschließend Sandbox-Test |
| GitLab CI | Runner/Minuten und Projektkonfiguration separat | compute-limited, lokal nicht gleich Hosted CI |
| Orbit | Ultimate/Premium, Beta/Experiment, Feature Flag | not production evidence |
| Supportpflichtige/Beta-Flächen | nicht aus „Ultimate“ automatisch ableiten | documentation ambiguous, bis beobachtet |

## C. Current Live NEXUS GitLab State

Als operator supplied, nicht durch diese Ausarbeitung live verifiziert, gelten: GitHub `nexusomegac27/NEXUS-OMEGA-EVIDENCE`, Draft-PR 12, Head `9f3fb541faec3aa802e05133043226b1a5606d5d`; GitLab-Projekt `nexus.omega.c27-group/nexus.omega.c27-project`, ID `81872416`, Draft-MR 1, Head `019b0954a8bbd1b2bbb68f60d6cce950a8adc1b2`. Der Cross-Forge-Zustand ist als acht byte-identische Shared Objects berichtet, lokale Reproduktion PASS, GitLab Hosted CI PASS jedoch nicht etabliert. Duo Remote/Foundational Flows und Security/Compliance werden als enabled berichtet. Orbit-User und Service Health sind verfügbar, Namespace-Indexierung jedoch nicht aktiviert. Diese Angaben dürfen nicht als externe Verifikation ausgegeben werden.

## D.–H. Duo Capability Map

GitLab unterscheidet Foundational Agents, Custom Agents, External Agents und Flows. Für NEXUS ist die entscheidende Achse nicht „wie intelligent“, sondern **welche Eingabe, welches Tool, welche Identität und welche Schreibmöglichkeit**. Ein Agent darf als Validator nur source-only lesen, deterministische Tests anstoßen und einen unveränderlichen Receipt in einen dafür vorgesehenen Ausgabekanal schreiben. Policy-, Evaluator-, Holdout- und Default-Branch-Schreibrechte bleiben ausgeschlossen.

| Agent-/Flow-Typ | NEXUS-Nutzen | Zulässiger Einsatz | Ausschluss |
|---|---|---|---|
| Foundational Agent | Reproduzierbare GitLab-Domainanalyse | Security-/CI-Diagnose als nicht-kanonischer Befund | kein Selbst-Approval, keine Policy-Mutation |
| Custom Agent | Rollenpräzise Validatoren mit festem Prompt | read-only oder candidate-branch output | kein Zugriff auf Hidden Holdout |
| External Agent | Provider-/Modell-Diversität | nur wenn Trial, Namespace, Kosten und Datenpfad verifiziert | keine Annahme unabhängiger Provenance |
| Custom Flow | Sequenzierung und Runner-Automation | sealed source → test → adversarial review → receipt | keine unbounded loops, kein Auto-Merge |
| Orbit-gestützter Agent | Kontext, Lineage, Blast Radius | analytische Hypothesen | Graphresultat nicht als Beweis |

## I. Composite Identity

Composite Identity ist seit GitLab 18.8 GA und automatisch in der Duo Agent Platform enthalten. Sie verbindet auslösenden Menschen und Agent-Servicekonto; der effektive Zugriff ist die restriktivere Kombination der Berechtigungen. AI-Catalog-Flows erzeugen ein Servicekonto typischerweise mit Developer-Rolle im Top-Level-Group-Kontext. OAuth-Tokens für AI-Workflows sind auf `ai_workflows` und `mcp` beschränkt; CI-Job-Tokens haben zusätzliche Einschränkungen [2].

Die zentrale NEXUS-Formel lautet:

```text
Human trigger + agent service account
        -> composite execution identity
        -> effective permission = intersection / most restrictive role
```

Das erfüllt „Agent can execute but cannot self-authorize“ nur teilweise. Es begrenzt technische Rechte, verhindert aber nicht automatisch, dass derselbe organisatorische Pfad produziert und bewertet. Daher müssen Validator-Projekt, Policy-Project, Hidden Fixtures und Adjudication außerhalb der Agenten-Schreibdomäne liegen.

## J. Agent Tool Governance

Tool Governance ist Beta. Read, Write und Delete werden auf Always Allow, Always Ask oder Always Deny abgebildet. Die Default-Matrix erlaubt GitLab-Resource-Reads, fragt bei lokalen Reads und fragt bei Writes/Deletes. Für Runner-/Background-Flows ist **Always Ask nicht verfügbar**; ein Tool ohne Runner-Regel fällt laut Known Issues auf Always Allow zurück [3].

Daraus folgt eine verbindliche NEXUS-Konfiguration: Web und IDE dürfen bei nichtkritischen Aktionen fragen; Runner erhalten eine vollständige explizite Allowlist. Alles Nicht-Aufgelistete wird durch Vorabprüfung blockiert oder der Flow wird nicht gestartet. `approvedTools: true` bei MCP wird nicht verwendet, weil damit auch künftig hinzukommende Tools automatisch genehmigt würden.

| Oberfläche | Read | Write | Delete | NEXUS-Regel |
|---|---:|---:|---:|---|
| Web/IDE | ask/allow nach Risiko | ask | deny/ask | keine kanonischen Writes |
| Runner/Background | explizit allow | deny | deny | kein impliziter Default |
| MCP extern | nur einzelne vertrauenswürdige Reads | deny | deny | Server-Block für Untrusted |
| Policy-/Holdout-Projekt | deny | deny | deny | nur Operator-SoD |

## K. Flow-Sandbox und Threat Analysis

Die größte Lücke ist nicht die Existenz eines Sandboxes, sondern der vollständige Lebenszyklus davor: Setup-Skripte, Runner-Image, Cache, Netzwerk-Egress, Tokens und Tool-Responses. Bis die aktuelle Semantik jedes Pfads verifiziert ist, gilt `setup_script = PROHIBITED` für Hochintegritätsvalidatoren. Eine spätere Minimal-Allowlist darf nur in einem vorgebauten, versionierten Image und ohne Secrets eingeführt werden.

| Bedrohung | Primäre Gegenmaßnahme | Verhalten |
|---|---|---|
| Token-Exfiltration | keine Secrets im Validator, deny env reads, Egress deny | blockiert |
| Prompt Injection | untrusted repo als Daten, Tool-Allowlist, Sealing | blockiert/markiert |
| MCP Tool Poisoning | Registry-Block, Einzeltool-Allowlist, Schema-Prüfung | blockiert |
| Setup-Script Escape | verbieten oder prebuilt image | hard stop |
| Cache-Leak | per-run isolierter Cache, keine Secrets | neuer Lauf erforderlich |
| Privilege Creep | separate Servicekonten, Rollenreview | blockiert |
| Branch Abuse | protected branches, candidate-only write | blockiert |
| Receipt Forgery | signed/hash-bound receipt, unabhängiger Fetch | divergiert |

## L.–M. MCP Richtungsmodell

**Cursor → GitLab MCP Server** und **GitLab Duo → externe MCP-Server** sind zwei verschiedene Datenflüsse. Der GitLab MCP Server ist Beta, unterstützt OAuth 2.0 Dynamic Client Registration und HTTP; GitLab dokumentiert eine Cursor-Konfiguration über `/api/v4/mcp` [4]. Für NEXUS ist dies als read-only Bridge sinnvoll, sofern der OAuth-Scope project-scoped bleibt und keine statischen Langzeit-Credentials im Repository liegen.

GitLab Duo kann seinerseits als MCP-Client externe Tools nutzen; dafür muss die Gruppenfreigabe aktiviert werden, und MCP-Tools sind standardmäßig sitzungsbezogen manuell zu genehmigen. Externe MCP-Server werden für die erste NEXUS-Phase blockiert. Die sichere Reihenfolge lautet: GitLab-MCP-Server read-only testen, Tool-Inventar und OAuth-Ereignis sichern, danach nur einzelne nicht-destruktive Werkzeuge freigeben.

## N. Orbit / Knowledge Graph

Orbit ist auf GitLab.com Premium/Ultimate verfügbar, aber Beta/Experiment. Orbit Remote indexiert SDLC-Objekte und Code als Property Graph, arbeitet mit dem letzten Indexzyklus und ist ausdrücklich analytisch, nicht transaktional. Code wird vom Default Branch indexiert; Orbit stellt REST-, MCP- und Duo-Zugänge bereit [5].

Orbit eignet sich daher für Abhängigkeitsfragen, Vulnerability Lineage, MR-/Pipeline-Kontext und Blast-Radius-Hypothesen. Es ist kein Snapshot der versiegelten Candidate Bytes und kein unveränderliches Evidence Ledger. Empfehlung: **erst nach read-only Entitlement-Inventar und getrenntem Namespace-Test aktivieren**; jede Orbit-Aussage muss auf immutable source bytes, commit SHA, Indexzeitpunkt und unabhängigen Receipt zurückgeführt werden.

## O.–Q. Ultimate Security und Policy Root

Security Policy Projects und Pipeline/Scan Execution Policies bilden den stärksten GitLab-seitigen Beitrag zur Nicht-Selbstvalidierung. Pipeline Execution Policies sind Ultimate/GA und können CI-Jobs projektübergreifend zentralisieren; Jobs in `.pipeline-policy-pre` laufen vor nachfolgenden Jobs, und ein Fehler überspringt nach aktueller Semantik spätere Jobs. Scan Execution Policies können Security Scans erzwingen, die lokale Projekt-YAML nicht überschreiben darf [6].

Ein dediziertes `NEXUS_GITLAB_SECURITY_POLICY_ROOT` muss außerhalb des Producer-Projekts liegen. Es enthält Policy-as-Code, scanner pinning, Validator-Harness und Policy-Receipts. Die Policy-Datei selbst braucht geschützten Default Branch, MR-Review durch unabhängige Operatoren und keinen Agenten-Write. Wichtig ist die Einschränkung der MR Approval Policies: Sie können Selbstgenehmigung und scannerbasierte Approvals erzwingen, prüfen aber nicht die Integrität/Authentizität der Scan-Report-Artefakte [7]. Deshalb bleibt die Receipt- und Hash-Prüfung außerhalb der Approval Policy erforderlich.

## R. MR Approval Design

Zielwerte sind geschützte Default Branches, mindestens zwei unabhängige Approver, Autor/Committer nicht als alleiniger Approver, erfolgreiche Policy-Pipeline, aufgelöste Diskussionen, kein Force-Push und **manuelle Operatorfreigabe**. Eligibility ist niemals Merge-Recht. Automatic Merge bleibt deaktiviert.

## S.–T. GitHub ↔ GitLab Vergleich

| Architektur | Unabhängigkeit | Provenance | Loop-Risiko | Urteil |
|---|---|---|---|---|
| A: getrennte Repositories, SHA-Receipts | hoch | stark | niedrig | **Primärdesign** |
| B: GitLab CI für externes GitHub-Repo | mittel | bindbar, aber gemeinsamer Source-Transport | mittel | späterer Vergleichstest |
| C: Pull-Mirror + GitLab Validation | mittel-niedrig | Mirror- und Lag-Risiko | mittel-hoch | nicht als Standard |
| D: Hybrid Clean Room | hoch | sehr stark bei commit-bound input | mittel | **Sekundärdesign** |

GitHub unterscheidet Checks und Commit-Statuses; beide können über APIs gesetzt werden, und ein übersprungener Job kann Success melden [8]. Deshalb werden nur origin-markierte Statusnamen wie `github/local/*`, `gitlab/independent/*` und `axiom/adjudication/*` verwendet. Kein Status darf einen anderen Providerstatus synthetisieren.

## U. Quartet-Rollenmodell

| Rolle | Primäraufgabe | Darf nicht |
|---|---|---|
| AXIOM | Preregistration, Claim Ceiling, Adjudication | fehlende Executable Evidence ersetzen |
| Cursor | Orchestration, local replay, rehash, reconciliation | providerlokalen PASS erzeugen |
| GitHub | öffentliche Primary Forge, lokale Actions/Attestations | GitLab PASS behaupten |
| GitLab | unabhängige Secondary Forge, policies, Duo, CI | kanonische AXIOM-Memory schreiben |

Die operative Architektur hat somit **drei Ausführungsdomänen plus einen Entscheidungsdomänenknoten**. Diese Benennung ist präziser als vier angeblich symmetrische Validatoren.

## V.–W. Event Loop und Loop Suppression

Jedes Ereignis erhält `event_id`, `parent_event_id`, `origin_provider`, `origin_component`, `subject_sha256`, `event_type`, `created_at`, `hop_count`, `max_hops`, `idempotency_key`, `seen_by`, `status` und `terminal`. Verarbeitung erfolgt nur, wenn `(event_type, subject_sha256, idempotency_key)` neu ist. Providerstatus werden nie umbenannt; Reconciliation erzeugt eine neue Eventklasse und darf keine Source Bytes ändern.

```text
on_event(e):
  reject if e.origin_component == current_component
  reject if e.hop_count > e.max_hops
  reject if seen(idempotency_key)
  reject if subject_sha256 != sealed_subject.sha256
  record immutable ingress receipt
  execute only if predecessor state is satisfied
  emit one new event with hop_count + 1
  mark terminal after receipt/adjudication; never re-trigger terminal event
```

Webhooks müssen zusätzlich auf Signatur, Timestamp-Fenster, monotone Sequenz/Version und Replay-Cache geprüft werden. Ein Retry ist nur bei neuem Input oder explizitem Operator-Override zulässig.

## X.–Y. Multi-Agent und Blind Validation

Der Producer gibt nur versiegelte Source Bytes und die Hypothese aus. Validator B und C erhalten denselben gebundenen Input, aber keine Ergebnisse des jeweils anderen. Ihre Prompts, Hidden Fixtures und Policy-Versionen liegen in einem getrennten Projekt. Erst nach Abschluss beider Receipts wird verglichen. Modellfamilien, Scanner-Engines, Rulesets, Runner-Images und Dependencies werden in einer Kopplungsmatrix offengelegt.

Unabhängigkeit ist mehrdimensional: Provider-, Runner-, Scanner-Engine-, Ruleset-, Modellanbieter- und Source-Copy-Unabhängigkeit. Ein GitLab-Job mit anderer UI, aber identischer Semgrep-Engine und identischem Ruleset ist **providergetrennt, jedoch scannergekoppelt**.

## Z. Provider-neutral Receipt Schema

```json
{
  "schema_version":"nexus-receipt-1.0",
  "event_id":"uuid",
  "subject":{"path":"...","sha256":"64-hex","bytes":1234},
  "provider_results":{
    "github":{"repository":"owner/repo","commit_sha":"...","workflow_run_id":"...","job_ids":[],"result":"PASS|FAIL|INCOMPLETE","attestation_id":null},
    "gitlab":{"project_id":"81872416","commit_sha":"...","pipeline_id":"...","job_ids":[],"result":"PASS|FAIL|INCOMPLETE","security_report_ids":[],"policy_evaluation":"PASS|FAIL|NOT_RUN"}
  },
  "cursor":{"local_rehash":"...","local_replay":"PASS|FAIL|NOT_RUN","divergence":"NONE|MISMATCH|INCOMPLETE"},
  "axiom":{"adjudication_state":"C1_PENDING|C1_ISSUED|HOLD","claim_ceiling":"C1"},
  "coupling":{"provider":true,"runner":true,"scanner_engine":"declared","model_family":"declared","source_copy":"bound"},
  "assertions":["github_success_is_not_gitlab_success","hash_match_is_not_scientific_validity","identity_match_is_not_content_validation"]
}
```

Das Schema ist kompatibel **als konzeptionelle Hülle** mit in-toto/SLSA/Sigstore-Prinzipien, beansprucht aber keine formale Konformität. GitHub-Attestations können Build- und SBOM-Provenance mit OIDC binden und offline verifiziert werden [9]; SLSA beschreibt Provenance- und Supply-Chain-Garantien, nicht fachliche Wahrheit [10].

## AA.–AB. Failure Domains und Threat Model

| Ausfall | Systemreaktion | Promotion |
|---|---|---|
| GitHub outage | GitLab/Local können weiterlaufen, GitHub-Lane hold | blockiert, wenn GitHub erforderlich |
| GitLab outage | GitHub/Local weiter, GitLab-Lane hold | blockiert, wenn GitLab erforderlich |
| Cursor failure | provider lanes bleiben, reconciliation fehlt | blockiert |
| AXIOM unavailable | receipts sammeln, keine Adjudication | blockiert |
| Credits/CI exhausted | keine stillen Retries; INCOMPLETE | blockiert |
| MCP auth failure | Bridge fail-closed | blockiert nur MCP-Lane |
| webhook duplicate/reorder | dedupe/sequence check | kein neuer Lauf |
| model/scanner drift | version mismatch receipt | Hold/Operator |
| compromised policy project | policy provenance invalid | sofort blockieren |
| malicious dependency | scanner/test failure oder unknown | mindestens Hold |

## AC. 50 Negative Fixtures

Jede Fixture muss einen erwarteten Denial/Failure, eine Detection Layer, Provider, erforderlichen Log und Receipt enthalten. Die folgende kompakte Matrix operationalisiert die geforderten Klassen.

| ID | Threat | Expected | Layer | Provider |
|---|---|---|---|---|
| NF01 | agent self approval | deny | MR policy | GitLab |
| NF02 | agent policy edit | deny | protected policy project | GitLab |
| NF03 | agent evaluator edit | deny | ACL | GitLab |
| NF04 | agent holdout read | deny | project boundary | GitLab |
| NF05 | default branch push | deny | branch protection | GitHub/GitLab |
| NF06 | merge attempt | deny | operator gate | both |
| NF07 | delete attempt | deny | tool governance | GitLab |
| NF08 | untrusted MCP tool | deny | MCP registry | GitLab |
| NF09 | MCP prompt injection | quarantine | agent boundary | both |
| NF10 | MCP scope escalation | deny | OAuth/ACL | GitLab |
| NF11 | service privilege escalation | deny | composite identity | GitLab |
| NF12 | OAuth exfiltration | deny/rotate | secret scan | both |
| NF13 | setup script token read | deny | runner preflight | GitLab |
| NF14 | cross-run cache leak | fail | cache isolation | GitLab |
| NF15 | webhook replay | dedupe | ingress | both |
| NF16 | event loop | deny | hop/idempotency | both |
| NF17 | out-of-order event | hold | sequence gate | both |
| NF18 | duplicate event | dedupe | idempotency store | both |
| NF19 | stale event | deny | timestamp/state | both |
| NF20 | wrong subject hash | fail | receipt verifier | Cursor |
| NF21 | GitHub status spoof | fail | origin check | GitHub |
| NF22 | GitLab status spoof | fail | origin check | GitLab |
| NF23 | GitHub relabeled GitLab | fail | semantic join | Cursor |
| NF24 | GitLab relabeled GitHub | fail | semantic join | Cursor |
| NF25 | local relabeled provider CI | fail | provenance check | Cursor |
| NF26 | missing job receipt | incomplete | receipt verifier | both |
| NF27 | missing pipeline ID | incomplete | schema validator | GitLab |
| NF28 | scanner removed by candidate | fail | policy injection | GitLab |
| NF29 | policy project mutation | deny | protected MR | GitLab |
| NF30 | failed artifact missing | fail | artifact gate | both |
| NF31 | malicious security report | quarantine | signed/hash receipt | GitLab |
| NF32 | agent A sees validator B | deny | sealed channel | GitLab |
| NF33 | B sees C early | deny | sealed channel | GitLab |
| NF34 | provider collision | hold | coupling matrix | both |
| NF35 | model version drift | hold | version pin | all |
| NF36 | runner image drift | hold | image digest | GitLab |
| NF37 | dependency drift | hold/fail | lockfile | all |
| NF38 | hidden network egress | deny | runner firewall | GitLab |
| NF39 | secret in comment | fail/redact | secret detection | both |
| NF40 | secret in MR | fail/redact | push protection | both |
| NF41 | secret in log | redact/fail | log policy | both |
| NF42 | receipt rewrite | fail | immutable store | Cursor |
| NF43 | history rewrite | deny | branch rules | both |
| NF44 | force push | deny | protected branch | both |
| NF45 | checksum self-hash | fail | canonical hash | Cursor |
| NF46 | missing canonical SHA256 | incomplete | schema gate | Cursor |
| NF47 | Git object ID treated as digest | fail | semantic validator | Cursor |
| NF48 | Orbit as canonical evidence | fail | evidence classifier | AXIOM |
| NF49 | AI audit as validation | fail | evidence classifier | AXIOM |
| NF50 | credit/compute exhaustion mid-flow | incomplete/hold | budget gate | GitLab |

Required artifacts per fixture: `fixture_id`, threat, expected outcome, detection layer, provider, structured log, and a Receipt whose result is `DENY`, `FAIL`, `HOLD` or `INCOMPLETE`, never silently PASS.

## AD. 30-Day Trial Experiment Plan

| Phase | Experiment | Cost/Risk | Evidence | Stop condition |
|---|---|---|---|---|
| P0 | read-only entitlement/settings inventory | minimal/low | dated matrix | any unknown critical permission |
| P1 | Orbit group test, if separately authorized | low/medium | index timestamp/scope | unexpected data scope |
| P2 | Cursor → GitLab MCP read-only | low/medium | OAuth/tool inventory | write/delete exposed |
| P3 | one read-only Agent test | credits/medium | session + model metadata | missing audit boundary |
| P4 | one sandbox Flow with explicit runner rules | compute/high | runner receipt | any implicit Allow/secret access |
| P5 | noncanonical validator fixture | low | source-bound receipt | cannot bind source |
| P6 | one policy-injected security scan | compute/medium | policy + job artifact | candidate can remove job |
| P7 | GitHub event → GitLab validation | compute/medium | two provider receipts | status relabel/loop |
| P8 | blind dual-agent validation | credits/high | sealed B/C receipts | result leakage |
| P9 | constrained cross-forge candidate | high | reconciliation object | any hard-stop failure |

Budgetprinzip: zuerst Struktur und Kontrollwirksamkeit, danach wenige gezielte Agentenläufe, zuletzt Stress. Keine Wiederholung ohne neue Information. Credits und Compute werden vor jedem Lauf reserviert und danach mit tatsächlichem Verbrauch dokumentiert.

## AE. Settings Gap Analysis

Die als FALSE gemeldeten Einstellungen sind nicht pauschal defekt. `Pipelines must succeed`, `all discussions resolved`, `security policy pipeline must succeed`, Secret Push Protection und Commit Signing sind **später enable-and-test**; Merge Trains bleiben für diese Forschungsrunde deferred. Duo Remote/Foundational Flows bleiben nur dort enabled, wo Tool Governance, Runner-Regeln und Rollback nachgewiesen sind. Keine Einstellung wird durch diese Ausarbeitung geändert.

## AF. Cursor Implementation Blueprint

| Phase | Inhalt | Rollback | Hard stop |
|---|---|---|---|
| I0 | Entitlement/Feature Inventory | Dokumente löschen | unverified entitlement |
| I1 | Duo Governance-Härtung | Regeln zurücksetzen | Runner default allow |
| I2 | Orbit read-only/index validation | disable/unlink | scope/retention unknown |
| I3 | MCP read-only | OAuth revoke | write tool exposed |
| I4 | Policy Root design | unlink test project | producer write path |
| I5 | enforced scan fixture | disable policy | removable validator |
| I6 | custom validator | disable catalog item | hidden input leakage |
| I7 | multi-agent flow | stop flow | non-idempotence |
| I8 | event bridge | remove webhook | loop/replay |
| I9 | receipt generator | reject schema | hash mismatch |
| I10 | blind validation | seal lane | B/C leakage |
| I11 | required-check candidate | no merge | status provenance loss |
| I12 | bounded stress | destroy fixtures | credit/compute exhaustion |

Jede Phase muss Files, Settings, Service Accounts, OAuth/Tokens, Runner, Policies, Agents, Flows, Webhooks, MCP, Tests, Negative Fixtures, Rollback, Expected Receipts und Hard Stops deklarieren. **Keine dieser Phasen ist mit diesem Bericht ausgeführt.**

## AG. Do-Not-Implement / Anti-Pattern Register

Nicht zulässig sind ein bidirektionaler Mirror als wissenschaftlicher Beweis, ein Agent als Produzent und eigener Reviewer, kopierte Providerstatus, Automerge nach zwei grünen Badges, unscoped PATs, gruppenweite überprivilegierte Servicekonten, Default-Allow-Runner-Governance, unbeschränkte Setup-Skripte, gemeinsamer Hidden Holdout, frühe Ergebnisweitergabe zwischen Validatoren, Security Policy im mutierbaren Producer-Projekt, Vertrauen in AI-Audit als Korrektheitsbeweis, Vertrauen in Orbit als Source of Record und kostenintensive Wiederholungen ohne neue Evidenz.

## AH. Source Register

[1] [GitLab Docs – Ultimate trials](https://docs.gitlab.com/subscriptions/free_trials/). 30-Tage-Trial, 24 Credits/Nutzer und Proxy-/Namespace-Einschränkungen.

[2] [GitLab Docs – Composite identity](https://docs.gitlab.com/user/duo_agent_platform/composite_identity/). Servicekonto, Human Trigger, restriktivste Berechtigung und Token-Semantik.

[3] [GitLab Docs – Agent tool governance](https://docs.gitlab.com/user/duo_agent_platform/agents/tool-governance/). Allow/Ask/Deny, Kaskade und Runner-Default-Allow.

[4] [GitLab Docs – GitLab MCP server](https://docs.gitlab.com/user/model_context_protocol/mcp_server/). OAuth Dynamic Client Registration, HTTP und Cursor-Konfiguration.

[5] [GitLab Docs – GitLab Orbit](https://docs.gitlab.com/orbit/). Beta/Experiment, SDLC-Graph, Indexzyklus und analytischer Charakter.

[6] [GitLab Docs – Pipeline execution policies](https://docs.gitlab.com/user/application_security/policies/pipeline_execution_policies/) und [Scan execution policies](https://docs.gitlab.com/user/application_security/policies/scan_execution_policies/). Zentrale Jobs, Policy-Pre-Stage und nicht überschreibbare Scans.

[7] [GitLab Docs – Merge request approval policies](https://docs.gitlab.com/user/application_security/policies/merge_request_approval_policies/) und [Security policy projects](https://docs.gitlab.com/user/application_security/policies/enforcement/security_policy_projects/). Protected branches, Approval Rules, Artefaktintegritätsgrenze und Policy-SoD.

[8] [GitHub Docs – Status checks](https://docs.github.com/en/pull-requests/reference/status-checks) und [Available rules for rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets). Checks/Statuses, Skip-Success und Rulesets.

[9] [GitHub Docs – Artifact attestations](https://docs.github.com/en/actions/security-for-github-actions/using-artifact-attestations/using-artifact-attestations-to-establish-provenance-for-builds). OIDC, Build-/SBOM-Attestations und Verifikation.

[10] [SLSA Specification v1.2](https://slsa.dev/spec/v1.2/). Provenance- und Supply-Chain-Sicherheitsgarantien.

## AI. Open Questions

Offen bleiben nach dieser quellenbasierten Runde insbesondere die exakt auf dem konkreten GitLab-Namespace aktivierten Duo-Feature-Flags, die tatsächlich verfügbare Credit-/Compute-Anzeige, die konkrete Runner-Image- und Egress-Semantik, die Export-/Retention-Tiefe von AI Audit Events, die vollständige aktuelle External-Agent-Unterstützung im Trial, die exakte Orbit-Indexierungsfreigabe für den Namespace sowie die Engine-/Ruleset-Überschneidung der konkret eingesetzten Scanner. Jede dieser Fragen ist ein P0- oder P1-Read-only-Test, nicht eine Annahme.

## AJ. Final Recommendation

NEXUS OMEGA sollte die Quartet-Idee weiterverfolgen, aber als **evidenzgetrenntes Drei-Domänen-System mit AXIOM als Adjudikator**. Der unmittelbare Mehrwert liegt in GitLab Policy-Enforcement, separater GitLab-CI, gezielter Security-Scan-Durchsetzung, read-only MCP und kontrollierter Agentenvielfalt. Der größte Risikotreiber liegt in Background-Runner-Defaults, Setup-Skripten, externen MCP-Servern, Status-Semantik und Modell-/Scanner-Kopplung.

Die korrekte nächste Entscheidung lautet nicht „alles aktivieren“, sondern: P0-Inventar → Runner-Governance explizit schließen → read-only MCP → Policy-Root-Test → ein nichtkanonischer Validator → erst dann blindes Cross-Forge-Experiment. GitLab Native CI gegen das externe GitHub-Repository bleibt sekundär; getrennte GitLab-Repository-Kontrolle plus SHA-bound Clean Room bleibt primär. Automatisierung darf Ausführung und Evidenztransport beschleunigen, aber weder Validierung selbst autorisieren noch C1-Claims automatisch erhöhen.

### Terminal Return

| Feld | Wert |
|---|---|
| OBJECT | NEXUS_OMEGA_QWEN_GITLAB_ULTIMATE_DUO_QUARTET_AUTOMATION_DEEP_RESEARCH_RETURN_20260901_R0 |
| STATE | AUTHORIZED_DEEP_RESEARCH_ONLY_C1 |
| CLAIM_CEILING | C1 |
| FEATURES_RESEARCHED | 30+ Capability-/Governance-/Provenance-Flächen |
| VERIFIED_AVAILABLE_NOW | Trial/Composite Identity/MCP-Basis/Policies/Orbit-Doku, nicht Namespace-Aktivierung |
| REQUIRES_ENABLEMENT | MCP, Orbit, Runner Governance, Policy Linking, Agent/Flow-Tests |
| TRIAL_RESTRICTED | Credits, Proxy/External Agents, Beta-/Supportflächen |
| NOT_ESTABLISHED | konkrete Namespace-Flags, tatsächliche Hosted PASS, AI-Exporttiefe |
| QUARTET_RECOMMENDATION | JA, asymmetrisch: 3 execution domains + 1 adjudicator |
| PRIMARY_ARCHITECTURE | getrennte GitHub-/GitLab-Repositories, SHA-bound receipts |
| SECONDARY_ARCHITECTURE | Hybrid Clean Room |
| CURSOR_GITLAB_MCP | Ja, read-only OAuth-first |
| ORBIT | später, research-only |
| SECURITY_POLICY_PROJECT | Ja, getrennt und SoD-geschützt |
| CURSOR_IMPLEMENTATION_ORDER_READY | JA, als nicht ausgeführter Blueprint |
| NO_IMPLEMENTATION | CONFIRMED |
