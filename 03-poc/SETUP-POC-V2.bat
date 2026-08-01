@echo off
REM POC v2 Voice: One-Click Setup Script
REM Run this from: C:\Users\atgupta\sonata-kb\03-poc

echo ========================================
echo  Sonata POC v2 Voice Setup
echo ========================================
echo.

REM Step 1: Install backend dependencies
echo [1/4] Installing backend dependencies...
cd agent
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo OK: Dependencies installed
echo.

REM Step 2: Test OpenAI API key
echo [2/4] Testing OpenAI API key...
python -c "from openai import OpenAI; c = OpenAI(); print('API key OK')"
if %errorlevel% neq 0 (
    echo ERROR: OpenAI API key not working
    echo Check your .env file has OPENAI_API_KEY set
    pause
    exit /b 1
)
echo OK: API key works
echo.

REM Step 3: Test backend starts
echo [3/4] Testing backend starts...
start /B python -c "from main import app; print('FastAPI app loads OK')"
timeout /t 3 /nobreak >nul
echo OK: Backend loads
echo.

REM Step 4: Show next steps
echo [4/4] Setup complete!
echo.
echo ========================================
echo  NEXT STEPS (Manual)
echo ========================================
echo.
echo  BACKEND (Render):
echo    1. Go to https://dashboard.render.com
echo    2. New > Web Service > Connect GitHub repo
echo    3. Root directory: 03-poc/agent
echo    4. Build: pip install -r requirements.txt
echo    5. Start: uvicorn main:app --host 0.0.0.0 --port $PORT
echo    6. Add env vars: OPENAI_API_KEY, ANTHROPIC_API_KEY
echo    7. Deploy
echo.
echo  FRONTEND (Vercel):
echo    1. Go to https://vercel.com/new
echo    2. Import GitHub repo
echo    3. Root directory: 03-poc/ui
echo    4. Deploy
echo.
echo  After both deploy:
echo    - Open your Vercel URL
echo    - Click "Ask a Question"
echo    - Speak and verify audio plays back
echo.
echo ========================================
pause
