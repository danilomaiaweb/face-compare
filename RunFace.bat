@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

:: ===============================================
:: 🎯 COMPARADOR FACIAL PAINHO TRAMPOS - AUTORUN
:: ===============================================
:: Arquivo: RunFace.bat
:: Versão: 1.0.0
:: Descrição: Script automático para executar o sistema
:: ===============================================

title Comparador Facial Painho Trampos - Inicializador Automático

:: Cores para output
set "GREEN=[92m"
set "RED=[91m"
set "YELLOW=[93m"
set "BLUE=[94m"
set "PURPLE=[95m"
set "CYAN=[96m"
set "WHITE=[97m"
set "NC=[0m"

:: Limpar tela e mostrar header
cls
echo.
echo %PURPLE%===============================================%NC%
echo %CYAN%    🎯 COMPARADOR FACIAL PAINHO TRAMPOS       %NC%
echo %PURPLE%===============================================%NC%
echo %WHITE%    Inicializador Automático v1.0.0           %NC%
echo %PURPLE%===============================================%NC%
echo.

:: Verificar se está rodando como administrador
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo %RED%❌ ERRO: Execute como Administrador%NC%
    echo %YELLOW%   Clique com botão direito e selecione "Executar como administrador"%NC%
    pause
    exit /b 1
)

echo %GREEN%✅ Executando como Administrador%NC%
echo.

:: ===============================================
:: 📋 VERIFICAÇÃO DE PRÉ-REQUISITOS
:: ===============================================

echo %BLUE%📋 Verificando pré-requisitos...%NC%
echo.

set "PYTHON_OK=0"
set "NODE_OK=0"
set "NPM_OK=0"
set "MONGO_OK=0"
set "GIT_OK=0"

:: Verificar Python
echo %CYAN%🐍 Verificando Python...%NC%
python --version >nul 2>&1
if %errorLevel% equ 0 (
    for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
    echo %GREEN%   ✅ Python !PYTHON_VERSION! encontrado%NC%
    set "PYTHON_OK=1"
) else (
    echo %RED%   ❌ Python não encontrado%NC%
    echo %YELLOW%   📥 Baixe em: https://python.org%NC%
)

:: Verificar Node.js
echo %CYAN%📦 Verificando Node.js...%NC%
node --version >nul 2>&1
if %errorLevel% equ 0 (
    for /f %%i in ('node --version') do set NODE_VERSION=%%i
    echo %GREEN%   ✅ Node.js !NODE_VERSION! encontrado%NC%
    set "NODE_OK=1"
) else (
    echo %RED%   ❌ Node.js não encontrado%NC%
    echo %YELLOW%   📥 Baixe em: https://nodejs.org%NC%
)

:: Verificar NPM
echo %CYAN%📦 Verificando NPM...%NC%
npm --version >nul 2>&1
if %errorLevel% equ 0 (
    for /f %%i in ('npm --version') do set NPM_VERSION=%%i
    echo %GREEN%   ✅ NPM !NPM_VERSION! encontrado%NC%
    set "NPM_OK=1"
) else (
    echo %RED%   ❌ NPM não encontrado%NC%
)

:: Verificar MongoDB
echo %CYAN%🍃 Verificando MongoDB...%NC%
mongod --version >nul 2>&1
if %errorLevel% equ 0 (
    echo %GREEN%   ✅ MongoDB encontrado%NC%
    set "MONGO_OK=1"
) else (
    echo %YELLOW%   ⚠️  MongoDB não encontrado ou não está no PATH%NC%
    echo %YELLOW%   📥 Baixe em: https://mongodb.com/try/download/community%NC%
    set "MONGO_OK=1"
    :: Continuamos mesmo sem MongoDB pois pode estar instalado como serviço
)

:: Verificar Git
echo %CYAN%📚 Verificando Git...%NC%
git --version >nul 2>&1
if %errorLevel% equ 0 (
    echo %GREEN%   ✅ Git encontrado%NC%
    set "GIT_OK=1"
) else (
    echo %YELLOW%   ⚠️  Git não encontrado (opcional)%NC%
    set "GIT_OK=1"
)

echo.

:: Verificar se requisitos mínimos estão OK
if %PYTHON_OK% equ 0 (
    echo %RED%❌ ERRO: Python é obrigatório%NC%
    echo %YELLOW%   Instale Python 3.8+ e execute novamente%NC%
    pause
    exit /b 1
)

