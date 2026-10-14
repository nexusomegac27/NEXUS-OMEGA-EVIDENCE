# MATH_PROOF_AND_COUNTEREXAMPLES.md (Lane M) — C1, signed scalar real lambda

All computations in this document were executed in a deterministic TypeScript sandbox; the SHA-256 implementation used elsewhere in this return is FIPS-180-4 self-tested and is unrelated to these numeric results (pure floating point, double precision).

## M1 — Basel refutation of the prior witness; correct witness for l2 strict subset c0

Claim under test: d_t = 1/(t+1) witnesses D2 strict subset D0 on t >= 0. FALSE.
Proof: sum_{t>=0} 1/(t+1)^2 = sum_{k>=1} 1/k^2 = pi^2/6 (Basel problem) < infinity, and 1/(t+1) -> 0, so d is in l2 and in c0; it cannot witness proper containment. Executed check: partial sum to 10^6 terms = 1.64493306684877 vs pi^2/6 = 1.6449340668482264 (match within 1e-6). Correct witness: d_t = 1/sqrt(t+1). Then d_t -> 0 (executed: d at t = 10^6 equals 0.001) but sum d_t^2 = sum 1/(t+1) is the harmonic series and diverges (executed: partial sum 14.392726722864989 at 10^6 terms, consistent with ln(10^6)+gamma approx 14.3927). Hence c0 minus l2 is nonempty and l2 is a proper subset of c0. QED.

## M2 — ISS convolution gain in l2 for all signed real |lambda| < 1; sharpness; maximizing frequency

System: e_{t+1} = lambda e_t + d_t, e_0 given; solution e_t = lambda^t e_0 + (h * d)_t with causal kernel h_j = lambda^j, j >= 0.
(1) Gain bound: ||h||_1 = sum |lambda|^j = 1/(1-|lambda|). Young's convolution inequality: ||h*d||_2 <= ||h||_1 ||d||_2 = ||d||_2 / (1-|lambda|). Executed randomized check: 0 violations in 200 trials across lambda in (-0.95, 0.95).
(2) Sharpness: the operator norm of convolution by h on l2 equals sup_omega |H(omega)|, H(omega) = 1/(1 - lambda e^{-i omega}) (Parseval multiplier of the bilateral extension; the causal l2(N0) norm equals the same supremum as the limit of finite sections). |1 - lambda e^{-i omega}| is minimized at omega = 0 for lambda >= 0 (value 1 - lambda) and at omega = pi for lambda < 0 (value 1 - |lambda|). Therefore the gain is exactly 1/(1-|lambda|), sharp, with maximizing angular frequency 0 for lambda >= 0 and pi for lambda < 0. Executed check: fine omega-grid spectral maximum equals 1/(1-|lambda|) to < 1e-6 for lambda in {-0.9, -0.5, -0.3, 0.3, 0.5, 0.9}, argmax omega = pi exactly for negative, 0 for positive; truncated alternating-kernel sums converge to the bound (e.g. lambda = -0.9: omega=0 kernel sum 0.526..., omega=pi kernel sum 10.0).
(3) Conservative combined estimate (used by the R5 erratum): with (a+b)^2 <= 2a^2 + 2b^2,
||e||_2^2 <= 2|e_0|^2/(1-lambda^2) + 2||d||_2^2/(1-|lambda|)^2.
Executed randomized check: 0 violations in 200 trials. (Tighter non-conservative form: (|e_0|/sqrt(1-lambda^2) + ||d||_2/(1-|lambda|))^2.)

## M3 — Finite N=1000 counterexample at lambda = -0.5; falsification of the 2/(1-lambda)^2 universal denominator

Setup: lambda = -0.5, e_0 = 0, d_k = (-1)^k for 0 <= k < 1000, N = 1000.
Closed form (proof by induction): e_t = (-1)^{t-1} (2 - 2^{1-t}); trace executed: e_1 = 1, e_2 = -1.5, e_3 = 1.75, e_1000 = -2.
Exact sum: sum_{t=1}^{1000} e_t^2 = sum_{t=1}^{N} (2 - 2^{1-t})^2 = 4N - 8(1 - 2^{-N}) + (4/3)(1 - 4^{-N}) = 4000 - 8 + 4/3 (to machine precision) = 3993.333333... Executed recurrence: 3993.333333333333; executed closed-form sum: identical (difference < 1e-9).
Invalid universal bound: 2N/(1-lambda)^2 = 2000/2.25 = 888.8888888888889. The executed sum 3993.333... exceeds it by factor 4.4933. The universal claim FAILS. Randomized falsification: with negative lambda in (-0.8, 0) and random inputs, the invalid formula was violated in 112 of 200 trials.
Corrected bound: 2N/(1-|lambda|)^2 = 2000/0.25 = 8000 >= 3993.333... holds. Alternatives per order M3: either use |lambda| universally, or explicitly restrict the theorem to 0 <= lambda < 1 (where 1-lambda = 1-|lambda| and both forms coincide).

## M4 — e_t -> 0 under d_t -> 0; vanishing vs l2 energy; scope

e_t = lambda^t e_0 + sum_{j=0}^{t-1} lambda^{t-1-j} d_j. Fix eps > 0. Since d_t -> 0, choose T with |d_j| <= eps(1-|lambda|)/2 for j >= T. The tail sum is bounded by eps(1-|lambda|)/2 * sum_k |lambda|^k = eps/2. The finite head and lambda^t e_0 vanish as t -> infinity because |lambda| < 1. Hence limsup |e_t| <= eps/2, and eps was arbitrary: e_t -> 0. This uses only d in c0 — strictly weaker than l2; the l2 gain bound (M2) requires d in l2. Distinction is real: d_t = 1/ln(t+20) is in c0 but not l2, and e_t still vanishes. Executed demo: lambda = 0.999, e_0 = 1000: e = 999.334 (t=0), 86.934 (t=10^5), 81.960 (t=2*10^5), decaying toward the quasi-steady value d_t/(1-lambda) -> 0. Scope of all statements: scalar real lambda; e_0 explicitly included; infinite-horizon l2 statements, with finite-N counterexamples valid in finite truncation. Generalization to vector/matrix A is NOT claimed and is false in general without induced-norm or semigroup estimates (nonnormal matrices: eigenvalues inside the unit disk do not bound ||A^k||; a Kreiss-type estimate or explicit ||A^k|| bound is required). No C2 promotion.

## M5 — Minimal erratum diff and corrected theorem

Erratum diff (one denominator, one hypothesis line):
- CHANGE: "2/(1-lambda)^2" -> "2/(1-|lambda|)^2"
- ADD hypothesis line: "valid as written for all signed real |lambda| < 1; the (1-lambda)^2 form requires 0 <= lambda < 1"
- ADD: "sharp l2 impulse gain = 1/(1-|lambda|); maximizing frequency 0 for lambda >= 0, pi for lambda < 0".

Corrected theorem: For real scalar lambda with |lambda| < 1, initial value e_0 and disturbance d in l2(N0), the solution of e_{t+1} = lambda e_t + d_t satisfies
||e||_2 <= |e_0|/sqrt(1-lambda^2) + ||d||_2/(1-|lambda|),
the input-output gain ||h*d||_2/||d||_2 is at most 1/(1-|lambda|) and this constant is sharp, and if additionally d in c0 then e_t -> 0. No universal bound of the form C/(1-lambda)^2 with C independent of the sign of lambda exists (M3 counterexample). QED.
