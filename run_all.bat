@echo off
chcp 65001 >nul
title Clinic Management System - Full Stack Launcher
echo =========================================================================
echo   HỆ THỐNG QUẢN LÝ PHÒNG KHÁM ĐA KHOA THÔNG MINH TÍCH HỢP AI HÀNH CHÍNH
echo =========================================================================
echo [INFO] Launching both Backend and Frontend in separate windows...
echo.

cd /d "%~dp0"

REM Launch Backend in a new command window
start "CMS Backend (FastAPI :8000)" cmd /k "call run_backend.bat"

REM Brief delay before launching frontend
timeout /t 3 /nobreak >nul

REM Launch Frontend in a new command window
start "CMS Frontend (React Vite :5173)" cmd /k "call run_frontend.bat"

echo =========================================================================
echo [SUCCESS] Both services have been launched!
echo.
echo   * Backend REST API:    http://localhost:8000
echo   * Swagger UI Docs:     http://localhost:8000/docs
echo   * Frontend Web SPA:    http://localhost:5173
echo.
echo -------------------------------------------------------------------------
echo DEFAULT LOGIN CREDENTIALS:
echo -------------------------------------------------------------------------
echo   1. Quản trị viên (Admin):    admin        / admin123
echo   2. Lễ tân (Receptionist):     receptionist / rec123
echo   3. Kế toán (Accountant):      accountant   / acc123
echo   4. Bác sĩ (Doctor):           dr_nam       / doc123
echo                                 dr_huong     / doc123
echo                                 dr_minh      / doc123
echo                                 dr_lan       / doc123
echo =========================================================================
echo Keep this window open or press any key to exit this launcher.
pause >nul
