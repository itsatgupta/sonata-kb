@echo off
cd /d "%~dp0"
venv\Scripts\python.exe -c "from orchestrator import ask; print(ask('What is the default page size for searchEmployer?')[0][:200])"
pause
