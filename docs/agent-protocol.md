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

## GitHub automated handoff

For external-agent or Cursor returns that are meant to continue through GitHub
without routine Operator mediation, submit a v1 handoff envelope under:

```text
research/pipeline/handoff/inbox/<HANDOFF_ID>/handoff.json
```

The fixed stage order is:

```text
INBOX
-> VALIDATE
-> BIND
-> RELAY
-> ACK
```

The envelope must bind payload bytes, Entry Receipt, Exit Receipt, File-Event
Ledger, Workflow-Event Ledger, token/continuation status and Authority-Gate
status. GitHub automation may emit bind/relay/ack receipts as workflow
artifacts or repository receipts, but it cannot merge, force-push, write main,
promote claims, promote foundations or validate a producer's own scientific
return.

## GitHub rollout preparation

For a validated handoff chain that needs a complete rollout package, submit or
consume a v1 rollout plan under:

```text
research/pipeline/rollout/plans/<ROLLOUT_ID>/rollout.json
```

The fixed preparation order is:

```text
PREPARE
-> VALIDATE
-> PACKAGE
-> AUTHORITY_GATE
-> ACK
```

Rollout preparation may emit readiness, authority-gate and ack receipts. It
must not execute merge, main-write, force-push, public release, deployment,
claim promotion, foundation promotion or integration authority without a
separate Operator receipt.

## Failure

Missing or divergent bytes are reported as `SOURCE_NOT_PRESENT`, `NOT_COMPUTABLE`, or `FAIL_CLOSED` as appropriate. Never reconstruct missing evidence from conversation order.
