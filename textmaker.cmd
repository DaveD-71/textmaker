@echo off
setlocal
set "TEXTMAKER_CALLER_CWD=%CD%"

call :prepend_if_exists "%USERPROFILE%\AppData\Local\Pandoc" "pandoc.exe"
call :prepend_if_exists "%LOCALAPPDATA%\Pandoc" "pandoc.exe"

rem Detect common Windows-local installs for PDF/OCR dependencies on the active machine.
call :prepend_if_exists "%USERPROFILE%\AppData\Local\Programs\MiKTeX\miktex\bin\x64" "pdfimages.exe"
call :prepend_if_exists "%LOCALAPPDATA%\Programs\MiKTeX\miktex\bin\x64" "pdfimages.exe"
call :prepend_if_exists "%ProgramFiles%\poppler\Library\bin" "pdfimages.exe"
call :prepend_if_exists "%ProgramFiles%\poppler\bin" "pdfimages.exe"
call :prepend_if_exists "%ProgramFiles(x86)%\poppler\Library\bin" "pdfimages.exe"
call :prepend_if_exists "%ProgramFiles(x86)%\poppler\bin" "pdfimages.exe"

call :prepend_if_exists "%USERPROFILE%\AppData\Local\Programs\Tesseract-OCR" "tesseract.exe"
call :prepend_if_exists "%LOCALAPPDATA%\Programs\Tesseract-OCR" "tesseract.exe"
call :prepend_if_exists "%ProgramFiles%\Tesseract-OCR" "tesseract.exe"
call :prepend_if_exists "%ProgramFiles(x86)%\Tesseract-OCR" "tesseract.exe"

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

:prepend_if_exists
set "_TM_DIR=%~1"
set "_TM_EXE=%~2"
if not defined _TM_DIR goto :eof
if not defined _TM_EXE goto :eof
if exist "%_TM_DIR%\%_TM_EXE%" (
  set "PATH=%_TM_DIR%;%PATH%"
)
set "_TM_DIR="
set "_TM_EXE="
goto :eof
