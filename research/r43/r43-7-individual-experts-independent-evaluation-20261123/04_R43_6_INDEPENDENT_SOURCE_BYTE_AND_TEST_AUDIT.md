# R43-6 AXIOM independent byte/script/crypto audit · R43-7 source-class ledger

### Raw original uploaded artifacts
- `R43_6_~2.ZIP` 83648B sha256 adf3d6cd571615ef7c59013780eb6b73ea7364da5d16256f4d9190581a634896; inner `r43_6_evaluator_return_zai_20261123_SEALED.zip` 87138B sha af6a41ac283cc95e3b04fa5c5ae2eb1694f5e4c3b31aef89cc1b0845386116d8, manifest 83/83 PASS CRC PASS.
- `R43_6_~1.ZIP` 59942B sha bbbca9bc497f6e68cb1dfeb1c71378c33169494699df37bfa2f88301528c6743, inner 49064B sha d8222dd97f3e43e79181fa0e48271558508a232b84b959ae67c064443b13b67e, manifest 12/12 PASS, CRC PASS. Expert actor self-declared/unregistered, not custodian.
- `subagent_02.zip` 1361161B sha 939f12b8ab9cdd7365bff6ec602b2c42a8e781a98357ecca5a95cbca799eccff outer manifest 14/14. Two separate 6/6 source mirrors; these are duplicates. Contains preview PDF not examined (no science claims borrowed from preview).
- Independent GitHub source audits `NEXUS-~1(20261123-141657).MD` 17844B SHA 3c343447964c27120bbc2a398c42c2635114fc7a35650d2290ff7e605889ec50; `Mistral_Return.txt` 25215B SHA e3ab3cd7e8b9aa4d2af1740a6170efb10eaf3e0f578a5e379f34d95a2abaa046; `NEXUS_~1(20261123-141702).MD` 8910B SHA 3500f3ef90053e35d93ac6f06b5a5693c2e1fd6dcac01968b10b6e83fef6730e, advisory old R43-6 foundation readback not independent new adaptive evaluation.

### Actual independent original code execution
Evaluator raw bytes `code/r43_6_evaluator.py` = `freeze/evaluator_frozen.py`, SHA256 `375ecedf7d1bae9184d713c641e30c8996c89bada9a7ca066e5312a6c1062fc4`. AXIOM extracted safe ZIP paths to throwaway temp and ran Python `-I -S` with `R43_6_BASE` redirected. Exit0, EXACT 4-arm components/ledger/integrity fixture equality with producer receipt, distinct only in post-final timeline since original receipt predates final_evaluation event. Credible narrowed local replay, not external custodian.
Synthetic E32 20/20 eval sessions, v0/v1 coverage .700/halfwidth 7.1022/WIS 4.5434; v2 1.0/2.7914/1.3289; broad interval control 1.0/1000/97.356. 20/20 exact two-sided 95% binomial interval (0.83157,1.0); no physical reference.
Cryptography: AXIOM used original pinned Ed25519 public keys from ZIP and independently verified exact original signed envelope bytes for UTF8 charlength 43 vs bytes 44, correct normative u1 negative/u2 positive, and ASCII/BE32/LE32 correct diagonal. All tests local with public TEST roots not registered FC2 actor.
Race: AXIOM imported exact frozen original race module and independently executed 3×32-thread barrier: broken 32 accepts, locked 1 accept every run. This validates the intentionally vulnerable synthetic engine, not production replay protection.
Budget: original `arms/*/resource_ledger.json`: v0 wall33.45 CPU (postnormalizer)0.032, network0; v1 wall135.72 postnormalizer CPU0.053 network372394; v2 wall135.38 postnormalizer CPU0.052 network372389; b_wide wall38.32 postnormalizer CPU0.021 network0. Equal reported 1.2 s normalizer is a *subtask*, not a matched total resource budget. Tokens not instrumented. Actual G3 full parity unverified/failed observed.

### Original discovered security counterexamples — hard scientific positives
Examined function `check_integrity` in exact `code/r43_6_evaluator.py`: tests `bundle.get("actor_ack") and not bundle["actor_ack"].get("signature")`; arbitrary nonempty bytes bypass check without Ed25519 verifier and registered trust anchor. AXIOM original function called with impostor actor and `signature='garbage-nonempty'` returns (True,'CLEAN'); this is HARD_NEGATIVE that R43-6 eight fixture tests did not cover.
Second original test only checks `set(eval_ids)==set(feedback_ids)`. AXIOM called same function with partially intersecting ID sets, result (True,'CLEAN'). Partial leakage fails closed requirement; full set equality fixture passes but is insufficient.
Thus `EVALUATOR_SELFTEST=8/8` is only a scoped test-count fact, not independent authentication/holdout security.
The source itself includes literal test `actor_ack.signature='sig-abc'`; this is not a legitimate cryptographic signer.
No change to original scripts/receipts is made; R43-7 must demand red-before/green-after in independent new source branch under operator oversight and no production Cursor dispatch.

### Data-class and claim boundary
The reference/source discovery strings may relate to previously known OpenSim/OpenCap and PAMAP2. Novelty against NEXUS original registry NOT independently established. W1 200 status/HTML/browser original authenticated source gap remains; public privacy V3 HOLD; original Kotlin/Gradle/FC2/C5/X15 absent; 10 substantive passes 0/10; registered independent actor groups 0/3. No external write, human-device or clinical claim.
