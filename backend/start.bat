@echo off
cd /d "%~dp0"
echo Starting Mirai Backend Server...
echo Backend will be available at: http://localhost:8000
echo API Documentation: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.
"%USERPROFILE%\AppData\Local\Programs\Python\Python312\python.exe" -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
