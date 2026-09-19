# External observation intake

One JSON object per independently returned external-agent observation. Files in this directory are measurement inputs, not votes.

Required rules:

- validate against `../observation.schema.json`;
- preserve the original return SHA-256;
- declare provider/model/source/toolchain dependencies;
- never infer user personality, religion, ideology, or motive;
- a new observation changes `RAW_N`, not automatically `Effective_N`;
- KSM/KSE require a separately declared estimator and adequate independence.

The current verified source set contains **zero empirical external-agent observations**. This is intentional and is rendered as `NOT_ESTIMABLE`, not converted into a synthetic score.
