# Bodytwin Live-C1 P0 Spatial Repair (AXIOM, 2026-11-08)

The published live panel inserts itself as the **first child of the existing `<main>`** in its original JS source. This is a layout-collision risk when the 4D viewer uses a grid/flex container. This proposed **additive** hotfix moves the same panel after `<main>` and applies only panel-scoped CSS. It does not change the 4D geometry, source reducer, Cron, status polling, or evidence.

`site/layout-hotfix-r0.js` and `.css` are the only public assets. `tests/layout-contract.test.mjs` provides 15 deterministic tests, with standalone fake DOM; Chromium CDP was attempted but the current container blocked local and file navigations. The live browser gap is explicit. Full staged release and rollback contract in `ops/CURSOR_SCOPED_PUBLIC_LAYOUT_REPAIR_20261108_R0.md`.

**Never claim this source-only candidate proves the overlap is repaired live.** Hostinger deploy & CDP proof are separate. `C1_DESCRIPTIVE_ONLY`, `BODYTWIN_VALIDATED=NO`.
