#!/bin/bash

# ativa_venv.sh
# Script para detectar Python e criar ambiente virtual no Linux

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

# Função para verificar se uma instalação Python é válida
test_valid_python() {
    local python_path=$1
    
    if ! command -v "$python_path" &> /dev/null; then
        return 1
    fi
    
    local version
    version=$("$python_path" -c "import sys; print(sys.version)" 2>/dev/null)
    
    if [[ $version =~ ^[0-9]+\.[0-9]+\.[0-9]+ ]]; then
        return 0
    else
        return 1
    fi
}

# Função para encontrar uma instalação válida do Python
find_valid_python() {
    print_colored "33" "\nProcurando instalações do Python..."
    
    # Lista de comandos Python para tentar
    local python_commands=("python3" "python" "python3.11" "python3.10" "python3.9" "python3.8")
    
    # Verifica cada comando
    for cmd in "${python_commands[@]}"; do
        echo -n "  Verificando: $cmd..."
        if command -v "$cmd" &> /dev/null && test_valid_python "$cmd"; then
            print_colored "32" " [ENCONTRADO]"
            echo "$cmd"
            return 0
        else
            print_colored "90" " [não encontrado]"
        fi
    done
    
    # Verifica caminhos comuns
    local common_paths=(
        "/usr/bin/python3"
        "/usr/local/bin/python3"
        "/opt/python3/bin/python3"
    )
    
    for path in "${common_paths[@]}"; do
        echo -n "  Verificando: $path..."
        if [[ -f "$path" ]] && test_valid_python "$path"; then
            print_colored "32" " [ENCONTRADO]"
            echo "$path"
            return 0
        else
            print_colored "90" " [não encontrado]"
        fi
    done
    
    return 1
}

# Função para instalar Python no Linux
install_python_linux() {
    print_colored "33" "\nInstalação do Python no Linux"
    
    # Detecta a distribuição
    if command -v apt-get &> /dev/null; then
        # Debian/Ubuntu
        print_colored "36" "Distribuição baseada em Debian/Ubuntu detectada"
        echo "Instalando Python3 e python3-venv..."
        sudo apt-get update
        sudo apt-get install -y python3 python3-venv python3-pip
    elif command -v yum &> /dev/null; then
        # RedHat/CentOS
        print_colored "36" "Distribuição baseada em RedHat/CentOS detectada"
        echo "Instalando Python3..."
        sudo yum install -y python3 python3-pip
    elif command -v dnf &> /dev/null; then
        # Fedora
        print_colored "36" "Distribuição Fedora detectada"
        echo "Instalando Python3..."
        sudo dnf install -y python3 python3-pip
    elif command -v pacman &> /dev/null; then
        # Arch Linux
        print_colored "36" "Distribuição Arch Linux detectada"
        echo "Instalando Python3..."
        sudo pacman -S python python-pip
    else
        print_colored "31" "Não foi possível detectar o gerenciador de pacotes"
        print_colored "33" "Por favor, instale o Python3 manualmente:"
        echo "  Debian/Ubuntu: sudo apt-get install python3 python3-venv python3-pip"
        echo "  RedHat/CentOS: sudo yum install python3 python3-pip"
        echo "  Fedora: sudo dnf install python3 python3-pip"
        echo "  Arch: sudo pacman -S python python-pip"
        return 1
    fi
    
    # Verifica se a instalação foi bem sucedida
    if command -v python3 &> /dev/null; then
        print_colored "32" "\nPython3 instalado com sucesso!"
        echo "python3"
        return 0
    else
        print_colored "31" "Falha na instalação do Python3"
        return 1
    fi
}

