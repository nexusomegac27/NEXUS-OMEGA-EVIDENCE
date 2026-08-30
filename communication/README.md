# Scientific Communication Ledger

This namespace implements the append-only, content-addressed ledger defined by the Open Science Agent Communication Manifest.

## Layout

```text
communication/
  index/v1/records.jsonl
  index/v1/latest.json
  objects/sha256/<aa>/<bb>/<sha256>/record.json
```

## Integrity model

Each scientific communication/provenance record is stored as exact UTF-8 bytes under its SHA-256 content address.

`records.jsonl` is an append-only discovery chain. Each line contains:

- a monotonically increasing sequence;
- exact record byte count and SHA-256;
- the content-addressed object path;
- `previous_index_line_sha256`, which is the SHA-256 of the exact prior JSONL line bytes **without** its trailing LF.

The current line does not contain its own digest. The next line binds it. `latest.json` exposes the current head-line digest.

Index lines use `NEXUS_SORTED_JSON_V1`: UTF-8 JSON with sorted object keys, compact separators, no BOM, and LF line termination. This is a deterministic repository profile but is **not claimed to be RFC 8785 JCS**.

## Append locally

```bash
python3 scripts/append_scientific_record.py path/to/record.json --root .
python3 scripts/validate_scientific_ledger.py --root .
```

The append tool performs no network write. Review, commit, push, release, and external witnessing remain separate governed operations.

## What the ledger can record

It can record events that are actually observed or receipted, including controlled human/AI communications, GitHub events, validator returns, file transfers, rehashes, corrections, and provider aggregate snapshots.

It cannot convert anonymous public GitHub access into identified events. When only aggregate telemetry or no telemetry exists, the record must use the corresponding observability class.

```text
NO_RECEIPT != NO_ACCESS
UNOBSERVABLE != ZERO
AGGREGATE != INDIVIDUAL_EVENT
HASH_CHAIN != SCIENTIFIC_TRUTH
```

## Genesis

Sequence 1 binds the verified GitHub merge event for Manifest PR #2. It is a provenance/governance record only, not an independent validation of the manifest's scientific content.

## Governance

```text
CLAIM_CEILING = C1
CLAIM_PROMOTION = FALSE
FOUNDATION_PROMOTION = FALSE
INTEGRATION_AUTHORITY = NONE
```
