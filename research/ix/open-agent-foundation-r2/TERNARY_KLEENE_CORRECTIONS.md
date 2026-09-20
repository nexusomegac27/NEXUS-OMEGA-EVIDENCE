# R2 ternary / Kleene / uncertainty-state research — corrections

Two public balanced-ternary projects from the R2 research were independently located.

## Helix9 Virtual Ternary CPU

The public repository describes experimental software using numerical states -1, 0, +1. Its
repository LICENSE file is Apache-2.0. The README currently contains an inconsistent "License: MIT"
header, so any reuse must pin and inspect the exact LICENSE object at the exact revision.

The repository explicitly describes itself as experimental simulation software rather than physical
silicon.

## SBTCVM Gen2-9

SBTCVM is a balanced-ternary VM/toolchain using -1, 0, +1 numerical trits and is published under
GPL-3.0-or-later terms in its repository documentation.

## Scientific boundary

~~~text
NUMERIC_TRIT_0 != KLEENE_UNKNOWN
BALANCED_TERNARY_ARITHMETIC != KLEENE_K3_TRUTH_TABLES
~~~

Calling a numeric state "Unknown" in application prose does not establish K3 semantics. A K3
implementation claim requires explicit truth tables/operator semantics and conformance tests.

NEXUS may use a three-state epistemic representation such as SUPPORTED / CONTRADICTED / UNRESOLVED,
but this is a NEXUS state contract, not automatically Kleene logic.

The mapping to ZPD/scaffolding is retained only as a design heuristic. "Airgap" remains a metaphor
unless a physical/network security boundary is actually implemented and tested.
