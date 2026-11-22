# NEXUS OMEGA · R41 STAGE-2 · E17–E20 + W1

OBJECT = NEXUS_OMEGA_AXIOM_R41_STAGE2_INDEPENDENT_EXPERT_FALSIFICATION_AND_BODYTWIN_LIVE_SOT_20261122_R0
AUTHORITY = OPERATOR_ALEXANDER_VIA_AXIOM
STATE = EXPERT_RESEARCH_MISSION_POSTED_NO_ACTOR_ACK
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
ALT_D_DO_NOT_RUN_ACTIVE; BODYTWIN_VALIDATED=NO; CONSENT_BIND=OPEN
NO_DEVICE_CAPTURE; NO_APK_INSTALL; NO_HOSTINGER_WRITE; NO_WWW_WRITE; NO_PR_MERGE
EXTERNAL_WRITE = DENY_PENDING_REGISTRATION
EXPERT_QUORUM = NOT_ESTABLISHED

## Source-exact causal bridge and custody
The parent R41 Cursor BodyTwin/Expert Intake Bind Return was independently received and rehashed by AXIOM:
- ZIP = 4966 bytes, SHA256 = 2e050df80d825b039d0848c67b7be8becca971a27d2c32381c0ef2032a431436; CRC PASS; internal 5/5 SHA-256 PASS.
- Original sidecar 167 bytes SHA256 = 84ff96db155c9c95aa60c181661c572b28297aa18e5fda2693b1045bae89fcd3; CONTENT_MATCH.
- E17–E20 original advisory ZIP = 32522 bytes, SHA256 = 8f9065ca54b236de2537f57ef29522d4d1ca47364bfc486fd9c733b0538dbd7f; internal 7/7 reported and ZIP CRC checked by AXIOM.
- AutoClaw X15 advisory ZIP = 55986 bytes, SHA256 = 58dd8aaa0e9f20ea77842d9c89b06716849caa050b1fc4cf50dfff33f4f78a79; 5/5 reported, CRC checked.
- R41 implementation origin = Issue #395; Draft PR #396 HEAD ba3f187daa1949c712bba9b822ab6005d0ae6363 (4 offline C1 statuses sourced by two producer-local receipts; no Gradle runtime proof).
- Public BodyTwin read-only parity origin = Issue #397. Historic R40 Stage1 Draft PR #393 HEAD 8122c422a75ef9a7979775a554bd35ec9e41d340; all 14 physical hard gates unchanged.
- The original ZIP itself is NOT hosted via this GitHub issue. Local separately sealed full Stage-2 expert package: 13166 B SHA256 4a8227241c6129b6affd68157477801df50700dde20a0ad5e8ef0b0c9b977650; GitHub post != ZIP_RECEIVED.

## Freeze four key findings as hypothesis candidates, not promotions
1. E17: source filter `should_accept_sample(deadline, now)` has zero/negative deadline -> accept all, and missing event timestamp; delivery vs origin time is conflated. The source snippet is in PR #396.
2. E17/X15: 6001 creation-in-window samples, 6000 accepted after event-time + drain; missing one sample remains a material falsifier. An unmeasured fixed drain interval must not be claimed lossless.
3. E18: reported synthetic naive coverage 0.354 vs alternative ~0.95 is NOT OPPO device accuracy and must be independently re-executed with identical seeds/model/physical units.
4. E19: legacy status aggregator failed 5/5 adversarial inputs while a proposed reference validator blocked 5/5; actual R41 runtime-level independent reproduction NOT_ESTABLISHED.

## E17 — Android Sensor Runtime / Dual-Time Admission Control (PRIORITY 1)
Independently propose, implement and falsify four **competing policies**: A delivery-only reject, B event-time-only, C event-time + bounded drain + quarantine, D DO_NOT_RUN. Preserve exact event-time vs delivery-time and explicit clock domain. Invariants: valid start < deadline; event_time in [start, deadline); late arrivals bounded by evidence-based drain; post-deadline event origin always rejected; unknown clock, missing timestamps, deadline <=0 MUST ABORT instead of accept-all.
Run at least N17-01..N17-10: zero and negative deadline, missing timestamp, event exactly at deadline, late in-window delivery, out-of-window event with early delivery, FIFO reorder, time rollback, activity lifecycle interruption, flush timeout; plus X15 6001/6000 proof or independent refutation. Provide JVM/Android integration test plan and separable hermetic runner. `GRADLE_PASS` only if actually executed.

## E19 — Evidence Verification / Adversarial Governance (PRIORITY 1)
Build reference fail-closed engine: trusted expected SHA from independently authorized manifest, raw-byte hash before trust, verified author/scope/signature/nonces/version, source pin, expiry, second-party provenance; no self-generated `verdict=PASS` suffices. Split **SOFTWARE_EVIDENCE** and **PHYSICAL_EVIDENCE** and combine noncompensatorily. Run at least N19-01..N19-12: forged PASS, post-check file swap, replay, path traversal, actor spoof, expired receipt, producer as sole validator, JSON canonicalization ambiguity, wrong bytes hashed, 4 pseudo-gates from 2 receipts, false merge-authority, R40_CLOSED=>PHYSICAL_GO. Positive real-authenticated control required; no blanket reject treated as success.

