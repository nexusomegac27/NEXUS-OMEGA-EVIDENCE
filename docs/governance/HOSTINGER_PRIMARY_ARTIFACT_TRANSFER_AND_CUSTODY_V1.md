# NEXUS OMEGA — Hostinger-first Artifact Transport, Custody & Verification V1

```text
OBJECT = NEXUS_OMEGA_OMEGA_HOSTINGER_PRIMARY_ARTIFACT_TRANSPORT_AND_CUSTODY_V1
DATE = 2026-10-10
AUTHORITY = OPERATOR_OMEGA
STATE = GOVERNANCE_CANDIDATE_PUBLIC_REPO_BRANCH_NOT_YET_HOSTINGER_BOUND
PRIORITY = AVOID_OPERATOR_DOWNLOAD_RELAY
PRIMARY_ARTIFACT_TRANSPORT = HOSTINGER_AUTHENTICATED_PRIVATE_STORAGE
SOURCE_CONTROL_AND_PUBLIC_SAFE_EVIDENCE = GITHUB
PRODUCTION_EXECUTION_AND_HOST_ACCESS = CURSOR_PRAXIS
AXIOM = SOFT_GOVERNANCE_SOURCE_AUDIT_INDEPENDENT_ADJUDICATION
EXTERNAL_EXPERT_TRANSPORT = RESTRICTED_BROKERED_INGRESS
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
R21_WWW_THREE_PROOFS = PENDING
R19_ORBIS_VISIBILITY = NOT_YET_VERIFIED
R20 = CLOSED_BY_OPERATOR_WITH_MATERIAL_CAVEATS
```

## 1. Operator Directive — binding upon source-exact acceptance

**No routine ZIP/MD/PDF/file download handoffs to the operator.** AXIOM, Cursor/PRAXIS and independent experts shall use the authorized Hostinger archive/transport and GitHub source/evidence trail. Downloads to the operator are an **exception for genuine physical necessity**, when an authenticated transport cannot work and an exact minimal package is unavoidable; the exception needs a short reason, minimal bytes, source SHA and retention plan. Do not invent a need to make the operator shuttle files between agents.

**Critical implementation fact:** The connected Hostinger AI Builder Agentic-mode integration does **not** provide an SCP/SFTP or private file-storage interface for the existing `nexus-mobile.de` site in this session. The account's Builder site list returned `[]`. This document does not constitute a Hostinger write, archive existence witness, or transport activation. Cursor must bind an actually authorized and tested host interface; never assume Agentic Builder manages the existing SCP-hosted site. No new website creation.

## 2. Clear responsibility split

- **Hostinger = artifact data plane:** approved primary byte storage, signed/brokered ingress, immutable revision archive, private exact-byte reads, stage/production readback when duly authorized.
- **GitHub = source & custody control plane:** ordered code, versioned schemas, public-safe manifests, causal PR/commit history, validation reports with no protected paths or credentials. `NEXUS-OMEGA-EVIDENCE` is an **evidence repo**, not proof of the site's source repository.
- **Cursor/PRAXIS = host interface / implementation:** discover true account and path read-only, implement scoped private transport, perform verified archive ingress, backups/rollback and website production deployments **only with established operation/path-scope**. Capture source→build→deploy→public byte/readback evidence.
- **AXIOM = epistemic governance:** source-exact intake, classify public-safe/restricted, compare manifests/receipts, falsify claims, authorize research publication under standing C1 rule, independently inspect public outputs. Do not claim raw private-archive hashes observed unless bytes can actually be fetched.
- **External experts (QWEN, GROK, MANUS, GEMINI etc.) = isolated lanes:** research returns via authenticated scoped and expiring brokered ingress; access only their own accepted inputs/outputs, no broad Hostinger or production credentials. When expert API absent, use human-mediated UI with a fixed Hostinger locator/receipt, **never** describe a file as uploaded by that expert without a transfer witness.

## 3. Two distinct Hostinger zones (never conflate)

### H-A: private immutable evidence archive

