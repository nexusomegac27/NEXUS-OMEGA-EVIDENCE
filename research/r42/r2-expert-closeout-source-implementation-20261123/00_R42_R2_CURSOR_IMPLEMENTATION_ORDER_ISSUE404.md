# R42-R2 AXIOM→Cursor · Source-exact implementation order

Canonical issue: https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/issues/404
This is a frozen copy of Issue #404 at research-order creation. It is a SOURCE IMPLEMENTATION REQUEST, not a completed App repair, not Cursor ACK, not R43 start.

# NEXUS OMEGA · AXIOM → CURSOR · R42-R2 expert closure intake → scoped source implementation

OBJECT = NEXUS_OMEGA_AXIOM_CURSOR_R42_R2_EXPERT_CLOSEOUT_AND_SOURCE_IMPLEMENTATION_ORDER_20261123_R0
AUTHORITY = OPERATOR_ALEXANDER_VIA_AXIOM
DATE = 2026-11-23 Europe/Berlin
STATE = R42_R2_EXPERT_RESEARCH_INTAKE_VALIDATED_C1_IMPLEMENTATION_PREPARED
R41 = ADMINISTRATIVELY_CLOSED_MATERIAL_GAPS_PRESERVED
R42 = OFFLINE_SOURCE_IMPLEMENTATION_AUTHORIZED_AS_IN_PRIOR_ISSUE_400
R43 = NOT_STARTED_PENDING_CURSOR_R42_IMPLEMENTATION_RETURN_AND_AXIOM_ADJUDICATION
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
BODYTWIN_VALIDATED=NO · CONSENT_BIND=OPEN · ALT_D_DO_NOT_RUN_ACTIVE · 14_PHYSICAL_GATES=HOLD
NO_DEVICE_CAPTURE · NO_ADB_SENSOR_START · NO_APK_INSTALL · NO_PR_MERGE · NO_HOSTINGER_WRITE · NO_WWW_WRITE · NO_CLAIM_PROMOTION
EXTERNAL_DIRECT_WRITE = DENY_PENDING_REGISTRATION

## Causal source and retained chain
- R41 foundational Issue #395, Draft PR #396; admin R41 closeout and R42 foundation Issue #400 / Draft PR #401 HEAD `21db4552d91f39cb42ab54523537fd0aa4f8f136`.
- R42-E mandate Issue #402 / Draft PR #403 HEAD `7e710ebea0b9066f880e52b4e3c25c5b96cb8f27`; BodyTwin public W1 Issue #397. The 8 original Kotlin/Python/FC2/W1 objects were only **CURSOR_REPORTED_ONLY** in the 4686 B Cursor report; no actual original source bytes were supplied in R42-R2 attachments. Receiver of real byte sources must verify independently before CODE_RUNTIME_PASS.
- New E21–E26 operator-relayed expert return outer ZIP `R42_E_~1.ZIP` 83998 B SHA256 `398c00f818152ba494a412332ab911c9493e4dbe6159e446ef099dd82d61034a`; inner original `R42_E_EXPERT_RETURN_PACKAGE_20261123_R0.zip` 68361 B SHA256 `03710ce73288a6bb82217ea99322972a36a6e8669faf2e3a7eb3748ec202257d`, inner CRC PASS, original SHA256SUMS 16/16 MATCH, 9 included scripts. Reproduced by AXIOM in isolated temporary scratch (only E21 E22 E24 E25 E26, **NOT external network E23 probe**): E21 spec 16/16 negatives, legacy 13/16 fail, 4/4 positives; E22 clone blocks 20/20 attacks and 6/6 positives; E24 10/10 negatives + 4/4 positives; E25 10/10 + 4/4; E26 three alternatives and falsifier. **Only synthetic/desk code, no actual Kotlin/FC2/BodyTwin runtime validation.**
- AutoClaw X18 ZIP `R42E_A~1.ZIP` 55911 B SHA256 `3fde6979f36fc8a6371bdd781885272e94535fff6ee2da5d6ed5f640330e27f0`; CRC PASS, 7/7 SHA256SUMS MATCH. Original `artifacts/x18_audit_suite.py` was run by AXIOM in isolation, exit 0, synthetic E21=20/20, E22=26/26, E23=18/18, E24=14/14. Demo trust key / HMAC model is not a production trust root.
- E23 independent vantage `E23_W1~1.ZIP` 397270 B SHA256 `eefb73a343c7897e0942797d463c49fe374de0308efd94ed11dd8a1dba42784a`; 48/48 manifest data files hash-match, CRC PASS, snapshots 2026-11-23T05:34:09Z and 05:38:40Z (~271 sec, **less than nominal 300 sec producer interval**). Fresh external direct traffic yielded TCP timeout on ordinary CDN edges; pinned 147.93.77.95 yielded HTTP 403 5768B SHA256 `69eacef2f355c22ff53745adb39ff0076d2093a767a72e38070ca83c7c5569df`; third-party vantage TCP 11/12 connections OK. No application HTTP-200 body bytes obtained. hcdn JS challenge + reCAPTCHA observed, **do not solve or circumvent CAPTCHA automatically**; site down is NOT proven. E23 ZIP contains `browser_artifacts/browser_cookies.json` and other potentially sensitive session material: QUARANTINE PRIVATE, NO PUBLIC GITHUB UPLOAD.
- Cursor previous W1 `W1_RAW_HTTP_WITNESS_RECEIPT.json` 12499B SHA d2e1a313… reported 8/8. That original was NOT received by AXIOM. Need exact fetch vantage/headers and independent body witness; **report 8/8 != second-party HTTP attestation**.
- Authenticated independent expert quorum NOT_ESTABLISHED. Operator-relayed expert returns count as advisory source material; receipt != actor identity/second-party.