if %NODE_OK% equ 0 (
    echo %RED%❌ ERRO: Node.js é obrigatório%NC%
    echo %YELLOW%   Instale Node.js 16+ e execute novamente%NC%
    pause
    exit /b 1
)

if %NPM_OK% equ 0 (
    echo %RED%❌ ERRO: NPM é obrigatório%NC%
    echo %YELLOW%   Instale Node.js (inclui NPM) e execute novamente%NC%
    pause
    exit /b 1
)

echo %GREEN%🎉 Todos os pré-requisitos OK!%NC%
echo.

:: ===============================================
:: 🚀 CONFIGURAÇÃO DO AMBIENTE
:: ===============================================

echo %BLUE%🚀 Configurando ambiente...%NC%
echo.

:: Definir diretórios
set "SCRIPT_DIR=%~dp0"
set "BACKEND_DIR=%SCRIPT_DIR%backend"
set "FRONTEND_DIR=%SCRIPT_DIR%frontend"
set "VENV_DIR=%BACKEND_DIR%\venv"

:: Verificar se os diretórios existem
if not exist "%BACKEND_DIR%" (
    echo %RED%❌ ERRO: Diretório backend não encontrado%NC%
    echo %YELLOW%   Certifique-se de que o script está na pasta raiz do projeto%NC%
    pause
    exit /b 1
)

if not exist "%FRONTEND_DIR%" (
    echo %RED%❌ ERRO: Diretório frontend não encontrado%NC%
    echo %YELLOW%   Certifique-se de que o script está na pasta raiz do projeto%NC%
    pause
    exit /b 1
)

echo %GREEN%✅ Estrutura do projeto encontrada%NC%

:: ===============================================
:: 🐍 CONFIGURAÇÃO DO BACKEND
:: ===============================================

echo.
echo %BLUE%🐍 Configurando Backend Python...%NC%

:: Navegar para o diretório do backend
cd /d "%BACKEND_DIR%"

:: Verificar se ambiente virtual já existe
if exist "%VENV_DIR%" (
    echo %GREEN%   ✅ Ambiente virtual já existe%NC%
) else (
    echo %CYAN%   📦 Criando ambiente virtual...%NC%
    python -m venv venv
    if %errorLevel% neq 0 (
        echo %RED%   ❌ ERRO ao criar ambiente virtual%NC%
        pause
        exit /b 1
    )
    echo %GREEN%   ✅ Ambiente virtual criado%NC%
)

:: Ativar ambiente virtual
echo %CYAN%   🔧 Ativando ambiente virtual...%NC%
call "%VENV_DIR%\Scripts\activate.bat"
if %errorLevel% neq 0 (
    echo %RED%   ❌ ERRO ao ativar ambiente virtual%NC%
    pause
    exit /b 1
)
echo %GREEN%   ✅ Ambiente virtual ativado%NC%

:: Verificar e instalar dependências
echo %CYAN%   📦 Verificando dependências Python...%NC%
if not exist "requirements.txt" (
    echo %RED%   ❌ requirements.txt não encontrado%NC%
    pause
    exit /b 1
)

:: Atualizar pip
echo %CYAN%   🔄 Atualizando pip...%NC%
python -m pip install --upgrade pip >nul 2>&1

:: Instalar dependências
echo %CYAN%   📦 Instalando dependências (pode demorar alguns minutos)...%NC%
pip install -r requirements.txt >nul 2>&1
if %errorLevel% neq 0 (
    echo %YELLOW%   ⚠️  Algumas dependências podem ter falhado, continuando...%NC%
) else (
    echo %GREEN%   ✅ Dependências Python instaladas%NC%
)

:: Verificar arquivo .env
if not exist ".env" (
    echo %CYAN%   📝 Criando arquivo .env...%NC%
    (
        echo MONGO_URL=mongodb://localhost:27017
        echo DB_NAME=facial_comparison
        echo CORS_ORIGINS=http://localhost:3000
    ) > .env
    echo %GREEN%   ✅ Arquivo .env criado%NC%
) else (
    echo %GREEN%   ✅ Arquivo .env já existe%NC%
)

:: ===============================================
:: 📦 CONFIGURAÇÃO DO FRONTEND
:: ===============================================

echo.
echo %BLUE%📦 Configurando Frontend React...%NC%

:: Navegar para o diretório do frontend
cd /d "%FRONTEND_DIR%"

