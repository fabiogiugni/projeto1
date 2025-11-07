#!/usr/bin/env bash

echo -e "\n=== SCRIPT DE CONFIGURAÇÃO DE AMBIENTE VIRTUAL PYTHON ==="
echo "Este script irá configurar um ambiente virtual Python para seu projeto."
echo

# ---------- Função para verificar se o Python é válido ----------
is_valid_python() {
    local py=$1
    if [ ! -x "$py" ]; then
        return 1
    fi
    local version=$($py -c "import sys; print(sys.version)" 2>/dev/null)
    if [[ $version =~ ^[0-9]+\.[0-9]+\.[0-9]+ ]]; then
        return 0
    else
        return 1
    fi
}

# ---------- Função para encontrar Python válido ----------
find_python() {
    echo -e "\nProcurando instalações do Python..."
    local paths=(
        "/usr/bin/python3.13"
        "/usr/bin/python3.12"
        "/usr/bin/python3.11"
        "/usr/bin/python3.10"
        "/usr/bin/python3.9"
        "/usr/local/bin/python3"
        "$(which python3 2>/dev/null)"
        "$(which python 2>/dev/null)"
    )

    for path in "${paths[@]}"; do
        [ -z "$path" ] && continue
        echo -ne "  Verificando: $path... "
        if is_valid_python "$path"; then
            echo "[ENCONTRADO]"
            PYTHON_PATH="$path"
            return 0
        else
            echo "[não encontrado]"
        fi
    done

    return 1
}

# ---------- Buscar Python ----------
if ! find_python; then
    echo -e "\nNenhuma instalação válida do Python foi encontrada automaticamente."
    echo "Você pode:"
    echo "1. Instalar Python com seu gerenciador de pacotes (ex: sudo apt install python3.12)"
    echo "2. Ou digitar o caminho manualmente."
    read -rp $'\nDigite o caminho completo do Python (ou deixe em branco para sair): ' user_path
    if [ -z "$user_path" ]; then
        echo "Saindo..."
        exit 1
    fi
    if is_valid_python "$user_path"; then
        PYTHON_PATH="$user_path"
    else
        echo "❌ Caminho inválido. Saindo..."
        exit 1
    fi
fi

echo -e "\n=== PYTHON ENCONTRADO ==="
echo "Usando Python de: $PYTHON_PATH"
$PYTHON_PATH --version

# ---------- Atualizar pip ----------
echo -e "\n=== ATUALIZANDO PIP ==="
$PYTHON_PATH -m pip install --upgrade pip || {
    echo "❌ Falha ao atualizar pip."
    exit 1
}

# ---------- Criar ambiente virtual ----------
echo -e "\n=== CRIANDO AMBIENTE VIRTUAL ==="
if [ -d "venv" ]; then
    echo "Removendo ambiente virtual existente..."
    rm -rf venv
fi

echo "Instalando virtualenv..."
$PYTHON_PATH -m pip install virtualenv

echo "Criando ambiente virtual..."
$PYTHON_PATH -m virtualenv venv || {
    echo "❌ Falha ao criar ambiente virtual."
    exit 1
}

# ---------- Ativar e instalar dependências ----------
echo -e "\n=== ATIVANDO AMBIENTE VIRTUAL ==="
# shellcheck disable=SC1091
source venv/bin/activate

if [ -f "requirements.txt" ]; then
    echo -e "\n=== INSTALANDO DEPENDÊNCIAS ==="
    pip install -r requirements.txt
else
    echo -e "\nArquivo requirements.txt não encontrado. Pule esta etapa ou crie um."
fi

echo -e "\n✅ === AMBIENTE VIRTUAL ATIVADO COM SUCESSO ==="
echo
echo "INSTRUÇÕES DE USO:"
echo "1. O ambiente virtual está ATIVO agora."
echo "2. Você verá (venv) no início do prompt."
echo "3. Para DESATIVAR o ambiente: 'deactivate'"
echo "4. Para REATIVAR no futuro: source venv/bin/activate"
echo "5. Para instalar novos pacotes: pip install nome-do-pacote"
echo "6. Para salvar dependências: pip freeze > requirements.txt"
echo
