# ativa_venv.ps1
# Script para detectar Python e criar ambiente virtual
# Resolve problemas com alias do Windows Store

Write-Host "`n=== SCRIPT DE CONFIGURAÇÃO DE AMBIENTE VIRTUAL PYTHON ===" -ForegroundColor Cyan
Write-Host "Este script irá configurar um ambiente virtual Python para seu projeto" -ForegroundColor Gray

# Função para verificar se uma instalação Python é válida
function Test-ValidPython {
    param([string]$pythonPath)

    if (-not (Test-Path $pythonPath)) { return $false }
    
    try {
        $version = & $pythonPath -c "import sys; print(sys.version)" 2>&1
        return $version -match "^\d+\.\d+\.\d+"
    }
    catch {
        return $false
    }
}

# Função para encontrar uma instalação válida do Python
function Find-ValidPython {
    Write-Host "`nProcurando instalações do Python..." -ForegroundColor Yellow
    
    # Caminhos comuns de instalação do Python
    $commonPaths = @(
        "C:\Python311\python.exe",
        "C:\Python310\python.exe",
        "C:\Python39\python.exe", 
        "C:\Python38\python.exe",
        "C:\Program Files\Python311\python.exe",
        "C:\Program Files\Python310\python.exe",
        "C:\Program Files\Python39\python.exe",
        "C:\Program Files\Python38\python.exe",
        "C:\Program Files (x86)\Python311\python.exe",
        "C:\Program Files (x86)\Python310\python.exe"
    )

    # Verifica caminhos comuns primeiro
    foreach ($path in $commonPaths) {
        Write-Host "  Verificando: $path..." -ForegroundColor Gray -NoNewline
        if (Test-ValidPython $path) {
            Write-Host " [ENCONTRADO]" -ForegroundColor Green
            return $path
        } else {
            Write-Host " [não encontrado]" -ForegroundColor DarkGray
        }
    }

    # Tenta encontrar Python na pasta AppData (instalações de usuário)
    Write-Host "  Verificando instalações de usuário..." -ForegroundColor Gray
    $userPaths = Get-ChildItem -Path "$env:LOCALAPPDATA\Programs\Python\Python*" -ErrorAction SilentlyContinue | 
                Where-Object { $_.PSIsContainer } | 
                ForEach-Object { Join-Path $_.FullName "python.exe" }
    
    foreach ($path in $userPaths) {
        Write-Host "  Verificando: $path..." -ForegroundColor Gray -NoNewline
        if (Test-ValidPython $path) {
            Write-Host " [ENCONTRADO]" -ForegroundColor Green
            return $path
        } else {
            Write-Host " [não encontrado]" -ForegroundColor DarkGray
        }
    }

    return $null
}

# Encontrar Python ou pedir caminho ao usuário
$pythonPath = Find-ValidPython

if (-not $pythonPath) {
    Write-Host "`nNenhuma instalação válida do Python foi encontrada automaticamente." -ForegroundColor Yellow
    Write-Host "`nVocê tem duas opções:" -ForegroundColor Cyan
    Write-Host "1. Baixar e instalar Python do site oficial" -ForegroundColor Cyan
    Write-Host "2. Fornecer o caminho para uma instalação existente do Python" -ForegroundColor Cyan
    
    $option = Read-Host "`nEscolha uma opção (1/2)"
    
    if ($option -eq "1") {
        Write-Host "`nAbrindo o site do Python para download..." -ForegroundColor Green
        Write-Host "IMPORTANTE: Durante a instalação, marque a opção 'Add Python to PATH'!" -ForegroundColor Yellow
        Write-Host "Após instalar, execute este script novamente." -ForegroundColor Green
        Start-Process "https://www.python.org/downloads/"
        Write-Host "`nPressione qualquer tecla para sair..."
        $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
        exit 0
    }
    elseif ($option -eq "2") {
        $userPath = Read-Host "`nDigite o caminho completo para python.exe (ex: C:\Python39\python.exe)"
        Write-Host "Verificando o caminho fornecido..." -ForegroundColor Gray
        if (Test-ValidPython $userPath) {
            $pythonPath = $userPath
            Write-Host "Caminho válido!" -ForegroundColor Green
        }
        else {
            Write-Error "O caminho fornecido não é uma instalação válida do Python."
            Write-Host "`nPressione qualquer tecla para sair..."
            $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
            exit 1
        }
    }
    else {
        Write-Error "Opção inválida selecionada."
        exit 1
    }
}

