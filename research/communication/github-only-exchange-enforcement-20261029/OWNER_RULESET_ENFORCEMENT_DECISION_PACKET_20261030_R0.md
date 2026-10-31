# Owner Ruleset Enforcement Decision Packet · 20261030 R0

**OBJECT:** `NEXUS_OMEGA_OWNER_RULESET_ENFORCEMENT_DECISION_PACKET_20261030_R0`  
**PARENT_ORDER:** `NEXUS_OMEGA_AXIOM_CURSOR_GITHUB_INDEPENDENT_RECEIVER_PILOT_READINESS_20261030_R0`  
**RULESET:** `main-evidence-protection` · id `21252293`  
**CLAIM_CEILING:** `C1_DESCRIPTIVE_ONLY`  
**CURSOR_MUTATION:** `PROHIBITED_THIS_ORDER`  
**PR185:** `DRAFT · NO_AUTO_MERGE`

---

## Observed state (read-only)

```text
required_status_checks.contexts = ["validate"]
required_status_checks.strict = true (as observed at intake)
require_code_owner_review = false
required_approving_review_count = 0
dismiss_stale_reviews = true
require_last_push_approval / unattributed = true (extra approval for unattributed)
required_review_thread_resolution = true
CODEOWNERS = "* @nexusomegac27"
GITHUB_MAIN_ENFORCEMENT = PARTIAL
EXPERTENKODEX_REQUIRED_CHECK_ON_MAIN = PARTIAL
  (Expertenkodex pytest runs inside validate-repository-structure workflow;
   ruleset required context name remains "validate" only)
```

---

## Problem (self-approve deadlock)

```text
IF require_code_owner_review = true
AND CODEOWNERS = only @nexusomegac27
AND sole collaborator = owner
THEN owner cannot satisfy independent code-owner review without a second principal
→ SELF_APPROVE_DEADLOCK_RISK = HIGH
```

GitHub Docs: required status checks and pull-request review rules are separately configurable. Do not conflate CODEOWNERS with required checks.

---

## Decision options (operator chooses; Cursor does not PATCH)

### Option A — Required check expansion only (preferred first step)

```text
ADD required status check contexts that already exist on CI tip, e.g.:
  - validate
  - (optional alias if GitHub check-run name differs)
KEEP require_code_owner_review = false
KEEP required_approving_review_count = 0 OR raise to 1 only AFTER second principal enrolled
PRO: no CODEOWNERS deadlock; Expertenkodex stays covered if it remains inside validate job
CON: Expertenkodex not independently named as required context
```

### Option B — Named Expertenkodex check + keep CODEOWNERS false

```text
Split workflow job so check-run name = "expertenkodex" (or similar)
ADD that name to ruleset required contexts alongside validate
require_code_owner_review = false until distinct reviewer exists
PRO: explicit main enforcement for Kodex
CON: requires workflow change + ruleset Freigabe
```

### Option C — Second principal + review count 1

```text
Enroll distinct GitHub user (or team) as collaborator / CODEOWNER line for exchange paths
required_approving_review_count = 1
require_code_owner_review = true ONLY after CODEOWNERS includes ≥1 non-owner principal
PRO: real review gate
CON: blocked until enrollment; current census = HOLD_ADAPTER_NOT_CONNECTED
```

### Option D — Do nothing until receiver enrollment

```text
Preserve PARTIAL enforcement
Document gap; no ruleset mutation
PRO: matches this readiness order (no mutation without Freigabe)
CON: GITHUB_MAIN_ENFORCEMENT remains PARTIAL
```

---

## Recommended sequence (operator)

```text
1. Enroll distinct authenticated external principal (TYPE_C / Operator)
2. Option B or A — make Expertenkodex visible as required check (Freigabe)
3. Option C — only after CODEOWNERS has non-owner entry
4. Never set require_code_owner_review=true while CODEOWNERS is owner-only
```

---

## Explicit non-actions this bind

```text
NO gh api PATCH /repos/.../rulesets/21252293
NO CODEOWNERS rewrite
NO PR185 auto-merge
NO invent WRITE_ACK / Hostinger
NO claim GITHUB_MAIN_ENFORCEMENT = FULL
```

---

## Disposition

```text
PACKET = BOUND_C1_DECISION_ONLY
RULESET_MUTATION = NOT_EXECUTED
GITHUB_MAIN_ENFORCEMENT = PARTIAL
NEXT = OPERATOR_FREIGABE_THEN_OPTIONAL_RULESET_PATCH
```