main() {
    print_header
    
    # Encontrar Python ou pedir ao usuário
    python_cmd=$(find_valid_python)
    
    if [[ -z "$python_cmd" ]]; then
        print_colored "33" "\nNenhuma instalação válida do Python foi encontrada automaticamente."
        print_colored "36" "\nVocê tem duas opções:"
        print_colored "36" "1. Instalar Python automaticamente (requer sudo)"
        print_colored "36" "2. Fornecer o caminho para uma instalação existente do Python"
        
        read -rp $'\nEscolha uma opção (1/2): ' option
        
        if [[ "$option" == "1" ]]; then
            python_cmd=$(install_python_linux)
            if [[ $? -ne 0 ]]; then
                print_colored "31" "Falha na instalação do Python. Saindo..."
                exit 1
            fi
        elif [[ "$option" == "2" ]]; then
            read -rp $'\nDigite o comando ou caminho para o Python (ex: python3, /usr/bin/python3): ' user_path
            echo "Verificando o caminho fornecido..."
            if test_valid_python "$user_path"; then
                python_cmd="$user_path"
                print_colored "32" "Caminho válido!"
            else
                print_colored "31" "O caminho fornecido não é uma instalação válida do Python."
                exit 1
            fi
        else
            print_colored "31" "Opção inválida selecionada."
            exit 1
        fi
    fi
    
    # Temos um comando Python válido, prosseguir com a configuração
    print_colored "32" "\n=== PYTHON ENCONTRADO ==="
    print_colored "32" "Usando Python: $python_cmd"
    python_version=$("$python_cmd" --version 2>&1)
    print_colored "32" "Versão do Python: $python_version"
    
    # Atualizar pip
    print_colored "36" "\n=== ATUALIZANDO PIP ==="
    print_colored "37" "Atualizando o gerenciador de pacotes pip..."
    "$python_cmd" -m pip install --upgrade pip
    
    # Criar novo ambiente virtual
    print_colored "36" "\n=== CRIANDO AMBIENTE VIRTUAL ==="
    if [[ -d "venv" ]]; then
        print_colored "33" "Removendo ambiente virtual existente..."
        rm -rf venv
        print_colored "37" "Ambiente anterior removido."
    fi
    
    # Criar ambiente virtual
    print_colored "36" "\nCriando ambiente virtual na pasta 'venv'..."
    "$python_cmd" -m venv venv
    if [[ $? -ne 0 ]]; then
        print_colored "31" "Falha ao criar ambiente virtual"
        print_colored "33" "Tentando instalar python3-venv..."
        
        if command -v apt-get &> /dev/null; then
            sudo apt-get install -y python3-venv
        elif command -v yum &> /dev/null; then
            sudo yum install -y python3-venv
        elif command -v dnf &> /dev/null; then
            sudo dnf install -y python3-venv
        fi
        
        # Tenta novamente
        "$python_cmd" -m venv venv
        if [[ $? -ne 0 ]]; then
            print_colored "31" "Falha ao criar ambiente virtual. Saindo..."
            exit 1
        fi
    fi
    
    # Ativar o ambiente
    activate_script="venv/bin/activate"
    print_colored "36" "\n=== ATIVANDO AMBIENTE VIRTUAL ==="
    print_colored "37" "Ativando o ambiente virtual..."
    
    # Source do script de ativação
    source "$activate_script"
    
    # Instalar requirements
    if [[ -f "requirements.txt" ]]; then
        print_colored "36" "\n=== INSTALANDO DEPENDÊNCIAS ==="
        print_colored "32" "Arquivo requirements.txt encontrado!"
        print_colored "37" "Instalando pacotes listados no requirements.txt..."
        pip install -r requirements.txt
        print_colored "32" "\nDependências instaladas com sucesso!"
    else
        print_colored "33" "\nArquivo requirements.txt não encontrado."
        print_colored "37" "Pule esta etapa ou crie um arquivo requirements.txt com suas dependências."
    fi
    
    print_colored "32" "\n=== AMBIENTE VIRTUAL ATIVADO COM SUCESSO! ==="
    print_colored "36" "\nINSTRUÇÕES DE USO:"
    print_colored "37" "1. O ambiente virtual está ATIVO agora"
    print_colored "37" "2. Você verá (venv) no início do prompt"
    print_colored "37" "3. Para DESATIVAR o ambiente: digite 'deactivate'"
    print_colored "37" "4. Para REATIVAR no futuro: source venv/bin/activate"
    print_colored "37" "5. Para instalar novos pacotes: pip install nome-do-pacote"
    print_colored "37" "6. Para salvar dependências: pip freeze > requirements.txt"
    print_colored "32" "\nVocê pode agora executar código Python neste ambiente!"
}

# Executar função principal
main "$@"