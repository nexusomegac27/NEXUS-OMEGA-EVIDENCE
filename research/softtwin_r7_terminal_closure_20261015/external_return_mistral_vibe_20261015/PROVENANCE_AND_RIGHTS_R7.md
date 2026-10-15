# PROVENANCE_AND_RIGHTS_R7 — Quellen-Ledger, Rechte und Receipt-Trennung

**CLAIM_CEILING:** C1_DESCRIPTIVE_ONLY · **Empfaenger:** AXIOM (adjudiziert unabhaengig) · **Sender:** MISTRAL/VIBE-Expert-Session 2026-10-15

## Quellen-Ledger (alle ACTUAL_BYTES_REHASHED mit eigener SHA-256-Toolchain)

| Objekt | Bytes | SHA-256 | Verifikation |
|---|---|---|---|
| R7-Auftrags-ZIP (research/softtwin_r7_terminal_closure_20261015/NEXUS_OMEGA_AXIOM_R7_MAXIMUM_EXPERT_TERMINAL_CLOSURE_20261015_R0.zip, Git-Blob 01b0f8115cb1d819a4c33335890bd7246dd3cbf5) | 32412 | 95c35d3fced603f704fbd885c2d35cc9acb1a44a7ef51240e6586bd2d190ae0a | byte-exakt in dieser Expert-Session verifiziert |
| Order-Doc (Git-Blob 17f1a18121a23a24c54181d3b36b5ee97e20fe8f) | 22567 | dbf995c1aba3550670f5b6702bc33609842d3f06ad3954ca151ff710faf49424 | im Fortsetzungslauf neu gerehashet; Praefix dbf995c1 exakt; Kreuzvalidierung gegen MANIFEST_SHA256.json |
| R7_CLOSURE_BOUNDARY_AND_PRIORITIES.md (Blob 5e186eef195218cad517d7e544b0c5c381c02a9a) | 5019 | 8e8d519654b2cb696f698bf3edea7f72fc9175e0c9f60f1963353a62b8a202c0 | neu gerehashet |
| R7_OPERATOR_DISPATCH_DE.md (Blob f67840fe39e0035ea4ee28ae665ec13fa453b206) | 1645 | 69f11984d60bb0ae9313f8585c90a1f8b5af5a9d890b5cb8467ef8411ba58d8e | neu gerehashet |
| MANIFEST_SHA256.json (Blob b410fb2e1391ce40cbaeb8a3f6248f858f6c1ce9) | 2740 | ca230d3fc00002229573ebf5ec3aa34037366f3002639901fa396e86aa51c66c | neu gerehashet; enthaelt die 13 internen ZIP-Dateihashes, alle konsistent |
| R7_PREPARATION_TEST_REPORT.json (Blob db9c1819660174ca33008772d04744318d71de9a) | 859 | 6eb9f8ada3bd2f880afffbe3bda7baf9049cf62f5647d209b463b34fd41d9124 | neu gerehashet |
| R7_CLOSURE_GATE_MATRIX.json (Blob e30af3ecec03790bb4b2ca91aa07017ba15a8fbe) | 5232 | 832f177354e1d213a69919408b9be47a39a4e2bb18b1d2dccbcaf2229cfc84f2 | neu gerehashet; Struktur NEXUS_R7_CLOSURE_GATES_V1 unveraendert uebernommen |
| R7_EXTERNAL_FINAL_RETURN_SCHEMA.json (Blob 077e201eeffd0b19bf0c1abd9678bc1bffd112de) | 7136 | e7c2314708aaf9307d2d59e4f44ae76a9915ef4f097ba60db9401bc534a45f6b | neu gerehashet; FINAL_RETURN.json validiert gegen dieses Schema |
| PUBLIC_R7_SOURCE_INDEX.json (Blob f0c4fffbd6fcaf20fdc4b033c275bd427e12b159) | 3407 | 43fdd7232c0c163bf58585c306d7d1005d11fa452d5ae9cf522efd2a008257d6 | neu gerehashet; Git-Blob verifiziert |
| src/nexus_artifact_triage_v04.py | 15786 | a2972e6a1eaef8e933fcb2597bc5be85be76a36b6cbb3ad82ec28175103bff3a | byte-exakt verifiziert (aus oeffentlicher R6-Kapsel) |
| Oeffentliche R6-Kapsel (research/softtwin_r6_axiom_v04_20261014/NEXUS_OMEGA_AXIOM_R6_V04_RESEARCH_CAPSULE_20261014.zip) | 47436 | 7f31a9177a8e38f64e81c13b1cdd2d28edf47b102e5f8db26492eed3d2b93aac | byte-exakt verifiziert, 18/18 CRC |
| morluto/rea package.json @ 0f55f247cdd2ae9bd7903d5e45962b19dfc233dc | 23946 | a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c | neu gelesen und gerehashet: name=rea-agents, version=6.5.0, license=MIT (MCP-Server) |

## Rechte und rechtliche Einordnung (C1, deskriptiv)

- EuGH C-13/20 (Top System) und C-650/17 (Royalty Pharma): Primärtexte auf EUR-Lex/CURIA sind robot-blockiert; keine primaere Byte-Verifikung in dieser Session -> EXTERNAL_REPORTED_ONLY. C-13/20 betrift notwendige Fehlerkorrektur, C-650/17 betrifft (nicht Levola) gueltige Vorlagen-Fiktion im Patentkontext.
- §69d UrhG: Primärtext blockiert (Retry erfolglos). §69e UrhG via dejure.org inhaltlich konsistent bestaetigt (Interoperabilitaet, Dekompilierungszweck).
- APPNOTE: p1k.se-Mirror der ZIP-Specification v6.3.3 FINAL verifiziert; ein Mirror ist nicht der offizielle Signer.
- REA/Lookalike-Risiko: morluto/rea am gepinnten Commit verifiziert; NPM-Tarball-Korrespondenz NICHT geprueft (NPM_TARBALL_CORRESPONDENCE_NOT_ESTABLISHED, kein Blocker). Kein npm install, kein npx, keine Ausfuehrung.
- MCP: Security Best Practices (2026-07-28) und tool-annotations verifiziert; readOnlyHint ist nur ein Hinweis, keine Autorisierung.
- SLSA v1.2 provenance und in-toto attestation v1.2 als Referenzmodelle geprueft (Separation von Hash, Signatur, Quittung).

## Receipt-Disziplin

- Hash ist nicht Signatur ist nicht Quittung. Store-Signer: UNSIGNED. Es existiert kein behaupteter R6-Multi-Agenten-Krypto-Signer.
- Der Git-Push dieses Returns ist KEIN Receiver-ACK; transport.receiver_ack = NOT_ESTABLISHED.
- Private R6-Originale sind PRIVATE_SCOPE_EXCLUDED, kein neuer genereller Quellen-Gap.
- Redaktionsscan (mechanisch, im Build): 0 Treffer ueber alle 20 Umschlagsdateien.
