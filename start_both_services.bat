@echo off
echo ============================================================
echo Starting LiteLLM Microservices
echo ============================================================
echo.
echo Starting API Service on Port 5000...
start "LiteLLM API Service" cmd /k "cd litellm_service && ..\.venv\Scripts\python.exe api_service.py"
timeout /t 3 /nobreak >nul
echo.
echo Starting WebUI on Port 5500...
start "LiteLLM WebUI" cmd /k "cd webui && ..\.venv\Scripts\python.exe app.py"
timeout /t 2 /nobreak >nul
echo.
echo ============================================================
echo Both services are starting!
echo ============================================================
echo.
echo API Service:  http://localhost:5000
echo WebUI:        http://localhost:5500
echo.
echo Opening WebUI in browser...
timeout /t 3 /nobreak >nul
start http://localhost:5500
echo.
echo Press any key to close this window (services will keep running)
pause >nul

