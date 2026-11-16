# NEXUS OMEGA R31 — Deep Research: Framework-wide evidence-bound publication reconciliation

OBJECT = NEXUS_OMEGA_AXIOM_R31_FRAMEWORK_WIDE_VERIFIED_PUBLICATION_RECONCILIATION_DEEP_RESEARCH_20261116_R0
DATE = 2026-11-16
SCOPE = CROSS_FRAMEWORK_PROVENANCE_PLUS_PUBLICATION_CONSISTENCY_RESEARCH_AND_OFFLINE_PROTOTYPE
AUTHORITY = OPERATOR_ALEXANDER_VIA_AXIOM
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
CLAIM_PROMOTION = NO
PREDECESSOR_R30 = CLOSED_C1_HISTORICAL_CHECKPOINT
PREDECESSOR_BODYTWIN = NEXUS_OMEGA_CURSOR_BODYTWIN_C1_PROGRESS_WWW_DEPLOY_RETURN_20261115_R0
OPERATOR_GOAL = EVERY_VERIFIED_PUBLICATION_RELEVANT_FRAMEWORK_SURFACE_IS_UPDATED_OR_EXPLICITLY_HELD_WITH_REASON
NEW_RUNTIME_AUTHORITY = NO
PR_MERGE = NO
HOSTINGER_WRITE = NO
OPPO_CAPTURE = NOT_AUTHORIZED
EXTERNAL_ACTOR_WRITE = DENY

## A. Problem and observed NEXUS counterexample

The Operator reported a visually stagnant BodyTwin page despite extensive scientific C1 work since September. AXIOM prepared public progress PR #361, whose offline tests (13/13) and 9/9 GitHub checks were independently read on its pinned HEAD `f4cb682f34dd72b9e0d7132cac7f5c6e8e67537b`. Cursor subsequently returned `LIVE_WWW_PASS_C1_WITH_CAVEATS` after a reported Hostinger scoped SCP four-file release and repeat GET checks.

On 2026-11-16, a separate read-only Exa URL fetch observed:
- `https://www.nexus-mobile.de/bodytwin/updates/`: actual dated November 15 timeline visible.
- `https://www.nexus-mobile.de/bodytwin/updates/events.json`: 5 objects present; crucially **historical candidate fields remain `published_live=false` and `release_status=PUBLICATION_CANDIDATE_NOT_HOSTINGER_VERIFIED` despite URL live availability.** These fields are not a post-deploy independent witness.
- `https://www.nexus-mobile.de/bodytwin/live/current.json`: producer `seq=2405` `run_utc=2026-11-16T05:05:03Z` `interval_seconds=300` `source_changed=false` `last_change_utc=2026-11-07T20:50:02Z`; `bodytwin.validated=NO`; consent remains OPEN.
- `https://www.nexus-mobile.de/bodytwin/`: original symbolic Soft-View remains reachable in fetched content.

AXIOM did NOT independently rehash remote bytes, directly attest HTTP 200 for each GET, or collect a 320/390/768/1280 browser DOM/CSS witness in this research turn. Cursor's report of exact HTTP statuses and SHA256 is **producer-reported** until independently observed with exact transport bytes. The user's pasted November 15 6146B Cursor return ZIP was not attached in this turn; its reported hash is not a second-party rehash.

**First R31 negative control:** self-hosted status `seq` advancing while `source_changed=false` must NOT imply new science. Second: publicly reachable `/updates/` with author-time `published_live=false` must be classified `HISTORICAL_METADATA_DRIFT`, not silently overwritten or treated as proof of a failed live deployment. The publication receipt should be a new independently verified object attached to the immutable release.

## B. Rigorous separation of six distinct truth/evidence domains

