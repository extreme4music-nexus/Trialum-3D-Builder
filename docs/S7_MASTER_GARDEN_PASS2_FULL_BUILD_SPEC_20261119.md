# TRIALUM · S7 MASTER GARDEN — FULL BUILD SPEC / PASS 2

**Date:** 19 November 2026  
**Owner:** Trialum  
**Builder repo:** `extreme4music-nexus/Trialum-3D-Builder`  
**Scene:** `projects/trialum-s7-master-garden-pass2.json`  
**Status:** IMPLEMENTED IN BUILDER PREVIEW; **OWNER VISUAL PASS PENDING**  
**Scope:** Incrementally improve the completed MASTER scene (372 original objects preserved), NOT rebuild from scratch. Do NOT touch Trialum game, classic beta or production deployment.

## 1 · Owner-approved work request (19 Nov)

- The existing greenhouse, 1+3 physical water basins, water animation, four real growing fingers, G00L shelving, G01 water core and current material/lighting foundation are retained.
- Small floor gaps must be filled with genuine modular stone/marble GLBs.
- G00L workstation must sit **at the BACK of the new glass service room** alongside RS/RM racks, not near the water or blocking the corridor.
- The new glass service wing needs **ONE proper door**, with actual visible transparent leaf, frame, handle, correct gap and open/close animation.
- Deliver ONE polished PASS 2 variation first: **F02 black marble surrounding water**, **F01 white marble for remaining promenades**, **F03-S and F03-T stone in the nursery areas**, with some circular stone motifs.
- Land seedlings visually must be densely spaced and **in straight upright rows**, no arbitrary diagonal/tilted staging.
- Add actual modelled pumps, tanks, filters, valves, flexible hoses; owner explicitly **does not want drip-by-drip irrigation across beds**.
- Owner edits in 3D Builder, saves a JSON and sends it back; only **after approval** start negotiations on a much broader Trialum engine simulation rebuild.
- Derive **three more floor-only designs** from the final, owner-approved PASS 2 MASTER, not in this pass.

## 2 · Current Builder deliverables and provenance

| Item | Physical, editable delivery |
|---|---|
| Glass room | Original G00L open annex retained; one **NEW real GLB** `s7-pass2-g00l-glass-partition-door.glb` |
| Door | True glTF 2.0, two meshes, chrome frame and transparent leaf, 2.30m opening, hinged Y-axis, `door-open-hold-close-10s` animation |
| Desk | Original W01 desk and W02 chair moved to room rear (z=22.3 and z=20.92), with W03 monitor at Y=0.93, W05 keyboard/W06 mouse at Y=0.94; workstation tower and repair tool repositioned |
| G01 water | All four original physical basins and original morph water clip untouched, helper floor stays off for S7 greenhouse |
| Water floor | 67 individual F02 black marble panels + 61 individual F01 white panels; **geometric clearance checks** ensure each avoids all four physical water openings |
| Decorative circles | 19 central F03 wedge accents beside G01 water; 32 **clean, rectilinear F03-S/T frame panels** around the four beds (no loose radial pieces near nursery soil) |
| Nursery | 20 canonical main land specimens remain exactly five per bed, spaced at 0.59m in straight rows; 88 **additional decorative seedling PREVIEWS** within 44 existing soil islands |
| Natural stone | 32 F03-S/T stone bed-frame modules in continuous, organized borders; loose scattered stone squares were **removed**; portions of nursery promenades retiled with F03 natural stone |
| Water hardware | Existing per-bed equipment rearranged; original 4 driplines **replaced** with non-drip flexible hoses; real I01 tank, I02 pumps/filters, I03 hoses, I04 valves, I06 sensors and visible G00L shared water station |
| Gap closures | 8 path-connector modules and 4 door-threshold modular tiles, each independently editable |
| Archive | Original `trialum-s7-master-garden-review.json` and historical V1–V4 scenes remain intact |

