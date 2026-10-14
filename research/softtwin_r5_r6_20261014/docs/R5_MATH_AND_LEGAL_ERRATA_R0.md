# AXIOM R5 — Mathematical and EU-Law Errata, C1

## A. ℓ² witness

The input `d_t=1/(t+1)` **is** square-summable because `Σ |d_t|² = Σ 1/(t+1)² = π²/6`. It cannot demonstrate that `D2={d∈ℓ²}` is properly contained in `D0={d:d_t→0}`. A valid witness is `d_t=1/sqrt(t+1)`: it tends to zero, while `Σ |d_t|²=Σ 1/(t+1)` diverges.

## B. Gain bound for signed λ

For real scalar `e_(t+1)=λe_t+d_t`, `|λ|<1`, the causal impulse kernel is `h_j=λ^j`; the ℓ¹ kernel norm is `Σ |λ|^j=1/(1-|λ|)`.

Young's inequality and `(a+b)²≤2a²+2b²` give the valid conservative estimate:

`||e||_(ℓ²)² ≤ 2 |e0|²/(1-λ²) + 2 ||d||_(ℓ²)²/(1-|λ|)².`

A `2/(1-λ)²` denominator is valid only if `λ∈[0,1)`, or another hypothesis ensures an appropriate bound. Counterexample: `λ=-0.5`, `e0=0`, `d_k=(-1)^k` for `0≤k<1000`. Direct finite-time recurrence yields `Σ_(t=1)^1000 |e_t|² = 3993.333333…`; the invalid RHS is `2×1000/(1.5²)=888.888888…`. Correct RHS is `2×1000/(0.5²)=8000`. Thus the written universal formula FAILS; the numerical checks in a prior external return did not exhaust adversarial inputs. For negative λ, the frequency that maximizes the scalar transfer gain is π rather than zero.

The statement `e_t→0` for stable |λ|<1 when d_t→0 remains valid. No C2 promotion; revise theorem and proof under original scope first.

## C. Law and incorrect case citation

A previous R5 return labels `C-650/17` as the CJEU software decompilation correction case. Relevant judgment: **C-13/20, Top System, 6 Oct 2021, ECLI:EU:C:2021:811**. This addresses necessity-limited error correction for lawful users. Interoperability-based decompilation and error correction arise under distinct provisions; neither licenses indiscriminate RE, use of proprietary fragments or unauthorized deployment.

Official primary source: https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=celex%3A62020CJ0013 .
