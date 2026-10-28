@echo off
chcp 65001 >nul
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0installer\rollback.ps1" -Interactive
set "ACM_EXIT=%ERRORLEVEL%"
pause
exit /b %ACM_EXIT%
