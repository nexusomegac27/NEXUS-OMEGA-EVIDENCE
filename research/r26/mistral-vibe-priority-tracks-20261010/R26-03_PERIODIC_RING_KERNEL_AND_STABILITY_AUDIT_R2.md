# NEXUS OMEGA · R26 — Periodic Ring Kernel Audit — R2 Precision Annotation

## MISTRAL/VIBE · annotates R26-03_R1 (non-destructive; R1 remains in force) · C1 · DESIGN_ONLY

```text
OBJECT              = NEXUS_OMEGA_R26_MISTRAL_VIBE_PERIODIC_RING_KERNEL_PRECISION_ANNOTATION_20261010_R2
ANNOTATES           = R26-03_PERIODIC_RING_KERNEL_AND_STABILITY_AUDIT_R1.md (sha256 809921233654b29bf383ecceee222da57b4dc59f2ef55b324ffae8c7b8798b83, blob 9b84b4de48c0b202397d79d5354d31c0b8b8e33b)
DOES_NOT_SUPERSEDE  = R26-03_R1 (R1 findings unchanged; this annotation encodes implementation-domain limits only)
TRIGGER             = AXIOM R1 adjudication (PR #72 merged, main b11bd1becaa47a256fe2aa8da628acd278b532e4,
                     adjudication sha256 5bad43e76f80be29e25c4cb21d194b8f272bec6db9d63aba7a4b921264b980cc,
                     sections 2A and 5.2: "successor correction/annotation must encode the branch/float-precision limits")
PARENT_ORDER_SHA256 = 4fc40bdc1898ab308617e736b6e9d0aa7eff33ff64e8964e6edc5b2b601d64d9
CLAIM_CEILING       = C1_DESCRIPTIVE_ONLY
EXECUTION_CLASS     = NOT_EXECUTED (deterministic IEEE-semantics witnesses only)
REPO_LAW            = corrections append; R26-03_R1 and R0 remain unmodified (AGENTS.md rule 5)
```

## 1 · IEEE rational-branch guard (adjudication §2A)

That even-numerator/odd-denominator rational powers are mathematically real on negative
input does NOT mean IEEE `pow` computes that branch. Deterministic witnesses
(base = cos(2) = -0.416147):

| Expression | IEEE result |
|---|---|
| pow(base, 2/3) | NaN |
| pow(base, 1/3) | NaN |
| pow(base, 1.5) | NaN |
| pow(base, 2) | 0.173178 (integer exponent: computable) |

Reason: a binary double never equals a non-integer rational, so no implementation can
infer an odd denominator from the exponent value. The real branch must be implemented
deliberately. The canonical real branch for p = a/b (b odd, a even),
sign(x)^a · |x|^(a/b), is verified to coincide with |x|^(a/b) everywhere (max deviation
0.0e+0 over a 60-point ring grid) — i.e. every implementation
that honors the real branch computes K_wrap semantics (|cos(Δ/2)|^p); literal pow
computes NaN; only integer p is directly computable (odd p: computable but anti-periodic,
rejected by T1).

**Freeze guard:** restrict the kernel to integer p (K_B class recommended), or declare a
custom branch routine with mandatory unit fixtures: (i) pow(cos(2), 1.5) must be NaN
(fail-closed literal-pow detector); (ii) custom-branch ≡ K_wrap identity check.

## 2 · Domain restriction p > 0

K_wrap_p has a pole at the antipode for p < 0 (witness: K_wrap_−2(π) = 2.667093788113571e+32,
K_wrap_−1(π) = 16331239353195370). All declarations are restricted to p > 0,
including negative even integers; p = 0 is the constant 1 (no bump structure).

## 3 · Smoothness statement, precise form

For p > 0 with p ∉ 2ℤ: K_wrap_p ∈ C^m(S¹) iff m < p. For positive even integers
p ∈ 2ℤ: K_wrap_p is C^∞. (Restates R26-03_R1/T2 without ambiguity; the even-integer
exception is explicit.)

## 4 · Floating-point precision fixture (new; adjudication §2A numerical conditioning)

Algebraic equivalence of the two closed forms does not guarantee floating-point
equivalence. Near the antipode, form A ((1+cos Δ)/2)^(p/2) loses relative precision
through cancellation in 1+cos Δ, while form B cos(wrap(Δ)/2)^p (wrap-first) preserves it.
Deterministic witnesses (p = 1):

| Δ | form A | form B | relative deviation |
|---|---|---|---|
| π−1e-3 | 0.0005000 | 0.0005000 | 0.00% |
| π−1e-5 | 0.000005000 | 0.000005000 | 0.00% |
| π−1e-7 | 4.998e-8 | 5.000e-8 | 0.04% |
| π−1e-9 | 0.000 | 5.000e-10 | 100.00% |

Edge at exactly Δ = π: cos(π/2) = 6.123e-17 ≠ 0.0 in IEEE —
fixtures must assert a tolerance (|K(π)| ≤ 1e−16 · K(0)), never equality with 0.

**Freeze guard:** wrap-first evaluation is mandatory; a precision fixture must compare
both forms on a declared antipode grid (e.g. Δ = π − {1e−3, 1e−5, 1e−7, 1e−9}) with a
declared tolerance, and the Δ = π edge case must be asserted with tolerance, not equality.

## 5 · D1 declaration fields (extended set)

The seven-field list of R26-03_R1 §3 is extended (not contradicted) by:
DOMAIN (p > 0), FLOAT_FORM (wrap-first mandatory), PRECISION_FIXTURE (antipode grid,
declared tolerance), NEGATIVE_FIXTURES (pow NaN detector; p<0 pole rejection),
SOFTWARE_SEMANTICS (IEEE-754, fail-closed). Full freeze field list:
FUNCTION / WRAP_CONVENTION / ENDPOINTS / SMOOTHNESS / DOMAIN_P_GT_0 / NORMALIZATION /
SOFTWARE_SEMANTICS / FLOAT_FORM / PRECISION_FIXTURE / NEGATIVE_FIXTURES / HISTORICAL_MAPPING.

## 6 · Status grammar

```text
R26_03_R2_STATUS          = ISSUED_PRECISION_ANNOTATION_DESIGN_ONLY
R26_03_R1                 = IN_FORCE_UNCHANGED (annotated, not superseded)
IEEE_RATIONAL_BRANCH      = NOT_COMPUTABLE_VIA_POW (NaN); real branch ≡ K_wrap (verified)
DOMAIN                    = P_GT_0 (poles at antipode for p<0)
ANTIPODE_PRECISION        = WRAP_FIRST_MANDATORY (form A cancellation witnessed)
D1_FREEZE_FIELDS          = EXTENDED (11 fields)
CLAIM_CEILING             = C1_DESCRIPTIVE_ONLY
EXPERIMENTS               = NOT_EXECUTED
```

*NEXUS OMEGA — Quelle ist nicht Wahrheit. Prüfung bleibt das Fundament.*
