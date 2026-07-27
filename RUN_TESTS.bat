@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>nul
if %errorlevel%==0 (
  py -3 tools\validate_site.py && py -3 tools\http_smoke_test.py && py -3 tools\browser_contract_test.py
  pause
  exit /b %errorlevel%
)
where python >nul 2>nul
if %errorlevel%==0 (
  python tools\validate_site.py && python tools\http_smoke_test.py && python tools\browser_contract_test.py
  pause
  exit /b %errorlevel%
)
echo Python 3 was not found.
pause
exit /b 1
