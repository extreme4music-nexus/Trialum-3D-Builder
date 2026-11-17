# Builder startup fix — blocked Three.js importmap (2026-11-17)

**Owner-observed error:** `Uncaught TypeError: Failed to resolve module specifier "three". Relative references must start with either "/", "./" or "../".`

## Root cause
`index.html` already contains a correct inline `<script type="importmap">` mapping `three` to `./vendor/three.module.js` and `three/addons/` to `./vendor/addons/`. Both localhost HTTP servers shipped `Content-Security-Policy: script-src 'self'`, unintentionally blocking that *inline* importmap. The browser then sees bare `three` with no mapping and aborts the module graph. HTML controls render but none of the Three.js editor initializes.

## Fix
- `scripts/server.py` and `scripts/server.mjs` now **compute SHA-256 of the exact index.html importmap text** on each response, and allow only that hash in the CSP `script-src`; no global `unsafe-inline`, third-party CDN, unsafe eval, network enablement or bearer secrets.
- `tests/importmap-csp.test.mjs` runs both localhost servers, checks the exact CSP hash, validates the vendor module route, and prevents regression.
- Original F01 GLB and project JSON remain unchanged.
- This is a Builder-only fix. **Do not modify Trialum Classic, LW-D game, production Google Play or Android signing.**

## Windows verification
1. Exit the previous START-BUILDER-WINDOWS console completely (old Python server keeps serving old CSP).
2. GitHub Desktop → `Trialum-3D-Builder` → `main` → Fetch origin → Pull origin.
3. Double-click `START-BUILDER-WINDOWS.bat` again; open `http://127.0.0.1:8765/` in Edge.
4. Hard refresh `Ctrl+Shift+R`. If a new browser tab is stale, close and reopen it; check DevTools Network Headers of document for `Content-Security-Policy` containing `script-src 'self' 'sha256-…'`.
5. Expect the 3D grid, catalog and **S7 Проект** to work. Test selection/orbit, model placement, undo and save.
6. If the same error persists, check Console for `Refused to parse an import map because it violates Content Security Policy`, and verify no different process is using port 8765. A Node or Python server must be restarted, not merely the tab.

The SHA is intentionally regenerated from the HTML, avoiding fragile hardcoded allowlisting after future importmap changes.
