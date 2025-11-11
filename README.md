# 🏢 Sistema de Gerenciamento Empresarial

Este projeto foi desenvolvido como parte do **Trabalho 1** da disciplina **Análise, Projeto e Programação Orientada a Objetos (APPOO)** da **UFMG**.  
O sistema tem como objetivo fornecer uma plataforma integrada para **gerenciamento de métricas empresariais**, como **OKRs (Objectives and Key Results)** e **KPIs (Key Performance Indicators)**, utilizando princípios sólidos de **Programação Orientada a Objetos (POO)**.

---

## 📚 Sumário

- [Visão Geral](#visão-geral)
- [Arquitetura do Sistema](#arquitetura-do-sistema)
- [Funcionalidades Principais](#funcionalidades-principais)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Instalação e Execução](#instalação-e-execução)
- [Estrutura de Pastas](#estrutura-de-pastas)
- [Fluxo de Dados](#fluxo-de-dados)
- [Resultados Obtidos](#resultados-obtidos)
- [Autores](#autores)

---

## 🧠 Visão Geral

O sistema permite o gerenciamento hierárquico de empresas, departamentos, equipes e funcionários, bem como o registro e acompanhamento de **indicadores de desempenho (KPIs e KRs)**.  
A aplicação é composta por duas camadas principais:

1. **Backend (Python / FastAPI / SQLite)** — responsável pela lógica de negócio, persistência e autenticação.
2. **Frontend (React.js)** — interface web interativa e responsiva que se comunica com a API.

O modelo de dados segue uma estrutura orientada a objetos, com herança, encapsulamento e polimorfismo, permitindo flexibilidade e reutilização de código.

---

## 🏗️ Arquitetura do Sistema

O sistema adota uma arquitetura **cliente-servidor** com camadas bem definidas:

```

Frontend (React)  →  API REST (FastAPI)  →  Database (SQLite)

```

Cada entidade (como `Company`, `Department`, `Team`, `Person`, `RPE`, `Objective`, `KPI`, `KR`) é representada por uma classe no backend, armazenada no banco de dados com integridade referencial.

---

## ⚙️ Funcionalidades Principais

- **Cadastro e autenticação de usuários** (diretores, gerentes e funcionários)
- **Criação e gerenciamento** de empresas, departamentos e equipes
- **Associação de métricas (OKRs e KPIs)** a diferentes níveis hierárquicos
- **Visualização de desempenho** por meio de relatórios e indicadores
- **Controle de permissões** conforme o papel do usuário
- **Deleção em cascata** e manutenção de integridade de dados

---

## 🧰 Tecnologias Utilizadas

### Backend

- **Python 3.11+**
- **FastAPI** — framework para construção da API REST
- **SQLite** — banco de dados leve e relacional
- **Uvicorn** — servidor ASGI
- **uuid** — geração de identificadores únicos
- **json / sqlite3** — manipulação e persistência de dados
- **ABC** — classes abstratas para interfaces e contratos

### Frontend

- **React.js**
- **React Router Dom** — roteamento de páginas
- **CSS Modules / Figma** — design modular e responsivo

### Ferramentas de Apoio

- **Git / GitHub** — controle de versão
- **LucidChart** — diagramas UML
- **Figma** — prototipagem de interface

---

## 🚀 Instalação e Execução

### 1️⃣ Clonar o repositório

```bash
git clone https://github.com/fabiogiugni/projeto1.git
cd projeto1
```

### 2️⃣ Criar ambiente virtual e instalar dependências do backend

```bash
source ativa_venv.sh  # Linux/macOS
.\ativa_venv.ps1     # Windows
```

### 3️⃣ Executar o servidor

```bash
python3 backend/main.py # Linux
python backend\main.py # Windows
```

O backend será iniciado em:
👉 [http://localhost:8000](http://localhost:8000)

### 4️ Executar o frontend

Para rodar o frontend, é necessário instalar o Node.js de acordo com o guia a seguir: 👉 [https://nodejs.org/pt0](https://nodejs.org/pt)

```bash
cd frontend
npm install
npm start
```

O frontend será iniciado em:
👉 [http://localhost:3000](http://localhost:3000)

---

## 🗂️ Estrutura de Pastas

```
.
├── backend/
│ ├── model/
│ │ ├── database/
│ │ │ └── database.py
│ │ └── entities/
│ │ ├── init.py
│ │ ├── actionInterface.py
│ │ ├── company.py
│ │ ├── data.py
│ │ ├── dataInterface.py
│ │ ├── department.py
│ │ ├── director.py
│ │ ├── entity.py
│ │ ├── group.py
│ │ ├── kpi.py
│ │ ├── kr.py
│ │ ├── manager.py
│ │ ├── objective.py
│ │ ├── person.py
│ │ ├── rpe.py
│ │ ├── team.py
│ │ └── userAuth.py
│ ├── services/
│ │ ├── BaseModels/
│ │ ├── init.py
│ │ └── api.py
│ └── main.py
├── frontend/
│ └── src/
│ ├── components/
│ ├── pages/
│ └── App.js
├── README.md
└── requirements.txt
```

---

## 🔄 Fluxo de Dados

1. O usuário realiza uma ação na interface React (ex.: criar um novo KPI).
2. O frontend envia uma requisição à API REST do backend.
3. A API interpreta os dados e os converte em objetos Python.
4. A classe `Database` executa comandos SQL (insert/update/select/delete).
5. O resultado é retornado em formato JSON para o frontend.

Esse ciclo assegura uma comunicação consistente entre as camadas, com base em princípios de modularização e encapsulamento.

---

## 🧩 Resultados Obtidos

- Integração completa entre frontend, backend e banco de dados.
- Aplicação prática dos conceitos de **POO** (herança, polimorfismo e encapsulamento).
- Sistema funcional com controle hierárquico e gestão de métricas empresariais.
- Base sólida para futuras expansões (gamificação, dashboards, SCRUM).

---

## 👨‍💻 Autores

| Nome                                | Matrícula  |
| ----------------------------------- | ---------- |
| **Fábio Braga Giugni**              | 2024022779 |
| **Samuel Felipe Verçosa Gonçalves** | 2022055475 |
| **Thales Eduardo Dias de Souza**    | 2024022647 |

---
