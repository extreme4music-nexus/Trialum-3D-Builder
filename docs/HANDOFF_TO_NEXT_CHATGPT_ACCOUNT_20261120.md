# TRIALUM 3D BUILDER — TECHNICAL HANDOFF TO NEXT AI / CODEX

**Snapshot 20 November 2026.** This file contains only project technical facts, no credentials or personal account information. The owner also possesses a more complete *private*, **TRIALUM-ONLY** handoff ZIP with complete game history, detailed 3D design/simulation roadmap, the byte-exact 703-instance scene JSON and 363-GLB catalog; it should be uploaded into the new ChatGPT account.

## Current source of truth

- Repository: `extreme4music-nexus/Trialum-3D-Builder`, branch `main`, verified at `4523c272d4b72ecefe3668a6869b877fea2b6c9c` (always re-fetch before edits).
- S7 MASTER PASS2 visual design: `projects/trialum-s7-master-garden-pass2.json`, 703 independently editable instances; `assets/catalog.json` lists 363 genuine GLB files.
- Stable design docs: `docs/S7_MASTER_GARDEN_PASS2_FULL_BUILD_SPEC_20261119.md`, `docs/S7_MASTER_GARDEN_RECONSTRUCTION_REPORT_20261119.md`, `docs/S7_GARDEN_ANDROID_VISUAL_APK_QA_20261120.md`.
- G01: original central + three satellite water holes, four Aquaglow slots, 6s morph GLB water animation. G00L: open glass service wing, animated 2.3m glass door, shelves, desk, monitor, robot R01, pumps, filters and hoses.
- G02–G05: four canonical land beds x five actual gameplay slots; decorative seedling previews do not create game objects/harvests. Owner explicitly disallows drip-by-drip irrigation on beds.
- Original PASS1 and V1–V4 scenes are preserved as prior layouts, NOT four final approved PASS2 floor variants.

## Highest priority: unresolved G02 visual/grid regression

**Owner explicitly reports that the left-bed correction is NOT visually acceptable. Do not claim fixed because a GLB or APK builds.**

1. Keep **G01 central, G00L service room, G03, G04, G05** completely unchanged.
2. Work only on **G02 left growing finger**: a straight centerline of real stone paving, visually flush, no gaps/sideways blocks.
3. The last main change modified only 4 existing `master-finger-1-path-[1..4]` `assetId` values to `f03-s-stone-full`. It did NOT correct the rotated local grid or transform/snap behavior.
4. Fix `src/main.js` editor placement/grid snapping in local bed coordinates rather than the global XZ grid. Source G02 bearing approximately `-73 degrees`; local basis radial `[sin(theta), -cos(theta)]`, lateral `[cos(theta), sin(theta)]`. Inspect physical GLB pivot/Box3 and validate the coordinate convention in Blender/actual browser before committing.
5. Use real local Windows Builder/Chrome/Edge and, if available, installed Blender (`bpy` or Computer Use) with top-down and eye-level screenshots/video. Start by visually placing 8–10 modules on the centerline, ask owner for visual PASS. CI only checks code; it cannot certify visual arrangement.
6. Diff JSON instances: exclude only explicitly approved G02 instance IDs; prove the remaining instances, metadata, water and other rooms are unchanged. Preserve owner autosaves and existing scene exports.

## Desktop and APK procedures

- Windows: `GitHub Desktop` -> Builder `main` -> `Fetch/Pull`, stop old localhost server, run `START-BUILDER-WINDOWS.bat`, open `http://127.0.0.1:8765/?preset=garden-master&view=bed1`.
- Builder UI: top room dropdown only for real rooms; separate **left-hand** package/category/individual-GLB selection.
- Android visual QA source in `android-preview/`, distinct from game app. Its 363-GLB/703-instance preview is **not** the game engine. The earlier assistant manually repacked one APK using only JAR signing; the owner reported `App not installed`.
- Fixed independent debug APK GitHub run `44693799413`, branch `fix/g02-left-bed-stone-signed-apk-20261120`, package `com.trialum.gardenpreview.g02stone`; Android v2 signing and build verified, but **OWNER DEVICE INSTALL/RENDER PASS NOT CONFIRMED**.
- Main Builder CI run `44694204672` succeeded at the above SHA. APK and technical build PASS are not proof of visual quality.

## Future engine boundary

