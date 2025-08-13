@echo off
cd /d %~dp0\..

if not exist ".venv" (
    python -m venv .venv
)

.venv\Scripts\python.exe -m pip install --upgrade pip
.venv\Scripts\python.exe -m pip install -r run\requirements.txt

echo -------------------------------------------------
echo                     OffBook
echo Setup complete. Use run\run.bat to start the app.
echo -------------------------------------------------
pause