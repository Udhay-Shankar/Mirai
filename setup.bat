@echo off
REM Mirai Setup Script for Windows
REM This script helps set up the Mirai project on Windows

echo ========================================
echo Mirai Setup Script
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.9+ from https://python.org
    pause
    exit /b 1
)

echo [OK] Python is installed

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js is not installed or not in PATH
    echo Please install Node.js 16+ from https://nodejs.org
    pause
    exit /b 1
)

echo [OK] Node.js is installed
echo.

REM Setup Backend
echo ========================================
echo Setting up Backend...
echo ========================================
cd backend

REM Create virtual environment
if not exist "venv" (
    echo Creating Python virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing Python dependencies...
pip install -r requirements.txt

REM Create .env if it doesn't exist
if not exist ".env" (
    echo Creating .env file from template...
    copy .env.example .env
    echo [ACTION REQUIRED] Please edit backend\.env with your credentials
)

REM Check for Firebase credentials
if not exist "firebase-credentials.json" (
    echo.
    echo [WARNING] Firebase credentials not found
    echo [ACTION REQUIRED] Please download firebase-credentials.json from Firebase Console
    echo and place it in the backend directory
)

echo.
echo Backend setup complete!
echo.

cd ..

REM Setup Frontend
echo ========================================
echo Setting up Frontend...
echo ========================================
cd frontend

REM Install dependencies
echo Installing Node dependencies...
call npm install

REM Create .env if it doesn't exist
if not exist ".env" (
    echo Creating .env file from template...
    copy .env.example .env
    echo [ACTION REQUIRED] Please edit frontend\.env with your Firebase config
)

echo.
echo Frontend setup complete!
echo.

cd ..

REM Summary
echo ========================================
echo Setup Summary
echo ========================================
echo.
echo [OK] Backend dependencies installed
echo [OK] Frontend dependencies installed
echo.
echo Next Steps:
echo 1. Configure backend\.env with your Awario API key and JWT secret
echo 2. Download Firebase credentials and place in backend directory
echo 3. Configure frontend\.env with your Firebase config
echo 4. Run: start_dev.bat (to start both servers)
echo.
echo For detailed instructions, see:
echo - README.md
echo - QUICKSTART.md
echo.
pause
