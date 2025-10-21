#!/bin/bash

# ativa_venv.sh
# Script para detectar Python e criar ambiente virtual no Linux
# DEVE ser executado com: source ativa_venv.sh

print_colored() {
    local color_code=$1
    local message=$2
    echo -e "\033[${color_code}m${message}\033[0m"
}

print_header() {
    echo
    print_colored "36" "=== SCRIPT DE CONFIGURAÇÃO DE AMBIENTE VIRTUAL PYTHON ==="
    print_colored "37" "Este script irá configurar um ambiente virtual Python para seu projeto"
}

# Verifica se o script está sendo executado com source
check_source_execution() {
    if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
        print_colored "31" "ERRO: Este script deve ser executado com 'source'"
        print_colored "33" ""
        print_colored "33" "USO CORRETO:"
        print_colored "32" "  source ativa_venv.sh"
        print_colored "33" ""
        print_colored "33" "Ou:"
        print_colored "32" "  . ativa_venv.sh"
        print_colored "33" ""
        print_colored "33" "NÃO USE:"
        print_colored "31" "  ./ativa_venv.sh"
        print_colored "33" "  bash ativa_venv.sh"
        print_colored "33" ""
        print_colored "33" "Motivo: O ambiente virtual precisa ser ativado no shell atual"
        exit 1
    fi
}

# Função para verificar se uma instalação Python é válida
test_valid_python() {
    local python_path=$1
    
    if [ ! -f "$python_path" ]; then
        return 1
    fi
    
    # Verifica se o Python é executável e retorna versão
    local version_output
    version_output=$("$python_path" -c "import sys; print(sys.version)" 2>/dev/null)
    local exit_code=$?
    
    if [ $exit_code -eq 0 ] && [[ $version_output =~ ^[0-9]+\.[0-9]+\.[0-9]+ ]]; then
        return 0
    else
        return 1
    fi
}

# Função para encontrar uma instalação válida do Python
find_valid_python() {
    print_colored "33" "\nProcurando instalações do Python..."
    
    # Comandos Python comuns no Linux
    local python_commands=("python3" "python" "python3.11" "python3.10" "python3.9" "python3.8")
    
    # Verifica comandos disponíveis
    for cmd in "${python_commands[@]}"; do
        local full_path
        full_path=$(command -v "$cmd" 2>/dev/null)
        
        if [ -n "$full_path" ]; then
            echo -n "  Verificando: $full_path... "
            if test_valid_python "$full_path"; then
                print_colored "32" "[ENCONTRADO]"
                echo "$full_path"
                return 0
            else
                print_colored "90" "[não válido]"
            fi
        fi
    done
    
    # Verifica caminhos comuns no Linux
    local common_paths=(
        "/usr/bin/python3"
        "/usr/local/bin/python3"
        "/opt/python3/bin/python3"
        "/usr/bin/python"
        "/usr/local/bin/python"
    )
    
    for path in "${common_paths[@]}"; do
        if [ -f "$path" ]; then
            echo -n "  Verificando: $path... "
            if test_valid_python "$path"; then
                print_colored "32" "[ENCONTRADO]"
                echo "$path"
                return 0
            else
                print_colored "90" "[não válido]"
            fi
        fi
    done
    
    return 1
}

# --- INÍCIO DO SCRIPT ---

# Verifica se está sendo executado com source
check_source_execution

print_header

# Encontrar Python ou pedir caminho ao usuário
python_path=$(find_valid_python)

