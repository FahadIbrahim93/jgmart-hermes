@echo off
color 0A
title JG MART — Daily Start

:menu
cls

echo.
echo  ╔════════════════════════════════════════════════════╗
echo  ║                                                    ║
echo  ║     ██╗ ██████╗     ███╗   ███╗ █████╗ ██████╗ ████████╗
echo  ║     ██║██╔════╝     ████╗ ████║██╔══██╗██╔══██╗╚══██╔══╝
echo  ║     ██║██║  ███╗    ██╔████╔██║███████║██████╔╝   ██║
echo  ║     ██║██║   ██║    ██║╚██╔╝██║██╔══██║██╔══██╗   ██║
echo  ║     ██║╚██████╔╝    ██║ ╚═╝ ██║██║  ██║██║  ██║   ██║
echo  ║     ╚═╝ ╚═════╝     ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝
echo  ║                                                    ║
echo  ║            ██████╗  ██████╗  ██████╗ ██████╗       ║
echo  ║            ██╔══██╗██╔═══██╗██╔═══██╗██╔══██╗      ║
echo  ║            ██║  ██║██║   ██║██║   ██║██████╔╝      ║
echo  ║            ██║  ██║██║   ██║██║   ██║██╔══██╗      ║
echo  ║            ██████╔╝╚██████╔╝╚██████╔╝██║  ██║      ║
echo  ║            ╚═════╝  ╚═════╝  ╚═════╝ ╚═╝  ╚═╝      ║
echo  ║                                                    ║
echo  ║              ——— GOOD MORNING! ———                  ║
echo  ║                                                    ║
echo  ╚════════════════════════════════════════════════════╝
echo.
echo                         %date%
echo.
echo  ════════════════════════════════════════════════════════
echo.
echo     [1]  Open os.html ............ daily driver (recommended)
echo     [2]  Open field_ops.html ..... phone view for Krishi Market
echo     [3]  Open ops.html .......... operations dashboard
echo     [4]  Open data.html ......... data manager / add customers
echo     [5]  Open start.html ........ first-time setup wizard
echo     [6]  Open ALL of the above
echo     [7]  Exit
echo.
echo  ════════════════════════════════════════════════════════
echo.
set /p choice="  Enter your choice [1-7]: "

if "%choice%"=="1" goto opt1
if "%choice%"=="2" goto opt2
if "%choice%"=="3" goto opt3
if "%choice%"=="4" goto opt4
if "%choice%"=="5" goto opt5
if "%choice%"=="6" goto opt6
if "%choice%"=="7" goto end
goto menu

:opt1
start "" "os.html"
goto menu

:opt2
start "" "field_ops.html"
goto menu

:opt3
start "" "ops.html"
goto menu

:opt4
start "" "data.html"
goto menu

:opt5
start "" "start.html"
goto menu

:opt6
start "" "os.html"
start "" "field_ops.html"
start "" "ops.html"
start "" "data.html"
start "" "start.html"
echo.
echo  ✅ All pages opened. Happy selling!
timeout /t 2 >nul
goto menu

:end
color 07
cls
echo.
echo  ╔════════════════════════════════════════════════════╗
echo  ║                                                    ║
echo  ║     Have a great day at JG Mart! 🚀                ║
echo  ║                                                    ║
echo  ╚════════════════════════════════════════════════════╝
echo.
timeout /t 2 >nul