1. **Science adjudication:** C1 descriptive observations and limitations. Falsification and uncertainty remain; SHA MATCH does not prove truth.
2. **Source/provenance:** exact original bytes/commit/dependency/build/process; independent digest and verified attestation when supported.
3. **Authorization:** bounded owner approval, target-scoped rights, expiry and genuine external principal. One reviewer's signature cannot grant production authority.
4. **Deployment:** the hosting system actually received exact desired bytes; GitHub PR, checks or Hostinger shell command alone do not imply public success.
5. **Publication witness:** independently obtained HTTP response bytes, correct MIME, DOM, routes and freshness observed after deployment.
6. **Consumer synchronization:** every relevant registered surface has processed that verified release version; private data stays private; unrelated pages are not force-updated.

Never flatten these six into one `PASS`; never infer science validity from green code CI, public HTTP, popularity, or externally self-declared consensus. Promotion to C2 is outside R31.

## C. External primary-source methods evaluated (online, as of 2026-11-16)

| Method | Original primary specification/documentation | What it actually solves | What it does NOT prove |
|---|---|---|---|
| SLSA v1.2 Build Provenance | https://slsa.dev/spec/v1.2/build-provenance | Build subject digest, builder ID, parameters, resolved dependencies; verification expectations | Scientific validity or www presence |
| in-toto Attestation Framework | https://github.com/in-toto/attestation/blob/main/spec/v1/statement.md | Subject digest and typed predicate; chain of authorized functions | Reviewer's truth or operator's consent by itself |
| W3C PROV-O | https://www.w3.org/TR/prov-o/ | Entity–Activity–Agent lineage; `wasDerivedFrom`, `wasGeneratedBy` | Signed trust or last-mile deployment |
| Sigstore Cosign/Fulcio/Rekor | https://docs.sigstore.dev/quickstart/quickstart-cosign/ | Short-lived signing identity, bundle, timestamp/transparency-log inclusion | No scientific adjudication; depends on approved signer/builder policy |
| CloudEvents 1.0.x | https://github.com/cloudevents/spec/blob/main/cloudevents/spec.md | Portable `id`, `source`, `type`, `specversion` identifiers and event routing | Event delivery guarantees, identity authority, or content integrity alone |
| Transactional Outbox | https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html | Avoid dual-write gap between committed release record and queued notification | Exactly-once external effects; consumers need idempotence |
| Debezium Outbox Router | https://debezium.io/documentation/reference/stable/transformations/outbox-event-router.html | Optional CDC relay of committed outbox rows, ID/key/partition order | Necessary dependency for a one-host pilot |
| GitOps reconciliation / Argo CD | https://argo-cd.readthedocs.io/en/stable/user-guide/auto_sync/ | Desired-versus-actual state comparison; self-healing/pruning can be enabled separately | A Hostinger shared-host deployment need not run Kubernetes |
| TUF security principles | https://theupdateframework.io/docs/security/ | Rollback/freeze/mix-and-match resistance, bounded trust keys/roles, metadata freshness | A deployment source digest automatically authorized by producer |
| RFC 9110 HTTP semantics | https://www.rfc-editor.org/rfc/rfc9110 | Conditional GET with `If-None-Match`, ETag and conditional changes avoiding lost updates | A proxy's response is independently attested without a distinct trust path |
| RFC 8785 JSON canonicalization | https://www.rfc-editor.org/rfc/rfc8785 | Cross-language deterministic JSON bytes for signature payloads | Generic `json.dumps(sort_keys=True)` is NOT RFC 8785 |
| GitHub Webhook verification | https://docs.github.com/en/webhooks/using-webhooks/validating-webhook-deliveries | Raw-payload HMAC verification and event delivery idempotence | Webhook arrival is not authorized publish or complete delivery |
| GitHub delivery best practices | https://docs.github.com/en/webhooks/using-webhooks/best-practices-for-using-webhooks | Dedupe `X-GitHub-Delivery`, 10s ack, enqueue/retry/redelivery | Exactly-once business effect |
| OpenTelemetry context propagation | https://opentelemetry.io/docs/concepts/context-propagation/ | Trace ID/span ID linkage from source to witness for diagnosis | Independent authentication or evidence validity |

