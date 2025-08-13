#!/bin/bash
cd "$(dirname "$0")/.."

source .venv/bin/activate

python home_gui.py

deactivate