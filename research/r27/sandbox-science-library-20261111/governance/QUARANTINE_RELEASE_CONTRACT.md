# R27 Research Sandbox — Quarantine, Rights and Release Contract

OBJECT = NEXUS_OMEGA_R27_SANDBOX_QUARANTINE_AND_RELEASE_CONTRACT_20261111_R0
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY

## Boundary by action

| Research activity | Permitted in read-only design lane? | Actual execution permission |
|---|---|---|
| Read operator-scoped, hash-verified files | Within actual access permissions | source-scoped READ only |
| Propose hypotheses, criticism, architecture | Yes, role-free and provider-neutral | no external command implied |
| Create a descriptive candidate or return | Yes in a distinct quarantined output workspace | outbox writer alone, no canonical store mutation |
| Import third-party fragment or run executable | Design-only specification | DENY; requires separately approved isolated runtime |
| Grant agent, API, GitHub or host permissions | No | DENY by default |
| Promote claimed scientific result | No | separately reviewed release authority; never from hash/consensus |
| Copy private originals to WWW/GitHub public | No | DENY by default; specifically selected public-safe metadata only |

**Fail-closed** governs effective permissions. The epistemic states `VALIDATED_STATIC | PARTIAL | MISSING_EVIDENCE | REJECTED` document evidence, not a permission switch.

## Gate proof required for any future runtime activation

Independent source identity/rehash; real OS/container sandbox read-only enforcement; deny-by-default outbound network; bounded CPU/memory/time; no host mount secrets; actor enrollment and four-eyes review; negative injection/path/truncation/rollback fixtures; immutable audit receipt; kill switch, rollback and verified environment. None are established by this static site.

## External research autonomy

Thought is free; roles are not allocated to external experts. Experts self-identify and may challenge all foundations. Actions are governed by identities and scopes, not by philosophical agreement. Agent/provider/run identity is never automatically attested.

## Publication semantics

`GITHUB_COMMIT != HOSTINGER_DEPLOY != WWW_HTTP_PASS != SCIENTIFIC_TRUTH`. The site is a non-executing public navigator and carries no access-control enforcement: the effective privacy barrier is that protected originals are not uploaded to public endpoints.
