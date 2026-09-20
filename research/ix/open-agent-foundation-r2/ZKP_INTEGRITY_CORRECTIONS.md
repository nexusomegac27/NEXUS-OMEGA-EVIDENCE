# R2 ZKP / integrity research — scientific scope corrections

Zero-knowledge proof systems may be useful when NEXUS needs to prove a precisely formalized
predicate while hiding selected witness data. They are candidates for privacy-preserving integrity
receipts, not truth engines.

~~~text
ZKP = PROOF_OF_FORMAL_STATEMENT_RELATIVE_TO_CIRCUIT_AND_ASSUMPTIONS
ZKP != SCIENTIFIC_VALIDITY
ZKP != SEMANTIC_CORRECTNESS
ZKP != HUMAN_AUTHORSHIP
~~~

A signature or proof of possession can establish that a cryptographic key was used under the
specified protocol. It does not establish that a named human personally authored, understood or
endorsed the semantic content.

R2 does not adopt a global hidden quality score. Proving that a committed value lies in a range
does not validate the measurement semantics that produced the value.

## Candidate-specific corrections

- EZKL: real ZKML/computational-graph proof candidate; exact release, backend, audit and license state must be pinned.
- Lurk: real recursive/ZK computation research candidate; current pre-1.0/transitional maturity prevents critical-system assumptions.
- Cedar: runtime authorization and formal analysis are separate. The runtime evaluates policy; separate specification/analysis tooling proves properties about the formal policy semantics.
- IPLD: content-addressed data-model building block, not an append-only ledger by itself.
- Ceramic: signed/event-log protocol/runtime candidate with separate consistency/availability assumptions.
- Bulletproofs: range-proof primitive; a range proof does not validate the scientific meaning of the committed number.

## Negative knowledge

R2 rejects the rule that negative knowledge must require mathematical proof. Negative knowledge may
come from physical contradiction, source mismatch, counterexample, failed reproduction, statistical
falsification, schema failure, policy violation or formal proof. The evidence type must be explicit.
