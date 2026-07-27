@echo off
setlocal
cd /d "%~dp0"
echo ============================================================
echo ASTERION FCTA-1 Siemens NX native builder
echo ============================================================
echo.
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0nxopen\run_asterion_builder.ps1" %*
set EXITCODE=%ERRORLEVEL%
echo.
if not "%EXITCODE%"=="0" (
  echo Builder did not complete. See the message above.
  echo You may specify NX manually, for example:
  echo RUN_ASTERION_BUILDER.bat -NxBin "C:\Program Files\Siemens\NX2306\NXBIN"
) else (
  echo Builder completed. Check native_output\NX_NATIVE.
)
echo.
pause
exit /b %EXITCODE%