:: Verificar se node_modules existe
if exist "node_modules" (
    echo %GREEN%   ✅ Dependências Node.js já instaladas%NC%
) else (
    echo %CYAN%   📦 Instalando dependências Node.js (pode demorar alguns minutos)...%NC%
    npm install >nul 2>&1
    if %errorLevel% neq 0 (
        echo %RED%   ❌ ERRO ao instalar dependências Node.js%NC%
        echo %YELLOW%   Tentando com yarn...%NC%
        yarn install >nul 2>&1
        if %errorLevel% neq 0 (
            echo %RED%   ❌ ERRO também com yarn%NC%
            pause
            exit /b 1
        )
    )
    echo %GREEN%   ✅ Dependências Node.js instaladas%NC%
)

:: Verificar arquivo .env do frontend
if not exist ".env" (
    echo %CYAN%   📝 Criando arquivo .env do frontend...%NC%
    echo REACT_APP_BACKEND_URL=http://localhost:8001 > .env
    echo %GREEN%   ✅ Arquivo .env do frontend criado%NC%
) else (
    echo %GREEN%   ✅ Arquivo .env do frontend já existe%NC%
)

:: ===============================================
:: 🍃 CONFIGURAÇÃO DO MONGODB
:: ===============================================

echo.
echo %BLUE%🍃 Configurando MongoDB...%NC%

:: Tentar iniciar MongoDB como serviço
echo %CYAN%   🔧 Iniciando serviço MongoDB...%NC%
net start MongoDB >nul 2>&1
if %errorLevel% equ 0 (
    echo %GREEN%   ✅ MongoDB iniciado como serviço%NC%
) else (
    echo %YELLOW%   ⚠️  MongoDB não está configurado como serviço%NC%
    echo %YELLOW%   ℹ️  Tentando iniciar manualmente...%NC%
    
    :: Procurar MongoDB em locais comuns
    set "MONGOD_PATH="
    if exist "C:\Program Files\MongoDB\Server\*\bin\mongod.exe" (
        for /d %%d in ("C:\Program Files\MongoDB\Server\*") do (
            if exist "%%d\bin\mongod.exe" set "MONGOD_PATH=%%d\bin\mongod.exe"
        )
    )
    
    if defined MONGOD_PATH (
        echo %CYAN%   🚀 Iniciando MongoDB manualmente...%NC%
        start /min "MongoDB Server" "!MONGOD_PATH!" --dbpath "%SCRIPT_DIR%data\db" >nul 2>&1
        timeout /t 3 >nul
        echo %GREEN%   ✅ MongoDB iniciado%NC%
    ) else (
        echo %YELLOW%   ⚠️  MongoDB não encontrado, mas continuando...%NC%
        echo %YELLOW%   📝 Certifique-se de que o MongoDB está rodando%NC%
    )
)

:: ===============================================
:: 🚀 INICIANDO OS SERVIÇOS
:: ===============================================

echo.
echo %BLUE%🚀 Iniciando serviços...%NC%
echo.

:: Criar pasta para logs
if not exist "%SCRIPT_DIR%logs" mkdir "%SCRIPT_DIR%logs"

:: Iniciar Backend
echo %CYAN%🐍 Iniciando Backend (FastAPI)...%NC%
cd /d "%BACKEND_DIR%"
call "%VENV_DIR%\Scripts\activate.bat"
start /min "Backend - Comparador Facial" cmd /c "uvicorn server:app --host 0.0.0.0 --port 8001 --reload > %SCRIPT_DIR%logs\backend.log 2>&1"

:: Aguardar backend inicializar
echo %CYAN%   ⏳ Aguardando backend inicializar...%NC%
timeout /t 5 >nul

:: Testar conexão com backend
for /L %%i in (1,1,10) do (
    curl -s http://localhost:8001/api/ >nul 2>&1
    if !errorLevel! equ 0 (
        echo %GREEN%   ✅ Backend iniciado com sucesso!%NC%
        goto backend_ok
    )
    timeout /t 2 >nul
)
echo %YELLOW%   ⚠️  Backend pode não ter iniciado corretamente%NC%
:backend_ok

:: Iniciar Frontend
echo %CYAN%📦 Iniciando Frontend (React)...%NC%
cd /d "%FRONTEND_DIR%"
set BROWSER=none
start /min "Frontend - Comparador Facial" cmd /c "npm start > %SCRIPT_DIR%logs\frontend.log 2>&1"

