# External Agent Protocol v1

## Consume

1. Fetch `index/v1/latest.json` from the public repository or Pages view.
2. Fetch the referenced manifest from the immutable release or content-addressed path.
3. Reject duplicate JSON keys; canonicalize according to RFC 8785 where applicable.
4. Verify the asset byte count and SHA-256.
5. Verify every declared semantic scope separately.
6. Verify the GitHub immutable release and release asset.
7. Verify at least one independent witness: Zenodo DOI or Software Heritage SWHID.
8. Preserve every caveat and the C1 claim ceiling.
9. Begin semantic work only after the preceding checks pass.

## Return

Publish a separate content-addressed result and return only:

```text
RETURN_MANIFEST_URL
RETURN_MANIFEST_SHA256
RETURN_ASSET_SHA256
RETURN_ANCHOR_LEVEL
```

Chat content is never a substitute for externally retrieved bytes.

## Failure

Missing or divergent bytes are reported as `SOURCE_NOT_PRESENT`, `NOT_COMPUTABLE`, or `FAIL_CLOSED` as appropriate. Never reconstruct missing evidence from conversation order.
