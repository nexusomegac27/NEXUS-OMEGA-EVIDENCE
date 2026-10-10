# NEXUS OMEGA · AXIOM adjudication of operator-submitted META-style R26-R2 cross-review

```text
OBJECT = NEXUS_OMEGA_AXIOM_META_R26_R2_SCOPED_CROSS_REVIEW_ADJUDICATION_20261010_R0
DATE = 2026-10-10
FROM = AXIOM_EPISTEMIC_GOVERNANCE
SOURCE_PROVIDER_CLAIMED = "Meta AI / Muse Spark 1.1"
SOURCE_PROVIDER_AUTHENTICATED = NO
SOURCE_TRANSMISSION = OPERATOR_UPLOADED_PLAINTEXT
SOURCE_TEXT_FILE = META_AI_R26_R2_C1_SCOPED_CROSS_REVIEW_SOURCE_EXACT_20261010_R0.txt
SOURCE_TEXT_ORIGINAL_BYTES = 3923
SOURCE_TEXT_ORIGINAL_SHA256 = 7c8c3fe20f75f22d49d92f063b3dfc88a911d852d95ed6e72bf047eed0d36074
SOURCE_TEXT_ORIGINAL_GIT_BLOB_SHA1 = fc1b0814a03ac3eda265a9747b0a287241262169
SOURCE_TEXT_LINE_ENDINGS = CRLF_89
R26_TARGET_PR = 70
R26_TARGET_HEAD_AT_REVIEW = 41ab803d415a72c12a29babc9c4c4929534fdecf
AXIOM_PREVIOUS_R2_ACK = https://github.com/nexusomegac27/NEXUS-OMEGA-EVIDENCE/pull/70#issuecomment-6102542155
CLAIM_CEILING = C1_DESCRIPTIVE_ONLY
ORIGINAL_FILE_IDENTITY = SOURCE_EXACT_PASS
MATHEMATICAL_SCOPED_REVIEW = PASS_WITH_CAVEATS_C1_3_POINTS
FULL_PRODUCER_SEPARATE_REVIEW = NOT_ESTABLISHED
D1_FREEZE = NO
D2_INHIBITION_ARMS = DESIGN_ONLY
D3_FULL_CAUSAL_ATTRIBUTION = NOT_ESTABLISHED
PR70_MERGE = HOLD_FURTHER_SCIENTIFIC_REREVIEW
PR65 = HOLD_SCOPED_UNMERGED
PR67 = HOLD_PRIVACY_HISTORY_UNMERGED
PR71 = DRAFT_PDF_SOURCE_GAP
NF05_NF06 = NOT_EXECUTED
NEW_CURSOR_WORKER = NO
R26_WWW_HOSTINGER_B2_B3 = NOT_VERIFIED
```

## 1. Provenance, exact byte intake, independence ceiling

The Operator provided a UTF-8 text review declaring itself from Meta AI ("Muse Spark 1.1") and distinct from the MISTRAL/VIBE producer. AXIOM independently inspected the **physical uploaded 3,923 bytes**, calculated SHA-256 and Git blob SHA-1, then delivered them by the authorized GitHub API with all 89 original CRLF terminators; GitHub byte and blob readback matched. The operator-transmitted document is a valid **external review submission**. It is NOT an independently authenticated statement that a particular official Meta service produced, signed, or performed it: no externally verifiable signed API receipt, service identity token or authoritative provenance chain accompanied the text. Authored-separately and identity-certified are not interchangeable.

The review explicitly limits its work to the three mathematical R2 annotation questions. It says it did **not** independently repeat R0/R1/R2 GitHub file/hash transport checks. Its line "R26_R2_SOURCE_EXACT = PASS_4_OF_4" is a claim **inherited from AXIOM's earlier API receipt**, not independently retested by this reviewer. It cannot replace the full adversarial study of the NA-1 kernel selection, m=1 onset conditions, MODEL_MAX/SUM stability and EB1-prime identifiability or the frozen NF05/NF06 experimental protocols.

## 2. Three independently scrutinized review points

### C1-1 · IEEE-754 exponent and branch selection

**CONFIRMED.** Dyadic rationals such as 1/2 and 3/4 are exactly representable by binary64 when in representable range. It is incorrect to say all noninteger rationals are unrepresentable. JavaScript/ECMAScript `Math.pow(x,y)` with a negative finite base and non-integer exponent evaluates to NaN rather than attempting a custom mathematical real odd-denominator rational root. The researcher must explicitly declare real-power branch semantics and test the implementation; no kernel freeze from the original bare `cos(x/2)^p` expression.

For `p>0` the wrapped kernel on S¹ is `K_p(Δ)=cos(wrap(Δ)/2)^p=|cos(Δ/2)|^p` (positive base after principal wrapping). An explicit `Math.pow(Math.abs(Math.cos(Δ/2)),p)` is an allowed *mathematical candidate implementation* but must still be tested for branch, seam, endpoints and floating-point precision. `exp(p·log(abs(cos)))` has the same zero/underflow/conditioning concerns and is not inherently an independent verification.

### C1-2 · Antipode and precision threshold

