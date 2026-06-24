@echo off
cd /d %~dp0

echo =====================================
echo Multi-Agent Prompt Factory
echo =====================================
echo.

if not exist .env (
    echo Cannot find .env file.
    echo.
    echo Please copy .env.example and rename it to .env
    echo Then fill in your API Key.
    echo.
    pause
    exit /b
)

if not exist .venv (
    echo Virtual environment not found.
    echo Please run setup_windows.bat first.
    pause
    exit /b
)

call .venv\Scripts\activate

echo Running app...
python app.py

echo.
echo Finished.
echo Result saved to output\final_prompt.md or output\result.md
pause
