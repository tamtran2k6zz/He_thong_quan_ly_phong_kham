@echo off
chcp 65001 >nul
title Clinic Management System - Automated Test Suite Runner
echo =========================================================================
echo [CMS] Running Automated Pytest Test Suite (RBAC, Conflict, PII, AI, E2E)...
echo =========================================================================

cd /d "%~dp0"

REM Activate virtual environment if present
if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
)

REM Set PYTHONPATH
set PYTHONPATH=%cd%

REM Execute Pytest
echo [INFO] Executing Pytest on backend/tests...
python -m pytest backend/tests -v --tb=short

if %ERRORLEVEL% EQU 0 (
    echo.
    echo =========================================================================
    echo [TEST PASSED] All automated tests executed successfully!
    echo =========================================================================
) else (
    echo.
    echo =========================================================================
    echo [TEST FAILED] Some tests failed. Please review the output above.
    echo =========================================================================
)

pause
