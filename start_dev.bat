@echo off
REM Start both backend and frontend development servers

echo ========================================
echo Starting Mirai Development Servers
echo ========================================
echo.

REM Start Backend in new window
echo Starting Backend Server...
start "Mirai Backend" cmd /k "cd backend && venv\Scripts\activate && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

REM Wait a moment
timeout /t 3 /nobreak >nul

REM Start Frontend in new window
echo Starting Frontend Server...
start "Mirai Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo ========================================
echo Servers Starting!
echo ========================================
echo.
echo Backend:  http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo Frontend: http://localhost:5173
echo.
echo Press Ctrl+C in each window to stop the servers
echo.
