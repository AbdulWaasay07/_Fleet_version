@echo off
echo Starting Fleety AI System...
echo ==========================================

:: Start Backend
echo Starting Backend Server...
start "Fleety Backend" cmd /k "cd backend && call venv\Scripts\activate && uvicorn app.main:app --reload"

:: Wait a moment for backend to initialize
timeout /t 2 /nobreak >nul

:: Start Frontend
echo Starting Frontend Dashboard...
start "Fleety Frontend" cmd /k "cd frontend && npm run dev"

echo ==========================================
echo System started successfully!
echo Backend API: http://localhost:8000/docs
echo Frontend UI: http://localhost:5173
echo ==========================================
pause
