# Research pipeline event store

One lifecycle event = one immutable JSON file.

Canonical path:

```text
research/pipeline/events/YYYY/MM/DD/<UTC_TIMESTAMP>_<EVENT_ID>.json
```

Why one event per file:

- avoids a shared mutable JSONL append hotspot;
- makes Git review/diff simple;
- preserves exact historical event bytes;
- permits deterministic index rebuilding;
- supports parallel package activity without requiring all writers to append one shared ledger file.

Event files are never edited after merge. Corrections are new `CORRECTION` events.
