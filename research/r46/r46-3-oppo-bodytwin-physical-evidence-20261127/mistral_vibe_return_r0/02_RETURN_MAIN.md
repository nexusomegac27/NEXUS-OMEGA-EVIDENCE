# MISTRAL/VIBE return R0 - main findings (R46-3)
OBJECT=NEXUS_OMEGA_AXIOM_R46_3_OPPO_BODYTWIN_PHYSICAL_EVIDENCE_EXPERT_ORDER_20261127_R0
EXPERT=MISTRAL_VIBE, independent external lane. CLAIM_CEILING=C1_DESCRIPTIVE_ONLY.
No formal gate credit, no physical validation claim, no production readiness claim.
ADJUDICATION=PENDING_AXIOM, SELF_ACK=NO, MERGE=PROHIBITED, CURSOR=PROHIBITED_UNTIL_R46_9_CLOSEOUT.

## 0. Transport and custody
- GitHub-only transfer per order: branch vibe/r46-3-mistral-vibe-physical-evidence-return-20261127-c1 created from the order branch axiom/r46-3-oppo-bodytwin-physical-evidence-20261127-c1 at HEAD d7e1c95d276b20254b8c30a4de4b1310d18a1b31; draft PR targets the order branch. No merge action performed by this agent.
- Transport path: agent connector push via operator-authorized custody (authenticated account nexusomegac27). Label: OPERATOR_AUTHORIZED_GITHUB_SEND_VIA_AGENT_CONNECTOR.
- Binary ZIP push is not supported by the connector; the ZIP ships as base64 text (R46_3_MISTRAL_VIBE_RETURN_R0.zip.b64) plus .sha256 sidecar. Decode: base64 -d, then sha256sum -c.
- All return documents are ASCII-only by design (see D7).

## 1. Order verification
- Order branch HEAD confirmed at d7e1c95d276b20254b8c30a4de4b1310d18a1b31; all 11 order-path entries enumerated with GitHub tree blob SHA-1.
- 5/8 text members reproduced bit-exactly through the connector text delivery and match BOTH the SHA-256 in 99_SHA256SUMS.txt AND the recomputed git blob SHA-1: 02_EVIDENCE.json, 03_SOURCES.md, 04_REFERENCE.js, 05_RESULTS.json, 06_GATES.json.
- 3/8 text members (00_START_HERE.md, 01_ORDER.md, 07_SERIES_PLAN.md) contain non-ASCII characters. Their delivered text is identical across three independent transports (connector contents API, raw.githubusercontent.com, cdn.jsdelivr.net) and consistent with the committed sizes (1154 / 5858 / 1349 bytes) and charset {U+03A9, U+2014, U+2192}, but does NOT reproduce the recorded SHA-256 nor the git blob SHA-1. Status: TEXT_CONSISTENT_LENGTH_AND_CHARSET, BYTE_INTEGRITY_UNRESOLVED (see D7). The authoritative check is operator-side: git clone + sha256sum -c 99_SHA256SUMS.txt.
- Order ZIP: the connector returns no binary content (placeholder text only). Integrity therefore rests on the GitHub tree blob SHA-1 ef342880581501efd4adf1d882fb6fea6c8eb03f and the sidecar value e3a3c946a39ff0b9c0fe084080fbee103ad70f3b28becdddb0759792b47995d0; a byte-level independent hash was NOT obtainable and stays UNKNOWN (no assertion).
- AXIOM 04_REFERENCE.js executed unmodified in this sandbox: all 7 checks true; aggregate arithmetic bit-exact: acc 100.15353299112422 Hz, gyro 100.15354838260195 Hz, median reciprocal 100.1533648475911 Hz, mean_minus_conventional_g 0.026088001091459034.

## 2. A - R21 aggregate audit findings
A1 Rates (W1): (N-1)/duration reproduces both reported rates bit-exactly (acc 100.15353299112422, gyro 100.15354838260195). Effective rate exceeds the requested 100 Hz by 0.15353299112422292 Hz; requested rate != measured rate (Android sensors_overview, SL-02). Median reciprocal 1/0.009984687 = 100.1533648475911 Hz sits just below the (N-1)/duration values, consistent with near-uniform sampling.
A2 Residual identity (W2): reported gravity_residual_mean_abs 0.026088001091459367 equals abs(mean(mag)-g0) on the rounded mean 0.026088001091459034 to 96 ULP (hex 3f9ab6d01e05f860 vs 3f9ab6d01e05f800). This matches AXIOM 04_REFERENCE. It is NOT identifiable as mean(abs(norm-g0)) without raw norms.
A3 Jensen lower bound (W3): on the two-point distribution {m-s, m+s} that matches the reported mean and population SD exactly, abs(mean-g0) = 0.026088001091459034 while mean(abs residual) = 0.026088001091459034; gap = 0. abs(mean-g0) is only a lower bound.
A4 Local gravity conflation (W4): with plausible German local g in [9.806, 9.822] m/s^2 (example 9.8105), the residual 0.026088001091459034 shrinks to 0.022238001091459125; the remainder conflates sensor bias and scale error. Conventional g0 was not an independently measured local value.
A5 SD definition UNKNOWN (W5): population vs sample SD differ by factor 1.000071293622876 at n=7014 (~71 ppm). Any downstream uncertainty statement needs the ddof definition.
A6 Gap rule blindness (W10): removing 70 of 7000 synthetic events in clusters of <= 4 consecutive events yields a maximum gap of exactly 5x median dt; the strict > 5x-median rule flags 0 gaps. R21 gaps_gt_5x_median = 0 therefore does NOT establish zero packet loss.
A7 Phase synchronization between ACC and GYRO cannot be checked from aggregates; per-event timestamps are absent (SOURCE_GAP).
A8 Units and frames stay conditional on the actual Android SensorEvent mapping in NEXUS_APP (SL-01 defines standard units and device coordinates; the app mapping is PRODUCER_REPORTED only).
A9 From norms alone NOT computable: axis covariance, bias vector, Allan curve, effective sample size, whiteness, drift, calibration, NIS/NEES, confidence intervals. 12 aggregates summarize 14018 events; 99.91439577685833 percent of event-level information is absent (W11).

