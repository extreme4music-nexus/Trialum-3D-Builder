@echo off
setlocal
cd /d "%~dp0"
title Trialum 3D World Builder
echo ==========================================================
echo  TRIALUM 3D WORLD BUILDER - PRIVATE DESIGN STUDIO
echo ==========================================================
if not exist "vendor\three.module.js" goto missing
if not exist "assets\models\f01-marble-cream-full.glb" goto missing
goto verify
:missing
echo Local 3D dependencies or GLB files are missing.
echo Pull the latest MAIN using GitHub Desktop first.
echo Python 3 can also prepare them automatically:
where py >nul 2>nul
if not errorlevel 1 (
  py -3 scripts\setup.py
  if errorlevel 1 goto failedsetup
  goto verify
)
where python >nul 2>nul
if not errorlevel 1 (
  python scripts\setup.py
  if errorlevel 1 goto failedsetup
  goto ready
)
echo Please install Python 3 or pull generated files from MAIN.
pause
exit /b 1
:failedsetup
echo Setup failed. Check internet connection or pull MAIN from GitHub.
pause
exit /b 1
:verify
if not exist "assets\models\atrium.glb" goto incomplete
if not exist "assets\models\warehouse-shell.glb" goto incomplete
if not exist "assets\models\food-cold-annex-shell.glb" goto incomplete
if not exist "assets\models\food-packing-annex-shell.glb" goto incomplete
if not exist "assets\models\greenhouse-shell.glb" goto incomplete
if not exist "assets\models\g01-main-basin.glb" goto incomplete
if not exist "assets\models\g01-water-surfaces-animated.glb" goto incomplete
if not exist "assets\models\aquaglow-mature.glb" goto incomplete
goto ready
:incomplete
echo.
echo Some original Trialum room GLBs are missing from this local clone.
echo In GitHub Desktop choose Trialum-3D-Builder MAIN, Fetch origin, Pull origin.
echo All 41 models MUST be present; do not use a half-empty catalogue.
echo If necessary run npm install --prefix tools/b1 and py -3 scripts/build_all_assets.py.
pause
exit /b 1
:ready
echo.
echo Your builder is at http://127.0.0.1:8765/
echo Keep this window open while you edit.
echo.
where py >nul 2>nul
if not errorlevel 1 (
  start "" "http://127.0.0.1:8765/"
  py -3 scripts\server.py
  goto :eof
)
where python >nul 2>nul
if not errorlevel 1 (
  start "" "http://127.0.0.1:8765/"
  python scripts\server.py
  goto :eof
)
where node >nul 2>nul
if not errorlevel 1 (
  start "" "http://127.0.0.1:8765/"
  node scripts\server.mjs
  goto :eof
)
echo Requires Python 3 or Node.js 20+ for the local server.
pause
exit /b 1
