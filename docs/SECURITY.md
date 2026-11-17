# Trialum Builder — Security & Privacy Boundary

This editor is private and offline-ready. It does not perform social
network actions, account deletion, inventory operations, food manufacturing,
AI conversation/memory operations, financial transactions or Play publishing.

- Local HTTP server binds ONLY to 127.0.0.1:8765, allows GET and HEAD,
  prevents path traversal/hidden file requests and sends a restrictive CSP.
  There is no mutation API.
- Pinned Three.js release 0.180.0 is downloaded once by scripts/setup.py,
  kept locally under vendor/, and included under upstream MIT license.
  No remote runtime JS, fonts or analytics are loaded.
- Project data is pure JSON, normalized on import, with 6000 instance limit
  and coordinate/scale/string caps; never run imported JSON as JavaScript.
- Catalog model load requires local assets/models/*.glb path. Imported custom
  GLB must have glTF2 magic/version and be <=32MB, but can still carry complex
  GPU geometry. Import only GLBs with licenses you trust.
- Optional binding field is only declarative text. Never evaluate it
  or send it as authenticated command to real Trialum engine.
- Browser File System Access API asks the user to select folder; save actions
  affect only projects/, assets/models/ and assets/catalog.json inside that
  explicitly selected folder. Use your cloned Builder repository ROOT.
- Imported models cached by IndexedDB are NOT automatically git-tracked;
  press Save to write files into your clone, then commit/push.
- Owner's scene files are their own authored work. Do not silently regenerate,
  overwrite, move, or delete them based on changes to the source models.
- The GitHub bootstrap workflow requests contents:write only in the Builder
  repo, to put reproducible generated GLBs and pinned Three.js vendor into
  main. It does not obtain privileged token access to the source game repo.
- No credentials, API tokens, signing keys or private server URLs should be
  stored in projects/ JSON. The owner is the final approval gate for Android.
