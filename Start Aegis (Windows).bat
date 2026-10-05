@echo off
title Aegis
cd /d "%~dp0"
where py >nul 2>nul && (set PY=py) || (set PY=python)
%PY% --version >nul 2>nul || (
  echo Python is not installed. Get it from https://www.python.org/downloads/ and tick "Add Python to PATH".
  pause & exit /b 1
)
%PY% -c "import flask, cryptography, jsonschema" >nul 2>nul || (
  echo First run: installing 3 packages ^(needs internet once^)...
  %PY% -m pip install -r requirements.txt || (pause & exit /b 1)
)
echo.
echo Aegis is running at http://127.0.0.1:8765  -  close this window to stop it.
%PY% run.py
pause
