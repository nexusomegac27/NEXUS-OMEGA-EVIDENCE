# IST-SOLL GAP MATRIX

| ID | Class | Soll | Ist |
|----|-------|------|-----|
| P0-STOP | PRESENT_DIFF | Lease expiry/revoke/epoch/replay/scope/quorum deny EFFECT | PRESENT_IN_ZIP_ONLY scripts/r45_stop_gate.py (Gate,authorize,effect,stop,quorum,register_key,revoke_ |
| P0-STOP-ASSERT | CONFIRMED_DEFECT | Schema reject without relying on assert/-O | assert 'tolerance' not in req @ r45_stop_gate.py |
| P0-NODEBUS | PARTIAL_OTHER_MODEL | Operator STOP authority aligned | .nexus/node-bus/server/nexus_node_bus.py lease/replay job model |
| P0-BODYTWIN-WHITEN | NOT_PRESENT | Whitening orientation + validity flags | research FolderX R7/R8; no PFV .py |
| P0-JOINT-COV | NOT_PRESENT | Joint coverage runtime | research texts only |
| P0-AR1 | DESIGN_BOUND_MATH_OK | Stationary AR(1) f_n with fixed marginal sigma2 | formula BOUND; MISTRAL constants OK; GLM extra 1/(1-rho^2) rejected |
| P0-FISHER | NOT_PRESENT | Fisher identifiability checks | R44-2 fail documented; no runtime FIM module in PFV |
| P0-MERKLE | PARTIAL | RFC inclusion+consistency+Ed25519 verify | Partial: r45_fault_matrix in ZIP; node-bus merkle_root concat; Ed25519 MISSING in R45 scripts |
| P0-CUSTODY | SOURCE_GAP | Historical script versions + private original hashes | 8/16 historical script identity mismatch reported; originals NOT in R45-2 package |
| P0-B05 | OPEN | Non-cyclic package self-seal | B05 OPEN historical R43 receipt stale; this intake uses external receipt class |
| P1-ELG | DESIGN_ONLY | Epistemic learning graph | DESIGN_ONLY |
| P1-INDEP-EVAL | NOT_ESTABLISHED | Authenticated quorum 3 | 0_OF_3 |
| P2-MAGNONICS | DESIGN_ONLY_NO_IMPL | Continuous error / inverse design | Advisory C1 in package; no productive impl |
| WALLS | HOLD | 0/24 0/3 0/10 BODYTWIN NO | PRESERVED |

## Minimal repair sequence (NOT EXECUTED)
- Step 1 [P0]: Extract r45_stop_gate to isolated test harness; replace assert with explicit raise; add 7 AXIOM negatives + prior 16 — auth=SEPARATE_REPAIR_ORDER
- Step 2 [P0]: Map/align node-bus lease semantics vs STOP-gate or document NON_IDENTITY — auth=SEPARATE_REPAIR_ORDER
- Step 3 [P0]: Bind AR(1) stationary covariance helper with exact f_n; freeze GLM wrong-factor as FAIL fixture — auth=SEPARATE_REPAIR_ORDER
- Step 4 [P0]: Locate or declare ABSENT whitening/joint_coverage/Fisher modules; no silent invention — auth=SEPARATE_REPAIR_ORDER
- Step 5 [P0]: Private original custody plan: path/size/SHA for missing historical scripts; no public leak — auth=OPERATOR_CUSTODY
- Step 6 [P0]: Merkle inclusion+consistency + Ed25519 verify as independent offline suite; do not credit GLM vectors as runtime — auth=SEPARATE_REPAIR_ORDER
- Step 7 [P1]: Epistemic graph + independent evaluator lane — design only until authorized — auth=LATER
- Step 8 [P2]: Magnonics continuous-error — research only; ANALOGY_NOT_IDENTITY — auth=NO_IMPL
