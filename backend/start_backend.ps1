# Mirai Backend Startup Script
# This script starts the FastAPI backend server

Write-Host "🚀 Starting Mirai Backend Server..." -ForegroundColor Cyan
Write-Host ""

# Find Python installation
$pythonPaths = @(
    "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe",
    "$env:LOCALAPPDATA\Programs\Python\Python311\python.exe",
    "$env:LOCALAPPDATA\Programs\Python\Python310\python.exe",
    "C:\Python312\python.exe",
    "C:\Python311\python.exe",
    "C:\Python310\python.exe"
)

$pythonExe = $null
foreach ($path in $pythonPaths) {
    if (Test-Path $path) {
        $pythonExe = $path
        Write-Host "✅ Found Python at: $pythonExe" -ForegroundColor Green
        break
    }
}

# Try python command in PATH
if (-not $pythonExe) {
    try {
        $null = python --version 2>&1
        $pythonExe = "python"
        Write-Host "✅ Using Python from PATH" -ForegroundColor Green
    } catch {
        Write-Host "❌ Python not found!" -ForegroundColor Red
        Write-Host ""
        Write-Host "Please install Python from: https://www.python.org/downloads/" -ForegroundColor Yellow
        Write-Host "During installation, make sure to check 'Add Python to PATH'" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "After installing, restart PowerShell and run this script again." -ForegroundColor Yellow
        Write-Host ""
        pause
        exit 1
    }
}

# Check if in correct directory
if (-not (Test-Path "app\main.py")) {
    Write-Host "❌ Error: app\main.py not found!" -ForegroundColor Red
    Write-Host "Make sure you're running this script from the backend directory" -ForegroundColor Yellow
    Write-Host ""
    pause
    exit 1
}

# Check if .env exists
if (-not (Test-Path ".env")) {
    Write-Host "⚠️  Warning: .env file not found!" -ForegroundColor Yellow
    Write-Host "Creating default .env file..." -ForegroundColor Yellow
    Write-Host ""
    
    # The .env file should already exist, but just in case
    Write-Host "❌ Please configure your .env file with proper API keys!" -ForegroundColor Red
    Write-Host ""
}

Write-Host ""
Write-Host "🔧 Starting FastAPI server..." -ForegroundColor Cyan
Write-Host "Backend will be available at: http://localhost:8000" -ForegroundColor Green
Write-Host "API Documentation: http://localhost:8000/docs" -ForegroundColor Green
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""
Write-Host "----------------------------------------" -ForegroundColor Gray
Write-Host ""

# Start the server
try {
    & $pythonExe -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
} catch {
    Write-Host ""
    Write-Host "❌ Error starting server: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "Common solutions:" -ForegroundColor Yellow
    Write-Host "1. Make sure all dependencies are installed:" -ForegroundColor White
    Write-Host "   python -m pip install -r requirements_jwt.txt" -ForegroundColor Gray
    Write-Host ""
    Write-Host "2. Check if port 8000 is already in use:" -ForegroundColor White
    Write-Host "   netstat -ano | findstr :8000" -ForegroundColor Gray
    Write-Host ""
    pause
    exit 1
}