## 3. B - Identifiability and bounded calibration
B1 Measurement model with explicit conventions: a_meas = M R^T g + b + dynamic_acc + noise; omega_meas = R^T omega_world + b_gyro + noise. Unknowns: 9-entry M (scale + misalignment), 3 + 3 biases, local g magnitude/direction, noise law.
B2 Norm orientation (W6): magnitude is SO(3)-invariant up to double-precision round-off, max norm error over deterministic rotations = 1.7763568394002505e-15 (double-precision round-off level, <= 1e-12). Tilt and yaw are unobservable from norms; BodyTwin body-pose inference from phone-on-table magnitudes is unsupported.
B3 Axis covariance invisible (W7): constructions with all variation on +Z vs variation split X/Y give identical magnitude mean/SD while axis variance is diag(0,0,v) vs diag(v/2,v/2,0).
B4 Temporal order invisible (W9): three orderings of the same multiset share mean 0 and population SD 2.7386127875258306 while lag-1 autocorrelation takes -0.8333333333333334 / 0.6 / 0.65.
B5 Bias/rotation ambiguity (W8): constant gyro bias and constant true rotation are observationally equivalent (two-worlds witness). Gyro magnitude mean = 27.155570045359095x Earth rate = 0.11345775136782411 deg/s; Earth-rate comparison alone cannot resolve the ambiguity; an independent angle reference is required.
B6 Scale/bias ambiguity: one-pose affine calibration is non-unique (04_REFERENCE models witness, reproduced bit-exact).
B7 Independent challenge of 04_REFERENCE and of the shipped error cases: E1 (1e-9 relative fault) FLAGGED as intended; E3 comparator ACCEPTs the genuine hash and REJECTs a single-hex-digit manifest tamper as intended. E2 (1e-13 relative fault vs fixed 1e-12 absolute tolerance) deviates from its intended lesson and is documented honestly in 05_RESULTS_R0.json error_case_observations: at value magnitude ~100.15 Hz the fault is ~1.0e-11 absolute, so the fixed tolerance caught it (FLAGGED, not MISSED). The ULP-scaled tolerance recommendation (N21) stands regardless.
B8 Compatible-set assessment for target quantities from ONLY {n, duration, rates, median_dt, gap count, mag_mean, mag_stdev}: orientation -> EMPTY set (ABSTAIN); {local g, bias, scale} -> non-empty but degenerate conflation (ABSTAIN on separation); no finite target width from these aggregates.
B9 Calibration DESIGNS ONLY (no measurement authorization; R39 14 gates and ALT_D preserved):
- D-R46-4-a stationary rest with independent local-g reference and sample/timing design.
- D-R46-4-b six-position static calibration for M and b (12-parameter model per SL-06), uncertainty budget per JCGM GUM (SL-10).
- D-R46-4-c controlled roll with independent angle/time reference for gyro scale/bias/axis alignment.
Essential raw fields for future PRIVATE replay: per-event (sensor type, 3 axis values in device frame, timestamp on a single declared time base, event index) plus declared units/frame mapping, ddof definition, app version, device model. No raw publication.

