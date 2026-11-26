# 02 · INTEGRITAET UND METHODE

## Eigene Krypto-Primitive (Sandbox)
- Eigener UTF-8-Encoder und eigener SHA-256-Stack. Selbsttest: SHA-256(abc) = ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad.
- Eigener SHA-1-Stack fuer Git-Blob-Verifikation. Selbsttest: SHA-1(abc) = a9993e364706816aba3e25717850c26c9cd0d89d.
- CRC-32 (IEEE, reflektiert). Selbsttest: CRC32(123456789) = cbf43926.

## ZIP-Erzeugung
- Das R45-6-Stack-ZIP wurde byte-exakt in der Sandbox erzeugt: Methode STORE ohne Kompression, feste DOS-Zeit 2026-11-26 12:00, 9 Mitglieder (00 bis 08).
- Selbstpruefung nach der Erzeugung: 9 von 9 CRC PASS, 9 von 9 Laengen MATCH.
- Base64-Abbildung: base64 -d r45-6-stack_R0.zip.b64 > r45-6-stack_R0.zip ist exakt rekonstruierbar. Die SHA-256 der dekodierten ZIP-Bytes steht in STACK_ZIP_SHA256.txt und im Issue-Kommentar und ist aus Zirkularitaetsgruenden nicht im ZIP selbst enthalten.

## Konnektor-Grenze
push_files nimmt ausschliesslich Textinhalte an; binaere ZIP-Bytes sind direkt nicht hochladbar. Verifikation nach dem Push: Git-Blob-SHA-1 ueber alle Dateien am Return-Branch (eigener SHA-1-Stack, Format blob <len> NUL Bytes). Kein Redundanz-Readback frueherer HEADs.

## Eingangsintegritaet nach AXIOM-R45-6 (Operator-Stand, Paragraf 1 und 2.1)
GLM-Teillieferung R1 Partial R0A, 94.546 Bytes, Manifest 38/38, CRC 39/39. Zweiter Forschungsreturn, 952.953 Bytes, Manifest 13/13, CRC 14/14. Quellen- und Bindungsarchiv, 73.907 Bytes, 6/6 SHA-256-Eintraege. AXIOM-R45-5-Vorbericht 25.737 Bytes identisch mit Quellenarchiv. MISTRAL/VIBE-Forschungsbericht 13.783 Bytes eingelesen und gehasht. Beide ZIP-Sidecars stimmen ueberein. GLM-R1-Return ist ausdrueckliche Teillieferung: Programm A bearbeitet, B nicht abgeschlossen, C und D nicht begonnen. Receipt-Kette: 18 Receipts, eigene Genesis, interne Vorgaengerbeziehungen 17/17 MATCH, Modulidentitaet nur 4/18 (Kustodieluecke, kein automatischer wissenschaftlicher Fehler). Das interne R45-5-Paket wurde vom Operator erneut abgerufen: 11.199 Bytes, SHA-256 MATCH, 7/7 Manifest, 8/8 CRC. Die strittige Funktion certificate_and_witness() ist im GLM-Originalstack enthalten; der zweite Return pruefte das separate Skript r454_verify.py; beide Quellenidentitaeten sind getrennt zu fuehren.

NEXUS Ω OMEGA

