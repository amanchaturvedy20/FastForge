# Set console encoding to UTF-8
[Console]::InputEncoding = [System.Text.Encoding]::UTF8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# Ensure we are in the script's directory
Set-Location -Path $PSScriptRoot

Write-Host "Starting FastForge Project Locally..." -ForegroundColor Green

# 1. Start the Backend API (FastAPI) on port 8000
Write-Host "Starting Backend FastAPI server..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location -Path '$PSScriptRoot\backend'; py -m uvicorn app.main:app --host 127.0.0.1 --port 8000"

# 2. Start the Frontend Web Server on port 5500
Write-Host "Starting Frontend HTTP server..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location -Path '$PSScriptRoot\frontend'; py -m http.server 5500"

# 3. Open the Frontend website in Google Chrome (fallback to default browser if Chrome is not found)
Start-Sleep -Seconds 2
Write-Host "Opening website in Google Chrome..." -ForegroundColor Green
try {
    Start-Process "chrome.exe" -ArgumentList "http://127.0.0.1:5500" -ErrorAction Stop
} catch {
    Start-Process "http://127.0.0.1:5500"
}
