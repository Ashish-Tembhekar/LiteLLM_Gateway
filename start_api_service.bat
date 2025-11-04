@echo off
echo ============================================================
echo Starting LiteLLM API Service on Port 5000
echo ============================================================
cd litellm_service
..\.venv\Scripts\python.exe api_service.py
pause