## 4. C - App to WWW semantic lineage
C1 Layers: L0 raw immutable private; L1 deterministic reconstruction with target/uncertainty/provenance; L2 synthetic Dream separate; L3 approved minimal projection. Details and golden schema in 07_EVIDENCE_CONTRACT_R0.json.
C2 The R21 physical aggregate (2026-11-09) is DERIVED_FROM_CURSOR_PUBLIC_SAFE_AGGREGATE_NOT_RAW and is distinct from any live feed.
C3 Fresh bounded receipts, 2026-11-27, text-level: /bodytwin/ (4,479 chars, sha256 6415480698a1eb8d422f6e0de1d8d3bd6b327f7993966fc9d150d87c2d328958) declares C1_DESCRIPTIVE_ONLY, promotion FALSE, phase5 FALSE, live_class AUTHORITATIVE_LIVE_SOT, canon V8.4.5 (prior-session capture additionally: BODYTWIN_VALIDATED NO, Consent OPEN, Trial 001 DESIGNED_NOT_EXECUTED, physical IMU NOT AUTHORIZED, last feed 2026-11-22T21:55:02Z, last real source change 2026-11-07T20:50:02Z). /bodytwin/live/current.json (1,130 chars, sha256 4434ba71548608e876d38ec8abb7238a7d85d6178d4ca6f37f8dfd29e1a36450) is schema nexus-bodytwin-live-feed/1, run_utc 2026-11-27T12:50:02Z, seq 5663, source_changed=false, gates physical_imu NOT_AUTHORIZED, bodytwin_validated NO, trust SELF_HOSTED_PUBLIC_C1_NOT_INDEPENDENT_WITNESS. /bodytwin/status.json and /forschungsstatus.json returned the transport block placeholder: status NO_DATA, no outage asserted.
C4 This supersedes the AXIOM failed /bodytwin/ fetch at TEXT level only; byte-level body hashes remain unobtainable through the text transport (D7). Receipt class: OBSERVED_INDEPENDENT_TEXT_LEVEL.
C5 Producer tick vs source change: live/current.json carries producer run_utc/seq with source_changed=false; source freshness must come from source-change fields, never from tick freshness. historical vs live is explicitly labeled in the feed schema.

## 5. D - Evidence transfer integrity
D1 Order intake dual-verified for 5/8 ASCII members (SHA-256 sums + git blob SHA-1), see section 1.
D2 Return readback: every pushed return member is fetched back and compared to the pushed text; ASCII-only design makes byte-exactness checkable (results in 05_RESULTS_R0.json verification and MANIFEST_SHA256_R0.json).
D3 Privacy: this return contains no raw data, no raw digests, no device serials, no session paths.
D4 Missing raw or missing model -> SOURCE_GAP / NOT_COMPUTED only; no numerical placeholders.
D5 B4a (observer readiness before approved effect) and B4b (independent readback after) remain DESIGNS ONLY.
D6 No new tool permissions; no Cursor; no new capture; no installs; no live writes; no merge.
D7 NEW transport finding: non-ASCII content does not survive the available text transports byte-faithfully (section 1). Mitigations shipped with this return: ASCII-only documents; ULP-scaled and transport-probe controls (08_GATES N22/P06); operator-side git clone + sha256sum -c recommended as the authoritative order verification.
D8 Environment finding: bash sha1sum/sha256sum in the authoring sandbox are broken (error: Cannot read properties of undefined (reading digest)). SHA-256/SHA-1 were self-implemented and verified against official NIST test vectors (empty, abc, quick-brown-fox, 56-byte NIST vector, 1,000-byte vector). A bit-length encoding bug (dropped (bl>>>8) byte) that earlier caused false verification failures was found and fixed; all hashes in this return come from the verified implementation.

## 6. E - Integrated conclusion
AR1 Rates: any 100 Hz sampling claim must state requested vs effective rate and the (N-1)/duration definition (W1; falsifier F1).
AR2 Residual metrics: any gravity residual claim must state WHICH statistic and the ddof (W2/W3/W5; falsifier F2).
AR3 Orientation/pose claims from magnitude-only data are PROHIBITED (W6/W7; falsifier F3). Units/frame mapping must be declared from the actual app code.
AR4 Temporal/whiteness/drift/NIS/NEES claims require raw data or an independent reference (W8/W9; falsifier F4).
AR5 Live/BodyTwin status claims must cite a bounded receipt with route, time, text sha256, and the text-level caveat (C3; falsifier F5).
Evidence request list for the R46-9 consolidated Cursor return:
1. R21 raw NDJSON for PRIVATE replay only, or per-axis histograms plus a representative timestamp sample.
2. SD definition (ddof) and the exact producer aggregation code path.
3. The actual Android SensorEvent mapping in NEXUS_APP (frame, units, time base).
4. A local-g survey value for the capture site or an independent reference measurement.
5. Byte-level checksums of the public BodyTwin routes (curl -s | sha256sum) to close D7.
6. Actual Kotlin/Gradle outputs and APK source XML for the 226-test app lineage claim.

## 7. Limitations
- C1_DESCRIPTIVE_ONLY throughout; designs are not executed tests; synthetic witnesses are not physical evidence.
- Text-level receipts cannot prove byte-level page state (D7); order ZIP bytes unverified by this agent (UNKNOWN).
- 3/8 order text members byte-integrity unresolved (D7).
- Prereg timestamp is local only, not externally attested.
- No access to private raw, no independent local-g measurement, no device access, no subagents.
- Resource receipt: 09_RESOURCE_RECEIPT.json. Executed outputs: 05_RESULTS_R0.json.
