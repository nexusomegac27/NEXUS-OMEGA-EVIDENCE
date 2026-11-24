# R43 1–9 AXIOM scientific state-of-knowledge: hard fact/falsifier/uncertainty architecture

## 1. Staged scientific objects
- L0 (partly observed): GitHub/ZIP bytes, source provenance, event clocks, state ledger and public receipt. "Uploaded", "received", "independent" and "source-origin" are **not synonyms**.
- L1: measured dual-smartphone accelerometer, gyro/magnetometer streams and reference time frame; early operator study reports quiet-state NIS≈1 and sensor-variance/Ω/k* history. No comparable real original OPPO/Pixel reference in R43 uploads.
- L2: observed/estimated kinematics of motion, step/gait events, placement, slip and latencies, requiring independent optical/pressure/IMU reference and uncertainty.
- L3: person-specific longitudinal kinematic twin across subject/session/mount/day/device, not yet established.
- L4: clinical/physiological human twin, not authorized, no validation claim.

## 2. What the nine rounds actually falsified or constrained
- E28 DSSE: custom BE32 and LE32 PAE cannot be presented as normative DSSE v1; UTF8 BYTE count from actual payload type required. Cryptographic sign fixture PASS uses demo keys, not real actor trust.
- E32 synthetic identifiability: common signed Delta may cancel in phone difference, or different source model can reintroduce it; source models must be byte-exact before comparing coverage. NIS mean1 not enough; NEES needs true state.
- Adaptive v0→v1→v2: no independent general gain; R43-5 evaluator amended after arm, R43-6 cost budget mismatch, R43-7 frozen 6 TEST cases only network_latency_correlation give v0=v2=fusion 18.303982903117085; ref-only6.6217 on task input already containing reference. Reference-only oracle is NOT equivalent to deployable phone input.
- Fisher scalar toy yA=theta+epsA, yB=theta+epsB with unit var and rho: FI single1, joint2/(1+rho), e.g. rho0:2, rho0.5:4/3, rho0.9≈1.05263. Even co-mounted phones may add information with independent noise; correlation and timing must be included.
- For theta=(theta1,theta2), y=theta1+theta2+noise, likelihood FI [[1,1],[1,1]] rank1: sum identifiable, difference not. Prior I2 makes posterior precise in difference axis without adding measurement. `ABSTAIN` target-specific, distinguish prior-based prediction from measured identification.
- Global identifiability: y=theta²+noise permits same likelihood ±theta despite local FI nonsingular away from0; do not issue global positive claim from local rank.
- Unit scaling: phi=1e6 theta makes FI scale 1e-12 for otherwise unchanged physical observation, so raw eps_rank1e-8 false negative. Candidate `kappa1e8, tau0.85, weak_frac0.05` need prereg unit/scale and empirical cost.
- Sum of near-zero eigenvalues/trace is unusable for exactly zero eigenvalues. Report nullity, projected target and reparam sensitivity.
- GUM/JCGM100/101 covariance and model structure ≠ generic FI^-1 CRB; posterior precision additivity only under stated assumptions, shared prior once, no retrospective priors calibrated against protected test.
- W1 authenticated 2×4 real HTTP-200 status/headers/body/browser parity and temporal ≥ feed interval never established externally; CDN403 challenge not proof of site outage; no CAPTCHA bypass.
- FDA official 374 vs official research GitHub370 conflict source exact; 20 people and different back vs thigh phone placements, not OPPO+Pixel co-located. UCI MHEALTH original archive now independently sha-rehashed; wearable 10-person 3-Shimmer2 and not two phones.

## 3. Original ten hard scientific passes and measured transfer status
| Gate | Scientific acceptance test | R43→Cursor checkpoint status |
|---|---|---|
| P01 | Real original app Kotlin Gradle FC2 W1 source bytes, chain & tests | SOURCE_GAP or SOURCE_REPORTED_ONLY until original operator paths rehashed |
| P02 | Actual Android event-time, batching, stop/drain, reboot/dedup calibration | R42 13/13 C1 offline report, physical reference and source independent rehash not completed |
| P03 | FC2 actual authorized signer root, roles/nonces/revocation and real verification | Demo tests only, production trust NOT_ESTABLISHED |
| P04 | 2x4 full public W1 second-party raw+browser/status interval | OPEN_PARTIAL; ≥300s not verified |
| P05 | E23 Privacy V3 public-safe release with consent, retention and redaction | HOLD |
| P06 | Licensed biomechanical original data independent physical-reference replay | UCI original Q4 bytes present, but MHEALTH is NOT dual-phone/reference-kinematics and no model replay |
| P07 | GUM/MC FIM target observability, calibrated NIS/NEES and WIS | Partially sound mathematical counterexamples; real original model and physical source absent |
| P08 | L2+ kinematic/longitudinal/clinical claim ladder with evidence | BODYTWIN_VALIDATED=NO; clinical not authorized |
| P09 | Matched-cost dual/single/differential/null/C5 original | SOURCE_GAP_C5, real comparator/holdout not run |
| P10 | Three distinct authentic independently registered evaluator families | 0_OF_3, no self certification |

Each scientific gate is orthogonal. No promoting from 0/10 because 10 log hashes matched or code fixture 400k samples simulated.

## 4. Cross-round K01–K14 thought spaces / priority
**K01 information in second phone**, K02 mount as latent, K03 boot/event/delivery-time triangulation, K04 structural identifiability, K05 GUM covariance, K06 leave-subject/phone/day/mount, K07 oracle-vs-deploy reference firewall, K08 twin L0–L4, K09 optical geometric and yaw observability, K10 event ledger vs producer tick, K11 independently tested adaptive research, K12 longitudinal privacy and consent, K13 selective risk-calibrated abstention, K14 original dataset/version/rights rehash.

P0 K07,K01,K06,K14; P1 K04,K05,K13; P2 K03,K10,K12; P3 K08,K09,K02,K11. This is a priority ordering, not scientific closure.

## 5. Verifiable-source research clause VSRD-C1 is mandatory in all future R44 experts
For every material claim use at least one official original publisher/institution/DOI/immutable Git source and a nonredundant second scientific/metadata/counterevidence route. Store exact URL/final redirect, fetched status/date/author/version/commit/retracted/rights, scope actually read, bytes SHA iff truly obtained, and Q0 candidate/Q1 identity/Q2 metadata/Q3 primary text/Q4 raw source SHA/Q5 genuinely independent evidence or QX source gap. Allow discovery of new primary sources; registry is seed not exclusion. Institutional URL or HTTP200 not validation. A registered actor and byte-integrity are separate.

## 6. Difference between authorized work and science goal
This handoff authorizes Cursor to ingest, hash, independently rerun and prepare reversible offline research/code fixes on source-exact authorized paths. It does NOT authorize human capture, APK installation, CI-triggered external deployment, Hostinger/www, merge, private/public license violations or C1→C2/C3 promotion. Operator provides actual original paths separately. R44 entrance only after explicit operator decision.
