@echo off
title AdsPower Tool Pro - Install Software

echo.
echo ========================================
echo   AdsPower Tool Pro - Install Software
echo   Step 1: Install Python Environment
echo ========================================
echo.

REM Try to run Python script
python install_software.py
if errorlevel 1 (
    echo.
    echo Python not found! Please install Python first:
    echo 1. Go to https://www.python.org/downloads/
    echo 2. Download Python 3.11 or later
    echo 3. During installation, CHECK "Add Python to PATH"
    echo 4. Restart computer after installation
    echo 5. Run this script again
    echo.
)

pause