The PASS 2 catalog contains **363 genuine GLBs** (previous 362 + one original animated glass door GLB). Scene contains **703 editable objects**. Existing stock models have not been overwritten. All parts can be repositioned/rotated/scaled in the Builder inspector and exported to JSON.

### Real material and physical layout zones

- **G-00L service room**: x approximately -19 to -3; z 5 to 25, side extension LEFT of real entrance, not a fifth production finger. New partition is x=-3.12 / z15.5–24.5, single clear door z19.0–21.3. Rear workstation approximately x=-10.15 / z22.3.
- **G-01 water core**: one 6.96m-radius primary basin at (0,0) and three satellite basins, approximately (-10,0) r2.32, (10,1) r2.32 and (0,-11) r2.22. Tiles use a conservative diagonal-clearance margin: NOT placed over any aperture.
- **G-02**: first growing finger, bearing -73°, one 5-slot bed; **G-03** -38°; **G-04** -2°; **G-05** +37°. Each retains its existing physical greenhouse architecture and five canonical plant display slots.
- **Plant spacing**: five main visual plants per real bed, all on one equal-radius line, lateral increments exactly 0.59m. All plant models upright with `rotationY=0`. Extra 88 seedling visuals and earlier 44 decorative foliage elements do **not** create any plant IDs, harvests, capacity or ownership.

## 3 · Animation and technical behavior boundaries

The Builder is a visual layout tool; **a glTF animation is not a running game simulation**. Current preview assets support:
- Original G01 water `G01_WATER_RIPPLES_LOOP_6S` with four live morph meshes.
- Original original flora `idle-sway` and available plant clips with AnimationMixer.
- G00L glass door `door-open-hold-close-10s`, a 10-second hinge animation; it does **not yet** signal character collision, navigation or state.
- Pumps, valves, filters, hoses, plant rows, storage racks and robots are rendered 3D geometry. This pass does NOT consume water or resources, generate actual plant growth or move robots autonomously.

Current constraints remain unchanged: **4 land beds × 5 original gameplay slots + 4 aquatic slots**. There are no additional real seedlings created, no stock transfers, no drip irrigation, no false automation, no Android live build.

## 4 · Owner review procedure / definitive acceptance

1. GitHub Desktop → Builder `main` → Fetch / Pull. Close the old localhost process. Re-run `START-BUILDER-WINDOWS.bat` and `Ctrl+F5`.
2. Open **Избери 3D просторија → 🌿 MASTER PASS 2**, or `http://127.0.0.1:8765/?preset=garden-master`. User's previous MASTER PASS1 or personal scene can be recovered using the archive and existing backup control.
3. Inspect water at G01 and orbit around the central basin; check black marble panels never cover the 1+3 open water holes.
4. Enter the G00L door (currently a **visual opening in Builder**, not runtime collision behavior), inspect desk/monitor/keyboard and rack/robot clearances from inside.
5. Inspect G02, G03, G04, G05 **at eye level**: five plants in one straight line on each real bed, dense miniature seedlings and stone edges, physically legible paths, pumps and hoses outside plant slots.
6. Test the **door animation** and at least one plant `idle-sway` and water ripples while orbiting.
7. Move any object as desired, save / export normal **JSON**; send the edited `trialum-s7-master-garden-pass2.json` or Builder-exported JSON in ChatGPT. The JSON is the physical positioning source of truth for next engine planning.
8. **Owner PASS** is a specific positive statement *after reviewing the desktop or filmed actual WebGL view*, not a GitHub Action result. Record rejections/changes; revise PASS 2 until accepted.

### Automated QA checks (necessary but NOT sufficient)

- Assert all 372 original MASTER instance IDs still exist; all 363 GLBs are genuine; 4 G01 openings preserved and open; 4×5 canonical land display slots + 4 aquatic.
- The glTF door has correct 2.30m gap, 10s animated hinged rotation, real glass material, exactly one scene occurrence.
- No `s7-i05-*` drip emitters/dripline assets exist in PASS 2; pumps, hoses, filters and valves are present.
- G01 overlay tile corners never intersect a water aperture; F02 black around water and F01 white remainder; stone in nursery and circular motifs.
- Test Builder JSON serialize→deserialize round-trip and safe `meta.nextEngineHandoff` persistence with `gameplayWrites=0`.
- Headless Chromium screenshots for water, G00L, the **glass door**, rear workstation, full overview and all four beds to catch visual clashes; user visual inspection must still follow.