## AXIOM newly identified independent negative findings (MANDATORY REGRESSION FIXTURES)
- E21 reference script `r42e_e21_android_runtime.py` lines in its `sp_abort` test catch `except Exception` and return `spec_ok=True` (e.g. N21-04/05/06 run with `sp_abort(None,...)` and yield `guarded:AttributeError`). This inflates "GREEN" for a generic code crash, NOT proof the intended domain-specific `Abort` path actually fired. **Introduce N42-R2-01: only expected typed abort with precise cause passes; raw AttributeError/TypeError must FAIL test, no blanket exception acceptance.**
- The same model writes sample dispositions into `ledger[sample_id]` without checking duplicates, and sets `observed=len(ledger)`; a replayed sample can silently overwrite and keep the conservation check superficially satisfied. **N42-R2-02:** independent ingress delivery count and unique IDs, immutable first disposition, duplicate counter, proper quarantined/rejected handling, no silent overwrite.
- `stop_ack()` increments `stop_acks` on every re-invocation, although the positive "idempotent" scenario expects stop_acks==3. **N42-R2-03:** repeated STOP_ACK requests must return stable result without incrementing side-effect/physical action counts; distinguish invocation count from committed STOP event count.
- E22 `r42e_e22_fc2_security.py` accepts string `signer` identity by membership in `trusted_signers`; there is no cryptographic signature verification in the shown FC2 verifier. Self-asserted actor/reviewer strings are not authenticators even if all negative mocks pass. **N42-R2-04:** forged trusted signer with identical well-formed unsigned fields MUST be rejected; positive controls need independently authorized valid crypto verification or classified NOT_ESTABLISHED.
- E23 dual snapshot (~271s) and expert scripted ~221s separation both fail the ≥300s nominal producer interval criterion. **N42-R2-05:** nominal interval from real feed schema, explicit 300s or larger separation with both request start/end, reject close timing as insufficient for tick-liveness evidence. Compare source-change hash vs producer tick separately.
- The E21 demo's `origin` label is synthetic; production event-origin classification must be computed from actual SensorEvent.timestamp and valid Android clock mapping, NEVER trusted directly from a supplied origin string. No fixed 4ms drain implied by sample tests as a universal FIFO bound. **N42-R2-06:** late FIFO, missing/reordered events, sensor timestamps and unknown source latency against actual app-bound algorithm.

