#!/bin/bash
cd "$(dirname "$0")/.."

if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi

.venv/bin/pip install --upgrade pip
.venv/bin/pip install -r run/requirements.txt

mkdir -p config output

echo "-----------------------------------------------------"
echo "                       OffBook                       "
echo "Setup complete. Use run/run.command to start the app."
echo "-----------------------------------------------------"

exit 0