# Trialum Builder bootstrap status — 17 Nov 2026

## Verified GitHub repository and source
- Private repo exists: https://github.com/extreme4music-nexus/Trialum-3D-Builder
- Main contains actual code (index.html, 3D Three.js editor, CSS, project serializer, local server, Windows starter), 11 GLB catalogue entries, four byte-for-byte original F01 deterministic Python source generators, and complete docs.
- JavaScript syntax of src/main.js and src/project.js was parsed and checked using the connected tools. Six schema/catalogue in-memory checks passed, including grid snap, JSON import/export and 11 catalogue entries.
- Example scene is in projects/example-room.json; no source Trialum/Classic/Play or warehouse game code edited.

## GitHub Actions infrastructure blocker — do not claim CI green
The newly created private repository currently fails to provision an Actions job.
- Original bootstrap workflow run #44147563490, attempts 1 and 2 both FAILED *before any reported step*, with no available job logs / steps in the connected GitHub API.
- Minimal separate runner smoke #44148060908, using a single echo step on ubuntu-24.04, also FAILED before any reported step and exposes no logs.
- Because even an independent echo probe fails, cannot attribute this to the Builder code, Python model generator or Three.js downloads. May be GitHub account Actions billing/runner permissions; only GitHub Actions UI/account can establish exact cause.
- **Consequently the 11 generated GLB binaries and pinned Three.js vendor files are NOT yet committed to Builder main.** Do not say GitHub Desktop clone alone is fully offline-ready.

## Fully implemented local recovery path
1. Clone Builder in GitHub Desktop and open its folder.
2. Make sure Python 3 is installed. At Windows terminal in Builder root run:
   py -3 scripts/setup.py
3. This generates the **11 exact original glTF2 A/B/C/D files** into assets/models and downloads the pinned Three.js module plus its addon dependencies under vendor/.
4. Double-click START-BUILDER-WINDOWS.bat; local URL http://127.0.0.1:8765/.
5. GitHub Desktop now sees generated GLB+vendor; commit/push them once from the user's local machine if GitHub Actions is still unavailable. Do not commit unrelated files.
6. Offline fallback for original 11 GLBs is also supplied in this conversation as Trialum-3D-Builder-F01-Real-GLB-Starter-Pack.zip; extract at Builder root, then run scripts/setup.py once to obtain the pinned Three.js vendor. The archive itself is not yet hosted as a GitHub binary.

## Next action
Get an actual local Chromium owner test before claiming PASS: exact real GLB loads, placement, save into cloned repo, reopen design and GitHub Desktop push. The small engine/schema tests are distinct from full visual WebGL testing.
When GitHub Actions infra is restored, rerun bootstrap and verify binary commit and CI before marking bootstrap green.
