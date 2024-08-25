@echo off
start /min "" cmd /c "
set PROJECT_DIR=C:\Users\Bobby\PycharmProjects\cursor_highlighter
set MAIN_SCRIPT=%PROJECT_DIR%\main.py

if exist "%PROJECT_DIR%\venv" (
    set "VENV_DIR=%PROJECT_DIR%\venv"
) else if exist "%PROJECT_DIR%\.venv" (
    set "VENV_DIR=%PROJECT_DIR%\.venv"
) else (
    echo Virtual environment not found.
    exit /b 1
)

start "" "%VENV_DIR%\Scripts\pythonw.exe" "%MAIN_SCRIPT%"
exit
"