if [ -z "$python_path" ]; then
    print_colored "33" "\nNenhuma instalação válida do Python foi encontrada automaticamente."
    print_colored "36" "\nVocê tem duas opções:"
    print_colored "36" "1. Instalar Python usando o gerenciador de pacotes"
    print_colored "36" "2. Fornecer o caminho para uma instalação existente do Python"
    
    echo
    read -p "Escolha uma opção (1/2): " option
    
    if [ "$option" = "1" ]; then
        print_colored "32" "\nInstalando Python..."
        
        # Detecta o gerenciador de pacotes
        if command -v apt-get >/dev/null 2>&1; then
            # Debian/Ubuntu
            echo "Detectado apt (Debian/Ubuntu)"
            sudo apt-get update && sudo apt-get install -y python3 python3-pip python3-venv
        elif command -v yum >/dev/null 2>&1; then
            # RedHat/CentOS
            echo "Detectado yum (RedHat/CentOS)"
            sudo yum install -y python3 python3-pip
        elif command -v dnf >/dev/null 2>&1; then
            # Fedora
            echo "Detectado dnf (Fedora)"
            sudo dnf install -y python3 python3-pip
        elif command -v pacman >/dev/null 2>&1; then
            # Arch Linux
            echo "Detectado pacman (Arch Linux)"
            sudo pacman -Sy python python-pip
        else
            print_colored "31" "Não foi possível detectar o gerenciador de pacotes."
            print_colored "33" "Por favor, instale o Python manualmente e execute este script novamente."
            return 1  # Usa return em vez de exit quando executado com source
        fi
        
        # Tenta encontrar o Python novamente após instalação
        python_path=$(find_valid_python)
        if [ -z "$python_path" ]; then
            print_colored "31" "A instalação do Python pode ter falhado."
            return 1
        fi
        
    elif [ "$option" = "2" ]; then
        echo
        read -p "Digite o caminho completo para python (ex: /usr/bin/python3): " user_path
        
        echo "Verificando o caminho fornecido..."
        if test_valid_python "$user_path"; then
            python_path="$user_path"
            print_colored "32" "Caminho válido!"
        else
            print_colored "31" "O caminho fornecido não é uma instalação válida do Python."
            return 1
        fi
    else
        print_colored "31" "Opção inválida selecionada."
        return 1
    fi
fi

# Temos um caminho Python válido, prosseguir com a configuração
print_colored "32" "\n=== PYTHON ENCONTRADO ==="
print_colored "32" "Usando Python de: $python_path"
python_version=$("$python_path" --version)
print_colored "32" "Versão do Python: $python_version"

# Atualizar pip
print_colored "36" "\n=== ATUALIZANDO PIP ==="
print_colored "37" "Atualizando o gerenciador de pacotes pip..."
"$python_path" -m pip install --upgrade pip

# Criar novo ambiente virtual
print_colored "36" "\n=== CRIANDO AMBIENTE VIRTUAL ==="
if [ -d "venv" ]; then
    print_colored "33" "Removendo ambiente virtual existente..."
    rm -rf venv
    print_colored "37" "Ambiente anterior removido."
fi

# Criar ambiente virtual usando venv (módulo padrão do Python)
print_colored "36" "\nCriando ambiente virtual na pasta 'venv'..."
"$python_path" -m venv venv

if [ $? -ne 0 ]; then
    print_colored "31" "Falha ao criar ambiente virtual"
    return 1
fi

# Ativar o ambiente
print_colored "36" "\n=== ATIVANDO AMBIENTE VIRTUAL ==="
print_colored "37" "Ativando o ambiente virtual..."

# Ativa o ambiente virtual no shell atual
source venv/bin/activate

if [ $? -ne 0 ]; then
    print_colored "31" "Falha ao ativar ambiente virtual"
    return 1
fi

# Instalar requirements
if [ -f "requirements.txt" ]; then
    print_colored "36" "\n=== INSTALANDO DEPENDÊNCIAS ==="
    print_colored "32" "Arquivo requirements.txt encontrado!"
    print_colored "37" "Instalando pacotes listados no requirements.txt..."
    python -m pip install -r requirements.txt
    print_colored "32" "\nDependências instaladas com sucesso!"
else
    print_colored "33" "\nArquivo requirements.txt não encontrado."
    print_colored "37" "Pule esta etapa ou crie um arquivo requirements.txt com suas dependências."
fi

print_colored "32" "\n=== AMBIENTE VIRTUAL ATIVADO COM SUCESSO! ==="
print_colored "36" "\nINSTRUÇÕES DE USO:"
print_colored "37" "✓ O ambiente virtual está ATIVO agora (veja (venv) no prompt)"
print_colored "37" "✓ Para DESATIVAR: digite 'deactivate'"
print_colored "37" "✓ Para REATIVAR: source venv/bin/activate"
print_colored "37" "✓ Para instalar pacotes: pip install nome-do-pacote"
print_colored "37" "✓ Para salvar dependências: pip freeze > requirements.txt"
print_colored "32" "\nPronto! Você pode agora executar código Python neste ambiente!"
