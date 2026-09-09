@echo off
title Installing Dependencies...
color 0A
cls

echo.
echo ========================================
echo   Installing Discord Username Checker
echo   Dependencies
echo ========================================
echo.

pip install -r requirements.txt

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo   Installation Complete!
    echo ========================================
    echo.
    echo You can now run: run.bat
    echo.
) else (
    echo.
    echo ========================================
    echo   Installation Failed!
    echo ========================================
    echo.
    echo Make sure Python and pip are installed
    echo and added to your PATH.
    echo.
)

pause
