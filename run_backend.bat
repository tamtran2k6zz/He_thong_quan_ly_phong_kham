@echo off
chcp 65001 >nul
title Clinic Management System - Backend Server (FastAPI)
echo =========================================================================
echo [CMS] Starting Clinic Management System Backend (FastAPI + AI Engine)...
echo =========================================================================

cd /d "%~dp0"

REM Check if Python is installed
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python is not found in PATH! Please install Python 3.10+ and add to PATH.
    pause
    exit /b 1
)

REM Setup Python Virtual Environment if not exists
if not exist ".venv" (
    echo [INFO] Creating Python virtual environment in .venv...
    python -m venv .venv
)

echo [INFO] Activating virtual environment...
call .venv\Scripts\activate.bat

REM Check and install backend dependencies
echo [INFO] Installing / verifying backend dependencies...
pip install -r backend\requirements.txt --quiet

REM Initialize and seed database if not already seeded
echo [INFO] Checking and initializing database schema and seed data...
python -c "from backend.app.seed.seed_data import seed_database; seed_database()"

REM Launch FastAPI Server with Uvicorn
echo =========================================================================
echo [READY] Backend REST API is running at: http://localhost:8000
echo [READY] Interactive Swagger Docs at:   http://localhost:8000/docs
echo [READY] Alternative ReDoc at:          http://localhost:8000/redoc
echo =========================================================================
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
pause
