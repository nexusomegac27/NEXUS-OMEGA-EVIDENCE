# 02 · INTEGRITAET UND METHODE

## Eigene Krypto-Primitive (Sandbox)
- UTF-8-Encoder und SHA-256 als eigener Stack, weil TextEncoder und crypto.subtle in dieser Umgebung unzureichend verfuegbar sind. Selbsttest: SHA-256(abc) = ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad.
- SHA-1 als eigener Stack fuer die Git-Blob-Verifikation. Selbsttest SHA-1(abc) = a9993e364706816aba3e25717850c26c9cd0d89d.
- CRC-32 (IEEE, reflektiert) fuer die ZIP-Erzeugung. Selbsttest CRC32(123456789) = cbf43926.

## ZIP-Erzeugung fuer diesen Return
- Das R45-5-Stack-ZIP wurde byte-exakt in der Sandbox erzeugt: Methode STORE ohne Kompression, feste DOS-Zeit 2026-11-26 12:00, Mitglieder 00 bis 08.
- Nach der Erzeugung wurde das ZIP in derselben Sitzung wieder geparst: alle CRC-32-Werte gegen die Originalbytes geprueft, Bytezahlen verglichen. Ergebnis: 9 von 9 CRC PASS, 9 von 9 Laengen MATCH.
- Base64-Abbildung: b64(zip) = r45-5-stack_R0_1.zip.b64 ist exakt dekodierbar. Dekodierung: base64 -d r45-5-stack_R0_1.zip.b64 > r45-5-stack_R0_1.zip. Die SHA-256 der dekodierten ZIP-Bytes steht in STACK_ZIP_SHA256.txt und im Issue-Kommentar. Diese Bindung kann nicht im Zip selbst stehen, weil ein Dokument sein eigenes aeusseres Hash nicht enthalten kann.

## Konnektor-Grenze (dokumentiert)
- push_files ueber den GitHub-Konnektor nimmt ausschliesslich Textinhalte entgegen; binaere ZIP-Bytes sind direkt nicht hochladbar. Deshalb laeuft die Bereitstellung als Base64-Sidecar.
- Verifikation nach dem Push: Git-Blob-SHA-1 ueber alle Dateien am Return-Branch (eigener SHA-1-Stack, Format blob <len> NUL Bytes). Kein Redundanz-Readback des R45-5-HEAD, weil dieser bereits von einer frueheren MISTRAL/VIBE-Sitzung byte-exakt readbacked wurde.

## Eingangsintegritaet nach AXIOM-R45-5 (Operator-Stand, Paragraf 1 und 11)
GLM-Stack 1.021.372 Bytes Sidecar MATCH; GLM-Manifest 55/55; GLM-Archiv 56/56 CRC; zweiter Return 853.255 Bytes Sidecar MATCH; zweites Manifest 14/14; zweites Archiv 15/15 CRC; eingebettetes AXIOM-R45-4-R1-Paket 37.863 Bytes MATCH; Receipt-Kette Sequenz 72 bis 93, 22/22; historische Skriptidentitaeten 11/22.

NEXUS Ω OMEGA

