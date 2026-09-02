# Rollout plans

Each rollout plan lives under:

```text
research/pipeline/rollout/plans/<ROLLOUT_ID>/rollout.json
```

Plans are preparation records only. They bind source evidence, gate state,
token and continuation handling, and the intended rollout phases. They do not
execute the rollout.
