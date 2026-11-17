# TRIALUM 3D WORLD BUILDER — COMPLETE RECOVERY HANDOFF
17 November 2026 · Builder v0.1 · Owner-directed private development

## Goal and ownership
The owner explicitly created a NEW private GitHub repository:
**extreme4music-nexus/Trialum-3D-Builder**.
The agent confirmed it exists and initialized its main branch.
This is a standalone Windows desktop browser HTML/Three.js GLB level editor.
The owner wants to **clone it with GitHub Desktop, position actual 3D models
like LEGO bricks, save projects into the clone and commit/push**.
Their layouts are authoritative DESIGN decisions. The 3D game engineer will
then integrate selected designs, UI and REAL gameplay linkages in a separate
game-repo PR after tests and owner's Android confirmation.

**Do not confuse repos.**
- Builder: extreme4music-nexus/Trialum-3D-Builder, branch main (authorized).
- Game LW-D: extreme4music-nexus/Trialum, private; warehouse integration
  Draft PR #92, branch feature/lw-d-s7-classic-warehouse-live-3d-integration-20261117.
- Game F01-D edge kit Draft PR #93, branch
  feature/lw-d-s7-f01-d-cream-marble-edge-trim-20261117.
- Codex separately operates trialum-beta and Trialum-Android-Builds;
  a future comprehensive security/AI/social handoff will eventually be
  integrated in LW-D, NOT by Builder work. Do not modify Classic Beta, auth,
  messages, friends, AI memory, account deletion or Android distribution.
- No main merge or Google Play release in the GAME repo.

## Current builder structure
README.md                         Macedonian Windows GitHub Desktop guide
START-BUILDER-WINDOWS.bat         double-click starter; Python3/Node fallback
START-BUILDER-LINUX.sh            Linux starter
index.html                        full desktop builder UI
src/style.css                     dark responsive professional styling
src/project.js                    safe versioned JSON schema/grid/helpers
src/main.js                       interactive Three.js GLTFLoader scene
assets/catalog.json               11 REAL original F01-A/B/C/D GLBs + placeholders
assets/models/*.glb               generated and git-tracked by CI
projects/example-room.json        eight-position original F01 A/B/C demo
tools/b1/build-s7-f01-*.py        ORIGINAL exact 4 Python asset generators
scripts/setup.py                  reproducible GLB + pinned Three vendor setup
scripts/server.py                 loopback-only zero-dependency server
scripts/server.mjs                Node alternate loopback-only server
tests/project.test.mjs            project/safety/grid tests
tests/editor-files.test.mjs       UI and catalogue static tests
tests/models.test.py              real shipped glTF2 and SHA tests
.github/workflows/bootstrap.yml   auto-build and commit original GLB+Three deps
docs/PROJECT_FORMAT.md            scene JSON contract
docs/SECURITY.md                  local safety boundaries

## Core builder interactions
- Three.js WebGLRenderer with Hemisphere+Directional illumination, OrbitControls
  right mouse orbit / middle zoom / left pan, TransformControls object gizmo.
- Select a catalogue model left and click floor to place real GLB.
- Floor modes, visible wall guides and wall placement; primitive mockups for
  machines before official GLBs, NOT an actual machine or game logic.
- Exact X/Y/Z, rotation Y degrees, scale, name, layer, locked/visible,
  optional STRING engine binding identifier; no execution of binding.
- Grid snap .05/.1/.25/.5/1.0m, room width/depth/height, grid visibility.
- Object list, duplicate/delete, Undo/Redo with 60 snapshots, local autosave,
  import existing JSON, import new GLB (size <= 32MB; glTF2 magic/version).
- Imported assets cached in browser IndexedDB; not a Git backup by itself.
- **Зачувај** uses Chromium File System Access API showDirectoryPicker and
  writes scenes to projects/<slug>.json; imported GLBs to assets/models/
  plus merges new IDs into assets/catalog.json in the *explicitly chosen*
  cloned repository folder. User then GitHub Desktop Commit/Push.
- JSON download or ZIP with scene plus imported GLBs for fallback transfer.
- No editor server API writes, no external services, no user account, no game
  stock mutation, no NPC simulation, no main/Play publication.

## Models exact source and visual constraints
F01-A original 1x1x.06m marble, approved by owner, sha256:
787965608e2e4005a0ee84c857d7f0379a8093149b39da6bacb2d012feafc147
384x384 original embedded PNG SHA256:
81c434a57b770148ced6e9c40dccabade929a844a27b143f2dc13a4da0ff8c98
F01-B1 and B2 are texture-aligned 1x.5 halves with phases 0 and .5.
F01-C1..C4 are .5x.5 quarters, with four texture UV phases.
F01-D north/south/east/west are 1m exposed 6cm trims OUTSIDE tile;
do not overlap them at perpendicular external corners — planned F01-E.
Original source F01-D CI 21/21 PASS:
https://github.com/extreme4music-nexus/Trialum/actions/runs/44123783191
F01-D artifact 14347021157.
Real asset status: A visual PASS, B/C/D automated CI PASS and owner review
pending unless new explicit owner message approves them. No F01 tiles actually
installed in canonical game room yet.
The original 9 material modules are A full B half C quarter D edge E corner
F radial wedge G border H service I wet finish. Do not invent curved G01
geometry: inspect actual four animated basins and owner S7 V3 topology first.

## Bootstrapping
Once scripts, original A-D generators, catalogue and workflow are committed,
GitHub Actions bootstrap.yml (permissions contents:write only THIS repo)
runs scripts/setup.py:
1) deterministic exact original A-D Python authors -> 11 GLBs in assets/models
2) local pinned MIT three@0.180.0 module and addon imports in vendor/
3) CI checks Node project tests, Python actual glTF geometry and original hash
4) commits only assets/models and vendor into Builder main for owner to Pull.
The setup script may fetch npm CDN once. Thereafter editor is offline-ready.
If action blocked/failed, Windows starter attempts setup via Python3; do not
claim assets are in Git until verify a GitHub commit with binary files.

## Specific acceptance QA (NOT yet owner confirmed)
1. Clone Builder repo and Pull after binary bootstrap commit.
2. Double-click START-BUILDER-WINDOWS.bat; Edge/Chrome local site opens.
3. Verify actual F01-A/B/C/D model load and preview, not red fallback box.
4. Place B1 then B2 adjacent z+0.5; see same cream stone texture.
5. Place all C1..C4 in quadrants, rotate/move, Undo/Redo, duplicate.
6. Use wall mode with optional decorative panel; check coordinates/snap.
7. Import one custom GLB; ensure local cache and scene save to repo root.
8. Verify projects/*.json and assets/models/*.glb appear in GitHub Desktop,
   commit and Push, reopen project after reload/new browser.
9. Check browser dev console, WebGL performance, zero game/Play changes.

## Next development AFTER Builder works
The owner requested next completion of other GLB assets, but not by mixing
them into the Classic Beta. Start F01-E straight marble corner finishing;
then F, G, H, I with actual reference measurements, each real glTF mesh +
PBR + standalone QA artifact and visual owner approval. Make Builder
catalogue entries for each only after source asset valid, without overwriting
the owner's scene JSON. After new models are in catalogue, the owner can
update design and push; 3D engineer takes JSON and wires into actual game
on separate staging branch.

## Quality and caution
GitHub Actions tests do not equal visual owner PASS.
Never silently replace owner-authored projects or merge game main.
GLB custom content may have third-party licensing and heavy GPU costs.
Use real canonical game engine for final storage/food/pet mechanics.
No secrets/tokens or production server URLs in Builder.
Use exact repo, branch and commit identifiers when continuing this work.
