#!/bin/bash
# Script de setup - Instala dependências e prepara ambiente

echo "=========================================="
echo "Setup - Inventário Kovi"
echo "=========================================="
echo ""

# Detecta o sistema operacional
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="mac"
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    OS="windows"
else
    OS="unknown"
fi

echo "Sistema detectado: $OS"
echo ""

# Verifica Python
echo "Verificando Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado!"
    echo "   Por favor, instale Python 3.8 ou superior"
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
echo "✅ $PYTHON_VERSION encontrado"
echo ""

# Cria ambiente virtual
echo "Criando ambiente virtual..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Ambiente virtual criado"
else
    echo "✅ Ambiente virtual já existe"
fi
echo ""

# Ativa ambiente virtual
echo "Ativando ambiente virtual..."
if [[ "$OS" == "windows" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi
echo "✅ Ambiente virtual ativado"
echo ""

# Atualiza pip
echo "Atualizando pip..."
pip install --upgrade pip
echo ""

# Instala dependências
echo "Instalando dependências Python..."
pip install -r requirements.txt
echo "✅ Dependências instaladas"
echo ""

# Instala Buildozer (opcional)
echo "Deseja instalar Buildozer para gerar APK? (s/n)"
read -r install_buildozer

if [[ "$install_buildozer" == "s" || "$install_buildozer" == "S" ]]; then
    echo "Instalando Buildozer..."
    pip install buildozer cython==0.29.33
    
    if [[ "$OS" == "linux" ]]; then
        echo ""
        echo "Instalando dependências do sistema (requer sudo)..."
        sudo apt-get update
        sudo apt-get install -y \
            python3-pip build-essential git zip unzip \
            openjdk-11-jdk wget libssl-dev autoconf libtool \
            ccache libncurses5:i386 libstdc++6:i386 \
            zlib1g-dev libltdl-dev libffi-dev
    fi
    
    echo "✅ Buildozer instalado"
fi

echo ""
echo "=========================================="
echo "Setup completo!"
echo "=========================================="
echo ""
echo "Para testar o app:"
echo "  1. Ative o ambiente: source venv/bin/activate"
echo "  2. Execute: python test_app.py"
echo ""
echo "Para gerar APK:"
echo "  1. Veja: COMO_GERAR_APK.md"
echo "  2. Ou execute: buildozer android debug"
echo ""
