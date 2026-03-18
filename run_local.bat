@echo off
REM Script para rodar o LinkedPro Analyzer localmente no Windows

echo ========================================
echo   LinkedPro Analyzer - Teste Local
echo ========================================
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python nao encontrado. Instale Python 3.8+
    pause
    exit /b 1
)

echo [OK] Python encontrado
echo.

REM Criar virtual environment se não existir
if not exist "venv" (
    echo [INFO] Criando ambiente virtual...
    python -m venv venv
    echo [OK] Ambiente virtual criado!
) else (
    echo [OK] Ambiente virtual ja existe
)

REM Ativar virtual environment
echo [INFO] Ativando ambiente virtual...
call venv\Scripts\activate.bat

REM Instalar dependências
echo [INFO] Instalando dependencias...
python -m pip install --quiet --upgrade pip
python -m pip install --quiet -r requirements.txt

echo [OK] Dependencias instaladas!
echo.

REM Verificar secrets
if not exist ".streamlit\secrets.toml" (
    echo [AVISO] Arquivo .streamlit\secrets.toml nao encontrado
    echo         O app vai funcionar, mas nao vai salvar leads
    echo         Para configurar, copie secrets.toml.example
    echo.
)

echo [INFO] Iniciando aplicacao...
echo [INFO] Acesse: http://localhost:8501
echo.
echo Pressione Ctrl+C para parar
echo.

REM Rodar Streamlit
streamlit run app.py
