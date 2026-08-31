# Scientific evidence object store

`objects/` contains content-addressed scientific evidence assets and manifests. It is paired with `index/`.

Canonical layout:

```text
objects/sha256/<first2>/<next2>/<full_sha256>/...
```

Do not place communication ledger records here; those use `communication/objects/`.
