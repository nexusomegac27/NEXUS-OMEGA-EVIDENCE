# TRANSFER_NOTE - binaerer Transport (ZIP als Base64)

GitHub-Commits in dieser Umgebung sind textbasiert. Das vollstaendige ZIP-Archiv

    R46_4_REFERENCE_METROLOGY_RETURN_20261127_GLM_R1.zip

liegt daher als textuelles Transportfile

    R46_4_REFERENCE_METROLOGY_RETURN_20261127_GLM_R1.zip.b64

(7-Bit-Base64, Zeilenlaenge 76, LF) plus Sidecar-Pruefsumme

    R46_4_REFERENCE_METROLOGY_RETURN_20261127_GLM_R1.zip.sha256

in diesem Verzeichnis.

## Wiederherstellung

    base64 -d R46_4_REFERENCE_METROLOGY_RETURN_20261127_GLM_R1.zip.b64 \
      > R46_4_REFERENCE_METROLOGY_RETURN_20261127_GLM_R1.zip

## Verifikation

    sha256sum R46_4_REFERENCE_METROLOGY_RETURN_20261127_GLM_R1.zip
    # erwarteter Wert (Sidecar):
    55f4ae1fb0e9aa82353174a9585c46da70adda46b58977e68b75229fa5f90eb1

ZIP-Eigenschaften: store-only (keine Kompression), fixer DOS-Timestamp
2026-11-27 12:00:00, 13 Mitglieder, CRC-selbstverifiziert (13/13).
Die 12 inhaltlichen Mitglieder entsprechen Byte fuer Byte den im selben
Verzeichnis abgelegten Einzeldateien; Pruefsummen in 99_SHA256SUMS.txt.
