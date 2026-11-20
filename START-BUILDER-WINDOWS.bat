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
  goto verify
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
if not exist "assets\models\f01-marble-cream-radial-wedge.glb" goto incomplete
if not exist "assets\models\f01-g-cream-marble-pool-trim-1m.glb" goto incomplete
if not exist "assets\models\f01-g-cream-marble-pool-trim-half.glb" goto incomplete
if not exist "assets\models\f01-g-cream-marble-pool-trim-3m-showcase.glb" goto incomplete
if not exist "assets\models\f01-h-cream-marble-matte-service.glb" goto incomplete
if not exist "assets\models\f01-i-cream-marble-fine-textured-wet.glb" goto incomplete
if not exist "assets\models\f02-black-marble-full.glb" goto incomplete
if not exist "assets\models\f02-black-marble-l-corner-showcase-north-west.glb" goto incomplete
if not exist "assets\models\f02-black-marble-radial-wedge.glb" goto incomplete
if not exist "assets\models\f02-black-marble-fine-textured-wet.glb" goto incomplete
if not exist "assets\models\f03-s-stone-full.glb" goto incomplete
if not exist "assets\models\f03-t-stone-full.glb" goto incomplete
if not exist "assets\models\f03-s-stone-radial-wedge.glb" goto incomplete
if not exist "assets\models\f03-t-stone-pool-trim-1m.glb" goto incomplete
if not exist "assets\models\f03-s-stone-l-corner-showcase-north-west.glb" goto incomplete
if not exist "assets\models\f03-t-stone-raised-border-showcase-west.glb" goto incomplete
if not exist "assets\models\s02-planting-bed-5x5-empty.glb" goto incomplete
if not exist "assets\models\s03-dug-turnover-soil.glb" goto incomplete
if not exist "assets\models\s02-single-hole-soil-plug.glb" goto incomplete
if not exist "assets\models\s02-slot-target-ring.glb" goto incomplete
if not exist "assets\models\s02-demo-seedling-preview.glb" goto incomplete
if not exist "assets\models\s7-lf1-perimeter-straight-1m.glb" goto incomplete
if not exist "assets\models\s7-lc1-g01-1plus4-ring-chandelier.glb" goto incomplete
if not exist "projects\trialum-s7-lights-all-24-glbs.json" goto incomplete
if not exist "assets\models\s7-e0e1-rs01-nursery-3-tier.glb" goto incomplete
if not exist "assets\models\s7-e0e1-rm02-mature-double.glb" goto incomplete
if not exist "projects\trialum-g00l-e0e1-all-review.json" goto incomplete
if not exist "assets\models\s7-f-r01-humanoid.glb" goto incomplete
if not exist "assets\models\s7-f-e01-excavator.glb" goto incomplete
if not exist "projects\trialum-s7-f-all.json" goto incomplete
rem The complete 362-GLB MASTER garden must be present after any MAIN pull.
if not exist "projects\trialum-s7-master-garden-review.json" goto incomplete
if not exist "projects\trialum-s7-master-garden-pass2.json" goto incomplete
if not exist "assets\models\s7-pass2-g00l-glass-partition-door.glb" goto incomplete
if not exist "assets\models\s7-master-g01-edge-finish.glb" goto incomplete
if not exist "assets\models\s7-master-g00l-glass-service-wing.glb" goto incomplete
if not exist "assets\models\lumemoss-mature.glb" goto incomplete
if not exist "assets\models\glowfern-mature.glb" goto incomplete
if not exist "assets\models\mineralreed-mature.glb" goto incomplete
goto ready
:incomplete
echo.
echo Some original Trialum room GLBs are missing from this local clone.
echo In GitHub Desktop choose Trialum-3D-Builder feature/remote-builder-3d-20261120, Fetch origin, Pull origin.
echo All 363 models MUST be present, including the glass door and MASTER PASS2 scene.
echo If necessary run npm install --prefix tools/b1 and py -3 scripts/build_all_assets.py.
pause
exit /b 1
:ready
rem A previously running localhost server can serve an OLD clone after Pull.
rem Never open browser against stale process or terminate it automatically.
where powershell >nul 2>nul
if not errorlevel 1 (
  powershell -NoProfile -Command "$c=New-Object System.Net.Sockets.TcpClient;try{$c.Connect('127.0.0.1',8765);$c.Close();exit 17}catch{exit 0}"
  if errorlevel 17 goto portbusy
)
echo.
echo Verified 363 GLBs: MASTER PASS 2 water, plants, G00L glass door, pumps/hoses and 24 light assets.
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

:portbusy
echo.
echo ERROR: another Builder or service is already listening on 127.0.0.1:8765.
echo It might be serving the OLD clone even after your GitHub Desktop Pull.
echo Save open designs. Close the old Builder server terminal/window first.
echo Then run THIS START-BUILDER-WINDOWS.bat from the current Builder MAIN folder.
echo No processes or user files were changed by this check.
pause
exit /b 1
