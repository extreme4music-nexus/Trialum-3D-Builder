@echo off
setlocal
cd /d "%~dp0"
title Trialum Builder - GitHub connection check
echo ============================================
echo  TRIALUM BUILDER - GITHUB CONNECTION CHECK
echo ============================================
where git >nul 2>nul
if errorlevel 1 (
 echo Git CLI not found. Install Git for Windows or GitHub Desktop with Git command line.
 echo https://git-scm.com/download/win
 pause
 exit /b 1
)
git --version
if not exist ".git" (
 echo This is not a Git clone. Clone extreme4music-nexus/Trialum-3D-Builder in GitHub Desktop.
 pause
 exit /b 1
)
for /f "delims=" %%R in ('git remote get-url origin 2^>nul') do set "ORIGIN=%%R"
echo Origin: %ORIGIN%
echo %ORIGIN% | findstr /C:"extreme4music-nexus/Trialum-3D-Builder" >nul
if errorlevel 1 (
 echo WARNING: Wrong origin. Refusing to synchronize.
 pause
 exit /b 1
)
for /f "delims=" %%B in ('git branch --show-current') do set "BRANCH=%%B"
echo Branch: %BRANCH%
if /I not "%BRANCH%"=="main" (
 echo Select Builder MAIN in GitHub Desktop before direct synchronization.
 pause
 exit /b 1
)
echo.
echo NOTE: GitHub Desktop or Git Credential Manager login is required; no password stored by Builder.
git status --short
echo.
echo Connection setup checked. Start START-BUILDER-WINDOWS.bat and use GitHub DOWN/UP buttons.
echo DOWN requires clean Git worktree. UP commits only saved projects and models.
pause
