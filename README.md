# 🎯 Comparador Facial Painho Trampos

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![React](https://img.shields.io/badge/React-18.0+-61DAFB.svg)](https://reactjs.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688.svg)](https://fastapi.tiangolo.com)
[![MongoDB](https://img.shields.io/badge/MongoDB-4.4+-47A248.svg)](https://mongodb.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> **Sistema avançado de comparação facial com interface moderna e algoritmos de reconhecimento de alta precisão.**

![Comparador Facial](https://img.shields.io/badge/Status-100%25%20Funcional-brightgreen)

---

## 📋 Índice

- [🎯 Sobre o Projeto](#-sobre-o-projeto)
- [✨ Características](#-características)
- [🛠️ Tecnologias](#️-tecnologias)
- [📋 Pré-requisitos](#-pré-requisitos)
- [🚀 Instalação](#-instalação)
- [▶️ Como Executar](#️-como-executar)
- [🎮 Como Usar](#-como-usar)
- [🔧 Configuração](#-configuração)
- [📂 Estrutura do Projeto](#-estrutura-do-projeto)
- [🌐 API Endpoints](#-api-endpoints)
- [🛡️ Segurança](#️-segurança)
- [🔍 Solução de Problemas](#-solução-de-problemas)
- [🤝 Contribuição](#-contribuição)
- [📄 Licença](#-licença)

---

## 🎯 Sobre o Projeto

O **Comparador Facial Painho Trampos** é uma aplicação web completa que utiliza tecnologias de visão computacional para comparar rostos e calcular similaridades entre pessoas. O sistema permite upload de uma imagem base e até 250 imagens de comparação, processando-as em tempo real e retornando resultados ordenados por porcentagem de similaridade.

### 🎨 Interface Moderna
- Design dark profissional
- Cards de resultado com fundo claro para melhor contraste
- Animações suaves e responsividade total
- Sistema de autenticação integrado

---

## ✨ Características

### 🔐 **Segurança e Autenticação**
- Sistema de login com senha personalizada
- Sessão persistente com localStorage
- Controle de acesso total à aplicação
- Proteção contra uso não autorizado

### 📤 **Upload e Processamento**
- Upload de imagem base obrigatória
- Suporte a até **250 imagens** de comparação simultânea
- Validação automática de formatos (PNG, JPG)
- Limite de 10MB por imagem
- Preview instantâneo das imagens carregadas

### 🧠 **Inteligência Artificial**
- Detecção facial automatizada com **OpenCV**
- Algoritmo de extração de características faciais
- Cálculo de similaridade usando **Cosine Similarity**
- Processamento otimizado para múltiplas imagens

### 📊 **Resultados Visuais**
- Exibição da imagem base como referência
- Grid organizado com thumbnails das comparações
- Porcentagens de similaridade em tempo real
- Ordenação automática por maior similaridade
- Badges visuais indicando qualidade da correspondência

### 🎯 **Experiência do Usuário**
- Interface intuitiva e responsiva
- Barra de progresso durante uploads
- Mensagens de erro em português
- Sistema de reset para nova comparação
- Animações e efeitos visuais modernos

---

## 🛠️ Tecnologias

### **Backend**
- **FastAPI** - Framework web moderno e rápido
- **Python 3.8+** - Linguagem principal
- **OpenCV** - Processamento de imagem e detecção facial
- **scikit-learn** - Algoritmos de machine learning
- **PIL (Pillow)** - Manipulação de imagens
- **Motor** - Driver assíncrono para MongoDB
- **Pydantic** - Validação de dados

### **Frontend**
- **React 19** - Biblioteca JavaScript
- **Tailwind CSS** - Framework de estilos
- **shadcn/ui** - Componentes UI modernos
- **Axios** - Cliente HTTP
- **Lucide React** - Ícones

### **Banco de Dados**
- **MongoDB** - Banco NoSQL para metadados

### **Infraestrutura**
- **Uvicorn** - Servidor ASGI
- **CORS** - Configuração de políticas de origem

---

## 📋 Pré-requisitos

Antes de começar, certifique-se de ter instalado em seu PC:

- **Python 3.8 ou superior** ✅ (já instalado conforme solicitado)
- **Node.js 16+ e npm/yarn** - [Download Node.js](https://nodejs.org/)
- **MongoDB** - [Download MongoDB](https://www.mongodb.com/try/download/community)
- **Git** - [Download Git](https://git-scm.com/)

### Verificar Instalações
```bash
python --version    # Deve mostrar Python 3.8+
node --version      # Deve mostrar Node 16+
npm --version       # Deve mostrar npm 8+
mongod --version    # Deve mostrar MongoDB 4.4+
```

---

## 🚀 Instalação

### **Passo 1: Clonar o Repositório**
```bash
git clone https://github.com/seu-usuario/comparador-facial-painho-trampos.git
cd comparador-facial-painho-trampos
```

### **Passo 2: Configurar o Backend**

#### 2.1 - Criar ambiente virtual Python
```bash
# Navegar para pasta do backend
cd backend

# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

#### 2.2 - Instalar dependências Python
```bash
pip install -r requirements.txt
```

#### 2.3 - Configurar variáveis de ambiente
```bash
# Criar arquivo .env na pasta backend
cp .env.example .env

# Editar o arquivo .env com suas configurações:
# MONGO_URL=mongodb://localhost:27017
# DB_NAME=facial_comparison
# CORS_ORIGINS=http://localhost:3000
```

### **Passo 3: Configurar o Frontend**

#### 3.1 - Instalar dependências Node.js
```bash
# Navegar para pasta do frontend
cd ../frontend

# Instalar dependências
npm install
# ou
yarn install
```

#### 3.2 - Configurar variáveis de ambiente do frontend
```bash
# Criar arquivo .env na pasta frontend
cp .env.example .env

# Editar o arquivo .env:
# REACT_APP_BACKEND_URL=http://localhost:8001
```

### **Passo 4: Configurar MongoDB**

#### 4.1 - Iniciar MongoDB
```bash
# Windows (como serviço):
net start MongoDB

# Linux/Mac:
sudo systemctl start mongod
# ou
mongod --dbpath /caminho/para/dados
```

#### 4.2 - Verificar conexão
```bash
# Conectar ao MongoDB
mongo
# ou
mongosh

# Verificar se conectou (deve mostrar prompt do MongoDB)
```

---

## ▶️ Como Executar

### **Método 1: Execução Manual (Recomendado para desenvolvimento)**

#### Terminal 1 - Backend:
```bash
cd backend
# Ativar ambiente virtual
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Executar servidor FastAPI
uvicorn server:app --host 0.0.0.0 --port 8001 --reload
```

#### Terminal 2 - Frontend:
```bash
cd frontend
# Executar aplicação React
npm start
# ou
yarn start
```

### **Método 2: Usando Scripts (Opcional)**
```bash
# Criar script start.sh (Linux/Mac) ou start.bat (Windows)

# start.sh:
#!/bin/bash
cd backend && source venv/bin/activate && uvicorn server:app --host 0.0.0.0 --port 8001 --reload &
cd frontend && npm start &
wait

# Executar:
chmod +x start.sh
./start.sh
```

### **Acessar a Aplicação**
- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8001
- **Documentação API:** http://localhost:8001/docs

---

## 🎮 Como Usar

### **1. Acessar a Aplicação**
- Abra seu navegador em `http://localhost:3000`
- Você verá a tela de login com tema dark

### **2. Fazer Login**
- **Senha padrão:** `painho123`
- Digite a senha completa e clique em "Entrar"

### **3. Upload da Imagem Base**
- Clique na seção "Imagem Base"
- Selecione uma imagem com pelo menos um rosto visível
- A imagem aparecerá como preview

### **4. Upload das Imagens de Comparação**
- Clique na seção "Imagens para Comparação"
- Selecione até 250 imagens para comparar
- Thumbnails aparecerão na interface

### **5. Processar Comparação**
- Clique no botão "Comparar Rostos"
- Aguarde o processamento (barra de progresso aparecerá)
- Resultados serão exibidos automaticamente

### **6. Visualizar Resultados**
- **Imagem Base:** Mostrada como referência
- **Grid de Resultados:** Cards com imagens e porcentagens
- **Ordenação:** Por maior similaridade primeiro
- **Badges:** Indicam qualidade da correspondência

### **7. Resetar ou Sair**
- **Resetar:** Limpa tudo para nova comparação
- **Sair:** Volta para tela de login

---

## 🔧 Configuração

### **Personalizar Senha de Acesso**
```javascript
// frontend/src/App.js - linha ~16
const VALID_PASSWORD = 'suanovaSenha'; // Altere aqui
```

### **Configurar Limite de Imagens**
```python
# backend/server.py - linha ~160
if len(comparison_images) > 250:  # Altere o número aqui
```

### **Ajustar Qualidade das Thumbnails**
```python
# backend/server.py - função image_to_base64
def image_to_base64(image_array, max_size=(150, 150)):  # Altere o tamanho
```

### **Configurar MongoDB**
```bash
# backend/.env
MONGO_URL=mongodb://localhost:27017
DB_NAME=facial_comparison
```

---

## 📂 Estrutura do Projeto

```
comparador-facial-painho-trampos/
├── 📁 backend/
│   ├── 📄 server.py              # Servidor FastAPI principal
│   ├── 📄 requirements.txt       # Dependências Python
│   ├── 📄 .env                  # Variáveis de ambiente backend
│   └── 📁 venv/                 # Ambiente virtual Python
├── 📁 frontend/
│   ├── 📁 src/
│   │   ├── 📄 App.js            # Componente principal React
│   │   ├── 📄 App.css           # Estilos personalizados
│   │   ├── 📄 index.js          # Ponto de entrada React
│   │   └── 📁 components/
│   │       └── 📁 ui/           # Componentes shadcn/ui
│   ├── 📁 public/
│   │   └── 📄 index.html        # Template HTML
│   ├── 📄 package.json          # Dependências Node.js
│   ├── 📄 tailwind.config.js    # Configuração Tailwind
│   └── 📄 .env                  # Variáveis de ambiente frontend
├── 📄 README.md                 # Este arquivo
├── 📄 .gitignore               # Arquivos ignorados pelo Git
└── 📄 LICENSE                  # Licença MIT
```

---

## 🌐 API Endpoints

### **Autenticação**
- Não requer API key (autenticação via frontend)

### **Endpoints Principais**

#### `GET /api/`
```json
{
  "message": "Face Comparison API"
}
```

#### `POST /api/compare-faces`
**Parâmetros:**
- `base_image`: Arquivo de imagem (obrigatório)
- `comparison_images`: Lista de arquivos (até 250)

**Resposta:**
```json
{
  "base_image_has_face": true,
  "base_image_data": "data:image/jpeg;base64,/9j/4AAQ...",
  "results": [
    {
      "image_index": 0,
      "similarity_percentage": 87.5,
      "has_face": true,
      "image_data": "data:image/jpeg;base64,/9j/4AAQ...",
      "error_message": null
    }
  ],
  "total_images": 5,
  "processing_time": 2.34
}
```

#### `POST /api/status`
Para criar registros de status (metadados)

#### `GET /api/status`
Para recuperar registros de status

---

## 🛡️ Segurança

### **Recursos de Segurança Implementados**
- ✅ Autenticação obrigatória via senha
- ✅ Validação de tipos de arquivo
- ✅ Limite de tamanho de arquivo (10MB)
- ✅ Limite de quantidade de arquivos (250)
- ✅ Sanitização de dados de entrada
- ✅ CORS configurado adequadamente
- ✅ Processamento temporário (imagens não são salvas)

### **Recomendações de Segurança**
- Altere a senha padrão em produção
- Configure HTTPS em produção
- Implemente rate limiting se necessário
- Monitore uso de recursos do servidor

---

## 🔍 Solução de Problemas

### **❌ Erro: "ModuleNotFoundError"**
```bash
# Certifique-se de ativar o ambiente virtual
cd backend
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Reinstalar dependências
pip install -r requirements.txt
```

### **❌ Erro: "MongoDB connection failed"**
```bash
# Verificar se MongoDB está rodando
# Windows:
net start MongoDB

# Linux/Mac:
sudo systemctl start mongod

# Verificar conexão:
mongo --eval "db.runCommand('ping')"
```

### **❌ Erro: "Port already in use"**
```bash
# Encontrar processo usando a porta
netstat -tulpn | grep :8001
# ou
lsof -i :8001

# Matar processo
kill -9 PID_DO_PROCESSO
```

### **❌ Erro: "OpenCV installation failed"**
```bash
# Instalar dependências do sistema (Ubuntu/Debian):
sudo apt-get update
sudo apt-get install python3-opencv

# Windows: Reinstalar via pip
pip uninstall opencv-python
pip install opencv-python
```

### **❌ Frontend não carrega**
```bash
# Limpar cache do npm
npm cache clean --force

# Deletar node_modules e reinstalar
rm -rf node_modules package-lock.json
npm install
```

### **❌ Erro: "No face detected"**
- Certifique-se de que a imagem tem pelo menos um rosto visível
- Use imagens com boa qualidade e iluminação
- Evite imagens muito pequenas ou de baixa resolução

---

## 🤝 Contribuição

Contribuições são sempre bem-vindas! Para contribuir:

1. **Fork** o projeto
2. Crie uma **branch** para sua feature (`git checkout -b feature/MinhaFeature`)
3. **Commit** suas mudanças (`git commit -m 'Add: Nova feature incrível'`)
4. **Push** para a branch (`git push origin feature/MinhaFeature`)
5. Abra um **Pull Request**

### **Diretrizes de Contribuição**
- Mantenha o código limpo e documentado
- Teste suas alterações localmente
- Siga os padrões de código existentes
- Atualize a documentação se necessário

---

## 📊 Características Técnicas Detalhadas

### **🔬 Algoritmo de Detecção Facial**
- **OpenCV Haar Cascades:** Detecta rostos em tempo real
- **Pré-processamento:** Conversão para escala de cinza
- **Parâmetros otimizados:** scaleFactor=1.1, minNeighbors=5
- **Tamanho mínimo:** 30x30 pixels para detecção

### **🧮 Cálculo de Similaridade**
- **Extração de características:** Histogramas de 256 bins
- **Normalização:** Redimensionamento para 128x128 pixels
- **Métrica:** Cosine Similarity para comparação
- **Range:** 0-100% de similaridade

### **⚡ Performance e Otimização**
- **Thumbnails:** Imagens reduzidas para 150x150px
- **Processamento paralelo:** Múltiplas imagens simultaneamente
- **Compressão:** Base64 com qualidade JPEG 80%
- **Memória:** Processamento temporário sem armazenamento

### **🎨 Interface e UX**
- **Design System:** Tailwind CSS + shadcn/ui
- **Tema:** Dark mode profissional
- **Animações:** Hover effects e transições suaves
- **Responsividade:** Mobile-first design
- **Acessibilidade:** Focus states e navegação por teclado

### **🔒 Controle de Acesso**
- **Autenticação:** Senha única configurável
- **Sessão:** Persistent storage com localStorage
- **Logout:** Limpeza completa de dados
- **Proteção:** Todas as rotas protegidas

### **📈 Métricas e Monitoramento**
- **Tempo de processamento:** Medição automática
- **Estatísticas:** Total de imagens, rostos detectados
- **Logs:** Console logging para debugging
- **Errors:** Tratamento gracioso com mensagens em português

---

## 🏆 Casos de Uso

### **👥 Identificação de Pessoas**
- Comparar foto de pessoa com banco de imagens
- Identificar duplicatas em coleções de fotos
- Verificação de identidade básica

### **📸 Organização de Fotos**
- Agrupar fotos por pessoas similares
- Encontrar todas as fotos de uma pessoa específica
- Limpar duplicatas de álbuns familiares

### **🔍 Investigação e Pesquisa**
- Comparar suspeitos com banco de dados
- Análise forense de imagens
- Pesquisa acadêmica em reconhecimento facial

### **🎯 Aplicações Comerciais**
- Sistema de presença baseado em fotos
- Controle de acesso por reconhecimento
- Marketing personalizado por demografia

---

## 📄 Licença

Este projeto está licenciado sob a **MIT License**. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

```
MIT License

Copyright (c) 2025 Painho Trampos

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 📞 Contato e Suporte

- **Projeto:** Comparador Facial Painho Trampos
- **Versão:** 1.0.0
- **Status:** ✅ 100% Funcional
- **Última atualização:** Janeiro 2025

### **Suporte Técnico**
- Abra uma **Issue** no GitHub para bugs
- Use **Discussions** para perguntas gerais
- **Pull Requests** são bem-vindos!

---

<div align="center">

**🎉 Desenvolvido com ❤️ por Painho Trampos**

[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![React](https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://reactjs.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)

</div>

---

> **⭐ Se este projeto te ajudou, não esqueça de dar uma estrela no GitHub!**
