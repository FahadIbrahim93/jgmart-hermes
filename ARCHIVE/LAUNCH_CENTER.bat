@echo off
title JG Mart — Hermes Edition
color 0A

echo.
echo  ╔══════════════════════════════════════════════════════════════╗
echo  ║              JG MART — LAUNCH CENTER                        ║
echo  ║         Japan Garden City Hyperlocal Grocery                ║
echo  ║                                                            ║
echo  ║     ⭐ NEW: RUN_ALL.bat — full essential apps launcher      ║
echo  ╚══════════════════════════════════════════════════════════════╝
echo.

:menu
echo  What would you like to open?
echo.
echo  0)  RUN_ALL.bat ......... (NEW primary launcher — all essential apps)
echo.
echo  1)  KPI Dashboard        (05_Tech_Dashboard/index.html)
echo  2)  Customer Catalog     (06_Web_Catalog/index.html)
echo  3)  Order Intake Form    (06_Web_Catalog/order_intake.html)
echo  4)  Quick Start Guide    (QUICK_START.txt)
echo  5)  Command Center       (COMMAND_CENTER.txt)
echo  6)  Investor One-Pager   (01_Investor_Deck/INVESTOR_1PAGER.txt)
echo  7)  Financial Model      (08_Financials/)
echo  8)  Open All Apps        (Dashboard + Catalog + Order Intake)
echo  9)  Exit
echo.
set /p choice=Enter number (0-9):

if "%choice%"=="1" start "" "%~dp005_Tech_Dashboard\index.html"
if "%choice%"=="2" start "" "%~dp006_Web_Catalog\index.html"
if "%choice%"=="3" start "" "%~dp006_Web_Catalog\order_intake.html"
if "%choice%"=="4" notepad "%~dp0QUICK_START.txt"
if "%choice%"=="5" notepad "%~dp0COMMAND_CENTER.txt"
if "%choice%"=="6" notepad "%~dp001_Investor_Deck\INVESTOR_1PAGER.txt"
if "%choice%"=="7" explorer "%~dp008_Financials"
if "%choice%"=="8" (
    start "" "%~dp005_Tech_Dashboard\index.html"
    start "" "%~dp006_Web_Catalog\index.html"
    start "" "%~dp006_Web_Catalog\order_intake.html"
    notepad "%~dp0QUICK_START.txt"
)
if "%choice%"=="9" exit /b
if "%choice%"=="0" (
    start "" "%~dp0RUN_ALL.bat"
    exit /b
)

if not "%choice%"=="" (
    echo.
    echo  Done! Window should be open.
    timeout /t 2 >nul
    cls
    goto menu
) else (
    goto menu
)
