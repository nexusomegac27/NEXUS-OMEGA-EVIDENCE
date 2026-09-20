# Field-Lab Airgap — independent C1 validation note

## Scope

This note validates the mathematics/software correspondence of the R1 Airgap preset. It does not
validate a physical air gap, security boundary, biological phenomenon or metaphysical model.

The inspected preset defines:

```text
P(x,y) = 1 - exp(-8 y^2)
Q(x,y) = 0.15 sin(pi x) y exp(-y^2)
```

The implementation uses central-difference derivatives with `h=1e-3` and a predictor/corrector
(Heun-like) integrator.

## Analytic checks

Along `y=0`:

```text
P(x,0) = 0
Q(x,0) = 0
```

so every point on that line is stationary in this illustrative field.

Independent symbolic differentiation gives:

```text
div F =
0.15 sin(pi x) exp(-y^2) (1 - 2 y^2)
```

and

```text
curl_z F =
y * [0.15*pi*exp(7*y^2)*cos(pi*x) - 16] * exp(-8*y^2)
```

The transverse derivative at the stationary line is:

```text
dQ/dy | y=0 = 0.15 sin(pi x)
```

therefore local transverse behavior alternates with `x`; the whole line must not be described as
uniformly attracting or repelling.

## Software caveat

The inspected integrator increments its internal time before predictor/corrector evaluation and
then evaluates both stages at the same updated time. This is a potential correctness caveat for
time-dependent fields.

The Airgap preset itself does not use `t`, so that caveat does not change this preset's
time-independent field equations.

## Verdict

```text
PRESET_FORMULAS = MATCH
STATIONARY_LINE = REPRODUCED
DIVERGENCE = REPRODUCED
CURL = REPRODUCED
TRANSVERSE_LINEARIZATION = REPRODUCED

STATE =
PASS_WITH_CAVEATS_C1_ILLUSTRATIVE_MATH_AND_CODE

PHYSICAL_MODEL_CLAIM = NO
SECURITY_PROOF = NO
TRINARY_LOGIC_PROOF = NO
```
