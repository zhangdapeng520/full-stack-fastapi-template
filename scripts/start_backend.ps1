# FastAPI Backend Server Startup Script
# Start a new PowerShell window and run backend service

# Set console encoding to UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host "========================================" -ForegroundColor Green
Write-Host "   FastAPI Backend Server Startup" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

# Get script directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir

# Change to project root directory
Set-Location $ProjectRoot

# Check if virtual environment exists
$VenvPath = Join-Path $ProjectRoot "backend\venv\Scripts\Activate.ps1"
if (-not (Test-Path $VenvPath)) {
    Write-Host "Error: Virtual environment not found!" -ForegroundColor Red
    Write-Host "Please ensure backend\venv directory exists and dependencies are installed" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if dependencies are installed
Write-Host "Checking dependencies..." -ForegroundColor Cyan
try {
    $null = python -c "import fastapi, uvicorn, sqlmodel" 2>$null
    Write-Host "Dependencies check passed" -ForegroundColor Green
} catch {
    Write-Host "Error: Dependencies not properly installed!" -ForegroundColor Red
    Write-Host "Please run: pip install -r requirements.txt" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "Check completed, starting backend service..." -ForegroundColor Green

# Build startup command
$StartCommand = @"
# Set console encoding
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# Change to project root directory
Set-Location '$ProjectRoot'

# Activate virtual environment
& '$VenvPath'

# Change to backend directory
Set-Location backend

# Display startup information
Write-Host '========================================' -ForegroundColor Green
Write-Host '   FastAPI Backend Server Starting...' -ForegroundColor Green
Write-Host '========================================' -ForegroundColor Green
Write-Host ''
Write-Host 'Service URL: http://localhost:8000' -ForegroundColor Cyan
Write-Host 'API Docs: http://localhost:8000/docs' -ForegroundColor Cyan
Write-Host ''
Write-Host 'Press Ctrl+C to stop service' -ForegroundColor Yellow
Write-Host ''

# Start uvicorn server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Keep window open
Write-Host ''
Write-Host 'Service stopped, press Enter to close window...' -ForegroundColor Yellow
Read-Host
"@

# Start new PowerShell window
Write-Host "Starting new terminal window..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", $StartCommand

Write-Host "Backend service started in new terminal window" -ForegroundColor Green
Write-Host "Service URL: http://localhost:8000" -ForegroundColor Cyan
Write-Host "API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Enter to close this window..." -ForegroundColor Yellow
Read-Host 