@echo off
setlocal
set "TEXTMAKER_CALLER_CWD=%CD%"

if exist "%USERPROFILE%\AppData\Local\Pandoc\pandoc.exe" (
  set "PATH=%USERPROFILE%\AppData\Local\Pandoc;%PATH%"
)

rem Ensure UNC script locations work by mapping to a temporary drive letter.
pushd "%~dp0" >nul 2>&1
if errorlevel 1 (
  echo Failed to access script directory: %~dp0
  exit /b 1
)

python -m scripts %*
set "EXIT_CODE=%ERRORLEVEL%"

popd
exit /b %EXIT_CODE%
