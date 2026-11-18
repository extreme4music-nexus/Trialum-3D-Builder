@echo off
setlocal
cd /d "%~dp0"
chcp 65001 >nul
title Trialum Builder - GitHub local clone doctor
echo =====================================================
echo   TRIALUM BUILDER - LOCAL GITHUB SAFETY CHECK
echo =====================================================
echo.
echo This tool DOES NOT delete .git, reset commits, or change designs.
echo.
where git >nul 2>nul
if errorlevel 1 (
 echo Git for Windows CLI is missing from PATH.
 echo Install Git for Windows, reopen terminal, and try again.
 pause
 exit /b 1
)
git --version
echo.
where py >nul 2>nul
if not errorlevel 1 (
 py -3 scripts\git_doctor.py
 goto result
)
where python >nul 2>nul
if not errorlevel 1 (
 python scripts\git_doctor.py
 goto result
)
echo Python 3 is required for this built-in Git diagnostic.
pause
exit /b 1
:result
if errorlevel 1 (
 echo.
 echo The local clone is not healthy for direct Builder GitHub sync.
 echo Open GitHub Desktop - Repository - Show in Explorer.
 echo Compare the folder with the Builder location printed above.
 echo Do NOT remove .git or lock files while another Git command may run.
 pause
 exit /b 1
)
echo.
echo The clone passed this local check.
echo Use GitHub Desktop OR Builder sync, but not both at the same time.
pause
exit /b 0
