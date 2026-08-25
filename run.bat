@echo off
echo Starting VPN Application...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH.
    echo Please install Python 3.10 or higher.
    pause
    exit /b 1
)

REM Check if requirements are installed
echo Checking dependencies...
pip show flet >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo Failed to install dependencies.
        pause
        exit /b 1
    )
)

REM Check if Xray exists
if not exist "core\windows\xray.exe" (
    echo WARNING: xray.exe not found in core/windows/
    echo Please download Xray-core from https://github.com/XTLS/Xray-core/releases
    echo and place xray.exe in the core/windows/ folder.
    echo.
    choice /C YN /M "Continue anyway"
    if errorlevel 2 exit /b 0
)

REM Run the application
echo Starting VPN Application...
python vpn.py

pause
