# S7 MASTER GARDEN — Reconstruction progress and owner visual review

Date: 2026-11-19. Branch: `feature/s7-master-garden-visual-rebuild-20261119` (Builder repo ONLY).

## Scope and authoritative safety
- This is a **visual, owner-review-only** Builder feature branch. Do NOT merge to Builder main or Trialum game, publish Android or overwrite V1–V4 without explicit owner PASS.
- Current master scene: `projects/trialum-s7-master-garden-review.json` — 372 editable scene objects.
- Current preview physical GLB library: **362** genuine GLBs; only 2 new real .glb meshes in this branch: `s7-master-g01-edge-finish.glb` (192-segment circular edge) and `s7-master-g00l-glass-service-wing.glb` (transparent open annex); original plant assets from previous S7 complete flora commit are unchanged.
- Existing `projects/trialum-s7-complete-garden-v1.json` through `v4.json` unchanged.
- Original `greenhouse-shell.glb`, `g01-water-surfaces-animated.glb` and canonical original engine unchanged.

## Points completed technically
1. **G01 open water:** remove the solid rectangular helper plane ONLY for S7 garden projects, because the reference plane at -0.018m occluded the physical water surface at -0.235m. Preserve the real 4 water nodes, 2 morph targets each, and `G01_WATER_RIPPLES_LOOP_6S` animation clip; tune water transparent material and depthWrite. Six second loop auto-plays via AnimationMixer/Tick (confirmed source); owner motion appearance still pending.
2. **Object height/pivots:** per-asset GLB bounds support grounding for props, but keep original underfloor water and true architecture untouched. For S02/S03 tile GLBs, center local lower-left-origin geometric bounds before rotating/scaling; otherwise five planted crops appear beside a bed.
3. **G00L:** assign workstation real desk height ~0.918m with keyboard, monitor and repair tool above surface; R01 beside charging dock, two RS and four RM racks. Physical 45-tile 2×2m service floor, 8 2m connecting tiles from service to original entrance; now protected by a physically modeled open glass roof/service wing without replacing original dome or creating fifth finger.
4. **Four beds:** expand 4 primary S02 soil plots to visually readable dimensions; five canonical preview plant places each, only 4×5 original real-game slot limit. Four distinct arched fingers retain angle/end geometry from original source.
5. **Living borders:** 44 physical decorative soil/plant clusters, pulled toward central walkway inside each finger, no added gameplay plants/ownership/stock. Existing flora GLBs with `idle-sway` clips are auto-playing in editor.
6. **Finish:** one real authored 192-segment G01 circular edge GLB around holed central pad; do not seal water. Exposure balanced for S7 separately from other rooms; cinematic camera checkpoints for G01, G00L and 4 beds.
7. **Visual testing:** `.github/workflows/s7-master-visual-preview.yml` launches actual localhost Builder in headless Chromium SwiftShader and uploads 6 PNG screenshots. `.github/workflows/s7-master-review.yml` tests source/JSON/GLB assets, true aqua morph clip, all 20 bed slots and supplemental 44 flora, and canonical inventory limits.

## Owner QA (NOT YET PASSED)
- Do not equate green CI with artistic approval; screenshots show recognizable architecture and water, but lighting, flora geometry, canopy shape, physically realistic appearance, animations over time and Android performance still require owner visual PASS.
- Developer review screenshots: GitHub Actions `S7 MASTER headless WebGL visual smoke` attached artifact `S7-MASTER-REVIEW-WEBGL-SCREENSHOT`. Inspect water/g00l/bed1...bed4.
- Check props: original model GLB bounds include irregular local origins; compare monitor's TRUE bottom on desktop with desk at 0.918m, desk tools, robotic devices and clipping.
- Check that G00L translucent annex matches intended owner's design; this is a **proposed visual treatment** to fix the previously uncovered left service corner, not a previously owner-approved wall/roof.
- Check that soil and five real-bed preview plant positions are inside physical bed bounds, not on an adjacent white panel.
- Check all six screenshots AND inspect a running water/plant animation in Edge on user's PC. The supplied WebGL PNGs alone cannot prove fluid motion, collisions or real Android FPS.

## How to view without damaging current work
1. In GitHub Desktop switch repository `Trialum-3D-Builder` to this feature branch. Keep personal local edits / JSON backups first; do not force reset.
2. Stop the older server if it still holds port 8765, then restart `START-BUILDER-WINDOWS.bat`.
3. Open `http://127.0.0.1:8765/?preset=garden-master` (not just root, because Builder restores local autosave by default). Optional close-up: add `&view=water`, `&view=g00l`, `&view=bed1`, `&view=bed2`, `&view=bed3`, `&view=bed4`.
4. Try orbiting from INSIDE the G00L annex to see workstation, rack and charging dock. Inspect from above for gaps, foliage in walls, clipped terraced pieces and real G01 1+3 water holes.
5. Save revised JSON or export handoff only after checking. The game main branch and old room designs are not changed by opening this branch.

## Next decisions / order
- GATE: human approval of current **ONE MASTER** visual scene. If owner identifies misplacements, fix that one stage first.
- After visual PASS, derive four complete V1–V4 floor-material permutations from the **approved master** and verify only floor textures/layout differ, not scene functionality. Do not multiply the original broken 873-object layouts.
- Only then perform original Trialum engine integration on isolated game branch, per separate roadmap S7.8-H and S7.8-I. Do NOT claim runtime irrigation, living flora engine behavior, robot AI jobs, inventory or Android production deployment now.
