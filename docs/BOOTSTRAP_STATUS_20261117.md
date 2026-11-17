# Trialum Builder bootstrap status — 17 Nov 2026

## ✅ GitHub Actions recovered after the repository became PUBLIC

- Repository: https://github.com/extreme4music-nexus/Trialum-3D-Builder
- **Visibility: PUBLIC**, changed by the owner intentionally to make GitHub Actions runners available. Do not describe this repository as private in future handoffs.
- **Final green bootstrap run:** https://github.com/extreme4music-nexus/Trialum-3D-Builder/actions/runs/44150701259
- Head/source SHA: `97e3ef9f29137c181dc2ae719c0cddf399d8775b`.
- **Result: SUCCESS, 1/1 job completed successfully.**
- Previous runs failed before provisioning a runner when repository was private; changing visibility enabled real runner execution. Once runners worked, two correctable setup/test issues surfaced: nullable `src` for intentional mock objects and a `curl | grep -q` pipeline SIGPIPE on 603 KB Three.js module. Both were fixed and verified by final run.

## ✅ Actual GLB and Three.js files committed to main

- **GitHub Actions binary commit:** https://github.com/extreme4music-nexus/Trialum-3D-Builder/commit/a5bf7dc
- `assets/models/` now contains **11 real binary glTF2 models**: F01-A ×1, F01-B ×2, F01-C ×4, F01-D ×4.
- `vendor/` contains pinned **three@0.180.0**, `three.module.js`, `three.core.js`, GLTFLoader, OrbitControls, TransformControls, BufferGeometryUtils and upstream MIT license.
- The canonical F01-A approved SHA256 check passed in Python.
- **9/9 Node tests PASS**, **3/3 Python model tests PASS** in workflow; 11 GLBs and local Three.js server bytes verified by complete direct comparison.
- Local static server bound to `127.0.0.1:8765` served HTML, vendor JS and real GLB; hidden git config request blocked. No game/Play/warehouse code changed.
- Repo `main` now includes these generated binaries and dependencies, so **manual Python bootstrap and the earlier fallback ZIP are no longer needed for a fresh GitHub Desktop clone**.

## What the owner should do

1. In GitHub Desktop, **Fetch origin → Pull origin** for `extreme4music-nexus/Trialum-3D-Builder`.
2. Open cloned folder → double-click `START-BUILDER-WINDOWS.bat` (requires Python 3 or Node.js 20+ for the loopback server).
3. Open `http://127.0.0.1:8765/` via Edge/Chrome. Place existing F01-A/B/C/D from catalogue.
4. Press **Зачувај**, explicitly choose the clone root, confirm new `projects/*.json` and any imported GLBs appear as changed files in GitHub Desktop, then Commit/Push.
5. Report the first owner Windows visual QA result, including whether real GLBs (not fallback boxes), drag, rotate, save, reload work.

**Note:** This repository is now PUBLIC; scene JSONs and models committed and pushed to main will be publicly accessible. Avoid publishing private data, server keys or designs intended to remain confidential.

## Remaining acceptance gate

CI is **GREEN**, GLB assets **AVAILABLE**, but **owner Windows browser/WebGL visual PASS is not yet recorded**. The verified server/http/tests are not evidence that the owner's particular Windows/Edge GPU renders every imported model flawlessly. Do not claim owner acceptance or Android game integration until separately verified.
