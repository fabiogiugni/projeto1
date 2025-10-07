#!/usr/bin/env bash

# ativa_venv.sh
# Script para detectar Python e criar ambiente virtual no Linux

is_not_sourced() {
    [[ "${BASH_SOURCE[0]}" == "${0}" ]]
}

if is_not_sourced; then
    echo "Execute: source $(basename "$0")
    "
    exit -1
fi

# Faz o script parar em caso de erro
set -e

# Nome da venv
VENV_DIR=".venv"

# Verifica se o Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Erro: Python3 não está instalado. Instale-o antes de continuar."
    exit 1
fi

# Cria a venv, se não existir
if [ ! -d "$VENV_DIR" ]; then
    echo "📦 Criando ambiente virtual em '$VENV_DIR'..."
    python3 -m venv "$VENV_DIR"
else
    echo "✅ Ambiente virtual já existe em '$VENV_DIR'."
fi

# Ativa a venv
echo "⚙️ Ativando ambiente virtual..."
# Detecta o shell e ativa corretamente
if [ -n "$ZSH_VERSION" ]; then
    source "$VENV_DIR/bin/activate"
elif [ -n "$BASH_VERSION" ]; then
    source "$VENV_DIR/bin/activate"
    echo "source $VENV_DIR/bin/activate"
else
    echo "⚠️ Shell não reconhecido. Ative manualmente com:"
    echo "source $VENV_DIR/bin/activate"
    exit 1
fi

# Verifica se o arquivo requirements.txt existe
if [ ! -f "requirements.txt" ]; then
    echo "⚠️ Nenhum arquivo requirements.txt encontrado. Pulando instalação de dependências."
else
    echo "📥 Instalando dependências do requirements.txt..."
    pip install --upgrade pip
    pip install -r requirements.txt
fi

echo "✅ Ambiente configurado com sucesso!"