# Temos um caminho Python válido, prosseguir com a configuração
Write-Host "`n=== PYTHON ENCONTRADO ===" -ForegroundColor Green
Write-Host "Usando Python de: $pythonPath" -ForegroundColor Green
$pythonVersion = & $pythonPath --version
Write-Host "Versão do Python: $pythonVersion" -ForegroundColor Green

# Atualizar pip
Write-Host "`n=== ATUALIZANDO PIP ===" -ForegroundColor Cyan
Write-Host "Atualizando o gerenciador de pacotes pip..." -ForegroundColor Gray
& $pythonPath -m pip install --upgrade pip

# Criar novo ambiente virtual
Write-Host "`n=== CRIANDO AMBIENTE VIRTUAL ===" -ForegroundColor Cyan
if (Test-Path "$PSScriptRoot\venv") {
    Write-Host "Removendo ambiente virtual existente..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force "$PSScriptRoot\venv"
    Write-Host "Ambiente anterior removido." -ForegroundColor Gray
}

# Instalar e usar virtualenv
Write-Host "`nInstalando virtualenv..." -ForegroundColor Cyan
& $pythonPath -m pip install virtualenv

Write-Host "`nCriando ambiente virtual na pasta 'venv'..." -ForegroundColor Cyan
& $pythonPath -m virtualenv venv
if (-not $?) {
    Write-Error "Falha ao criar ambiente virtual"
    Write-Host "`nPressione qualquer tecla para sair..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}

# Ativar o ambiente
try {
    $activateScript = Join-Path -Path $PSScriptRoot -ChildPath "venv\Scripts\Activate.ps1"
    Write-Host "`n=== ATIVANDO AMBIENTE VIRTUAL ===" -ForegroundColor Cyan
    Write-Host "Ativando o ambiente virtual..." -ForegroundColor Gray
    . $activateScript
    
    # Instalar requirements
    if (Test-Path "$PSScriptRoot\requirements.txt") {
        Write-Host "`n=== INSTALANDO DEPENDÊNCIAS ===" -ForegroundColor Cyan
        Write-Host "Arquivo requirements.txt encontrado!" -ForegroundColor Green
        Write-Host "Instalando pacotes listados no requirements.txt..." -ForegroundColor Gray
        python -m pip install -r requirements.txt
        Write-Host "`nDependências instaladas com sucesso!" -ForegroundColor Green
    } else {
        Write-Host "`nArquivo requirements.txt não encontrado." -ForegroundColor Yellow
        Write-Host "Pule esta etapa ou crie um arquivo requirements.txt com suas dependências." -ForegroundColor Gray
    }
    
    Write-Host "`n=== AMBIENTE VIRTUAL ATIVADO COM SUCESSO! ===" -ForegroundColor Green
    Write-Host "`nINSTRUÇÕES DE USO:" -ForegroundColor Cyan
    Write-Host "1. O ambiente virtual está ATIVO agora" -ForegroundColor White
    Write-Host "2. Você verá (venv) no início do prompt" -ForegroundColor White
    Write-Host "3. Para DESATIVAR o ambiente: digite 'deactivate'" -ForegroundColor White
    Write-Host "4. Para REATIVAR no futuro: .\venv\Scripts\Activate.ps1" -ForegroundColor White
    Write-Host "5. Para instalar novos pacotes: pip install nome-do-pacote" -ForegroundColor White
    Write-Host "6. Para salvar dependências: pip freeze > requirements.txt" -ForegroundColor White
    Write-Host "`nVocê pode agora executar código Python neste ambiente!" -ForegroundColor Green
} catch {
    Write-Error "Falha ao ativar ambiente virtual: $_"
    Write-Host "`nPressione qualquer tecla para sair..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}