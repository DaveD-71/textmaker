@echo off
setlocal

rem Ensure UNC script locations work by mapping to a temporary drive letter.
pushd "%~dp0" >nul 2>&1
if errorlevel 1 (
  echo Failed to access script directory: %~dp0
  exit /b 1
)

python -m textmaker %*
set "EXIT_CODE=%ERRORLEVEL%"

popd
exit /b %EXIT_CODE%
