# AXIOM / M50GRN R0

Dieses Verzeichnis enthält das vom Operator bestätigte äußere `M50GRN~1.ZIP` sowie den C1-begrenzten Forschungs- und Prüfstand von Manus AI. Der Inhalt baut kanonisch auf dem im Artefakt enthaltenen NEXUS-OMEGA-Stand auf und verändert dessen historische Evidence-Dateien nicht.

## Status

Der Status lautet **PASS_WITH_CAVEATS**. Die 16 im inneren `SOURCE-MANIFEST.json` gelisteten Evidence-Dateien stimmen byte- und SHA-256-genau. Das äußere Operator-Archiv ist ein separates Zustellobjekt und wird deshalb mit einer eigenen Digest-Bindung geführt.

> Ein Hash belegt Objektidentität, nicht wissenschaftliche Wahrheit, semantische Gültigkeit oder Autorität.

## Unabhängige Prüfung

```sh
sha256sum M50GRN~1.ZIP
sha256sum -c SHA256SUMS
```

Erwarteter Digest des äußeren Archivs:

```text
51ae10b55d1f6cfa7f4ed4aa85ecf4dc3d1e451ee31a7ecc50d48c30febd5487  M50GRN~1.ZIP
```

Das innere, vom eingebetteten Manifest gebundene NEXUS-Quellpaket ist im äußeren Archiv unter `attachments/NEXUS_~1.ZIP` enthalten und hat den Digest `c8ad4fa891580c5983a88caf807bddefb1c77616e298c3c15fb70bb38fbd4864` bei 212788 Bytes. Es ist absichtlich nicht mit dem äußeren Zustellobjekt gleichgesetzt.

## Veröffentlichungsgrenzen

Dieser Stand enthält keine Claim-Promotion, keine Foundation-Promotion und keine Behauptung wissenschaftlicher Validität. Eine Manifest-Selbstbindung, eine unabhängige AXIOM-Gegenprüfung und eine GitHub-Artifact-Attestation sind als offene Folge-Gates dokumentiert.

## Veröffentlichungsobjekt

Der Branch `axiom/m50grn-r0-20260831` ist ein separater Veröffentlichungsstand. `main` wird nicht direkt verändert. Für eine dauerhafte Distribution ist ein unveränderliches Release mit diesem Branch-Commit als Tag zu bevorzugen.
