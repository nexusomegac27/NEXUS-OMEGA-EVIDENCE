# Research package archive

Packages live permanently at:

```text
research/pipeline/packages/YYYY/MM/<PACKAGE_ID>/
```

The package directory is stable across lifecycle changes. Status is event-sourced; it is not encoded by moving the directory.

A sealed snapshot is immutable and lives at:

```text
snapshots/vN/
```

The package root may contain current derived views (`manifest.json`, `timeline.json`) while active. A sealed snapshot is never overwritten; later corrections create `vN+1`.

The package archive is shared by AXIOM and Cursor/PRAXIS. External-agent artifacts may be referenced from packages, but agent-specific raw research remains in its canonical research lane.
