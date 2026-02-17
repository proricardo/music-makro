@echo off
title Music-Makro - Instalador
echo ================================================
echo   Music-Makro - Instalador
echo ================================================
echo.

cd /d "%~dp0\.."

echo [1/5] Criando ambiente virtual...
python -m venv venv
call venv\Scripts\activate

echo.
echo [2/5] Instalando dependências Python...
pip install -r requirements.txt

echo.
echo [3/5] Verificando FFmpeg...
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
echo [4/5] Gerando SECRET_KEY...
python -c "import secrets; print('SECRET_KEY=' + secrets.token_urlsafe(32))" > temp_key.txt
type temp_key.txt
echo.
echo Copie a SECRET_KEY acima e adicione no arquivo .env
del temp_key.txt

echo.
echo [5/5] Gerando hash de senha exemplo...
python -c "from passlib.context import CryptContext; print('Hash da senha \"admin123\":', CryptContext(schemes=['bcrypt']).hash('admin123'))"

echo.
echo ================================================
echo   Instalacao concluida!
echo ================================================
echo.
echo Proximos passos:
echo 1. Edite o arquivo .env com suas configuracoes
echo 2. Execute: scripts\start_gui.bat (Interface Grafica)
echo 3. Execute: scripts\start_api.bat (API REST)
echo.
pause