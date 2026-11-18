# R35 — WWW structured entrypoint + archive migration plan (proposal, not execute)
OBJECT = NEXUS_OMEGA_R35_WWW_STRUCTURED_ENTRYPOINT_ARCHIVAL_MIGRATION_BLUEPRINT_20261118_R0
EXECUTION_AUTHORIZED = NO
C1_ONLY = YES
WWW_TARGET = https://www.nexus-mobile.de/
ORIGINAL_R30_R35 = NO_MUTATION
PRODUCTION_DEPLOY = NOT_EXECUTED

## Page contract
/ : short orientation, current focus and dated latest approved snapshot. One outstanding OPPO/BODYTWIN gate, link to full current scientific track; open questions and archive each a clear independent navigation. Keep secondary system/visual demos below the fold, not hero statements of proof.
/research/current/ : curated current approved public-safe records (not raw feed). Each has stable id, exact last verified date, evidence level, explicit open gates and changelog to predecessor.
/research/open/ : current negations, blockers and counterexamples with their active risk and source anchors.
/research/archive/ : paginated immutable publication index with bounded filters by topic, year, archive reason and source ID. Search and graph traversal strictly bounded.
/research/record/{immutable-id}/ : stable details, historical/active state, original source and hash, current successor link, corrective reason, all open gates.
/research/changes/ : chronological append-only publication transitions; not a moving social feed.
/research/sources/ : quarantined external discovery may be browsed as SOURCE_CANDIDATE; never presented as approved research.
/status/ : technical and data health, separate from visitor-facing scientific consensus.

## Minimal machine-readable interface
One publications/index.json for approved current pointers and count metadata; one publications/archive-index.json for archive metadata; per-record publications/events/{id}.json with versioned schema and digest; one signed/deployment-linked publications/release-manifest.json built from exact source custody. Use explicit fields status, evidence_class, source_generated_at, fetched_at, published_at, archived_at, supersedes, refutes, corrects, derived_from, current_pointer, privacy_class, source_sha256. No blind 301 for archived historical pages; safe canonical links in page UI rather than silent source substitution.
No direct linkage to public record if source is PRIVATE_RESTRICTED; use separate public-safe metadata with no reconstructable private CAS pointer.

## Phased migration (Cursor may plan; cannot run until distinct scoped authorization)
P0 Inventory all actual WWW paths, routes, backlinks, current release files, accessible original sources and their SHA. Do not guess or invent historical publication count.
P1 Build append-only source/transition manifest and versioned schema for existing public-safe records. Preserve the pre-migration exact bytes separately; correct absent evidence as SOURCE_GAP, not fabricated.
P2 Generate static, offline-safe entry, current, open and archive views against pinned manifests. Do not silently downgrade PUBLIC to PRIVATE or vice versa.
P3 Test source-exact links, stale data quarantine, contradictory titles/status badges, mobile/accessibility, XSS, DLP, search limits, failed current manifest, redirects, all old backlinks. Negative fixtures: contradictory latest pointers, circular supersedes, missing successors, revoked claims, old generated_at/new fetched_at, private CAS hash in public metadata.
P4 Independent second-party readback of full new build and rollback plan, then only explicit scoped reversible WWW deployment under operator permission.
P5 Distinct HTTP and browser witness from outside origin, compare live root and required page snapshots, archive navigation, no private metadata; evidence of PR merge is not a deploy witness.
P6 Rollback reversible if any active historical status loses provenance or privacy gate fails; keep original old release and audit receipt immutable.

## KPIs: scientific transparency instead of vanity
- Fraction of active publications with exact parent, source and evidence class.
- Fraction of archived records with original and current successor/reason accessible (when successor exists).
- Number of public old links broken postmigration (target zero).
- Number of stale/unverified statuses presented as current (target zero).
- Current unresolved negative results visible within one visitor route from homepage (target all scoped current negatives).
- Search request ceilings, private hash leakage rate (target zero), mobile accessibility. Time-to-find correct OPPO/BodyTwin current status should be tested on novice tasks, not presumed.

## Separation of responsibility
AXIOM = scientific doctrine, epistemic scope and adjudication.
CURSOR = sandbox architecture, PR staging, execution evidence, rollback, only after specific operator-scoped order.
EXTERNAL EXPERTS = independent information architecture/privacy/accessibility challenge; no write rights by implication.
R35 OPPO/BODYTWIN = unchanged primary scientific research; website work is separate support lane.
