@echo off
title ESP32 IoT Server
echo ================================================
echo   ESP32 IoT Server
echo ================================================
cd /d "%~dp0"

if exist "E:\pycharm\Miniconda3\python.exe" (
    echo Using E:\pycharm\Miniconda3\python.exe
    "E:\pycharm\Miniconda3\python.exe" start.py
    goto :end
)
if exist "E:\pycharm\python\python.exe" (
    echo Using E:\pycharm\python\python.exe
    "E:\pycharm\python\python.exe" start.py
    goto :end
)

py -3 start.py
if errorlevel 1 (
    echo Python launcher failed, trying python ...
    python start.py
    if errorlevel 1 (
        echo Python not found.
        echo This PC has a working Python at:
        echo   E:\pycharm\Miniconda3\python.exe
    )
)

:end
pause
