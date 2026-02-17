@echo off
title Music-Makro - Instalador
echo ================================================
echo   Music-Makro - Instalador
echo ================================================
echo.

cd /d "%~dp0\.."

echo [1/3] Criando ambiente virtual...
python -m venv venv
call venv\Scripts\activate

echo.
echo [2/3] Instalando dependencias Python...
pip install -r requirements.txt

echo.
echo [3/3] Verificando FFmpeg...
ffmpeg -version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo [AVISO] FFmpeg nao encontrado!
    echo Instalando via winget...
    winget install --id=Gyan.FFmpeg -e
    echo.
    echo [IMPORTANTE] Feche e abra o terminal novamente apos a instalacao!
)

echo.
echo ================================================
echo   Instalacao concluida!
echo ================================================
echo.
echo Proximos passos:
echo 1. Execute: scripts\start_gui.bat (Interface Grafica)
echo.
pause
