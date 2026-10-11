# NEXUS OMEGA · Perplexity Computer · R10R29 Kreuzvalidierung (C1)

```text
OBJECT            = NEXUS_OMEGA_PERPLEXITY_COMPUTER_R10R29_CROSS_VALIDATION_RECEIPT_20261011_R0
HANDSHAKE_CLASS   = INDEPENDENT_CROSS_VALIDATION_RECEIPT_NOT_CURSOR_RETURN
FROM              = PERPLEXITY_COMPUTER (operatorvermittelter Bridge-Transport, read-only auf Repo-Dateien)
TO                = NEXUS_OPERATOR_AXIOM · Issue #93
REPO              = nexusomegac27/NEXUS-OMEGA-EVIDENCE
MAIN_COMMIT       = 990298a07dba30d8c1cae6eecec2017f35b41d14
PR                = #97 MERGED 2026-10-11T19:20:19Z (head: codex/r10r29-open-mind-cross-domain-20261011)
CLAIM_CEILING     = C1_DESCRIPTIVE_ONLY
AUTORENKETTE      = NEXUS_OPERATOR -> AXIOM (Auftrag, PR #97) -> Computer-Validierung C1 (ZIP/PDF) -> PERPLEXITY_COMPUTER (Kreuzvalidierung R0)
```

## Bindung an den Kernsatz

> Vom Besitz zur Symbiose. Vom Ego zur Herkunft. Vom fertigen Gedanken zum lebenden Artefakt.

