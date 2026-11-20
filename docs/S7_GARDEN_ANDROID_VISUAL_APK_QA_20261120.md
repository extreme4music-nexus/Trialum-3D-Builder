# Trialum S7 Garden · Standalone Android Visual QA

**Date:** 20 November 2026  
**Status:** Android visual-preview-only build; owner visual PASS pending  
**Repository:** `extreme4music-nexus/Trialum-3D-Builder`, isolated `android-preview/`  
**Package:** `com.trialum.gardenpreview` — separate from actual Trialum `com.trialum.ziivaiskra`  
**Source of truth:** `projects/trialum-s7-master-garden-pass2.json`, exact 703 scene objects, 363 original GLB models

## What the APK intentionally is

An independent Android native WebView showing exactly the desktop Builder's **S7 MASTER GARDEN PASS 2** with Three.js / actual local GLB files bundled in the APK, original water morph clips, plant animation clips and physically modelled G00L service room / 2.3m hinged glass door. The first mobile screen provides nine direct views (whole garden, water, service, door, workstation, each of four growing beds). Users can rotate and pinch the scene. **Edit** reveals the actual Builder controls. **Save JSON** exports through Android's native Storage Access Framework and can be sent back to ChatGPT.

WebView loads only `https://appassets.androidplatform.net/assets/`, mapped to the APK's packaged files; external domains, tracker requests and remote fonts are denied by the app. No network server, account, advertising, tracking or storage service. It is a preview of **design**, not a real game's engine; mobile fluid simulation, growth, robot tasks and inventory will be decided and implemented later, after owner approval.

### Installing from GitHub Actions

Workflow: `.github/workflows/s7-android-garden-preview.yml`. On a successful run, download artifact `TRIALUM-S7-GARDEN-PASS2-PREVIEW-APK` and install the contained `TRIALUM-S7-GARDEN-PASS2-PREVIEW-debug.apk` on Android 8+ (minSdk 26). On Android, grant install-from-this-source only when installing the known file. This is a debug-signed internal APK, **not a Google Play release**. Each independently built debug APK may use a different debug key; if an update refuses to install, retain/export the prior JSON and reinstall the preview.

### Acceptance checklist

1. Install side-by-side with original Trialum; confirm the game's saves/apps are unaffected.
2. 3D overview loads without missing geometry; user can orbit/zoom in both orientations.
3. Water scene: main + 3 satellite basins remain open and ripple; black marble appears only outside water cutouts.
4. G00L: rear desk and monitor, glass partition and real hinged door visible; shelf models and R01 are in service wing.
5. G02–G05: 20 straight canonical crop models, 88 decorative seedlings, F03 stone and technical hoses / real pumps; no dripline.
6. Open Edit; adjust at least one model and export JSON via Android's document chooser; re-open in desktop Builder before using as engine handoff.
7. Watch device performance, load time, battery and crashes: 703 objects / 363 GLBs can be heavy. The package uses a 1.25x display-pixel-ratio cap to reduce mobile GPU work.
8. Human review and feedback (screenshots/videos/JSON) precede any actual `Trialum` engine-rebuild implementation.

### Technical and safety boundaries

- No changes to existing Android app, classic gameplay, Trialum Beta, Play release or server.
- No permission for writing to remote data, no API keys, FCM, in-app purchases, external analytics or ads.
- All local files under app-specific APK assets; JSON export uses Android's explicit save dialog.
- The WebView JavaScript bridge accepts only JSON strings (max 8 MB) and the requested output filename; external network requests are blocked. 
- Source location: `android-preview/` plus packaging tool `tools/android-preview/package_web.py`. CI requires Java 17, Android SDK 36, Gradle 8.11.1 and Android Gradle Plugin 8.10.1. Verifies APK contents after build.

This APK is **the assistant's FIRST visual proposal**, not a representation of the owner's unpublished design. After owner feedback and edited Builder JSON, design the actual Trialum 3D game engine subsystem-by-subsystem.
