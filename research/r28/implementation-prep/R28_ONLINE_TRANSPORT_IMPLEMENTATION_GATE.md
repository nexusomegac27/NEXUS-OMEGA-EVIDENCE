# R28 online transport implementation gate

This gate prepares the transition from local byte verification to a real online handshake without selecting a provider prematurely.

## Mandatory preflight

Every participating agent/session must declare and, where possible, **measure**:

```text
FILE_BYTE_ACCESS
BYTE_HASHING
ARCHIVE_INSPECTION
CODE_EXECUTION
SANDBOX_OR_VM
NETWORK_EGRESS
HTTP_DOWNLOAD
HTTP_UPLOAD
API_CALLS
PERSISTENT_STORAGE
GIT_READ
GIT_WRITE
HOSTINGER_READ
HOSTINGER_WRITE
MAX_FILE_SIZE
KNOWN_SESSION_LIMITS
```

```text
DECLARED_CAPABILITY != MEASURED_CAPABILITY
```

If a task requires a capability that is not measured as available, route the task elsewhere or mark `HOLD_CAPABILITY_GAP`.

## Backend candidates

The first online transport evaluation must compare at least:

- operator-controlled Hostinger gate;
- GitHub transport;
- OCI/ORAS registry transport;
- one provider-neutral object backend (for example an S3-compatible store).

No candidate is canonical by default.

## Required real handshake

```text
CAPABILITY_PREFLIGHT
→ SENDER_MANIFEST
→ SOURCE_BYTES
→ ONLINE_TRANSFER
→ RECEIVER_BYTE_ACCESS
→ RECEIVER_REHASH
→ RECEIVER_RECEIPT
→ RECEIPT_RETURN
→ SENDER_RECEIPT_VERIFICATION
```

`PASS` requires all stages to be evidenced. A URL, copied hash, chat acknowledgement, or file name is not a real handshake.

## Security boundary

```text
OWN_GATE = ALLOWED
OWN_POLICY = ALLOWED
OWN_CRYPTOGRAPHY = NO
```

Use standard TLS/authentication/signature primitives. Keep secrets out of code, Git, receipts and public logs. Upload intake must address traversal, decompression bombs, partial upload, replay, duplicate IDs, MIME confusion, size limits and hash mismatch.

## Provider-removal test

After a backend passes the online handshake, repeat independent verification with that provider removed from the verification path. Artifact identity, provenance references and receipt interpretation must remain reconstructible.

```text
BACKEND_CHANGE != ARTIFACT_IDENTITY_CHANGE
```