Dieser Beleg ersetzt keinen Vorgängerbeleg. Er knüpft an die Computer-Validierung (ZIP `c1b1c62e…bdc4b4`), an den AXIOM-Auftrag (PR #97) und an die bestehenden Verträge R21.1 Herkunfts-Atom und R21.3 Symbiose-Vertrag an. Jede Vorstufe bleibt als Herkunftsspur benannt.

## 1. Unabhängig nachgerechnete Bindungen

| Prüfung | Erwartet | Unabhängig beobachtet | Ergebnis |
|---|---|---|---|
| Order-Bytes (raw, Main-Commit) | 18205 | 18205 | MATCH |
| ORDER_SHA256 | `235c6763…6a7809807` | `235c67636ce7611c74ed762152c022e5033b6f3ca0921ffdbfdfb9a6a7809807` | MATCH |
| Order Git-Blob | `671456fe…` | `671456fe630ed5c894945c6771d6ecd327691553` | MATCH |
| Detached-Manifest Kinder | 4/4 | 4/4 Bytes + SHA-256 + Git-Blob | MATCH |
| Task Anchor (`validate_task_anchor_norm_v1.py`) | PASS | `ANCHOR_FORMAT_VALIDATED_ONLY`, exit 0, anchor `a8156c0e…ca70` | PASS (nur Format) |
| Workflows am Main-Commit | 5/5 | 5/5 push-Workflows success (+ Pages-Build success) | MATCH |
| PR #97 | MERGED | MERGED, merge commit = Main-Commit | MATCH |
| Issue #93 Publikationsbeleg | vorhanden | Kommentar 6112758111 (19:20:50Z) | MATCH |
| ZIP-Paket SHA-256 | `c1b1c62e…bdc4b4` | `c1b1c62e1735ea2e6b2ba229d15b9dc9588cab19491852e993e8ad1181bdc4b4` | MATCH |
| ZIP interne SHA256SUMS | 12/12 | 12/12 OK | MATCH |
| NEXUS_-1.TXT ≡ ZIP/NEXUS_1.TXT | identisch | `106e8f98…e92f` beide | MATCH |
| R10R29-1.PDF ≡ ZIP/Receipt-PDF | identisch | `a70b3f7c…8cc8a` beide | MATCH |
| NEXUS_-1.PDF (Kernsatz-Artefakt) | – | `c410a14e6c75971209c8822108ddd1e9681bb55d3a3b36a70648d99d2bd8ff71`, 4350 B | ERFASST |

## 2. Befunde (nicht blockierend, append-only)

- **F1 · Kernsatz vs. C1.** „wächst exponentiell“ ist im Repo nur als Prüf-Hypothese `Q_total = Q_base·(1+k)^L` (R21.3) verankert, nicht als Befund. Empfehlung: im Kernsatz-Artefakt „kann … wachsen (Prüfhypothese R21.3)“ führen, damit kein impliziter Claim über C1 entsteht.
- **F2 · Anchor-PASS ist Format-PASS.** Der Validator meldet `actor_authorization = NOT_ESTABLISHED_FROM_FORMAT` und `source_bytes = REQUIRES_INDEPENDENT_FETCH`. Die Bytes wurden hier unabhängig geholt (MATCH); die Akteursautorisierung bleibt eine Operator-Entscheidung.
- **F3 · Zeitstempel im ZIP.** `validation_log.txt` „2026-10-11T12:32:09“ ohne Zeitzone; README `19:32:09Z` (= 21:32 CEST); Receipt-PDF „21:24 CEST (Referenz)“. Die 21:24-Angabe ist eine Referenzzeit, nicht die Erzeugungszeit. Empfehlung: künftig nur ISO-8601 mit Offset.
- **F4 · Toolchain-Deklaration.** Receipt-PDF nennt pdfplumber/pypdf; Log dokumentiert PyMuPDF (fitz) als tatsächlich genutzten Fallback. Inhaltlich ehrlich, Deklaration sollte angeglichen werden.
- **F5 · GitHub Pages ≠ Hostinger.** Am Main-Commit lief automatisch „pages build and deployment“ (success). `WWW_WRITE = NO` bezieht sich auf Hostinger; die Pages-Auslieferung sollte im Ledger getrennt erwähnt werden.
- **F6 · Herkunftsspur im R29-Paket.** Der Auftrag führt `AUTHORITY_CHAIN`, aber keine `AUTORENKETTE` im Format von R21.1/R21.3 (z. B. Codex-Branch als ausführende Hand). Empfehlung: im Cursor-Return eine `AUTORENKETTE` ergänzen — Umsetzung von „Vom Ego zur Herkunft“.
- **F7 · Externe Experten.** Laut Order (Z. 62) bleiben externe Experten read-only bzw. operatorvermittelt; dieser Beleg schreibt keine Repo-Dateien; eine Ablage im Inbox-Kanal #93 erfolgt nur nach ausdrücklicher Operator-Freigabe.

## 3. Konnektor-Kreuzbezug

| Dienst | Befund |
|---|---|
| GitHub | Primärquelle; alle Bindungen oben unabhängig geprüft |
| Notion | Spiegelpraxis bestätigt (z. B. R26 Perplexity RECEIVE_ACK unter R33); R29 Mini-Node-FSM-Seite (QWEN) ist eine andere R29-Lane als R10R29 — nicht vermischen |
| Amplitude | Nur NEXUS AMP V1 Dashboard/Experiment-Draft (07/2026), keine R10R29-Daten — NOT_APPLICABLE |
| Lucid | Kein bestehendes NEXUS-Dokument gefunden — keine Quelle für R10R29 |

## 4. Terminaldisposition

```text
OBJECT = NEXUS_OMEGA_PERPLEXITY_COMPUTER_R10R29_CROSS_VALIDATION_RECEIPT_20261011_R0
STATE = PASS_C1_INDEPENDENT_CROSS_VALIDATION
ORDER_SHA256 = 235c67636ce7611c74ed762152c022e5033b6f3ca0921ffdbfdfb9a6a7809807 MATCH
DETACHED_MANIFEST = 4/4_MATCH (unabhängig)
ZIP_SHA256SUMS = 12/12_OK
TASK_ANCHOR = FORMAT_VALIDATED_ONLY
CI = 5/5_PASS (+PAGES_BUILD_SUCCESS)
FINDINGS = F1..F7_NON_BLOCKING
REPO_WRITE = NO
L3_SELECTED = NO
L3_EXECUTED = NO
NF05_NF06 = REVISIONS_REQUIRED
NODE_RESET = NO
WWW_WRITE = NO
CURSOR_EXECUTION = NOT_YET_CONFIRMED
AXIOM_RECEIPT = PENDING
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
NEXT = CURSOR_R10R29_SOURCE_BOUND_RETURN
```

Quelle ≠ Wahrheit; GitHub-Hash ≠ Wissenschaftsbeweis. Dieser Beleg bestätigt Bindung und Grenzen, keine Gate-Ausführung und keine Claim-Promotion.

— Herkunftsspur · 2026-10-11 · PERPLEXITY_COMPUTER · C1_DESCRIPTIVE_ONLY —
