# NEXUS OMEGA · Repository Steward V1 · 2026-10-13

## Authority and evidence scope

```text
OBJECT = NEXUS_OMEGA_REPOSITORY_STEWARD_NODE_SEEDLING_20261013_R0
AUTHORITY = OPERATOR_DIRECT_20261013
PREDECESSOR_MAIN = 437804b9a6eddee5afcf47cc1ca193f3ddcaac80
PREDECESSOR_STRUCTURE = 1.7.14
NEW_VERSION_PROPOSED = 1.7.15
ROLE = REPOSITORY_STEWARD_CI_LANE
PHYSICAL_NEXUS_NODE_BUS_IDENTITY = NOT_ESTABLISHED
EXECUTION_CLASS = EXISTING_GITHUB_ACTIONS_LOCAL_PYTHON
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
ALLOW = READ_ONLY_SCAN, DOCUMENT, CLASSIFY, REPORT, SUGGEST_MIGRATION
DENY = AUTO_RENAME, AUTO_MOVE, DELETE, REWRITE_HISTORY, NEW_ORCHESTRATOR,
       NEW_EXTERNAL_AGENT_WRITE_SLOT, NODE_RESET, HOSTINGER_DEPLOY
```

This is the first technical seedling, **not** a newly provisioned or verified NEXUS_NODE_BUS runtime agent. A repository CI runner executes a stateless deterministic steward capability. Future physical registration with the existing bus requires a separate actual identity/capability receipt. A CI PASS is not scientific validation.

## Full-tree inventory contract

On checkout HEAD, `scripts/nexus_repository_steward.py` scans **every tracked Git blob** through `git ls-tree -r -l -z HEAD`; it does not use a potentially stale navigation index. It records for every tracked file: path, owning domain, Git blob SHA-1 (explicitly not a SHA-256), original checkout SHA-256, byte count, Git mode, registered research lane, integrity faults and non-blocking naming advisories. Every parent directory is enumerated from tracked paths. Commit SHA and register version anchor the snapshot. Machine-readable JSONL may be emitted outside the tracked repository. GitHub Actions job summaries show counts; ephemeral runner outputs are not canonical stored objects.

No private Windows archive, TRANSFER custody, current MCP tool list or Website bytes are in scope. Git history cannot establish creation time of the scientific object and is not a substitute for immutable event time. Source SHA-256 proves byte identity only; it does not prove scientific meaning, license ownership or publication readiness.

## NEXUS naming and placement conventions (prospective)

| Artifact | New controlled convention | Existing legacy |
|---|---|---|
| Root | Only existing allowlisted control files/directories | Preserve A83 compatibility |
| New directories | Lower-case ASCII `kebab-case`, no spaces or platform reserved names | Record deviation, do not rename |
| New ordinary files | Meaningful lower-case hyphenated name with a declared extension; `README.md` exception | Existing path-bound uppercase IDs preserved |
| Canonical objects | Immutable `NEXUS_OMEGA_...` ID and explicit version; hash in manifest, not inferred from name | Preserve bound identity |
| Dates | ISO 8601 UTC in metadata; safe compact `YYYYMMDDThhmmssZ` in object filenames | Never alter historical dates |
| JSON | UTF-8, versioned schema, duplicate-key rejection on ingest | Do not silently normalize bytes |
| JSONL | One complete UTF-8 JSON value per line; append-only receipts where governed | Existing ledger format takes precedence |
| Markdown | UTF-8, `README.md` per owner/registered research lane, clear status and predecessor | Existing documentation remains |
| Source files | SPDX identifier + copyright provenance when rights established | No fabricated licenses |
| Release/CI | Branch+PR, current checks, independent source readback; pin dependencies where feasible | Historic checks and rules preserved |

No filename is made normative merely because it resembles a DIN identifier. The collision/unsafe-path checks are hard integrity signals. Legacy stylistic deviations are **REVIEW_ONLY**, not an automatic global HOLD.

## Controlled migration, not cosmetic moves

A future move of a bound path needs: old full commit/path/bytes/SHA-256; owning lane; dependencies and references; privacy/license decision; replacement path and new content identity; compatibility pointer where feasible; risk and rollback plan; reproducible reference tests; independent AXIOM adjudication and a new append-only migration receipt. Never rewrite sealed originals, content-addressed store paths or historical Git history. Low-risk new material is classified at intake, then routed to the already declared domain.

**Change priority:** (P0) unsafe/ambiguous paths and source integrity; (P1) missing owners/READMEs or broken references; (P2) stale discovery and unindexed legal artifacts; (P3) harmless case/underscore/filename style. Only P0 integrity prevents this steward step; P1/P2 require scoped follow-up and P3 is non-blocking.

## Why these public standards were selected

- **ISO 15489-1:2016** information/records management concepts — https://www.iso.org/standard/62542.html
- **ISO 8601-1:2019** date-time representations — https://www.iso.org/standard/70907.html
- **Google documentation guidance** owner/readme discoverability — https://google.github.io/styleguide/docguide/best_practices.html
- **GitHub CODEOWNERS** with separately configured branch protection — https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners
- **OCFL 1.1** archival object-version integrity — https://ocfl.io/1.1/spec/
- **W3C PROV-O** provenance representation — https://www.w3.org/TR/prov-o/
- **RO-Crate 1.3** research-object packaging (consider optional exporter, not installed) — https://www.researchobject.org/ro-crate/specification.html
- **REUSE 3.3** SPDX per-file copyright/license expressions — https://reuse.software/spec-3.3/

These are **design alignments**, not claims of ISO/DIN certification, OCFL/RO-Crate/REUSE conformance or any license clearance. The full paid ISO/DIN normative texts were not validated; public descriptions and openly published technical practices were used.

## Reproducible commands

```sh
python scripts/nexus_repository_steward.py --root . --output /tmp/nexus-tree.jsonl --fail-on-integrity
python -m unittest tests.test_nexus_repository_steward -v
python scripts/validate_repository_structure.py --root .
```

The existing `.github/workflows/validate-repository-structure.yml` adds these tests, emits a bounded summary and schedules a daily best-effort read-only check. **No new workflow file, token privileges or standing external agent**. The first scheduled run is not evidence until GitHub reports it. If a producer's report conflicts with the original bytes, preserve both and HOLD_SCOPED.

## Return / custody

```text
STATE = PROPOSED_SOURCE_CHANGE_UNTIL_MERGED_AND_CHECKED
HISTORY = APPEND_ONLY
SOURCE_RETURN = GITHUB_PR_AND_FULL_COMMIT
AXIOM_INDEPENDENT_ACK = PENDING_SOURCE_READBACK
CURSOR_REAUDIT = NO
NEXUS_NODE_BUS_RUNTIME = NOT_ASSESSED
```