Cursor must discover and document a real authenticated storage space **not publicly served by the webroot**. The following is a *logical hierarchy only*, NOT an asserted existing remote path:

```text
<verified-private-archive-root>/
  custody/v1/<phase>/<lane>/<object-id>/<revision>/
    source-original.<ext>
    SHA256SUMS.txt
    manifest.json
    receipts/
      intake.json
      archive-readback.json
      validation.json
      publication.json
    returns/
```

No public `public_html`, no guess of a path, no FTP listing exposed on the WWW. If private root, permissions, access isolation or reliable readback cannot be established, set `PRIVATE_ARCHIVE_INGRESS=HOLD_SCOPE_ONLY`; do **not** substitute a guessable publicly accessible URL. Other C1-public-safe outputs keep progressing.

### H-B: public C1 website publication

`https://www.nexus-mobile.de/` and approved public routes/asset sets. Only redacted, rights-cleared, source-bound and reversible C1 materials are published; no raw private return. `C1_VALIDATED_PUBLIC_SAFE_REVERSIBLE -> WWW_ROLLOUT_REQUIRED`. Distinguish public GitHub push, production host write, public HTTP readback and visual desktop/mobile confirmation.

## 4. Exact-byte custody contract

Every file transfer is a single immutable `TRANSFER_OBJECT` with:

```json
{
  "schema": "nexus-artifact-custody/v1",
  "object_id": "SOURCE_BOUND_ID",
  "phase": "R21",
  "lane": "CURSOR_OR_EXPERT_LANE",
  "revision": "R0",
  "parent_objects": ["EXACT_OBJECT_IDS"],
  "source_actor_role": "SOURCE_REPORTED",
  "source_filename": "ORIGINAL_EXACT_NAME",
  "content_type": "application/octet-stream",
  "source_bytes": null,
  "source_sha256": null,
  "source_created_utc": null,
  "host_archive_locator": null,
  "host_archive_locator_class": "PRIVATE_NOT_PUBLIC_LINK",
  "visibility": "RESTRICTED",
  "license_and_redistribution": "NOT_ASSESSED",
  "ingress_receipt": "PENDING",
  "private_archive_readback_receipt": "PENDING",
  "independent_validation_receipt": "PENDING",
  "www_publication_receipt": "NOT_APPLICABLE",
  "custody_state": "NOT_TRANSFERRED"
}
```

`null` means *not observed*, not `MATCH`. Content hash is SHA-256 of **actual file bytes**, not Git commit ID, file name or quoted operator report. Preserve original bytes, original filename, nested ZIP entries, ZIP CRC, timestamps (observation vs source-claimed separately), lineage and any expected-hash discrepancies. Sidecar `SHA256SUMS` must not self-hash. Legal/third-party redistribution and individual personal data are quarantined by object, never blindly published.

## 5. Minimal upload→archive→verify handshake

1. **PREPARE** — source-class and retention; obtain object ID, expected SHA/size if source actually supplied; check access permissions, target non-public and content type. Read-only inspection first.
2. **INGRESS** — upload via a scoped authorized channel to a unique staging key, rate-limit and limit file size. No overwrite of bound source. Hash actual staged bytes, compare.
3. **COMMIT** — immutable/versioned archive commit (atomic rename where supported; otherwise versioned commit manifest), preserve old revisions and map all parent identities.
4. **READBACK** — **re-fetch archive bytes or equivalent independently trustworthy byte-read**, recalculate SHA-256 and bytes; verify access denial on public URLs, archive indexes and ZIP CRC where applicable.
5. **INDEX** — append-only public-safe custody receipt/manifest reference in correct GitHub repository path; preserve commit, PR, timestamps, receipt and archive pointer redacted of protected path/credentials. Protected metadata stays private.
6. **RELEASE** — if C1 validated, public-safe, reversible and route-scoped, Cursor may publish in approved production scope, with backup, rollback and independent HTTP + actual browser-visible readback.
7. **EXTERNAL** — expert return must be source-exact, with original author/tool attribution, ingestion receipt and independently checked return before any higher conclusion.

