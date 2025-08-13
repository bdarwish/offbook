@echo off
cd /d %~dp0\..

if not exist ".venv" (
    python -m venv .venv
)

.venv\Scripts\python.exe -m pip install --upgrade pip
.venv\Scripts\python.exe -m pip install -r run\requirements.txt

if not exist "config" mkdir "config"
if not exist "output" mkdir "output"

echo -------------------------------------------------
echo                     OffBook
echo Setup complete. Use run\run.bat to start the app.
echo -------------------------------------------------

timeout /t 5 >nul