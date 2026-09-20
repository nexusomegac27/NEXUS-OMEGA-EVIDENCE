# IX R2 → R3 open gaps and falsification program

R2 establishes a public research foundation only. R3 should implement small controlled probes
rather than assemble a full agent stack.

## 1. Authority-boundary microbenchmark

Compare at least two open implementations/designs against one identical typed action proposal.
Test stale authorization, proposal-ID mismatch, disallowed actions, expired/revoked human
authorization and a direct model attempt to call a write capability.

Measure unauthorized writes, false allow/deny, provenance completeness, policy replayability and
state recovery. No real external target must be attacked.

## 2. ZKP utility falsification

Do not begin by proving "agent quality." Choose one narrow predicate with exact versioned inputs and
function. Compare an ordinary signed/hash receipt with a ZKP receipt.

Measure proof bytes, proving time, verification time, build reproducibility, setup assumptions,
circuit-version binding, failure modes, privacy delta and operational complexity. R3 may conclude
that ZKP adds no useful value for the selected NEXUS use case.

## 3. Three-valued state semantics

Implement a tiny explicit NEXUS state machine and, separately, Kleene K3 truth tables. Test whether
K3 supplies useful semantics beyond existing NEXUS states.

~~~text
NEXUS_STATE_MODEL != K3_BY_DEFAULT
~~~

Balanced-ternary VMs may be tested as computational substrates only after numerical semantics are
kept separate from the epistemic state model.

## 4. Provenance portability

Create one minimal task with source bytes, method, output, validation receipt and correction. Encode
it using the current NEXUS content-addressed/Fundus representation and one PROV-compatible candidate
representation. Destroy derived indexes and reconstruct both from canonical objects.

## 5. Boundary precedent extraction

Extract the reusable pattern rather than vendor-specific code:

~~~text
MODEL_REASONING
→ TYPED_PROPOSAL
→ DETERMINISTIC_POLICY
→ HUMAN_AUTH_WHEN_REQUIRED
→ BOUNDED_EXECUTOR
→ OBSERVED_OUTCOME
~~~

Test whether the boundary survives model/runtime/framework substitution.

## Mandatory negatives

~~~text
ZKP_CALLED_TRUTH
KEY_CALLED_PERSON
RANGE_PROOF_CALLED_QUALITY
TERNARY_ZERO_CALLED_KLEENE_UNKNOWN
MODEL_CONSENSUS_CALLED_INDEPENDENCE
CONTROL_DOC_CALLED_ENFORCEMENT
SOURCE_GAP_COMPONENT_IMPLEMENTED
GLOBAL_SCORE_REINTRODUCED
PUBLICATION_CALLED_ACTIVATION
~~~
