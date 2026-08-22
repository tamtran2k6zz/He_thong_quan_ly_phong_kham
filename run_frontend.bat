@echo off
chcp 65001 >nul
title Clinic Management System - Frontend SPA (React + Vite)
echo =========================================================================
echo [CMS] Starting Clinic Management System Frontend (React + Vite + Tailwind)...
echo =========================================================================

cd /d "%~dp0frontend"

REM Check if Node.js is installed
node --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Node.js is not found in PATH! Please install Node.js 18+ and add to PATH.
    pause
    exit /b 1
)

REM Install dependencies if node_modules missing
if not exist "node_modules" (
    echo [INFO] Installing frontend dependencies with npm...
    call npm install
)

REM Launch Vite Development Server
echo =========================================================================
echo [READY] Frontend Web Application is starting at: http://localhost:5173
echo =========================================================================
call npm run dev -- --host 0.0.0.0 --port 5173
pause
