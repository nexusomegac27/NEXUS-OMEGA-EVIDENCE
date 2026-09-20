# FILE_02 Hash Erratum (append-only)

```text
OBJECT = NEXUS_OMEGA_CURSOR_ASTRATIS_X_R2_FILE_02_HASH_ERRATUM_20260920_R0
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
SUPERSEDES = NONE
SUPPLEMENTS = packaged 01_R5_PHYSICAL_REHASH_RECEIPT.md inside FINAL ZIP e19f149c…
FINAL_ZIP_MUTATION = NO
```

## Defect

Inside the final ZIP, packaged copies of `01_R5_PHYSICAL_REHASH_RECEIPT.md` contain a FILE_02 hash field with **91 hex characters** (invalid as SHA-256). Independent inspection shows concatenated fragments of FILE_02 and FILE_01 digests.

## Correct physical bind (R1 archive, independent rehash)

| Field | Value |
|---|---|
| Name | `NEXUS_Delay-Tolerant Epistemic Provenance Network (DT-EPN).txt` |
| Bytes | 23644 |
| SHA256 | `c72fb3ede7701b5f8cb4a2bd0cd92cfebbb75e3e3b430b19d4e8734873b8ff23` |

R1 concat 01→02→03→04 remains `66d6929178d0cd9c4ed2ef83a3f7dd33f08cbde726c41e7a470b929d5894402d` (84676 bytes).

## Must-not-infer

- This erratum does **not** rewrite the sealed final ZIP.
- This erratum does **not** close R7.
- This erratum does **not** authorize push.
