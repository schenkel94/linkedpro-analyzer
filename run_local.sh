#!/bin/bash

# Script para rodar o LinkedPro Analyzer localmente

echo "🚀 LinkedPro Analyzer - Teste Local"
echo "===================================="
echo ""

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado. Por favor, instale Python 3.8+"
    exit 1
fi

echo "✅ Python encontrado: $(python3 --version)"
echo ""

# Criar virtual environment se não existir
if [ ! -d "venv" ]; then
    echo "📦 Criando ambiente virtual..."
    python3 -m venv venv
    echo "✅ Ambiente virtual criado!"
else
    echo "✅ Ambiente virtual já existe"
fi

# Ativar virtual environment
echo "🔧 Ativando ambiente virtual..."
source venv/bin/activate

# Instalar dependências
echo "📥 Instalando dependências..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

echo "✅ Dependências instaladas!"
echo ""

# Verificar se existe secrets.toml
if [ ! -f ".streamlit/secrets.toml" ]; then
    echo "⚠️  Arquivo .streamlit/secrets.toml não encontrado"
    echo "   O app vai funcionar, mas não vai salvar leads no Google Sheets"
    echo "   Para configurar, copie secrets.toml.example para .streamlit/secrets.toml"
    echo ""
fi

echo "🎯 Iniciando aplicação..."
echo "📱 Acesse: http://localhost:8501"
echo ""
echo "Pressione Ctrl+C para parar"
echo ""

# Rodar Streamlit
streamlit run app.py
