#!/bin/sh
set -eu
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
PYTHON="${PYTHON:-python3}"
"$PYTHON" -m venv "$ROOT/vendor/jeffy/.venv"
"$ROOT/vendor/jeffy/.venv/bin/python" -m pip install -r "$ROOT/vendor/jeffy/requirements.lock.txt"
"$ROOT/vendor/jeffy/.venv/bin/python" -m pip check
