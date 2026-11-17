# ALL KNOWN TRIALUM GLB ASSETS → BUILDER (2026-11-17)
**Status:** all 42 physical glTF2 binaries are Git-tracked in Builder `main`; owner visual QA pending.
**Game source:** `extreme4music-nexus/Trialum` commit `b801808a5b219284d52c52a8ae8e643700c84478` on the isolated LW-D scene stack; game source / gameplay unchanged by this Builder import.

## Verified model inventory
- **F01 original real marble**: 16 GLB (1 whole, 2 halves, 4 quarters, 4 edge strips, 4 corners, 1 F01-F radial wedge); F01-A owner original visual PASS, other parts pending.
- **Agro Atrium S1**: 1 GLB (`atrium.glb`).
- **Food Warehouse S4**: 7 original GLB (`warehouse-shell.glb`, `smart-storage-rack.glb`, `cold-locker.glb`, `cargo-crates.glb`, `conveyor-sorter.glb`, `holo-inventory-kiosk.glb`, `mini-transporter.glb`).
- **Two original S5 physical annex room layouts converted to new real GLB prefabs**: 2 (`food-cold-annex-shell.glb`, `food-packing-annex-shell.glb`), derived from dimensions and part positions in `warehouse-rooms.mjs`. These are **new GLB conversions**, not misrepresented as prior shipped binaries.
- **S7 Greenhouse original empty shell**: 3 (`greenhouse-shell.glb`, independently inspectable `greenhouse-floor-shell.glb`, `greenhouse-glass-roof-shell.glb`). The latter two are alternatives to parts of the full shell, not extra stacked construction.
- **G01 original candidate water-core**: 6 (main basin, satellites, railings and walkway, bridge, pumps, animated water with original morph-target clip).
- **Aquaglow original stage variants**: 6 (sprout, young, growing, mature, weakened, dead). These are a **library of variations**, not created aquarium plants; original engine only authorizes up to four real live aquatic specimens.
- **B1 original graybox pilot**: 1 (`pilot-room.glb`), historical technical test only, not a finished room.

**Math:** 15 + 1 + 7 + 2 + 3 + 6 + 6 + 1 = **42**. 40 are original real glTF2 sources authored in game (including the new F01-F owner-render-approved wedge); the two S5 annex GLBs are newly extracted from original runtime geometry.

## Source and binary provenance
- Canonical GLB generators mirrored under `tools/b1/` together with exact `scene.json` and `visual-recipe.json` snapshots in `prototypes/lw-d/scenes/`. Only *data* and generators are mirrored; no playable game code, server state or Android assets.
- `scripts/build_all_assets.py` regenerates 26 additional binary models, validates GLB2 headers and mesh structures, verifies byte-exact copies, and creates `assets/TRIALUM_LEGACY_GLB_MANIFEST.json` with SHA256 and sizes.
- `scripts/setup.py` independently regenerates frozen 15 F01 models and pinned Browser Three.js (0.180.0).
- The original two Node generators use pinned build-only Three.js 0.187.0 from `tools/b1/package.json`, matching game source rather than silently altering the geometry generator.
- GitHub Actions `.github/workflows/bootstrap.yml` validates **all 42** and commits binaries to `assets/models/` on Builder `main`. GitHub Desktop Fetch → Pull gets the real files, not temporary Actions artifact ZIPs.
- A separate test ensures the previous inline importmap CSP resolution fix still works with the larger library.

## Ready-to-open editable projects
| UI label | Project JSON | Actual GLBs |
|---|---|---|
| Агро лоби | `projects/trialum-agro-atrium.json` | 1 original atrium scene with source semantic doors |
| Главно стовариште | `projects/trialum-food-warehouse.json` | warehouse shell, real equipment, 2 attached structural annex prefabs |
| Разладна комора | `projects/trialum-cold-storage.json` | original-layout cold annex structural GLB and two real lockers |
| Пакување | `projects/trialum-packing-room.json` | original-layout packing annex GLB, racks and conveyor |
| Стаклена градина | `projects/trialum-agro-greenhouse.json` | original greenhouse shell; G01 candidate parts present but hidden pending physical floor cutouts |
| G01 водно јадро | `projects/trialum-g01-water-core.json` | six real G01 water candidate GLBs; preview only |
| S7 F01 | `projects/trialum-s7-f01-production.json` | preserved 70-part editable original marble tile staging project |

All are Builder data-only layouts. No game stock, per-pet reserves, money, history, account state or authoritative save writes. They do not fabricate greenhouse plants or unlock canonical growth slots.

## Owner QA / next handoff
1. On Windows **exit old localhost terminal**, GitHub Desktop Builder main **Fetch/Pull**, double-click `START-BUILDER-WINDOWS.bat`, Edge `http://127.0.0.1:8765/` → hard refresh.
2. Use **Избери 3D просторија…** to view all six rooms, and **S7 F01** for marble staging. Use the left-category filter to find all 41 real GLBs.
3. Inspect original scene geometry, interior clipping, annex door geometry, camera orbit, GLB animation, selection and inspector. **No CI pass substitutes this owner visual PASS.**
4. Save edits into cloned Builder `projects/` and use GitHub ↑ (commit/push) or GitHub Desktop. Never merge edited design into Trialum main without separate engine integration and owner consent.
5. Ongoing GLB production rule: source generators + matching exact output in both active game development branch and Builder main; filename, hash, pivot, size, visual review status in manifest. Continue one asset family at a time.

**Known limits:** catalogue dimensions for non-F01 modules are UI approximations, not authoritative physical collider bounds. Existing game GLBs use world-space geometry and some roofs obscure interiors; user may hide the structural shell during redesign. Existing standalone G01 core components are *review candidates* with a separate cutout/geometry owner gate; do not label full in-game greenhouse water integration finished based on this project.

## F01-F OWNER RENDER PASS → REAL GLB BUILT

The F01-F 1m radial dry perimeter wedge is a real 89,948-byte model with 32 curved subdivisions/392 triangles and original F01-A embedded PBR image. Its exact SHA256 is `0b76aaf4870dbb06ded35a961330f7337a172c68fdd0b0092d2e7db78443196c`; matching Git blob SHA `2735c84d70220bcf69b391debf3d01f57d85f07f` across both repositories. Open `projects/trialum-f01-f-radial-wedge-review.json` from the new room preset, compare with original A. Game CI and Builder CI are green; owner's physical model PASS still required. Neither source CI nor the earlier concept render certifies a pixel-perfect match under all lighting conditions.
