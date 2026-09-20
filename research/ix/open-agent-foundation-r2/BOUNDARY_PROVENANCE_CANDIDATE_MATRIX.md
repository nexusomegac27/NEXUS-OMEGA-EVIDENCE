# R2 boundary / provenance candidate matrix

This matrix records source-checked research candidates. It is not a ranking or component selection.

| Candidate | Public object established | R2 classification | Material caveat |
|---|---:|---|---|
| CUSTODY Framework | yes | agent-control framework candidate | control objectives; not a container/runtime implementation |
| NVIDIA MAIW | yes | authority-boundary reference candidate | warehouse-specific reference architecture; NEXUS suitability untested |
| Cedar | yes | authorization + formal-analysis candidate | runtime authorization and formal analysis stay separate |
| PROV-AGENT | yes | provenance research candidate | NEXUS implementation not established |
| Portable Agent Memory | yes | portable-memory research candidate | exact source/revision/reference implementation must be pinned |
| IPLD | yes | content-addressed data-model candidate | not an append-only ledger by itself |
| Ceramic | yes | signed/event-log protocol candidate | consistency/runtime assumptions require experiment |
| EZKL | yes | ZK computational-proof candidate | release/audit/license state must be pinned |
| Lurk | yes | recursive/ZK research candidate | pre-1.0/transitional |
| Bulletproofs | yes | range-proof primitive candidate | range proof does not validate measurement semantics |
| Helix9 | yes | balanced-ternary VM research artifact | numerical ternary != K3; license metadata conflict must be pinned |
| SBTCVM Gen2-9 | yes | balanced-ternary VM/toolchain artifact | numerical ternary != epistemic unknown |
| CHAI-T | yes | human-AI trust research source | not execution policy by itself |
| Keyhole Effect | yes | preprint/design-hypothesis source | not an established law |
| World Model Science | yes | contemporary research source | universal criticality/power-law claims not established |
| CIRIS | yes | open agent/governance project candidate | independent external evaluation remains a gap |
| Flamewalker Agentic Protocol | no exact source established | SOURCE_GAP | do not implement/cite as validated component |
| HE2-Net exact named system/claims | no exact source established | SOURCE_GAP | do not import stated module/axiom counts |

## Reusable authority-boundary pattern

The current public NVIDIA MAIW source separates model reasoning from operational authority:

~~~text
MODEL / AGENT
→ RECOMMENDED_ACTION
→ GOVERNANCE / DECISION
→ EXPLICIT APPROVAL WHERE REQUIRED
→ ACTION_EXECUTOR
→ WRITE CAPABILITY
~~~

Its source states that write capabilities are structurally blocked from the agent runtime and that
the model does not directly invoke the write path. NEXUS treats this as a useful open reference
pattern, not as evidence that MAIW should become the NEXUS core.

The current CUSTODY source is classified as a vendor-neutral control framework. R2 rejects the phrase
"CUSTODY container framework" unless a separately identified implementation supplies that runtime.

~~~text
CONTROL_OBJECTIVE != ENFORCEMENT_IMPLEMENTATION
~~~