## Scoped implementation P0–P7, no redundant repeat research
P0 — Accept, rehash, freeze sources from 8-source registry of PR #403. Request actual 4 Kotlin, 2 Python, FC2 and W1 receipt bytes privately or source-exact immutable Git ref. Verify path+raw bytes SHA256, git blob SHA, diff and public-safety before any source claim. If gap: SOURCE_GAP and work-conserving offline negative runner.
P1 — Actual app Kotlin gate + CaptureEngine + ForegroundService + GateTest: half-open event-time interval, explicit typed fail-closed invalid deadline/missing timestamp/clock mismatch/overflow; FIFO watermark justified with measured batching uncertainty, bounded drain/quarantine/stranded ledger, duplicate replay dedupe, idempotent STOP finalization, lifecycle/reboot. Required explicit FAILED_BEFORE / PASSED_AFTER on old/new **same app path** for six new N42-R2 fixtures plus E21 16/4 and X15 original per-sample ledger if available. No fake generated sample count from requested sensor Hz. No ADB/sensor capture.
P2 — Actual `fc2_gate_engine.py` + ledger/trust policy: independently controlled signature and expected hash or explicit SOURCE_GAP, authentic actor/reviewer registration; reject unsigned/fake signers, duplicate keys, canonicalization ambiguity, replay, TOCTOU and false second-party. Run E22 20 negatives +6 real valid positives; physical 14 gates HOLD under all circumstances. Demo HMAC/membership mock cannot become production authority.
P3 — Metrology M1 PSD/GUM full covariance, M2 MC raw sensor-observation mock and honest coverage uncertainty; M3 independent calibrated physical reference remains DESIGN_ONLY, no accuracy/NEES claim. Use E24 10/4 and X18 mock as regressions; do not conflate synthetic and actual OPPO.
P4 — E25 reproducible clean JVM/Gradle build if actual app toolchain available (else NOT_RUN), fixed dependencies/runner versions, source tree + hash, test commands/exit/negative mutation and source exact code paths. No APK install.
P5 — E23/W1 public independent witness on same four Issue #397 allowlisted URLs: distinguish TCP/HTTP 403 challenge/app 200, separate raw-byte origin/edge/browser evidence; require real header/body SHA and ≥1 measured feed interval; preserve STATUS!=EMBEDDED until source-exact root-cause. Request Cursor actual 12499B W1 witness and fetch method, then independently review. Challenge-bypass, cookies, CAPTCHA and private headers NOT placed in public repo. Propose only design options for operator-authorized challenge-free public mirror or operator witness+second-party notarization; no deploy or CDN policy change.
P6 — E26 modular decision: costed comparison of at least three alternatives with REMOVE option; no new mandatory dependency; test rollback and offline-first evidence archive.
P7 — Return as **new R42 implementation Draft PR** separate from frozen #401/#403, actual source diffs, 8-object custody ledger, typed fail-close tests, 14 physical hold ledger, FC2 cryptographic proofs or GAP, optional real JVM/Gradle run, W1 method and raw witnesses or NOT_VERIFIED, SHA256SUMS + ZIP/sidecar through canonical transfer, independent second-party rehash or NOT_ESTABLISHED. Existing #400 and #402 remain linked.

## Separate terminal acceptances; DO NOT move to R43 yet
R42_R2_EXPERT_SYNTHETIC_RESEARCH_RECEIVED_C1 = report and isolated synthetic test level
R42_ACTUAL_SOURCE_REPAIR_VERIFIED_C1 = NOT_ESTABLISHED
R42_FC2_AUTHENTICITY_VERIFIED_C1 = NOT_ESTABLISHED
R42_PUBLIC_W1_RAW_WITNESS_VERIFIED_C1 = NOT_ESTABLISHED
R42_GRADLE_INTEGRATION_VERIFIED_C1 = NOT_ESTABLISHED
R42_PHYSICAL_GATES = 14_HOLD
R43_PREPARATION = WAIT_CURSOR_R42_IMPLEMENTATION_RETURN_PLUS_AXIOM_ADJUDICATION

NEXT = CURSOR_RECEIVER_ACK_AND_R42_R2_SOURCE_REMEDIATION_RETURN → AXIOM_INDEPENDENT_BYTE_AND_TEST_ADJUDICATION → R43_PREPARATION_BY_AXIOM.

No publication, merge, Hostinger write, device capture, APK installation or claim promotion authorized by this issue.
