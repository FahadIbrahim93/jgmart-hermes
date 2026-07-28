@echo off
title JG MART — RUN_ALL Launch Center
color 0A
setlocal enabledelayedexpansion

:menu
cls

echo.
echo  ╔══════════════════════════════════════════════════════════════╗
echo  ║              JG MART — LAUNCH CENTER                        ║
echo  ║         Japan Garden City Hyperlocal Grocery                ║
echo  ║                      %date%  %time:~0,5%                              ║
echo  ╚══════════════════════════════════════════════════════════════╝
echo.
echo  ╔══════════════════════════════════════════════════════════════╗
echo  ║                    ESSENTIAL APPS                            ║
echo  ╠══════════════════════════════════════════════════════════════╣
echo  ║  1)  Open ALL Essential Apps                                ║
echo  ║      (os.html + data.html + field_ops.html + backup.html)    ║
echo  ║                                                            ║
echo  ║  2)  Open os.html Only (daily driver)                       ║
echo  ║                                                            ║
echo  ║  3)  Open os.html + data.html + backup.html                 ║
echo  ║                                                            ║
echo  ║  4)  Open DAILY_START.bat (interactive menu)                ║
echo  ║                                                            ║
echo  ║  5)  Open DEPLOYMENT_GUIDE.txt                               ║
echo  ║                                                            ║
echo  ║  6)  Exit                                                    ║
echo  ╚══════════════════════════════════════════════════════════════╝
echo.

rem Option 1: auto-start after 10 seconds
set /p choice="  Enter your choice [1-6] (1 auto-starts in 10s): "
if "%choice%"=="" set "choice=1"

if "%choice%"=="1" goto opt1
if "%choice%"=="2" goto opt2
if "%choice%"=="3" goto opt3
if "%choice%"=="4" goto opt4
if "%choice%"=="5" goto opt5
if "%choice%"=="6" goto end
goto menu

:opt1
cls
echo.
echo  ╔══════════════════════════════════════════════════════════════╗
echo  ║              LAUNCHING ALL ESSENTIAL APPS                    ║
echo  ╚══════════════════════════════════════════════════════════════╝
echo.
echo  Opening: os.html, data.html, field_ops.html, backup.html
echo.
echo  Press any key to start... (auto-launch in 10 seconds)
timeout /t 10 >nul
cls
echo.
echo  ╔══════════════════════════════════════════════════════════════╗
echo  ║                    OPENING APPS...                           ║
echo  ╚══════════════════════════════════════════════════════════════╝
echo.
start "" "%~dp0os.html"
start "" "%~dp0data.html"
start "" "%~dp0field_ops.html"
start "" "%~dp0backup.html"
echo  ✅ All essential apps opened successfully!
timeout /t 3 >nul
goto menu

:opt2
cls
echo.
echo  ╔══════════════════════════════════════════════════════════════╗
echo  ║              OPENING OS.HTML (Daily Driver)                  ║
echo  ╚══════════════════════════════════════════════════════════════╝
echo.
start "" "%~dp0os.html"
echo  ✅ os.html opened!
timeout /t 2 >nul
goto menu

:opt3
cls
echo.
echo  ╔══════════════════════════════════════════════════════════════╗
echo  ║         OPENING OS.HTML + DATA.HTML + BACKUP.HTML           ║
echo  ╚══════════════════════════════════════════════════════════════╝
echo.
start "" "%~dp0os.html"
start "" "%~dp0data.html"
start "" "%~dp0backup.html"
echo  ✅ Apps opened!
timeout /t 2 >nul
goto menu

:opt4
start "" "%~dp0DAILY_START.bat"
goto menu

:opt5
cls
echo.
echo  ╔══════════════════════════════════════════════════════════════╗
echo  ║              OPENING DEPLOYMENT GUIDE                        ║
echo  ╚══════════════════════════════════════════════════════════════╝
echo.
notepad "%~dp0DEPLOYMENT_GUIDE.txt"
echo  ✅ Deployment guide opened!
timeout /t 2 >nul
goto menu

:end
color 07
cls
echo.
echo  ╔══════════════════════════════════════════════════════════════╗
echo  ║                                                            ║
echo  ║     Thank you for using JG Mart — have a great day! 🚀     ║
echo  ║                                                            ║
echo  ╚══════════════════════════════════════════════════════════════╝
echo.
timeout /t 2 >nul
exit /b