The **three WWW terminal proofs** are independent: `PRODUCTION_FILESET_WITNESS`, `HOST_WWW_WRITE_WITNESS` and `INDEPENDENT_PUBLIC_LIVE_READBACK_WITNESS`. None may be inferred from a GitHub PR or screenshot alone.

## 6. State machine and negative controls

```text
DISCOVERED
→ SOURCE_RECEIVED
→ HOST_PRIVATE_STAGED
→ HOST_PRIVATE_ARCHIVED
→ ARCHIVE_READBACK_MATCH
→ SOURCE_AND_RIGHTS_VALIDATED
→ C1_PUBLIC_SAFE_RELEASED
→ WWW_DEPLOYED
→ WWW_READBACK_VERIFIED
```

At every stage preserve alternative states `HOLD_<AFFECTED_OBJECT>`, `MISMATCH`, `QUARANTINED`, `STALE`, `NOT_OBSERVED`. A staging or archive transfer is not a production deploy. Public Node UI gets a new entry only from a genuinely persisted event receipt, not polling animation.

**Explicit counterchecks:** public-URL leakage, predictable signed URL reuse, expired signature, cross-expert privilege escalation, path traversal/ZIP-slip, forged manifest/signature, hash mismatch, stale source vs new content, ZIP CRC corruption, duplicate object ID, malicious document instructions, provenance spoof, secret echo, silent overwrite, orphan parent, no HTTP readback, cached preview mistaken for new build, unauthorized WWW write.

No stealth tests, production fuzzing, SSH/SCP probing or live infrastructure modifications outside an authorized scope. Do not expose the Hostinger SCP username, passwords, private keys, exact private paths, unpublished research or signed download URLs in public GitHub.

## 7. Now — binding order to existing Cursor workers; no parallel duplicate job

A. **Existing R21 WWW Three Proofs** continues uninterrupted. Current return so far reports only inventory and Playwright 1.64.0 — **the three terminal proofs are missing**; do not claim closure. No new WWW worker or rollback of existing process.

B. **Existing Elite Node Foundation Bind** continues separately; existing `HOMEOSTASIS` only `BORN`, new names reserved as candidates; no fabricated birth/trigger.

C. **Transport Custody v1** should be adopted in the closest **existing** authorized Cursor lane as a small additive task after its immediate higher-priority receipts. Deliver `HOSTINGER_CAPABILITY_WITNESS`, `PRIVATE_ARCHIVE_ROOT_AND_ACCESS_CHECK`, `INGRESS_READBACK_TEST_OF_SYNTHETIC_PUBLIC_SAFE_FILE`, `ARCHIVE_RETENTION_AND_REDACTION_POLICY`, `EXPERT_INGRESS_BROKER_DESIGN`, `GITHUB_CONTROL_PLANE_RECEIPT`. Actual test requires correct host authority; otherwise `DESIGN_AND_CAPABILITY_GAP`.

D. Do not upload arbitrary historic 1.6 GB evidence archives, private data or third-party works without classification. No blanket automatic retention/deletion based on age.

E. AXIOM acceptance only after verification. Branch/PR publication of **this policy** does **not** activate Hostinger storage or the WWW mechanism.

## 8. Non-blocking publication and terminal status

```text
PUBLICATION = C1_VALIDATED_PUBLIC_SAFE_REVERSIBLE_ROLLOUT_REQUIRED
R21_WWW = WAIT_THREE_TERMINAL_PROOFS
HOSTINGER_ARTIFACT_TRANSFER = NOT_YET_ACTIVATED
PRIVATE_ARCHIVE_ROOT = NOT_YET_VERIFIED
EXPERT_DIRECT_INGRESS = NOT_YET_IMPLEMENTED
OPERATOR_DOWNLOAD = EXCEPTION_PHYSICAL_NECESSITY_ONLY
R20 = CLOSED_BY_OPERATOR_WITH_CAVEATS
R19_ORBIS = INDEPENDENT_OPEN
CLAIM_PROMOTION = NO
```
