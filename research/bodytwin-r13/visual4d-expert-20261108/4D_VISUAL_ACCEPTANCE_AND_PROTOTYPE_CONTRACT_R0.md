# NEXUS OMEGA — 4D visual C1 executable acceptance contract
OBJECT = NEXUS_OMEGA_AXIOM_BODYTWIN_4D_VISUAL_PROTOTYPE_AND_VALIDATION_CONTRACT_20261108_R0
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
IMPLEMENTATION_STATUS = CONTRACT_ONLY / EXISTING_VIEWER_SOURCE_NOT_YET_BYTE_BOUND
NO_CLAIM_PROMOTION = YES

## Baseline required before touching live /bodytwin/
- Cursor obtains exact live viewer JS/CSS/HTML source with original HTTP status, headers, raw SHA256/bytes, browser screenshots and console errors; discover real Hostinger docroot separately.
- Current public C1 feed: /bodytwin/live/current.json; record independent raw JSON and producer seq. Do not modify feed producer, Cron, current.json schema, or receipts.public.json.
- Current viewer observed controls: Perspective, Orthographic, Stereographic, Schlegel, Double-perspective; six angle sliders XY, XZ, XW, YZ, YW, ZW; symbolic B0/B2/B3/B5/B4/B6/B7/B7' layers and humility metrics. Test all before/after.
- Map each existing mode to its *actual* code and formula. If formula missing or mislabelled, mark SOURCE_GAP / FORMULA_UNVERIFIED, not PASS.

## E1 mandatory geometry tests with deterministic seed
T01 Tesseract combinatorics: 16 vertices with +/- coordinate tuples, 32 unique edges with exactly one changed coordinate, 24 square faces, 8 cubical cells; no duplicates.
T02 Identity rotation leaves every vertex unchanged within numeric tolerance.
T03 Each one of six 4D Givens plane rotations must preserve Euclidean length and R^T R=I and det(R)=+1 within declared float precision; inverse returns to original.
T04 Disjoint plane rotations commute (XY/ZW, XZ/YW, XW/YZ); non-disjoint arbitrary rotations need not commute. Test explicit seed counterexample.
T05 Multiple angle order is explicit and fixed; reset should be byte-equivalent in serialized state, not only visually similar.
T06 Projection pipeline: clip/reject nonfinite coords, epsilon-zero denominators and near-plane singularities; no NaN/Infinity written into DOM, GPU buffer, canvas transform or CSS.
T07 Projection names must correspond to actual math. In particular Schlegel uses an interpretable cell-centered projection; isoclinic claims require independent algebraic proof, otherwise label VISUAL_HYPOTHESIS.
T08 Visual layer mapping must never turn symbolic B0/B2/etc into literal anatomy or medical labels.

## Rendering/interaction/browser regression gates
V01 Existing controls/keyboard/touch screen and 4D graph stay responsive on desktop & narrow mobile layout; original interactive viewer still mounts with zero uncaught exceptions.
V02 Animation obeys reduced-motion, user pause/resume and user control of update frequency; no disabling of live feed when 4D animation is paused. W3C WCAG 2.2 2.2.2 applies to auto-update and motion.
V03 Event bursts/slider drag do not leak event listeners or animation frames. Discarded frame work and visibility-tab pause must have deterministic state restoration; no synthetic 60 FPS performance claim absent benchmark.
V04 WebGL if chosen handles context-loss/recovery, memory pressure and mobile fallback; secure local assets, no remote third-party script. Keep Canvas2D/SVG/static fallback and offline usability.
V05 Depth, projection legends and uncertainty cues make 4D->3D->2D distinction explicit; a static screenshot is not geometric ground truth.
V06 Public live feed sequence changes are observed but marked "producer tick"; source_changed=false means same underlying source; stale/missing/future feed -> C1 hold without clearing the 4D viewer.
V07 No static source file, read-only research record, consent state or physical IMU state is altered by visual interactions.
V08 Browser performance metrics (frame time p50/p95, heap/VRAM if measurable, main-thread delays, FPS under test scene, thermal environment if measured) are collected on named devices, methods and source commit. Define reasonable thresholds only after baseline measurement.

## Test lane matrix and falsification
| Area | Positive fixture | Negative fixture | Required evidence |
|---|---|---|---|
| SO(4) | orthonormal matrix, deterministic vertex orbit | invalid angle, precision loss, noncommuting order | implementation-independent numeric results |
| Projection | five declared projection modes with clearly specified formulae | singular denominator, outside frustum, wrong Schlegel center | rendered + pure math oracle |
| Input | sliders and controls respond to mouse/touch/keyboard | rapid movement, resize, hidden tab | CDP event trace and no exception |
| A11y | pause, reduced motion, focus order | auto movement without stop; invisible labels | keyboard/manual and automated audit |
| GPU | WebGL / Canvas fallbacks working | context loss, no WebGL | return to usable view |
| Live feed | same-origin status GET and tick rendered | 404/403, malformed JSON, future time, rollback | independent HTTP/CSP/browser witness |
| Governance | symbolic Soft/Hard partition preserved | medical, clinical, consciousness, fake sensor status injection | C1 fail-closed and review |
| Deployment | preview site works and passes backward compatibility | rollback triggered by broken 4D renderer or feed | previous bytes restored, postrollback browser |

## Deliverables, staged and independently inspectable
D0: baseline census and reproducible fixtures from public-safe source, original hashes.
D1: E1/E2/E3 independent written hypotheses, alternatives, counterexamples; E4/E5 adversarial reports.
D2: independent minimal patch proposal with tests, source exact GitHub HEAD and license inventory.
D3: interactive GitHub/Hostinger staging preview **only after** rollback and CSP validated.
D4: public-safe visual-only release on the existing root when Tier A2P criteria pass; exact browser/HTTP witness, Cron/poll unchanged; otherwise finite HOLD with minimal counterexample and specific recovery, not an idle stop.
D5: evidence ZIP+sha256 with 00_EXEC,10_HANDSHAKE,20_WALLS,30_RESULT,40_MACHINE,99_SHA256SUMS. Independent rehash and claim boundary.
All D stages append only; one positive demo or image is never scientific or clinical validation.

## Feedback and autonomy loop (without "self-learning" overclaims)
For each bounded patch Cursor computes measured deltas on baseline vs candidate: defects fixed, regression count, verified reviewer disagreements, measured performance, user-visible interaction gain, deployment safety/rollback. Use observations to prioritize the next GitHub issue; do not treat historical model memory or repeated prompts as continuous autonomous execution. Scheduled tasks/agents need verifiable run IDs and source exact receipts.

Reference: https://developer.mozilla.org/en-US/docs/Web/API/WebGL_API/WebGL_best_practices and https://www.w3.org/WAI/WCAG22/Understanding/pause-stop-hide
