# Trialum Builder — Windows owner QA checklist (17 Nov 2026)

## GitHub setup
1. Clone/pull `extreme4music-nexus/Trialum-3D-Builder` through GitHub Desktop to a writable folder.
2. Run `CONNECT-GITHUB-WINDOWS.bat` in that clone. It checks `git.exe`, exact GitHub origin and **main** branch; it does NOT request credentials.
3. Sign in to GitHub Desktop/Git Credential Manager, if not already connected. This remains an **owner action on their own computer**.
4. Start `START-BUILDER-WINDOWS.bat` with Python 3 and open `http://127.0.0.1:8765/` in Edge. GitHub buttons require Python server; Node fallback is read-only.

## GLB and scene
5. Confirm 15 F01 GLB assets are in library (A 1, B 2, C 4, D 4, E 4) plus 3 design-only placeholder blocks.
6. Press **S7 Проект**, confirm 70 placed original GLB parts, camera orbit, select, move/rotate, undo/redo, JSON download and explicit Save.
7. If blank, inspect red status area or F12 Console and confirm `vendor/three.module.js`, `vendor/addons/controls/TransformControls.js`, `assets/models/*.glb` exist in cloned repo.
8. Press **Дом JSON ↓**; generated data-only Living Spaces file must contain F01 instances with stable IDs and inactive gameplay bindings.

## GitHub direct round-trip
9. Change one tile position or label. Press **Зачувај**, select **the exact root of the cloned Builder repo** with package.json, approve folder write.
10. Press **GitHub ↑**, confirm. It commits **only** `projects/`, `assets/models/`, `assets/catalog.json` via Git credential helper to Builder main.
11. Confirm new design commit in GitHub web or GitHub Desktop. Edit on GitHub or another machine, then press **GitHub ↓**. Pull requires a clean Git worktree and refuses merge/force push.

## Security and scope
- Python service binds `127.0.0.1:8765` only and validates Git remote, branch, same origin and session CSRF. Never exposed to the internet.
- No personal token is stored. No automatic GitHub pushes; every push requires an explicit browser button and confirmation.
- Source scripts, secrets, firmware and game/Classic are **never** auto-committed by the editor.
- The shared Living Spaces edit kernel exists in both repositories; **full GLB-rendered player homes, multiplayer authority, persistent pet memory and real autonomous LLM placement are not yet owner-approved/implemented**.
- If 3D engine/WebGL fails, do NOT mark PASS merely because HTML controls render.
