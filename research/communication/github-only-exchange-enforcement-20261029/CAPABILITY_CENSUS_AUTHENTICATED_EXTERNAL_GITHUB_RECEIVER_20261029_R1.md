# Capability Census · Authenticated External GitHub Receiver (READ-ONLY)

**OBJECT:** `NEXUS_OMEGA_CAPABILITY_CENSUS_AUTHENTICATED_EXTERNAL_GITHUB_RECEIVER_20261029_R1`
**PARENT:** `NEXUS_OMEGA_AXIOM_CURSOR_EXPERTENKODEX_F10_F11_REMEDIATION_20261029_R1`
**REPOSITORY:** `nexusomegac27/NEXUS-OMEGA-EVIDENCE`
**PR_CONTEXT:** `#185`
**CLAIM_CEILING:** `C1_DESCRIPTIVE_ONLY`
**CREATED_UTC:** `2026-10-29T21:25:00Z`
**MODE:** `READ_ONLY_CENSUS`
**EXECUTE:** `NO`

## Purpose

Map **existing** GitHub capabilities that could support a future independently authenticated external expert handshake — without installing apps, granting new permissions, or inventing agent identities.

## Explicit non-actions this census

```text
GITHUB_APP_INSTALL = NOT_PERFORMED
OAUTH_APP_CREATE = NOT_PERFORMED
DEPLOY_KEY_CREATE = NOT_PERFORMED
FINE_GRAINED_PAT_CREATE = NOT_PERFORMED
NEW_BOT_USER = NOT_PERFORMED
EXTERNAL_WRITE_GRANT = NOT_PERFORMED
HOSTINGER = NO
WWW_WRITE = NO
```

## Observed surfaces (descriptive)

| Surface | Present in lane | Suitable for external ACK (design) | Status |
|---------|-----------------|--------------------------------------|--------|
| Public PR discussion / review comments | YES (PR #185) | Receipt + human/expert stamp | AVAILABLE_WITHOUT_NEW_GRANT |
| Commit SHA + Actions run conclusions | YES | Independent CI witness | AVAILABLE_WITHOUT_NEW_GRANT |
| Public blob / raw content SHA-256 | YES | Byte identity | AVAILABLE_WITHOUT_NEW_GRANT |
| Branch protection / required checks | UNKNOWN_THIS_CENSUS | Main enforcement | NOT_ESTABLISHED |
| GitHub App installation for third party | NO census execute | Strong external auth | NOT_ESTABLISHED · HOLD |
| Collaborator invite / outside collaborator | NOT_EXECUTED | Org-scoped human expert | NOT_ESTABLISHED · HOLD |
| Signed commits (GPG/SSH) by external | NOT_VERIFIED_THIS_TURN | Non-repudiation | NOT_ESTABLISHED |
| Expertenkodex header on dispatch | ENFORCED_AFTER_F11 | Mandatory bind | FAIL_CLOSED_LOCAL_CODE |

## Expert handshake minimum (design candidate only)

```text
CANDIDATE_MINIMAL_EXTERNAL_ACK =
  1 AUTHENTICATED_GITHUB_ACTOR (human or pre-authorized app — NOT invented here)
  2 PINNED_COMMIT_OR_PR_HEAD
  3 EXPERTENKODEX_HEADER_BOUND
  4 INDEPENDENT_REHASH_OF_ORDER_OR_RESULT
  5 PUBLIC_COMMENT_OR_REVIEW_AS_RECEIPT
≠ INSTALLED
≠ AUTHORIZED_BY_THIS_CENSUS
```

## Findings

```text
EXTERNAL_RECEIVER_ACK = NOT_ESTABLISHED
GITHUB_MAIN_ENFORCEMENT = NOT_ESTABLISHED
CAPABILITY_GAP = AUTHENTICATED_THIRD_PARTY_IDENTITY_NOT_BOUND
NEXT_REQUIRES = SEPARATE_OPERATOR_TYPE_C_OR_AXIOM_ORDER_FOR_GRANT
```

## Epistemic walls

```text
CENSUS ≠ GRANT
PUBLIC_PR ≠ AUTHENTICATED_EXTERNAL_EXPERT
CI_PASS ≠ RECEIVER_ACK
READ_ONLY ≠ LICENSE_TO_INSTALL_APP
```

## NEXT

```text
NEXT = AXIOM_INDEPENDENT_RECEIVER_AND_POLICY_ADJUDICATION
CURSOR_ACTION_AFTER_CENSUS = NONE_ON_IDENTITY_PLANE
```