- Visual scene JSON is editable layout, not the authoritative simulation. No current irrigation resource simulation, robot autonomy, plant growth/health integration or door collision/pathfinding should be claimed.
- Owner will review scene, optionally re-design in Blender/Builder, and export JSON. Only after owner approval discuss full Trialum runtime master rebuild (water mass balance, pump/valve/hose graph, 4x5 soil slots + 4 aquatic slots, biological growth, robot tasks, event-driven animations, durable backup/save, local-first consent/privacy).
- Trialum main and original Play distribution MUST NOT be changed from an S7 Builder visual task. Follow original game `AGENTS.md`, `docs/TRIALUM_3D_PHASE_GATES_20261115.md`, B1 owner gate and beta signing policies.
- No secrets, keys, license violations, private user backups or student data in public repos.

**Owner acceptance statement is the only visual gate.** If the owner has not watched the actual scene and said PASS, mark it pending and stop before other rooms/versions.


## Detailed source diagnosis: WHY G02 tiles stayed tilted
This is not a rendering-only defect or a wrong texture. The authoritative `src/main.js` editor has a world-space transform/snap system, but G02 follows a rotated garden finger:
- Line ~66: `gizmo.setSpace("world")`; floor slab drags use global axes.
- Lines ~73–80: after dragging, every X/Z component is independently rounded via `snap(n,gridStep())`; the floor Y special case resets to 0.
- Lines ~96,140,159: gridStep is a world interval, and `new THREE.GridHelper(...)` is global, origin/rotation unbound to a physical bed.
- Lines ~527–550: floor placement intersects global Y=0 plane; it snaps global X/Z and places floor GLB at `rotationY=0`, not the -73° G02 orientation.
- Original glass shell uses paw-shaped G02–G05 radial coordinates. A flat axis-aligned grid cannot be stretched or rotated to become a local G02 bed by changing four tiles' `assetId`.
**Immediate fix:** introduce an opt-in per-bed `originXZ, tangentXZ, lateralXZ, stepU, stepV` coordinate frame; apply inverse projection to grid snap and forward projection back to world, with a matching visible `GridHelper` and scene-GLB rotation/pivot check. Do NOT globally migrate all 703 existing positions or alter snap in unrelated rooms.

G02 radial direction at θ≈-73° is `(sinθ,-cosθ)`; lateral direction `(cosθ,sinθ)`. For world point P and bed origin O:
`u=dot(P−O,radial)`, `v=dot(P−O,lateral)`;
`Psnapped=O + round(u/stepU)*stepU*radial + round(v/stepV)*stepV*lateral`.
Before using this formula, confirm THREE.js axis/yaw direction, *real* GLB pivot and bed start from loaded geometry in Blender/browser. Owner should see an **8–10 tile seamless centerline** with top-down, eye-level and side-view verification. Record before/after screenshots/video from actual editor, not conceptual images.

## 3D full-development dependency after G02 owner acceptance
1. Owner reviews the left G02 lane; no merge or final visual PASS until explicitly confirmed.
2. Owner finishes remaining layout in Blender or Builder and exports a corrected complete MASTER scene JSON. Keep PASS1 and old V1–V4 as archives.
3. Using that exact accepted JSON, derive three additional material-only variants without moving non-floor objects or changing actual plant capacities.
4. **Separate game-engine project**, only on fresh owner authorization: source-of-truth runtime scene bridge; physical doors/collision; pump/filter/valve/hose water-flow graph and conservation; plant biology and state-driven GLB clips; robot logistics/tasks; deterministic offline ticks/backup/restore; preservation of original Classic, multiplayer, pet/food/inventory and AI consent.
5. Respect B1/Three.js renderer owner-gates in the game repository. A completed Builder scene or preview APK is not a completed integrated 3D game. Do not push engine changes/Play builds from a design handoff.

## Verified source-snapshot integrity (20 November)
The owner has an export ZIP, with both source files verified byte-exact against the GitHub blob IDs:
- `projects/trialum-s7-master-garden-pass2.json` blob `5d68670f7c073d1842b3f89c49b0394c20ffec91` (703 instances; four G02 ID substitutions, **NOT** visual PASS).
- `assets/catalog.json` blob `8e9eac716453e70b474de87380efb2788a9dec26` (363 real GLB catalog entries).
The ZIP has **no entire 363-GLB binary collection**: clone Builder from GitHub. New ChatGPT account GitHub connection and local Blender/Windows permissions require the owner's separate explicit setup; never assume they transfer.
