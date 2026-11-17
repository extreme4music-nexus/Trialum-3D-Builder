@echo off
setlocal
cd /d "%~dp0"
title Trialum 3D World Builder
echo ==========================================================
echo  TRIALUM 3D WORLD BUILDER - PRIVATE DESIGN STUDIO
echo ==========================================================
if not exist "vendor\three.module.js" goto missing
if not exist "assets\models\f01-marble-cream-full.glb" goto missing
goto ready
:missing
echo Local 3D dependencies or GLB files are missing.
echo Pull the latest MAIN using GitHub Desktop first.
echo Python 3 can also prepare them automatically:
where py >nul 2>nul
if not errorlevel 1 (
  py -3 scripts\setup.py
  if errorlevel 1 goto failedsetup
  goto ready
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
