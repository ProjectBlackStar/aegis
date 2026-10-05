#!/bin/bash
cd "$(dirname "$0")"
if ! command -v python3 >/dev/null; then
  echo "Python is not installed. Get it from https://www.python.org/downloads/"; read -r; exit 1
fi
if ! python3 -c "import flask, cryptography, jsonschema" 2>/dev/null; then
  echo "First run: installing 3 packages (needs internet once)..."
  python3 -m pip install -r requirements.txt || { read -r; exit 1; }
fi
echo; echo "Aegis is running at http://127.0.0.1:8765  -  close this window to stop it."
python3 run.py
