# AXIOM Alpha-Node C1 Loop · minimal runnable research reference

**This is an isolated C1 research candidate**, not a deployed AXIOM process and not a modification of GPT-6. It is intended to be read together with the Operator's already published direct C1 research publication rule.

- `ALPHA_NODE_C1_CONTINUOUS_SELF_MODIFICATION_R0.md`: architecture, stable standing instruction, event and evidence contract.
- `alpha_c1_evidence_reducer.py`: standard-library source-hash and candidate-disposition reducer. It never modifies GitHub or a production node.
- `test_alpha_c1_evidence_reducer.py`: twelve local deterministic cases (positive, one-defect negatives, duplicate, code-candidate isolation).
- `example_material.json` + `example_material.txt`: one physically hash-checkable example.
- `DETACHED_MANIFEST.json`: sha256+bytes for every sibling except itself; never include its own hash as a child.

## Run

```bash
python test_alpha_c1_evidence_reducer.py -v
python alpha_c1_evidence_reducer.py example_material.json example_material.txt
```

The verdict `KNOWLEDGE_APPEND` is not semantic science acceptance, source licensing proof, or direct push evidence. Its `research_push_eligible` flag is conditional on **independently established** publication rights and privacy classification; the prototype only checks that the caller supplied true booleans. A separate human/authorized contextual review is required when rights are ambiguous. `PATCH_CANDIDATE` is research only, not executable production integration.

Direct research publication remains subject to the existing GitHub branch rules/checks and main readback. The standing automation can reuse this contract but may not claim Python execution when its environment lacks it.
