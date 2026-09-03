@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo ====================================
echo Monitor CTAN - latex-base-dev
echo ====================================
python monitor_ctan.py
if errorlevel 1 (
    echo [ERRO] Falha na execução.
    pause
    exit /b 1
)
echo.
echo [OK] Verificação concluida.
