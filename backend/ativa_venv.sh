#!/bin/bash

# Script para configurar ambiente Python automaticamente
# Deve ser executado com: source setup_python_env.sh

echo "=== Configuração do Ambiente Python ==="

# Função para verificar a versão do Python
check_python_version() {
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
        echo "✓ Python encontrado: versão $PYTHON_VERSION"
        return 0
    elif command -v python &> /dev/null; then
        PYTHON_VERSION=$(python --version 2>&1 | awk '{print $2}')
        # Verifica se é Python 3
        if [[ $PYTHON_VERSION == Python\ 3.* ]]; then
            echo "✓ Python encontrado: versão $PYTHON_VERSION"
            return 0
        else
            echo "✗ Python 2 encontrado. É necessário Python 3."
            return 1
        fi
    else
        echo "✗ Python não encontrado no sistema."
        return 1
    fi
}

# Função para criar e ativar a venv
setup_venv() {
    local python_cmd=$1
    
    echo ""
    echo "--- Criando ambiente virtual ---"
    
    if [ ! -d "venv" ]; then
        echo "Criando venv..."
        $python_cmd -m venv venv
        if [ $? -ne 0 ]; then
            echo "✗ Erro ao criar venv. Verifique se o módulo venv está disponível."
            return 1
        fi
        echo "✓ Venv criada com sucesso"
    else
        echo "✓ Venv já existe"
    fi
    
    echo ""
    echo "--- Ativando venv ---"
    source venv/bin/activate
    
    if [ $? -eq 0 ]; then
        echo "✓ Venv ativada com sucesso"
        # Mostra o Python atual após ativação
        CURRENT_PYTHON=$(which python)
        echo "Python atual: $CURRENT_PYTHON"
        return 0
    else
        echo "✗ Erro ao ativar venv"
        return 1
    fi
}

# Função para instalar requirements
install_requirements() {
    echo ""
    echo "--- Instalando dependências ---"
    
    if [ -f "requirements.txt" ]; then
        echo "Encontrado requirements.txt"
        pip install -r requirements.txt
        
        if [ $? -eq 0 ]; then
            echo "✓ Dependências instaladas com sucesso"
            return 0
        else
            echo "✗ Erro ao instalar dependências"
            return 1
        fi
    else
        echo "⚠ requirements.txt não encontrado. Pulando instalação de dependências."
        return 0
    fi
}

# Função para mostrar instruções de instalação
show_installation_instructions() {
    echo ""
    echo "--- Instalação do Python ---"
    echo "Python não está instalado no sistema. Por favor, instale:"
    echo ""
    echo "Para Ubuntu/Debian:"
    echo "  sudo apt update && sudo apt install python3 python3-venv python3-pip"
    echo ""
    echo "Para CentOS/RHEL/Fedora:"
    echo "  sudo dnf install python3 python3-pip  # Fedora"
    echo "  sudo yum install python3 python3-pip  # CentOS/RHEL"
    echo ""
    echo "Para Arch Linux:"
    echo "  sudo pacman -S python python-pip"
    echo ""
    echo "Para macOS (com Homebrew):"
    echo "  brew install python"
    echo ""
    echo "Após a instalação, execute este script novamente."
}

# Função principal
main() {
    # Verifica se o Python está instalado
    if check_python_version; then
        # Determina o comando Python correto
        if command -v python3 &> /dev/null; then
            PYTHON_CMD="python3"
        else
            PYTHON_CMD="python"
        fi
        
        # Configura a venv
        if setup_venv "$PYTHON_CMD"; then
            # Instala requirements
            install_requirements
            
            echo ""
            echo "=== Configuração concluída! ==="
            echo "Ambiente virtual ativado. Para desativar, execute: deactivate"
            echo "Para reativar posteriormente, execute: source venv/bin/activate"
        fi
    else
        show_installation_instructions
        # Retorna código de erro para indicar falha
        return 1
    fi
}

# Executa a função principal
main
