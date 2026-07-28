@echo off
color 0C
title JG MART — End of Day

cls
echo.
echo  ╔════════════════════════════════════════════════════╗
echo  ║                                                    ║
echo  ║     ███████╗███╗   ██╗██████╗      ██████╗ ███████╗
echo  ║     ██╔════╝████╗  ██║██╔══██╗    ██╔══██╗██╔════╝
echo  ║     █████╗  ██╔██╗ ██║██║  ██║    ██║  ██║█████╗
echo  ║     ██╔══╝  ██║╚██╗██║██║  ██║    ██║  ██║██╔══╝
echo  ║     ███████╗██║ ╚████║██████╔╝    ██████╔╝███████╗
echo  ║     ╚══════╝╚═╝  ╚═══╝╚═════╝     ╚═════╝ ╚══════╝
echo  ║                                                    ║
echo  ║          ██████╗  █████╗ ██╗   ██╗                ║
echo  ║          ██╔══██╗██╔══██╗╚██╗ ██╔╝                ║
echo  ║          ██║  ██║███████║ ╚████╔╝                 ║
echo  ║          ██║  ██║██╔══██║  ╚██╔╝                  ║
echo  ║          ██████╔╝██║  ██║   ██║                   ║
echo  ║          ╚═════╝ ╚═╝  ╚═╝   ╚═╝                   ║
echo  ║                                                    ║
echo  ║          —— END OF DAY ROUTINE ——                   ║
echo  ║                                                    ║
echo  ╚════════════════════════════════════════════════════╝
echo.
echo                        %date%
echo.
echo  ════════════════════════════════════════════════════════
echo.
echo  Step 1: Open os.html and go to the Day End tab to
echo          prepare your export.
echo.
pause
start "" "os.html"
echo.
echo  ════════════════════════════════════════════════════════
echo.
echo  Step 2: Open data.html and click the Export button
echo          to save your customer / sales data.
echo.
pause
start "" "data.html"
echo.
echo  ════════════════════════════════════════════════════════
echo.
echo  Step 3: Data Export Confirmation
echo.

:ask_export
set /p exported="  Did you export your data? (Y/N): "

if /i "%exported%"=="Y" goto exported_yes
if /i "%exported%"=="N" goto exported_no
goto ask_export

:exported_yes
echo.
echo  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
echo   ✅  Great! Remember to save the JSON file somewhere
echo       safe — a backup folder or cloud drive.
echo  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
goto backup_step

:exported_no
echo.
echo  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
echo   ⚠️   Please export before closing! Your data is only
echo       stored in your browser's local storage. If you
echo       clear your cache, it will be lost forever.
echo  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
echo.
goto ask_export

:backup_step
echo.
echo  ════════════════════════════════════════════════════════
echo.
echo  Step 4: Weekly Backup Reminder
echo.
echo     📅  Is it the end of the week?
echo.
echo     Remember to copy your exported JSON files to a
echo     USB drive or cloud storage for safekeeping.
echo.
echo     Don't keep all your data in one place!
echo.
echo  ════════════════════════════════════════════════════════
echo.
pause
echo.
echo  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
echo.
echo      🌙  Thank you for your hard work today!
echo
echo          "Small daily improvements over time lead
echo           to stunning results."
echo
echo                     — Goodnight, JG Mart! —
echo.
echo  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
echo.
timeout /t 5 >nul
color 07
