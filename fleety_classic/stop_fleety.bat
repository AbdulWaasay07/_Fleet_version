@echo off
echo Stopping Fleety AI System...
echo ==========================================

:: Kill by window titles used in start_fleety.bat
taskkill /FI "WINDOWTITLE eq Fleety Backend*" /F /T
taskkill /FI "WINDOWTITLE eq Fleety Frontend*" /F /T

:: Backup: kill processes directly if they are still running
taskkill /IM uvicorn.exe /F 2>nul
taskkill /IM node.exe /F 2>nul

echo ==========================================
echo All Fleety processes have been stopped.
echo ==========================================
pause