:: Aguardar frontend inicializar
echo %CYAN%   ⏳ Aguardando frontend inicializar...%NC%
timeout /t 10 >nul

:: Testar conexão com frontend
for /L %%i in (1,1,15) do (
    curl -s http://localhost:3000 >nul 2>&1
    if !errorLevel! equ 0 (
        echo %GREEN%   ✅ Frontend iniciado com sucesso!%NC%
        goto frontend_ok
    )
    timeout /t 2 >nul
)
echo %YELLOW%   ⚠️  Frontend pode não ter iniciado corretamente%NC%
:frontend_ok

:: ===============================================
:: 🌐 ABRINDO NO NAVEGADOR
:: ===============================================

echo.
echo %BLUE%🌐 Abrindo aplicação no navegador...%NC%

:: Aguardar mais um pouco para garantir que está tudo carregado
timeout /t 3 >nul

:: Abrir no navegador padrão
start http://localhost:3000

echo.
echo %GREEN%🎉 SISTEMA INICIADO COM SUCESSO!%NC%
echo.
echo %PURPLE%===============================================%NC%
echo %WHITE%    🎯 COMPARADOR FACIAL PAINHO TRAMPOS       %NC%
echo %PURPLE%===============================================%NC%
echo.
echo %CYAN%📍 URLs de Acesso:%NC%
echo %WHITE%   🌐 Frontend: http://localhost:3000%NC%
echo %WHITE%   🔧 Backend:  http://localhost:8001%NC%
echo %WHITE%   📖 API Docs: http://localhost:8001/docs%NC%
echo.
echo %CYAN%🔐 Informações de Login:%NC%
echo %WHITE%   👤 Senha: painho123%NC%
echo.
echo %CYAN%📂 Funcionalidades:%NC%
echo %WHITE%   📸 Upload até 250 imagens%NC%
echo %WHITE%   🧠 Detecção facial automática%NC%
echo %WHITE%   📊 Comparação com porcentagens%NC%
echo %WHITE%   🎨 Interface dark moderna%NC%
echo.
echo %CYAN%📝 Logs:%NC%
echo %WHITE%   📋 Backend:  %SCRIPT_DIR%logs\backend.log%NC%
echo %WHITE%   📋 Frontend: %SCRIPT_DIR%logs\frontend.log%NC%
echo.
echo %YELLOW%⚠️  Para parar os serviços:%NC%
echo %WHITE%   - Feche as janelas minimizadas%NC%
echo %WHITE%   - Ou execute: taskkill /f /im node.exe /im python.exe%NC%
echo.
echo %GREEN%✨ Aproveite o Comparador Facial Painho Trampos!%NC%
echo.

:: ===============================================
:: 📊 MONITORAMENTO CONTÍNUO
:: ===============================================

echo %BLUE%📊 Monitoramento ativo - Pressione qualquer tecla para sair%NC%
echo.

:: Loop de monitoramento
:monitor_loop
:: Verificar se os serviços ainda estão rodando
tasklist /fi "imagename eq python.exe" | find "python.exe" >nul
set "BACKEND_RUNNING=%errorLevel%"

tasklist /fi "imagename eq node.exe" | find "node.exe" >nul
set "FRONTEND_RUNNING=%errorLevel%"

:: Mostrar status
if %BACKEND_RUNNING% equ 0 (
    set "BACKEND_STATUS=%GREEN%✅ Online%NC%"
) else (
    set "BACKEND_STATUS=%RED%❌ Offline%NC%"
)

if %FRONTEND_RUNNING% equ 0 (
    set "FRONTEND_STATUS=%GREEN%✅ Online%NC%"
) else (
    set "FRONTEND_STATUS=%RED%❌ Offline%NC%"
)

:: Atualizar display a cada 5 segundos
title Comparador Facial - Backend: !BACKEND_STATUS! - Frontend: !FRONTEND_STATUS!

:: Verificar se usuário quer sair
timeout /t 5 >nul
if %errorLevel% equ 0 goto monitor_loop

:: ===============================================
:: 🛑 LIMPEZA E SAÍDA
:: ===============================================

echo.
echo %YELLOW%🛑 Encerrando serviços...%NC%

:: Parar processos
taskkill /f /im node.exe >nul 2>&1
taskkill /f /im python.exe >nul 2>&1

echo %GREEN%✅ Serviços encerrados%NC%
echo.
echo %PURPLE%Obrigado por usar o Comparador Facial Painho Trampos!%NC%
echo.

pause
endlocal