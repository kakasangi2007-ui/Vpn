@echo off
echo VPN Application Installer
================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH.
    echo Please install Python 3.10 or higher from https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

echo Python found!
python --version
echo.

echo Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo Failed to install dependencies.
    echo Please try: pip install --upgrade pip
    pause
    exit /b 1
)

echo.
echo Dependencies installed successfully!
echo.
echo Checking Xray-core...
if not exist "core\windows\xray.exe" (
    echo.
    echo WARNING: xray.exe not found in core/windows/
    echo Please download Xray-core from: https://github.com/XTLS/Xray-core/releases
    echo Choose Xray-windows-64.zip, extract, and copy xray.exe to core/windows/
    echo.
    echo You can still run the application without Xray-core,
    echo but VPN functionality will not work.
    echo.
)

echo.
echo Installation complete!
echo.
echo To run the application: run.bat or python vpn.py
echo.
pause
