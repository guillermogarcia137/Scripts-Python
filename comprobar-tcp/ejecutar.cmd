@echo off
setlocal
where py >nul 2>&1
if errorlevel 1 (
    python "%~dp0script.py" %*
) else (
    py -3 "%~dp0script.py" %*
)
exit /b %errorlevel%
