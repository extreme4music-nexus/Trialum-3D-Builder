# Trialum S7 F01 production workspace

This is an **actual editable design project**, not the former demo room. On first launch or via the S7 quick-open button, load `projects/trialum-s7-f01-production.json`.

- 6 × 6 original approved F01-A marble tiles, four sides of original F01-D exposed straight edge trims, 4 original F01-E outer corners, 2 F01-B halves, and 4 F01-C quarter UV-phase modules.
- 70 objects, all genuine GLB asset IDs (no mock primitives). Staging geometry only, not an approved placement inside the signed G01 scene.
- Official spatial zoning is defined in Trialum `docs/blueprints/LW_D_AGRO_S7_GREENHOUSE_BLUEPRINT_V3_LAYOUT_20261117.json` on branch `feature/lw-d-s7-f01-e-cream-marble-corner-20261117`. This staging pad is **not** the 82×96m full greenhouse, the G01 water basin, or a calibrated G00L. Do not infer gameplay or approved layout from this staging pad.
- Use `Зачувај` to commit edited projects to Builder. Three.js and GLBs must be present in `vendor/` and `assets/models/`; if missing run `py -3 scripts/setup.py`.
- Every newly authored GLB: same canonical source generators + SHA manifest in the active **Trialum** development branch, copy original generator and output to **Builder main** with matching identity, update catalog, CI check, then owner visual PASS. Do **not** push models to Trialum game main, merge game PRs, or alter Classic gameplay.
