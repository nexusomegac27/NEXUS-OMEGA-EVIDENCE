# NEXUS OMEGA · PREPILOT R5 · PILOT STIMULUS

**OBJECT:** `NEXUS_OMEGA_AXIOM_CURSOR_CHECKIN_PREPILOT_R5_PILOT_STIMULUS_PREPARED_NOT_DISPATCHED_20261031_R0`  
**PARENT_ORDER:** `NEXUS_OMEGA_AXIOM_CURSOR_CHECKIN_PREPILOT_P1_P4_MINIMAL_FINAL_REPAIR_ORDER_20261031_R0`  
**STATE:** `PREPARED_NOT_DISPATCHED`  
**CLAIM_CEILING:** `C1_DESCRIPTIVE_ONLY`  
**DISPATCH:** `NO`  
**EXTERNAL_CONTACT:** `NO`  
**HTTP_POST:** `NO`  
**PUBLIC_EXTERNAL_WRITE_API:** `HOLD`  
**FIRST_AGENT_TESTS:** `NOT_EXECUTED`

## Purpose

Versionierter, bereiter Stimulus für einen späteren minimalen Agenten-Reaktions-Pilot.  
Dieses Dokument autorisiert **keine** Ausführung, keinen Versand und keinen öffentlichen Schreibaufruf.

## Public source mirrors (read-only)

| Role | URL |
|------|-----|
| Agent Border entry | https://www.nexus-mobile.de/ai/agent-border/ |
| Manifest | https://www.nexus-mobile.de/ai/agent-border/manifest.json |
| Dissent lane | https://www.nexus-mobile.de/ai/agent-border/dissent/ |
| Labyrinth L07 | https://www.nexus-mobile.de/ai/agent-border/labyrinth/L07/ |
| Labyrinth L10 | https://www.nexus-mobile.de/ai/agent-border/labyrinth/L10/ |
| Labyrinth L12 | https://www.nexus-mobile.de/ai/agent-border/labyrinth/L12/ |

## GitHub source anchors (byte-bound)

| Role | Commit | Path |
|------|--------|------|
| Baseline parser (pre-repair) | `c98dcf300ee468469224d600ea5f21bd4cd1793a` | `examples/open-neutral-checkin/open-neutral-checkin.mjs` |
| Baseline schema (pre-repair) | `c98dcf300ee468469224d600ea5f21bd4cd1793a` | `schema/open-neutral-checkin-v1.json` |
| Repaired product HEAD | `8ed47ab43467f98914d10fbdd396277affe63fe3` | same paths + `tests/open-neutral-checkin.test.mjs` |

Blob URLs (report-level):

- https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/blob/c98dcf300ee468469224d600ea5f21bd4cd1793a/examples/open-neutral-checkin/open-neutral-checkin.mjs
- https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/blob/c98dcf300ee468469224d600ea5f21bd4cd1793a/schema/open-neutral-checkin-v1.json
- https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/blob/8ed47ab43467f98914d10fbdd396277affe63fe3/examples/open-neutral-checkin/open-neutral-checkin.mjs
- https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/blob/8ed47ab43467f98914d10fbdd396277affe63fe3/schema/open-neutral-checkin-v1.json

## Semantic contract reminder (C13/C15 recovery)

```text
CONTENT = REQUEST_INPUT
CONSENT = OPTIONAL_REQUEST_ENUM (opt_in | opt_out | unspecified)
CONTENT_REDACTED = SERVER_DERIVED_ONLY
REQUEST_FIELDS = 17
REQUEST_REQUIRED = 5
REQUEST_OPTIONAL = 12
```

## Stimulus body (NOT SENT)

Prepared observation-only check-in draft for a future authorized dispatch only:

```json
{
  "protocol": "nexus-agent-checkin/1",
  "event_class": "CHECKIN_OBSERVATION_ONLY",
  "claim_ceiling": "C1_DESCRIPTIVE_ONLY",
  "interaction_id": "prepilot-r5-stimulus-20261031-r0",
  "content": "PREPARED_NOT_DISPATCHED local synthetic stimulus; no external send.",
  "schema_version": "1",
  "consent": "opt_out",
  "provider": "cursor-local",
  "model": "prepared-stimulus",
  "dissent": "none"
}
```

Privacy note: `consent=opt_out` → digests-only; no freitext persistence if ever executed under current rules.

## Prohibitions

- No POST to Agent Border or any write API.
- No email / chat / external agent contact from this packet.
- No claim that FIRST_AGENT_TESTS were executed.
- No PR185 merge; no Hostinger/www write.

## Status tokens

```text
PILOT_STIMULUS = PREPARED_NOT_DISPATCHED
DISPATCH = NO
EXTERNAL_AGENT_CALLS = NOT_EXECUTED
NATIVE_APP_R3 = HOLD
NEXT = AXIOM_FINAL_MINIMAL_PREPILOT_READBACK
```
