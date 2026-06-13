@echo off
setlocal

cd /d "%~dp0"

echo Arrancando Stock Intelligence App...
echo.
echo Carpeta: %CD%
echo URL local: http://127.0.0.1:8501
echo.

where py >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    set "PYTHON_CMD=py"
) else (
    set "PYTHON_CMD=python"
)

%PYTHON_CMD% -m streamlit run app.py --server.address=127.0.0.1 --server.port=8501 --server.fileWatcherType=none --browser.gatherUsageStats=false

echo.
echo Streamlit se ha cerrado. Pulsa una tecla para salir.
pause >nul