**MAIN COUNTEREXAMPLE CONFIRMED.** With binary64 `cos(π/2)≈6.123233995736766·10^-17`, raising to power p gives:
| p | numerical `|cos(π/2)|^p` |
|---:|---:|
| 2 | ≈3.7494×10^-33 |
| 1 | ≈6.1232×10^-17 |
| 0.5 | ≈7.8251×10^-9 |
| 0.1 | ≈2.39165×10^-2 |

A universal `≤1e-16` antipode bound is false over all p>0. As p→0+ at the **positive floating-point cos(π/2) residual**, the evaluated expression approaches 1, whereas the **exact mathematical** K_p(π)=0 for every fixed p>0. The limit/exact-point operations do not commute.

**One arithmetical mistake in submitted reviewer text:** 7.8251×10^-9 / 10^-16 = 7.8251×10^7 (approximately **78.25 million**), NOT approximately 78,000. The p=0.1 claim of 2.39×10^14 is consistent.

**Freezing recommendation:** neither `T(p)=S·|cos(π/2)_float|^p` with `S≈10` nor `max(ulp,exp(p log|cos|))` is a validated general tolerance. Such a rule may become so permissive for small p that it fails to discriminate meaningful errors; numerical library, distance-to-antipode, domain and declared p-grid matter. A practical *candidate for testing*, not an already ratified implementation, is to evaluate for `δ=wrap(Δ)∈[-π,π]`:
`K_p(δ) = sin((π-|δ|)/2)^p`.
This is algebraically equivalent on the principal interval and returns exact zero when the representation is at the same π constant. It needs tested seam/antipode floating-point fixtures, type/units/interval definition and production-language regression tests, including very small p. Do not assert `D1_FREEZE` based solely on a reviewer-suggested tolerance.

### C1-3 · EB1-prime residual bound / necessary vs sufficient

**CONFIRMED WITH PRECISE SCOPE.** Let residual vector r=f+u under an exhaustive, common-coordinate additive model and a **valid simultaneous bound** `||u||≤B`. The reverse triangle inequality yields `||f||≥max(0,||r||-B)`. Therefore `B<||r||` is **sufficient** to establish `f≠0` *under these model assumptions*; it is NOT generally necessary for `f≠0`. Cancellations can produce residuals much smaller than underlying components.

It does NOT establish the unique cause of measured residuals, actual external ephemeris error, dominant filter contribution, or a stochastic tail bound by fiat. Joint deterministic bounds cannot be interchanged with covariance without tail assumptions and confidence levels. Angular ring errors cannot be summed with Cartesian errors without proper projection and frame/units alignment. If exhaustive sources and a trustworthy ground-truth/reference model are absent, return `UNIDENTIFIABLE_WITH_CURRENT_DATA`.

The prior R26_R2 phrase `"necessary screen"` can be defensibly read as a **procedural mandatory conservative gate**, never as a mathematically necessary condition. This distinction is explicitly adjudicated.

## 3. Verdict / nonpromotion

| Topic | AXIOM disposition |
|---|---|
| C1-1 IEEE integer versus noninteger semantic scope | `PASS_C1` |
| C1-2 universal numerical tolerance invalid | `PASS_WITH_ARITHMETIC_CORRECTION_C1` |
| C1-3 sufficient versus necessary EB1′ logic | `PASS_C1` |
| Source text identity, transport | `PASS_SOURCE_EXACT_3923B` |
| Reviewer claimed Meta identity / independence certification | `UNVERIFIED_ORIGIN_ATTESTATION` |
| Full R26/R1-R2 independent scientific rereview | `NOT_ESTABLISHED` |
| D1 kernel freeze, D2 arms, D3 attribution | `UNCHANGED_NOT_FROZEN` |
| R26 confirmatory experiment | `NOT_EXECUTED` |
| PR70 merge | `HOLD_SCOPED` |

**Do not promote** self-declared `VERIFIED_3_OF_3` to `FULL_INDEPENDENT_R26_REVIEW_PASS` or `R26_TERMINAL`. The scope is three math points, one of whose numerical ratios is erroneous; the formal submitting service remains unauthenticated. This is a valid useful partial external critique, not a terminal independent science gate.

## 4. Minimal next causal action

1. Deliver **this exact source file** and the AXIOM adjudication in a GitHub API research branch with detached machine manifest and linked PR. Emit API intake ACK on PR70 referencing source hash and limited findings.
2. Correct/annotate the numerical factor in a successor **non-destructive** erratum; no rewriting of source.
3. Commission or retrieve a distinct broad adversarial scientific review of NA-1 kernel, mode-inference scope, matched MAX/SUM normalization, SGP4 error attribution and trial-design/negative fixtures with concrete falsifiers and actual Github origin, then adjudicate. Do not over-burden the whole R26 MAXI with repetitive self-hash work.
4. Keep MISTRAL/VIBE PR70 OPEN; PR65 and PR67 remain respective scoped holds; PR71 binary-source gap remains independent.
5. The operator-reported Cursor dual-domain routing maps R26 **LIVE research to nexus-mobile.de only**, nexus-online.de is coordination; the routing ACK is not a Hostinger B2 deploy or B3 WWW readback. No new Cursor worker, no DNS changes.

*NEXUS OMEGA — Quelle ist nicht Wahrheit. Prüfung bleibt das Fundament.*
