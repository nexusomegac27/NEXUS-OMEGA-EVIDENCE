# NEXUS Ω OMEGA — R46-4 external scientific mission (order draft, GLM_R1 lane)

OBJECT=NEXUS_OMEGA_AXIOM_R46_4_OPPO_BODYTWIN_REFERENCE_METROLOGY_ORDER_20261127_R0
STATE=ORDER_READY_FOR_OPERATOR_PUBLICATION
PARENT=R46-3 (Issue #470, return GLM_R1 adjudicated ACCEPTED_WITH_RESERVATIONS, receipt comment 7222655788)
SCOPE=R46-4 reference metrology, calibration and measurement uncertainty — design-only. Strict OPPO CPH2219 → NEXUS_APP → private evidence → BodyTwin https://www.nexus-mobile.de/bodytwin/ line.

## Standing rules (inherited, unchanged)
No Cursor involvement, handoff, dispatch or repair orders until operator-declared R46-9 series closeout. No new physical capture, no APK install, no public writes, no unrelated agent research. Aggregate-only inputs; no private raw or raw-digest access by external experts. C1_DESCRIPTIVE_ONLY, no claim promotion, formal gate credit NONE.

## Carried constraints from the adjudicated R46-3 return (binding)
- C1: mag_stdev identifies only the projection e_g'·Σ·e_g of the noise covariance onto the gravity direction (R46-3 F04/W12); any per-axis statement requires a multi-position design.
- C2: the "0 gaps over 5×median" statistic is gap-blind (R46-3 F03/W09); recording designs must demand a gap histogram or loss counter.
- C3: SD/ddof definitions must be documented at the producer (R46-3 W13).
- C4: gravity_residual must carry its exact formula field (R46-3 F02/W06/W07).
- C5: local-gravity correction requires an independent reference (R46-3 F08/W19, ABSTAIN standing).
- C6: orientation/heading is not derivable from stationary magnitude aggregates (R46-3 F05/W16).

## A — P0: six-position static calibration DESIGN (no measurement)
Formulate the design: a_meas = S·a_true + b + noise with S = scale/misalignment matrix, explicit sign/frame convention per Android SensorEvent docs. Derive identifiability: per-axis affine parameters require at least two distinct true-axis excitations (±g); full S,b (12 parameters) is identifiable from the six standard positions up to documented gauge choices. Provide executable rank witnesses (04_REFERENCE.js), target widths, conditioning, and the finite-sample dependence of scale/bias uncertainty. Provide the minimum raw-field list (per-axis timestamps, exact frame/units, ddof, gap histogram) for a future authorized capture. NO device interaction.

## B — P0: uncertainty budget per GUM
Build a written uncertainty budget template for stationary magnitude statistics and for future six-position calibration: statistical term (sd/sqrt(N) class), model-conditional terms (C1), reference uncertainty (local g, angle), and explicitly UNKNOWN entries (whiteness, drift, effective sample size). No numerical placeholders: missing inputs stay NOT_COMPUTED/SOURCE_GAP.

## C — P1: dynamic roll metrology DESIGN (no measurement)
Design a controlled roll experiment with an independent angle/time reference (design only): observable target (scale/misalignment in the roll plane), required sampling and duration, expected identifiability under documented assumptions, and the falsifiers. Preserve R39 14 gates and ALT_D; no permission to measure.

## D — P0: app→WWW semantic lineage for metrology outputs
Every metrology result must carry: evidence class, provenance, exact formula field, time basis, uncertainty, validity limits (R46-3 F01/F02/F09). Six executable contract negative cases extended to metrology (e.g., calibration-from-one-pose REJECT, uncertainty-from-norms-alone REJECT, design-presented-as-measurement REJECT, missing-ddof-aggregate REJECT, threshold-count-as-losslessness REJECT, local-g-without-reference REJECT).

## E — P0: integrated conclusion
Minimal target-specific acceptance requirements for R46-4 deliverables, exact falsifiers, updated evidence request list for the R46-9 consolidated Cursor return.

## Return contract (unchanged)
Independent expert returns: own lineage, prereg frozen before run (hash recorded), runnable offline code, full outputs, counterexample witnesses, exact source DOIs/links, resource receipt incl. retries and unknowns, limitations. GitHub-bound ZIP + SHA-256 sidecar via authorized custody; API custody carries UTF-8 payloads only, so byte-exact base64 transport files are acceptable. INTERMEDIATE_CURSOR_HANDOFF = PROHIBITED. NEXT_CURSOR_HANDOFF = R46_9_SERIES_CLOSEOUT.

NEXUS Ω OMEGA
