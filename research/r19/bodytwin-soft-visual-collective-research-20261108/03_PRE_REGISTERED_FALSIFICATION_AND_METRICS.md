# R19 · Forschungspräregistrierung der Widerlegung (noch kein Experiment)
**Nulllage:** R18 ist ein lokal geprüfter statischer Atlas, nicht ein browser- oder sensor-validierter Live-Bodytwin. Ohne unabhängige Laufzeit-, Rechte- und Observability-Belege bleiben Zusatzclaims verboten.
## Negativfixtures – mindestens folgende 20
N01 PNG serving with conversion WebP/AVIF vs actual PNG local SHA; N02 HTTP auto-gzip; N03 stale CDN cached index; N04 missing Content-Type; N05 Vary/Accept absent; N06 missing data layer; N07 manifest says one SHA but JS bytes differ; N08 CSP blocks iframe; N09 source tree parent modified; N10 shared-writer concurrent writes; N11 WebGL context lost mid-frame; N12 shader compile fail on mobile GPU; N13 viewport 320px horizontal scroll; N14 mobile context-loss fallback; N15 orgmale+orgfemale simultaneously; N16 false fully female body label; N17 attribution hidden behind slider; N18 single-IMU illegally animates multi-segment skeleton; N19 qL=qIMU/qR=1 falsely called pure 3D SO(4) rotation; N20 NaN/Infinity joint or quaternion; N21 out-of-range joint; N22 stale or missing timestamp; N23 30/291 meshopt subset falsely promoted to global; N24 unlicensed Lane B asset included.
## Positive controls – mindestens folgende 10
P01 identical local SHA for skeleton; P02 expected female organs exclusive; P03 canonical correct CC BY attribution visible; P04 no-GPU fallback; P05 keyboard-only navigation; P06 preexisting SO(4) inputs unchanged; P07 individual asset source ledger; P08 unchanged parent page absent authorized add-only step; P09 WebGL2 fallback behavior when supported; P10 byte→semantic distinction preserved in UI.
## Messplan
- Three truth layers: **physical source byte SHA** / **HTTP delivered-response SHA and headers** / **decoded pixel semantic parity**; falsifizieren, wenn die Ebenen vermischt werden.
- Browser: Android OPPO, Pixel, desktop Chromium/Firefox; specify versions, GPU, viewport, cold/warm caches, thermal state, scene layer and mode.
- Record median/p95 frame time, memory/VRAM proxy, total transfer, scene load, contextloss frequency, GPU error, accessibility failures; **no invented measured values**.
- Visual review: independent source model provenance + manually inspected reference camera angles. Hausdorff-like errors are approximations unless exact algorithm/definition given.
- Null model for sensor mapping: constant T-pose with no inferential degrees of freedom. Compare proposed animation to this baseline; do not confuse attractiveness with physical correctness.
- Separate screening and holdout. Preregister seeds/hypotheses before any confirmatory run. Loss/corruption should fail closed.
`EXPERIMENTS_EXECUTED=NO`; all outcomes remain `PENDING`.
