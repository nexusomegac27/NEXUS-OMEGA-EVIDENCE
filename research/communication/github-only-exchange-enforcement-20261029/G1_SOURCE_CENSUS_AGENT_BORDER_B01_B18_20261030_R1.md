# G1 Source Census · Agent Border B01–B18 · 20261030_R1

OBJECT: `NEXUS_OMEGA_G1_SOURCE_CENSUS_AGENT_BORDER_B01_B18_20261030_R1`  
AUTHORITY: `OPERATOR_ALEXANDER_VIA_AXIOM`  
CLAIM_CEILING: `C1_DESCRIPTIVE_ONLY`  
LAW: `REUSE_BEFORE_INVENT` · `AEGIS = REUSE_NOT_DUPLICATE` · `NO_PARALLEL_BORDER`

## Live / Public plane (read-only verify)

| ID | Item | Finding |
|----|------|---------|
| B01 | Public route | `https://www.nexus-mobile.de/ai/agent-border/` present (prior HTTP 200 report-level) |
| B02 | Hostinger site root | Bound to existing WWW plane; no new Hostinger write this order |
| B03 | Agent Border UI | Existing public surface; extend semantically, do not fork |
| B04 | AEGIS / quarantine doctrine | Reuse Forum Astartes Aegis design + check-in quarantine ledger |
| B05 | Expertenkodex V1 | `docs/governance/NEXUS_EXPERTENKODEX_GITHUB_COMMUNICATION_V1.md` @ `b17d382…` SHA256 `adf69aa3…` MATCH |
| B06 | GitHub Evidence repo | `nexusomegac27/NEXUS-OMEGA-EVIDENCE` · DATA_ROUTE=GITHUB_ONLY |
| B07 | PR185 DRAFT | Branch `codex/github-expert-exchange-foundation-20261029` · OPEN_DRAFT · NO_AUTO_MERGE |
| B08 | Receiver Pilot Readiness | R0 design + R1 AXIOM adjudication; EXTERNAL_RECEIVER_ACK=NOT_ESTABLISHED |
| B09 | Task Anchor Norm V1 | `TASK_ANCHOR_…_20261030_R1.json` 9959 / `84e1787c…` MATCH |
| B10 | Maxi Order R1 | 26800 / `ecea5530…` @ `ad3949fa…` MATCH |
| B11 | PFV Agent Border PHP | `nexus-real/nexus-homepage/public/ai/agent-border/` — NexusIntake requires provider/model (anonymous gap) |
| B12 | Anonymous gap | Closed in new loopback check-in: provider/model optional |
| B13 | F10 | CLOSED · default-deny remote tools surface |
| B14 | F11 | CLOSED_TESTED_PATH · fail-closed validation |
| B15 | F12 | CLOSED_EMPTY_REGISTER · empty privilege register |
| B16 | Multi-Transport V3 | DRAFT_ONLY · not shipped |
| B17 | Public External Write API | HOLD · loopback bind 127.0.0.1 only |
| B18 | Native App R3 | HOLD · out of this order |

## Implementation reuse decision

- New code lives under Evidence `examples/open-neutral-checkin/` (isolated staging / loopback).
- No second public Border URL; no second AEGIS root; no Hostinger deploy from this gate.
- Production WWW extension awaits separate AXIOM acceptance + TYPE_C write ACK.

## Epistemic walls

```text
CENSUS ≠ DEPLOY
HTTP_200 ≠ IMPLEMENTATION_PASS
LOCAL_LOOPBACK ≠ PUBLIC_WRITE
REUSE ≠ DUPLICATE_FRAMEWORK
```
