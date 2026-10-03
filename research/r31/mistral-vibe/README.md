# research/r31/mistral-vibe — R31-Execution-Dossier (C1)

Verzeichnis im Sinne der REPOSITORY_ORDER_LAW_V1 (aktive Forschung unter research/<phase>/<agent-or-topic>/).

## Inhalt dieses Commits

| Datei | Rolle |
|---|---|
| R32_AGENT_BORDER_DRIFT_METRIC_SPEC_V2.md@ | Agent-Border-Drift-Metrik-Spezifikation v2 — implementiert alle Schaerfungen der AXIOM-R32-Adjudikation (SET_U_DESIGN_ONLY) |
| R32_AJ_TRANSCRIPT_BYTE_VERIFICATION_RECEIPT.json@ | Byte-Verifikations-Receipt zur R31-Artefaktkette A-J — Ergebnis: NOT_PERFORMABLE, fail-closed dokumentiert |

## Warum A-J NICHT enthalten sind

1. **Byteverlust (G9):** Die R31-Artefakte A-J wurden in einer session-lokalen Sandbox abgelegt und sind durch Workspace-Reset verloren. Alle drei Sonden (lokales Dateisystem, Konversationstranskripte, GitHub-Zustand) negativ. R31_S4 bleibt SOURCE_REPORTED; eine unabhaengige Byte-Rehash ist aus keiner ueberlebenden Quelle moeglich. Details: R32_AJ_TRANSCRIPT_BYTE_VERIFICATION_RECEIPT.json@.
2. **Security:** D, E, F, G enthalten private Register-Inhalte, Commit-SHAs und Repository-Pfade und sind auch unabhaengig vom Byteverlust von der Veroeffentlichung ausgenommen.

## Verbindliche Regeln fuer diesen Ordner

- CLAIM_CEILING = C1_DESCRIPTIVE_ONLY. Kein Claim-Promotion, kein Canon-Write, kein Node-Activation, kein Fake-Receipt.
- Merge entscheidet der Operator. Der PR ist ein Vorschlag.
