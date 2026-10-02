@echo off
setlocal
set "PCT_NOPAUSE="
:scan_options
if "%~1"=="" goto launch
if /i "%~1"=="-NoPause" set "PCT_NOPAUSE=1"
shift /1
goto scan_options
:launch
rem Select a documented runtime before launch; do not retry policy refusals with a bypass.
set "PCT_SHELL=powershell.exe"
if exist "%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\powershell\pwsh.exe" set "PCT_SHELL=%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\powershell\pwsh.exe"
where pwsh.exe >nul 2>nul
if not errorlevel 1 set "PCT_SHELL=pwsh.exe"
"%PCT_SHELL%" -NoLogo -NoProfile -File "%~dp0scripts\Start-Hike.ps1" %*
set "PCT_EXIT=%ERRORLEVEL%"
if not "%PCT_EXIT%"=="0" (
    echo.
    echo Trail Dossier needs attention. Review the message above and data\launcher.jsonl.
    echo Saved hike history is preserved. No administrator launch is required.
    if not defined PCT_NOPAUSE pause
)
exit /b %PCT_EXIT%
