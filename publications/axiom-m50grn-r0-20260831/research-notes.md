
## GitHub-Provenienz-Recherche

GitHub dokumentiert Artifact Attestations als Bindung eines Subjects über dessen SHA-256-Digest an eine Provenienz-Aussage; die Verifikation erfolgt für ein lokales Artefakt mit `gh attestation verify ... -R owner/repository`.[1] GitHub dokumentiert außerdem unveränderliche Releases: Nach Veröffentlichung können Tag und Release-Assets nicht mehr verändert oder gelöscht werden; ein Release-Attestation bindet Tag, Commit-SHA und Assets.[2]

## Artefaktbefund

Die 16 im eingebetteten `SOURCE-MANIFEST.json` deklarierten Evidenzdateien stimmen byte- und SHA-256-genau mit den Dateien unter `public/evidence` überein. Die dort deklarierte Paketbindung bezieht sich jedoch auf das eingebettete `attachments/NEXUS_~1.ZIP`; dieses innere ZIP stimmt mit 212788 Bytes und SHA-256 `c8ad4fa891580c5983a88caf807bddefb1c77616e298c3c15fb70bb38fbd4864` überein.

Das tatsächlich vom Operator angehängte äußere ZIP `M50GRN~1.ZIP` hat 2598531 Bytes und SHA-256 `51ae10b55d1f6cfa7f4ed4aa85ecf4dc3d1e451ee31a7ecc50d48c30febd5487`. Es ist daher nicht identisch mit der im Manifest als `package` gebundenen inneren NEXUS-ZIP. Dieser Unterschied ist ein materialer Provenienz-Gap und muss in einem neuen AXIOM-Handoff als zweistufige Paketbindung (outer delivery envelope + inner source package) explizit gemacht werden.

Die aktuelle App verifiziert Stamp, Identitätsblock, eingebettete Stamp-Datei und die 16 Manifestbindungen. Sie berechnet weder die Selbstbindung des `SOURCE-MANIFEST` noch die äußere Operator-ZIP-Bindung. Der Browser-Ledger ist lokal; `sealStamp()` ist kein GitHub-Publish.

## Qualitätsgates

`npm ci` scheitert auf der Originalkopie wegen eines nicht synchronen `package.json`/`package-lock.json`-Zustands. In einer separaten Build-Kopie reparierte `npm install --ignore-scripts` die Installationsbasis nur für die Prüfung; die Originalbytes blieben unverändert.

Die JavaScript-Tests liefern 187 Pass und 8 Fail. Die acht Fehler liegen im Grok-PWA-Branding-Testpfad (`scripts/grok-pwa-plugin.test.mjs`) und zeigen Abweichungen zwischen Erwartungen und tatsächlich injiziertem NEXUS-OMEGA-Branding. `tsc --noEmit` besteht. ESLint scheitert an einem `no-empty`-Fehler in `src/lib/app-data/client.server.ts:214:13` sowie einer ungenutzten Disable-Warnung in `src/lib/auth/use-current-user.ts:59:3`.

[1]: https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations "GitHub Docs: Using artifact attestations to establish provenance for builds"
[2]: https://docs.github.com/en/code-security/concepts/supply-chain-security/immutable-releases "GitHub Docs: Immutable releases"