## 5 · Subsequent three material variations (NOT implemented before PASS)

Derive V2, V3, V4 by copying the exact accepted `instances` array from PASS 2. Only **floor object assetId, tile scale and decorative floor object positions** may vary. Preserve glass door, G00L desk, plants, irrigation, waterways, all machinery, all non-floor positions/animations. Require a scene-by-scene comparison of non-floor objects at every change. Never silently overwrite old four archived prototype JSON files.

## 6 · Next phase: proposed Trialum ENGINE MASTER REBUILD (DESIGN DRAFT, approval required)

The user's long-term requirement is a living, interactive garden whose water, growth and machines reflect **real simulation state**, not fake visual animation. Before changing the original game repo, settle this architecture contract with the owner:

**A. Authoritative entities:** `gardenRoom`, `physicalDoor`, `waterReservoir`, `pump`, `filter`, `valve`, `hoseEdge`, `soilBed`, `slot`, `plant`, `nurseryDisplay`, `robot`, `robotTask`. Unique persistent IDs and IDs separate from visual `assetId`/Builder `instanceId`. No duplicating slots or resources.

**B. Flow / matter balance:** maintain `waterTankLiters`, `sourceCapacity`, `pumpThroughput`, `valveState`, `filterCondition`, `lineLeakState`, `soilMoisture`, `aquaticVolume`, `mineralNutrients` and `electricEnergy`. Prevent negative inventory and phantom water. Pump water only through **connected routes**, never just because a hose mesh is visible. No drip mode.

**C. Biological life and actual health:** continue canonical `lumemoss`, `glowfern`, `mineralreed`, `aquaglow`. Real `growthStage`, age, health, hydration, nutrition, light, disease and transplant conditions. Owner-chosen physical display model follows true state. Decorative nursery visuals do not count as real organisms.

**D. Device and animation bridge:** deterministic simulation emits `eventId` events (`pump.started`, `valve.opened`, `hose.pressurized`, `plant.stageChanged`, `door.opened`, `robot.taskStarted`…), consumes them idempotently, and plays GLB clips with state-aware blending. No animation is allowed to directly mutate game inventory.

**E. AI/autonomy & player intent:** real user controls and validated robot tasks for refill, cleaning, transport and plant tending; preserve explicit human approvals for resource-costing tasks. Add pathfinding, door interactions, obstacles, permission checks and safe fallback if no animated component loads.

**F. Offline/local-first:** canonical gameplay state on client device; deterministic monotonic clock and bounded catch-up, durable JSON backup/restore, migration/rollback, no phantom pet/plant duplicates. Server or peer synchronization transfers only authorized minimal events. Avoid exposing sensitive user data or device location.

**G. Integration safety:** implement only after OWNER DESIGN PASS, in a separate `Trialum` game feature branch. Preserve Classic gameplay and current Play Store releases, check saves and restoration, idempotent action receipts, negative/overfill tests, collision/path tests, airplane-mode tests and Android A55 performance. Do not combine front-end art approval with engine code or publishing.

**Next handoff input:** user-edited Builder JSON + explicit owner visual approval, followed by discussion of the final engine simulation contract. No engine implementation, game commit, release, or paid hosting work is authorized by this PASS 2 spec alone.

## 7 · What Builder will NOT claim yet

Do NOT claim the scene is owner-approved; do NOT claim there are four final PASS 2 variants; do NOT claim robots pump water autonomously, pumps modify the game economy, the door collides with pets, or the project is integrated into the Android game. WebGL and CI PASS confirm **preview data/binaries and renderer can load**, not aesthetics, physical realism on the user's GPU, or live simulation.