**Research conclusion:** No single existing standard independently solves NEXUS's entire scientific adjudication → consent → multi-surface release → outside WWW observation chain. Combining **typed, signed provenance**, **transactional event delivery**, **a state reconciler**, **independent release witnesses**, and **fail-closed governance** addresses distinct failure modes. This is a source-grounded architecture proposal, NOT tested proof of end-to-end reliability.

## D. Counterfactual architectural evaluation

A. Direct GitHub-to-Hostinger webhook only: low complexity/latency; lost callback, repeated delivery, unverified browser, stale page and mistaken PR→live promotion remain. REJECT as authority-of-record.

B. Five-minute polling/Cron only: modest cost, useful anti-entropy fallback, but timer tick is not content change and can conceal persistent auth/deploy failures. RETAIN as periodic verifier, not status authority.

C. **Minimal four-gate provenance and release outbox + idempotent state reconciler + independent HTTP/DOM witness + anti-entropy polling.** RECOMMENDED R31 foundation. Durable SQLite or PostgreSQL transactional outbox (SQLite for single-host pilot); CloudEvents wire; source and signature validators as swappable adapters; declarative surface subscriptions. Use fixed 300s anti-entropy polling initially as **engineering test choice**, not an observed latency SLA.

D. Kafka/Debezium full CDC, Argo CD/Kubernetes, TUF end-to-end roles: capable but introduces avoidable operational and secret/key complexity before a single-host proven path. HOLD_OPTIONAL; assess only if actual throughput, actor concurrency or trust requirements demand them. No vendor lock or platform-wide dependency permitted.

## E. R31 framework publication graph and trust boundaries

```text
verified evidence (source bytes + independent scientific review)
 -> owner-scoped C1 public-safe release decision (authentic operator principal)
 -> immutable release manifest (source commit, binary SHA, privacy class, routes, claim ceiling)
 -> durable DB outbox record (same DB transaction)
 -> signed CloudEvent dispatch (webhook low latency + 300 s anti-entropy)
 -> deterministic route/topic subscription reducer with monotonic release_seq
 -> per-route staged, reversible deploy by authorized operator/Cursor adapter
 -> remote SHA256 + independent HTTP and Browser witness (different trust principal)
 -> signed observation receipt
 -> reconciliation: observed vs desired vs prior state; no science promotion
 -> protected public metadata update and internal status/alert (stale or mismatch)
```

The event must contain only public-safe metadata and hashes, not raw OPPO IMU, private records, passwords, screenshots of patients, private source originals, device identifiers or secret tokens. Registries are explicit: BodyTwin, Homepage, Forum, ORBIS/Astra, Research, Internal Memory. Only *subscribed/relevant* surfaces get a release; "update all" never means leaking a research lane or automatically editing all URLs.

## F. Source-derived state machine and scientific falsifiers

States: `DISCOVERED` → `SOURCE_BOUND` → `REVIEWED_C1` → `OWNER_AUTHORIZED` → `DEPLOYED_REPORTED` → `WWW_OBSERVED` → `RECONCILED`.
Terminal/errors: `HOLD_PRIVATE`, `HOLD_UNVERIFIED_SOURCE`, `HOLD_NO_SIGNATURE`, `HOLD_ROLLBACK`, `HOLD_EQUIVOCATION`, `HOLD_WWW_MISMATCH`, `HOLD_STALE_METADATA`, `NO_RELEVANT_SUBSCRIPTION`.

