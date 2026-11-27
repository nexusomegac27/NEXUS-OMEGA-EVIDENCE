# Sealed transfer — decode instructions

OBJECT = NEXUS_OMEGA_R45_9_EXPERT_RETURN_INDEPENDENT_20261127_R1

The expert return ZIP is binary and this connector writes text only. The byte-exact ZIP is
published here as base64 in two parts. Reconstruct and verify:

```
cat R45_9_EXPERT_RETURN_20261127_R1.zip.b64.part1 \
    R45_9_EXPERT_RETURN_20261127_R1.zip.b64.part2 > R45_9_EXPERT_RETURN_20261127_R1.zip.b64
base64 -d R45_9_EXPERT_RETURN_20261127_R1.zip.b64 > R45_9_EXPERT_RETURN_20261127_R1.zip
sha256sum R45_9_EXPERT_RETURN_20261127_R1.zip
diff <(sha256sum R45_9_EXPERT_RETURN_20261127_R1.zip) R45_9_EXPERT_RETURN_20261127_R1.zip.sha256
```

Expected:

```
ZIP_BYTES  = 44165
ZIP_SHA256 = 6c958dd7d343d596d73f2f44245307c0b1dc355ea2f1ffe8b9d6c4393e7f6776
MEMBERS    = 32 (31 manifest entries + MANIFEST.json itself)
CRC        = PASS (all members)
MANIFEST   = 31_OF_31_MATCH (loose member rehash)
RECEIPTS   = chain R00..R05, GENESIS anchored on external hashes (see RECEIPTS/R00)
```

Any hash deviation means the transfer is corrupted: do not adjudicate on a mismatched byte stream.
Sidecar: `R45_9_EXPERT_RETURN_20261127_R1.zip.sha256` (same directory).
