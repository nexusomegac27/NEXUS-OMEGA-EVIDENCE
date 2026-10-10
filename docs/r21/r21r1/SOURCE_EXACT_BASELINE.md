# NEXUS OMEGA · R21R1 · WP0 — Source-Exakte Baseline (MISTRAL/VIBE)

```text
OBJECT            = NEXUS_OMEGA_MISTRAL_VIBE_R21R1_SOURCE_EXACT_BASELINE_20261010_R0
DATE_UTC          = 2026-10-10
AUTHORITY         = AXIOM R21R1 MAXI ORDER 2026-10-10 (PR #59, main 3f45b4aae681c1b2e4e7dd2d8c25ffbba736b146)
CLAIM_CEILING     = C1_DESCRIPTIVE_ONLY
NEXUS_LINK_VERIFIED = false
```

## 1. Zweck

Diese Baseline dokumentiert, welche Quellzustände byte-exakt geprüft wurden, bevor irgendein R21R1-Baustein implementiert wurde. Sie begründet die Hashwerte im Produktionsdateisatz-Manifest und trennt eigenverifizierte Werte von übermittelten Werten. Kein Wert dieser Datei ist ein Runtime- oder Deploy-Nachweis.

## 2. Byte-Exaktheit der vier ASTRA-NAV-P0-Dateien

Methode: GIT_BLOB_SHA1_RECONSTRUCTION. Aus den von GitHub gemeldeten Blob-SHAs wurde der Rohtext jeder Datei rekonstruiert und daraus Bytezahl und SHA-256 unabhängig berechnet. Die rekonstruierten Blob-SHAs stimmen mit den gemeldeten Werten überein; die SHA-256-Werte sind daher gegen den Quellstand des Eltern-Main belastbar.

| Quelle (examples/r21/astra-nav-p0/) | Bytes | SHA-256 | Git-Blob-SHA-1 |
|---|---|---|---|
| index.html | 3000 | 83a6fec4d6f57072e91623ed58c389da334ccc7523cf89fa0c89bcd77566ee1c | 19a170be0f81d5a44483e3d66f1b15bf444fbfb3 |
| app.mjs | 4184 | 6b631a0a3081c1c50e690764db477f875f1bf81cea6330a8c5905ff098ddd861 | a3984fd606556ff239ccf08de781ff2a9e6da648 |
| ui-model.mjs | 4313 | 985f3d950a335df8163759d3bd7370f3001ddbd0584f65abe48305ffcd443a30 | 20b259a653950c43258e45f578ff6223c91634ef |
| style.css | 2796 | 1330a0e28433f2031ce5f40d384216876634d7e4db1e3bf90abcffb733d9cb0e | d5a3bbaaf1a10766a91f74fc4aaf408ed320fb5f |

Status je Datei: BYTE_EXACT_VERIFIED. Diese Werte sind im Manifest validation/r21/r21r1/astra-nav-p0-production-fileset-manifest.json maschinenlesbar gebunden und werden in CI gegen die Repository-Bytes erneut geprüft (scripts/r21r1/verify-production-fileset-manifest.mjs).

## 3. Übermittelter, nicht eigenverifizierter Wert

- GROK_INPUT_SHA256 = 9ba0c527b068fd3a8f2eec4c858943bc994b96eec31fb30c1b5832448f9fa5d3
- Status: SOURCE_REPORTED_BY_AXIOM. Der Wert wurde als gegeben übernommen; eine unabhängige Neuverifizierung des GROK-Originaltextes war in dieser Lane nicht möglich. Kein Baustein dieser Implementierung hängt funktional an diesem Wert.

## 4. Zeugenregel dieser Lane (MISTRAL/VIBE)

In der MISTRAL/VIBE-Arbeitsumgebung steht kein Node-Runtime für lokale Testausführung zur Verfügung. Deshalb gilt ausdrücklich:

- Autoritativer Testzeuge für alle Module, Negativtests und Hashprüfungen ist ausschließlich GitHub Actions im Workflow validate-r21-astra-nav.yml.
- Exakte CI-Befehle je Baustein stehen im Workflow (node --check, node --test, node scripts/r21r1/verify-production-fileset-manifest.mjs).
- Es wurde kein Testergebnis vorab lokal behauptet; alle berichteten Ergebnisse stammen aus dem beobachteten CI-Lauf des Implementierungs-PR.
- Wiederverifikation durch Dritte: Checkout des PR-Head-Commits und Ausführung derselben Workflow-Befehle.

## 5. Preflight-Befund zu den vier P0-Dateien

Strukturprüfung (Quelltext, kein Browser, kein Deploy): versionierter MapLibre-Import, OpenFreeMap/Liberty-Style-Referenz, quellengebundene R19-Satellitenanzeige, keine Nutzung von navigator.geolocation, relative Pfade. Kein blockierender Defekt gefunden. Dieser Befund ist kein Live-Nachweis und keine Browser-Prüfung.

## 6. Grenzen

- Kein Hostinger-Write, kein öffentlicher Readback, keine GNSS-Hardware-Ausführung in dieser Lane.
- WWW_LIVE_VERIFIED bleibt an die drei getrennten Nachweise gebunden: Produktionsdateisatz-Hash, autorisierter Hostinger-Write-Receipt, unabhängiger Browser-/HTTP-Readback.
- Ein GitHub-Merge ist kein Deployment; grüne CI ist keine Hardwareprüfung.