## E18 — Independent metrology, uncertainty and nonlinearity
Compare M0 diagonal RSS/angular noise (negative baseline) vs M1 full PSD covariance GUM with Mount/Bias/Clock cross-terms vs M2 Monte-Carlo propagation from raw ACC/GYRO components rather than directly added angular noise vs M3 independently characterized angle reference. Explicit JCGM GUM/2026 nonlinear amended scope. At least 8 negative tests incl rho=+0.7, correlated common-mode, invalid non-PSD matrix, seed change, nonlinear tilt, unmeasured Type-A, yaw gauge and units confusion. Coverage 0.354/0.95 only as *scenario*, include sample size, uncertainty of estimated coverage, data provenance. Never claim independent OPPO calibration.

## E20 — Competing architecture / scientific innovation
Offer at least three genuinely different, falsifiable alternatives (event sourcing, capability-bound attestations, differential source replay/state machine or better independently defended options), each with strongest counterargument, null model, >=3 unique hard-negative tests, non-goals, rollback, modular fallback and no new mandatory cloud or commercial dependency. Designs can explicitly reject R41 components. Cost of complexity and maintenance must be discussed.

## W1 — mandatory *independent* public BodyTwin witness (parallel to E17/E19)
Read only exact four endpoints:
1. https://www.nexus-mobile.de/bodytwin/
2. https://www.nexus-mobile.de/bodytwin/live/current.json
3. https://www.nexus-mobile.de/research/bodytwin/state.json
4. https://www.nexus-mobile.de/bodytwin/updates/

Cursor HTTP **REPORT ONLY** snapshot: current.json 1130B SHA a6eb83752e9c5d606cd904e29f0f88afc8b16c0930ca813a75427ebdc89a04f4; producer generated_at=2026-11-22T20:55:02Z, seq=4320; source_changed=false, source_updated_at=2026-11-07T20:50:02Z; STATUS raw SHA b49d28a61656080d49a299d380989d7a7ef9496638f36dad41b160f9cc60262d versus embedded d110095535e8b455293c476479abbe3d2fc9102fc741b4624e0a81cd6ebd9ca1 => differs; LIVE SHA 60674103ed2f7afdf73788a757dd5d2547a344fd1f813204a1f509096f6f88e2 matches embedded; MEMORY SHA 4ccc495e242313423707c37b7f4a34e412c3fa7e1ebdcd93356066886028faa9 matches embedded; research state 93e24636dc980c16096c632630cf5ed3dd24eed8ea7857d1d7b0ed76cf245d81; HTML 82349B SHA 69f3a5cf08fe7eb4ae602c2105aa2696c378e486e9587db8ef376a4e5e395a66.
**None is AXIOM independent HTTP raw-byte witness**. Older connected-browser tab showed seq 4318 @20:45:02Z, not a proof of new drift. Last independent AXIOM web GET of raw endpoints inaccessible; class NOT_VERIFIED, not SITE_DOWN. Experts capture actual HTTP status, raw bytes hash, server cache headers, embedded and browser render, canonicalization, reducer sequence and source metadata, *two time-separated snapshots* if accessible. Distinguish source delta from producer tick. STATUS root cause must be a falsifiable diagnosis (stale embed / canon version / projection / server cache / true semantic source difference). LIVE/MEMORY parity cannot mask STATUS. At least 12 negatives: tick-only, source-only change, STATUS-stale, LIVE masks STATUS, schema drift, 304 w/o cached payload, bad MIME, truncated JSON, HTTP block, reducer rollback, client clock jump, false BodyTwin-valid claim, service-worker stale HTML, private/CAS leak. No writes or deploys.

## Accepted deliveries A–J
(A) source pins and SHA; (B) original hypothesis and competing method; (C) >=5 genuinely new negative fixtures per lane; (D) reproducible original runner or NOT_EXECUTED; (E) clearly separate ORIGINAL/SYNTHETIC/DESK/REPORTED_ONLY; (F) actor registration + preexposure lineage or INDEPENDENCE_GAP; (G) all 14 R40 physical gates held; (H) operator, consent, BodyTwin and C1 wall held; (I) no secrets/private data or public write; (J) machine-readable return + manifest, secondary rehash or SECOND_PARTY_NOT_ESTABLISHED. Real registered distinct authors >=3 for independent quorum; documents from one multi-track model remain n_eff=1. GitHub Issue posted is an invitation, NOT provider acknowledgment.

## Disposition
Priority E17 + E19 and W1 in parallel, E18 and E20 research without unnecessary serial holds. Expert return(s) to be source-exact, independently rehashable, separate GitHub draft PR after actor registration/permission or operator-relayed package explicitly unauthenticated; **no direct expert write permissions granted by this post**. Cursor continues Issue #395 and #397 within their original scoped authority. AXIOM adjudicates only after received originals. NO_CLAIM_PROMOTION.

The local expert package contains five authored source docs + 5/5 SHA256SUMS and machine-return schema, ZIP 13166B SHA256 4a8227241c6129b6affd68157477801df50700dde20a0ad5e8ef0b0c9b977650; return must record whether original ZIP bytes were actually received or not.
