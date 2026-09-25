# 03 Shadow and Fixtures

## Shadow run

```text
SCRIPT = worker/scripts/run_shadow.py
EXIT = 0
FIXTURES_PASS = 12
FIXTURES_FAIL = 0
UNITTESTS = 6_OF_6_PASS
REPORT =
 worker/shadow/SHADOW_RUN_REPORT.json
REPORT_HASH =
 82b60a149a4d341cca132c150529a08bd7237cfcfa5b83836b2f0c22b04856fa
LEDGER_EVENTS = 5
GITHUB_PUSH_EXECUTED = false
E2E_CLASS_A = SHADOW_RECEIPT_ONLY
```

## Fixtures implemented (F01–F12)

| ID | Intent |
|----|--------|
| F01 | Invalid envelope fail-closed |
| F02 | Prompt injection in feed content |
| F03 | Unauthorized network destination |
| F04 | Structural change not Class A/B |
| F05 | Missing required event fields |
| F06 | Unauthorized publication class |
| F07 | Duplicate event DEDUP |
| F08 | Allowlist node violation |
| F09 | Claim ceiling breach |
| F10 | Validation fail path |
| F11 | News content treated as data not instruction |
| F12 | Shadow receipt without live push |

## Caveat: order mandatory list vs shipped subset

```text
ORDER_MANDATORY_LIST_INCLUDES_ALSO =
 STALE_PARENT · INVALID_SOURCE · SOURCE_CHANGED_DURING_FETCH
 · MISSING_RECEIPT · PUSH_FAILURE · CONCURRENT_TRIGGER
 · NEWS_SOURCE_TIMEOUT · MALFORMED_RSS · SECRET_EXFILTRATION_ATTEMPT
 · plus aliases covered partly by F01–F12

STATUS =
 CORE_FAIL_CLOSED_SUBSET = PASS_12_OF_12
 RESIDUAL_ORDER_FIXTURES = DESIGN_ONLY_NOT_CLAIMED_SHIPPED
 NO_SILENT_CLAIM_OF_FULL_MANDATORY_LIST = REQUIRED
```

## Epistemic walls

```text
SHADOW_PASS != LIVE_DEPLOY
FIXTURE_PASS != SCIENTIFIC_VALIDATION
RECEIPT_ONLY != PUSH_EXECUTED
HASH_MATCH != SCIENTIFIC_TRUTH
```
