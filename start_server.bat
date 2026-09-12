@echo off
title HomeLab OS — Server Engine Launcher (v4.0)
echo ==========================================================
echo       🏠 HomeLab OS Server Engine (FastAPI Backend)       
echo ==========================================================
echo Starting HomeLab OS Server on http://localhost:8000 ...
echo Press Ctrl+C at any time to stop the server.
echo ==========================================================

cd /d "%~dp0"
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --app-dir backend
pause