Experiment manifest (design-only, one round, prereg before any live run):
- F01 unsigned/fake operator grant; F02 valid grant wrong target route; F03 public source with private OPPO marker; F04 duplicate/replayed GitHub webhook; F05 reordered version/rollback; F06 same sequence, new digest equivocation; F07 HTTP 200 wrong bytes; F08 HTML MIME returned as JSON; F09 duplicate or inconsistent WWW witnesses; F10 status feed sequence advances without content change; F11 published_live=false while website independently observed; F12 observer shares the publisher principal; F13 review digest missing/unknown; F14 full public claim promotion from C1 to C2; F15 HTTP success but DOM/viewer regression; F16 partial multi-surface failure; F17 offline/timeout and backoff; F18 timebase/future timestamp; F19 content-addressed raw-vs-LF drift; F20 owner consent withdrawn between staging and apply.

Run each on independent positive and negative controls; record actual executed denominators and observed raw SHA, error class, clock uncertainty, source provenance and rollback evidence. Source-only unit tests may cover *reducer logic*, not Hostinger runtime behavior.

## G. Measurement protocol (candidate thresholds, NOT achieved results)

- **Coverage:** correctly reconciled eligible (release, surface) pairs / all registered eligible pairs. Requirement target for pilot: 100% in controlled synthetic fixture set, not claimed production.
- **False promotion:** unauthorized/private/unsigned releases marked `RECONCILED` / number of such negative tests. Required target 0 in adversarial controls.
- **Latency:** `t(WWW independent witness) - t(owner authorization)` per release, percentiles and range; initial pilot objective p95 under 15 minutes. *Not measured.*
- **Staleness:** time since last independently witnessed deployed artifact change, not since producer seq tick; classify 300s check when no new source.
- **Durability:** missing/duplicate/out-of-order event recovery counts, no lost queued release, no manual backfills represented as fresh science.
- **Consistency:** number of inter-surface release digest/version mismatches; no mixed epoch or partial release reported as whole framework `PASS`.
- **Privacy:** public payload DLP deny result, no private artifact transference.
- **Operator labor:** count manual interventions per 100 eligible (release,surface) pairs versus baseline. The historic 90%-automation objective is a target, not proven.
- **Control:** compare webhook-only vs outbox+reconciliation with randomized packet loss, duplicated delivery and exact same frozen release corpus; paired comparison with confidence intervals and precommitted stopping rule. No invented effect size.

## H. Existing offline code: exact epistemic status

`src/r31_reconcile.py` is a **read-only, pure-Python, no-runtime/no-network** state reducer: CloudEvents-like envelope, bounded strict JSON, SHA256 (local sorted JSON subset; explicitly NOT RFC 8785), HMAC-of-synthetic-grant and independent-witness test adapter, owner grant scopes, per-route subscription matching, sequence/rollback guard, witness conflicts, stale static metadata flags and absence-of-witness hold. It is neither an operational deployment engine nor a full SLSA/TUF/Sigstore implementation.

Signing test fixtures contain deliberately **nonproduction, public test keys** and cannot grant real publication. In production adopt operator-approved public-key/Sigstore signer policy, receiver key management and a genuinely independent HTTP/browser adapter before any run. No code in R31 uses the BodyTwin private R29 runtime, real sensors or Hostinger secrets.

## I. Evidence ceilings and operator decision

Scientific model = falsifiable C1 engineering candidate. It cannot promote `BODYTWIN_VALIDATED=NO`, `CONSENT_BIND=OPEN`, R30 source-only 3/3, PR#361 CI success or a self-hosted timestamp to physical truth. Previous R30 scientific review is independent and untouched.

**One path forward:** Cursor tests the exact R31 source candidate in an isolated staging copy; builds a real durable outbox and *read-only external witness first*, binds deployment recipient list and release authorization, runs adversarial F01–F20 with one matrix and one return. No automatic cross-framework write until release grant/rollback verified, no new research loop and no C2.

R31 STATUS = DEEP_RESEARCH_COMPLETE_SOURCE_ONLY · OFFLINE_IMPLEMENTATION_CANDIDATE · END_TO_END_RUNTIME_NOT_ESTABLISHED
NEXT = ONE_BOUNDED_CURSOR_OUTBOX_AND_INDEPENDENT_WITNESS_STAGING_VALIDATION
