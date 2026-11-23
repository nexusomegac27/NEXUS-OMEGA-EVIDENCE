# R43-6 · Independent evaluator and holdout custody protocol (protect the evaluator BEFORE the arms)

Evaluator role is E34-independent operator-certified custodian. This protocol is a **proposal** for a segregated read-only evaluation lane; no E34 custodian account has been authorized by creating the GitHub issue or PR.

## Freeze & access control
1. Create a private evaluator store with write access restricted to registered evaluator (NOT any researcher / agent) and separately audited read/execute; a public research PR may include only commitments and test schema, not answers, identity keys or private source data.
2. BEFORE any arm is allowed to run, evaluator records signed/immutable SHA256 of exact evaluator code, compiled runner/tool versions, taskbank, test labels and split membership; record SHA256 of original source snapshots. This is source provenance not truth.
3. Use separate sealed DEV (researcher can receive feedback) and TEST (not accessible to researcher). A TEST result may be published as aggregate; after release, retire the old test suite, no further claims on re-used test. Any suspected leakage invalidates that trial.
4. Any evaluator code change after precommit creates new evaluator version. If a new version is used, all arms (including v0) must be independently replayed under that exact new precommitted version on a fresh untouched test set. Never silently reuse metrics across old/new evaluation definitions.
5. Run independent synthetic wrong-evaluator fixtures: one byte evaluator mutation, 94fad101→9fa701a5 mismatch, fabricated actor ACK, mutated label, leaked key, post-hoc threshold and reused holdout must hard-fail. One clean separately signed and pre-frozen evaluator/labels must pass.
6. Registered actor identity: signed ACK from authentically registered reviewer, independently check trust source/key/role, not model-name persona or self-declared label. Researcher may submit via operator while direct GitHub writes remain DENY.
7. Match all arms on observed wall/CPU/tokens/network/GET bytes, with tool subprocess descendants counted. Randomization/order and task difficulty blinded/counterbalanced. Include condition intentionally wasting budget to verify normalization.
8. Primary outcomes: independent unique source-grounded facts and falsification success, error correction and honest abstention. Secondary: source novelty proven by content+version, false promotion and legal/privacy. For intervals use weighted interval score or interval score plus calibrated coverage+width, not coverage alone.
9. Safety: evaluator may not itself enable device capture, merge, Hostinger/www writes or export private data. Protected hidden labels remain outside public GitHub. No background autonomous execution by merely publishing this plan.

## Audit classes / fail-closed outputs
- `SOURCE_RECEIVED_HASH_MATCH` — bytes stable only.
- `LOCAL_EVAL_REPRODUCED_POSTHOC_SCORER` — current R43-5 level.
- `FROZEN_EVAL_FAIL_HASH_MISMATCH` — current R43-5 level.
- `HOLDOUT_EXTERNAL_SEPARATION_NOT_ESTABLISHED` — current R43-5 level.
- `COST_MATCH_FAIL_WALL_CLOCK` — current R43-5 level.
- `RESEARCH_ADAPTIVE_GAIN_INDEPENDENTLY_ESTABLISHED_C1` — reserved, cannot be granted until all independent gates pass and heldout delta is nonnegative with appropriate uncertainty while no false PASS/safety regression.
- `INCONCLUSIVE_UNDERPOWERED` or `NEGATIVE_ADAPTATION` — correct endpoints when evidence doesn't support improvement.
- `SELF_OPTIMIZATION_PROVEN` not used as global / persistent-agent claim; only scoped methods under exact tested conditions.

Official source DSSE LEN(type) byte standard https://github.com/dsse-lf/dsse/blob/master/protocol.md; open evaluation concerns https://sage.cs.princeton.edu/trends/ and https://pmc.ncbi.nlm.nih.gov/articles/PMC13663820/.
