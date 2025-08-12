@echo off
echo Starting Famoly Drive Servers...
echo.

echo [1/2] Starting Backend API Server (Port 8000)...
start cmd /k "cd backend && uvicorn simple_api:app --reload --port 8000"

timeout /t 3 /nobreak > nul

echo [2/2] Starting Frontend Server (Port 3000)...
start cmd /k "cd frontend && npm run dev"

echo.
echo ====================================
echo Servers are starting...
echo.
echo Backend API: http://localhost:8000
echo Frontend:    http://localhost:3000
echo.
echo Press any key to open the app in browser...
pause > nul

start http://localhost:3000

echo.
echo Servers are running!
echo Close this window to keep servers running.
pause