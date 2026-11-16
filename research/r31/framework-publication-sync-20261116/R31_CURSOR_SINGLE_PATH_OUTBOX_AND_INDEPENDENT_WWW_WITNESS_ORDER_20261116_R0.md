# R31 — Single bounded Cursor execution: publication outbox and independent WWW witness (STAGING ONLY)

OBJECT = NEXUS_OMEGA_AXIOM_CURSOR_R31_VERIFIED_PUBLICATION_RECONCILIATION_SINGLE_PATH_ORDER_20261116_R0
AUTHORITY = OPERATOR_ALEXANDER_VIA_AXIOM
PREDECESSOR_BODYTWIN = LIVE_WWW_PASS_C1_WITH_CAVEATS_SOURCE_REPORTED_PLUS_INDEPENDENT_PUBLIC_CONTENT_FETCH
PREDECESSOR_R30 = CLOSED_NO_REOPEN
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
RESEARCH_ROOT = research/r31/framework-publication-sync-20261116/
EXTERNAL_GITHUB_WRITE = DENY_EMPTY_ALLOWLIST
IMU_OPPO_CAPTURE = NOT_AUTHORIZED
HOSTINGER_REAL_WRITE_THIS_ORDER = NO
PUBLICATION_NEW_CLAIM_PROMOTION = NO
RUNTIME = STAGING_TESTS_ONLY_WITH_OWNER_BOUND_SOURCE
RESEARCH_LOOP = NO

## One objective

Stop stale/unsynchronized NEXUS scientific displays even when GitHub/Cursor/Hostinger each reports a partial PASS. Build and falsify a minimal durable synchronization adapter, independent of the existing BodyTwin viewer, R29/R30 sandbox, Forum, ORBIS, and private sensor pipeline.

Mandatory source readback on exact GitHub R31 head: `R31_AXIOM_DEEP_RESEARCH_SOURCE_AND_FALSIFICATION_20261116_R0.md`, `R31_FRAMEWORK_PUBLICATION_GRAPH_AND_GATE_CONTRACT_V1.json`, `src/r31_reconcile.py`, `tests/test_r31_reconcile.py` and this order. Verify exact original file hashes with local SHA256. No substitution or YAML-based virtual success.

## One implementation path, no parallel platform-sprawl

1. **Source verification**: check R31 PR HEAD, independently rehash each file, run all R31 Python 3.13 offline tests. Read-only GitHub fetch. Validate no real keys committed, no private original bytes.
2. **Source adapters**: define owner-controlled, scoped and authenticated `REVIEWED_C1` scientific status, a separate `OWNER_AUTHORIZED` release, never automatic C2, and a typed CloudEvents 1.0 metadata envelope. The included HMAC fixture adapter is demonstration only and never used to authorize production. Real signature verification must use genuinely authenticated operator identity/key, separate observer principal, TTL/revocation, and encrypted secret store. Favor Sigstore/in-toto if technically feasible; document any unproven issuer/identity.
3. **Durable outbox**: prototype atomic release record and notification record in ONE local SQLite transaction with a unique event ID; no HTTP delivery side effects from the DB transaction. Add dedupe, monotonic per-surface seq, retry backoff and terminal errors. SQLite/stdlib first, no mandatory Kafka/Redis/Debezium/Kubernetes.
4. **Registered surface fanout**: only confirmed subscribed routes, public metadata only. Project ledger per (release_id, surface_id) and record changed source bytes separately from 300s feed ticks. Preserve static historical `published_live=false` as provenance of creation; do NOT overwrite to fabricate an earlier live witness. Make a new separate immutable `release_witness` (event + remote byte digest + timestamp + independent principal).
5. **Independent observer**: build and run on an operator-authorized disposable staging host, fetching ONLY allowlisted public endpoints; record status, MIME, exact raw SHA256 and browser DOM witness if capable. A GET with no independent captured bytes is `HTTP_CONTENT_OBSERVED`, not `MATCH_RAW`. Agent cannot self-ACK its own deploy as independent witness. Verify the changed exact output against its source-derived intended release digest before claiming `WWW_OBSERVED`.
6. **Reconciliation**: periodic 300s anti-entropy (engineering default, not measured) plus authenticated webhook-driven low-latency wake-up. Use a lease/lock; no concurrent double-write. If queue delivery is delayed or lost, polling detects missing or stale release. If duplicate: idempotent; if rollback, hidden changes, false claim, observer conflict or permission mismatch: `HOLD` + source-bound diagnostics.
7. **Adversarial protocol**: execute F01–F20 from the R31 report, with positive and negative controls, exact bytes and counts. Freeze the executable stimuli, observation oracles, denominators, clock bounds and stopping rule BEFORE observing results. The 34 repository Python tests concern only reducer logic and are not F01–F20 measured Hostinger tests.
8. **One report**: return exact source & SHA256, SQLite proof (atomicity on injected crash), observer HTTP evidence under separate principal, 20× test statuses with null for NOT_RUN, false promotion counts, source changed vs heartbeat, two C1 public release types, scoped rollback/dedupe and the first measured time-to-visibility. If any real Hostinger access/gate is missing, return `STAGING_PASS_WWW_HOLD` with the precise blocker. No new research round or secret-bearing ZIP.

## Explicit R31 release conditions

- A verified and public-safe claim must have independent source-bound adjudication, authenticated owner release, exact target manifest, non-expired signer scopes, no private data, retained rollback and subscribed target route before deployment.
- Stage delivery only after authorization. Do not treat PR merge as direct WWW publish.
- Public success requires independent post-deploy source SHA256 plus browser witness; stale metadata must be reported as drift rather than overwritten.
- If a surface's semantic subscription is absent, do not update it merely to increase automation coverage.
- If real dependency unavailable, preserve a single reproducible offline proof and stop without perpetual HOLD/checkloop.

## Return

```text
OBJECT = NEXUS_OMEGA_CURSOR_R31_FRAMEWORK_PUBLICATION_STAGING_RETURN_20261116_R0
STATE = PASS_SCOPED_OFFLINE_AND_STAGING_C1 | HOLD_VERIFIED_GAP | REJECT_SECURITY_CAVEATS
SOURCE_HEAD = <40 hex>
OFFLINE_R31_TESTS = <observed passed/total>
OUTBOX_ATOMICITY = PASS|FAIL|NOT_RUN
REPLAY_DUPLICATE_NEGATIVE = PASS|FAIL|NOT_RUN
SIGNED_OPERATOR_GRANT = TEST_FIXTURE_ONLY|REAL_VERIFIED_WITH_AUTHORITY|NOT_RUN
EXTERNAL_WITNESS = TEST_FIXTURE_ONLY|INDEPENDENT_RAW_HTTP_WITNESS|NOT_RUN
R31_F01_F20 = <actually observed count / 20, not synthetic unit-test count>
WWW_PUBLICATION_NEW = NO
OPPO_CAPTURE = NO
BODYTWIN_VALIDATED = NO
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
CLAIM_PROMOTION = NO
NEXT = ONE_BOUNDED_FOLLOWUP_IMPLEMENTATION_DECISION
```

The R31 publication controller may later be deployed as an authorized service under an explicit rollout policy. This order does NOT itself authorize installation of long-running watchers, new Hostinger services, production keys, self-modifying framework logic or new external agents.
