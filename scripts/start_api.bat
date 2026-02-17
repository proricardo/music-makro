@echo off
title Music-Makro API
cd /d "%~dp0\.."
call venv\Scripts\activate
echo.
echo ================================================
echo   Music-Makro API Server
echo ================================================
echo.
echo Acesse: http://localhost:8000/docs
echo.
python -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
pause