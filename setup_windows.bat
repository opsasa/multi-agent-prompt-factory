@echo off
cd /d %~dp0

echo =====================================
echo Multi-Agent Prompt Factory Setup
echo =====================================
echo.

echo Checking Python...
python --version
if errorlevel 1 (
    echo.
    echo Python is not installed or not added to PATH.
    echo Please install Python 3.10+ from https://www.python.org/
    pause
    exit /b
)

echo.
echo Creating virtual environment...
python -m venv .venv

echo.
echo Activating virtual environment...
call .venv\Scripts\activate

echo.
echo Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

echo.
echo Setup finished.
echo You can now run run_windows.bat
pause
