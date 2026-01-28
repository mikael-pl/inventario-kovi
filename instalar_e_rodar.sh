#!/bin/bash
# Script para instalar dependencias e rodar o app
# Resolve problemas de compatibilidade com Python 3.13

echo "════════════════════════════════════════════════"
echo "  App de Inventario - Kovi"
echo "════════════════════════════════════════════════"
echo ""

# Navega para o diretorio do projeto
cd "$(dirname "$0")" || exit 1

echo "📂 Diretorio: $(pwd)"
echo ""

# Verifica a versao do Python
PYTHON_VERSION=$(python3 --version 2>&1 | grep -oE '[0-9]+\.[0-9]+')
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

echo "🐍 Python detectado: $PYTHON_VERSION"
echo ""

# Python 3.13 tem problemas com Kivy
if [ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -ge 13 ]; then
    echo "⚠️  Aviso: Python 3.13+ tem problemas de compatibilidade com Kivy!"
    echo ""
    echo "Solucoes:"
    echo ""
    echo "1. Instalar Python 3.12 com Homebrew (RECOMENDADO):"
    echo "   brew install python@3.12"
    echo "   /opt/homebrew/bin/python3.12 -m pip install kivy kivymd requests pillow"
    echo "   /opt/homebrew/bin/python3.12 test_app.py"
    echo ""
    echo "2. Usar versao de desenvolvimento do Kivy:"
    echo "   pip3 install --pre kivy[base] kivymd requests pillow"
    echo "   python3 test_app.py"
    echo ""
    echo "3. Tentar instalar mesmo assim (pode dar erro):"
    read -p "   Tentar instalar mesmo assim? (s/n): " resposta
    
    if [ "$resposta" != "s" ] && [ "$resposta" != "S" ]; then
        echo ""
        echo "❌ Instalacao cancelada."
        echo ""
        echo "Execute um dos comandos acima manualmente."
        exit 1
    fi
    
    echo ""
    echo "Tentando instalar versao de desenvolvimento do Kivy..."
    pip3 install --upgrade pip setuptools wheel
    pip3 install --pre kivy[base] kivymd requests pillow
else
    echo "✅ Versao do Python compativel!"
    echo ""
    echo "📦 Instalando dependencias..."
    pip3 install --upgrade pip
    pip3 install kivy kivymd requests pillow
fi

echo ""
echo "════════════════════════════════════════════════"
echo "🚀 Iniciando aplicativo..."
echo "════════════════════════════════════════════════"
echo ""

python3 test_app.py
