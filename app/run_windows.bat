@echo off
setlocal
cd /d "%~dp0"

echo [NIA Conversation Reaction Lab]
if not exist .venv (
    echo Creating virtual environment...
    py -3 -m venv .venv
)

call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python nia_reaction_lab.py
endlocal
