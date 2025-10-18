# 🚚 SupplyTrack - Sistema de Gestão Logística

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)
![MySQL](https://img.shields.io/badge/MySQL-8.0-orange.svg)
![Status](https://img.shields.io/badge/Status-✅%20Concluído-brightgreen.svg)

Sistema completo para gestão de frota, rastreamento de entregas e controle logístico em tempo real. Desenvolvido como projeto acadêmico para a disciplina de Desenvolvimento de Software.

## 📋 Índice

- [Funcionalidades](#-funcionalidades)
- [Tecnologias](#-tecnologias)
- [Instalação](#-instalação)
- [Configuração](#-configuração)
- [Como Usar](#-como-usar)
- [API Endpoints](#-api-endpoints)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Desenvolvimento](#-desenvolvimento)
- [Funcionalidades Implementadas](#-funcionalidades-implementadas)

## 🚀 Funcionalidades

### ✅ Implementadas
- **👥 Gestão de Usuários** - Cadastro e autenticação de usuários com diferentes perfis
- **🚗 Gestão de Veículos** - Controle completo da frota com status em tempo real
- **👨‍💼 Gestão de Motoristas** - Cadastro e acompanhamento de motoristas
- **📦 Registro de Cargas** - Controle de mercadorias e inventário
- **🗺️ Roteirização** - Planejamento e otimização de rotas de entrega
- **📮 Controle de Entregas** - Acompanhamento completo do ciclo de entregas
- **🚨 Sistema de Alertas** - Notificações automáticas para eventos importantes
- **📊 Dashboard Interativo** - Visualização de métricas e KPIs em tempo real
- **🔌 API REST Completa** - Interface para integração com outros sistemas

## 🛠 Tecnologias

### **Backend:**
- **Python 3.8+** - Linguagem principal
- **Flask 2.3.3** - Framework web
- **PyMySQL 1.1.0** - Conexão com MySQL
- **bcrypt 4.0.1** - Criptografia de senhas
- **python-dotenv 1.0.0** - Gerenciamento de variáveis de ambiente

### **Banco de Dados:**
- **MySQL 8.0+** - Banco de dados relacional

### **Frontend:**
- **HTML5** - Estrutura web
- **CSS3** - Estilização
- **JavaScript** - Interatividade
- **Chart.js** - Gráficos e visualizações

### **Ferramentas:**
- **Git + GitHub** - Controle de versão
- **VSCode** - Ambiente de desenvolvimento
- **Postman** - Testes de API

## 📦 Instalação

### Pré-requisitos
- Python 3.8 ou superior
- MySQL 8.0 ou superior
- Git

### Passo a Passo de Instalação

1. **Clone o repositório:**
```bash
git clone https://github.com/GabiCaproni/supplytrack-python.git
cd supplytrack-python
```

2. **Crie um ambiente virtual (recomendado):**
```bash
python -m venv venv

# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate
```

3. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

4. **Configure o banco de dados MySQL:**
```sql
CREATE DATABASE supplytrack;
-- Execute o script database/schema.sql para criar as tabelas
```

5. **Configure as variáveis de ambiente:**
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

6. **Execute a aplicação:**
```bash
python app.py
```

7. **Acesse o sistema:**
- 🌐 **API:** http://localhost:5000
- 📊 **Dashboard:** http://localhost:5000/dashboard
- 🧪 **API Tester:** http://localhost:5000/api-tester

## ⚙ Configuração

### Variáveis de Ambiente (.env)
```env
# Configurações do Banco de Dados MySQL
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=sua_senha_mysql
DB_NAME=supplytrack
DB_PORT=3306

# Configurações da Aplicação
DEBUG=True
SECRET_KEY=chave-secreta-para-producao
```

### Estrutura do Banco de Dados
O sistema utiliza as seguintes tabelas principais:
- `usuario` - Gestão de usuários e autenticação
- `motorista` - Cadastro de motoristas
- `veiculo` - Controle da frota veicular
- `carga` - Registro de cargas e mercadorias
- `rota` - Planejamento de rotas
- `entrega` - Controle do ciclo de entregas
- `alerta` - Sistema de notificações

## 🎮 Como Usar

### Primeiro Acesso
1. Acesse http://localhost:5000/api-tester
2. Use o API Tester para criar usuários, veículos e motoristas
3. Acesse o Dashboard para visualizar as métricas

### Fluxo de Trabalho Típico
1. **Cadastrar Recursos:** Usuários → Motoristas → Veículos
2. **Registrar Carga:** Criar carga e planejar rota
3. **Atribuir Entrega:** Associar carga a motorista e veículo
4. **Acompanhar:** Monitorar status em tempo real pelo Dashboard
5. **Finalizar:** Marcar entrega como concluída

### Perfis de Usuário
- **ADMIN:** Acesso completo ao sistema
- **MOTORISTA:** Visualiza e atualiza apenas suas entregas
- **OPERADOR:** Gestão de estoque e cargas

## 🔌 API Endpoints

### 👥 Usuários
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/api/usuarios` | Listar todos os usuários |
| `POST` | `/api/usuarios` | Criar novo usuário |
| `POST` | `/api/auth/login` | Autenticar usuário |

### 🚗 Veículos
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/api/veiculos` | Listar todos os veículos |
| `POST` | `/api/veiculos` | Cadastrar novo veículo |
| `GET` | `/api/veiculos/disponiveis` | Listar veículos disponíveis |
| `PUT` | `/api/veiculos/{id}/status` | Atualizar status do veículo |

### 👨‍💼 Motoristas
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/api/motoristas` | Listar todos os motoristas |
| `POST` | `/api/motoristas` | Cadastrar novo motorista |
| `GET` | `/api/motoristas/{id}/entregas` | Listar entregas do motorista |
| `PUT` | `/api/motoristas/{id}/status` | Atualizar status do motorista |

### 📦 Cargas e Logística
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/api/cargas` | Listar todas as cargas |
| `POST` | `/api/cargas` | Registrar nova carga |
| `POST` | `/api/logistica/registrar-carga` | Processo completo (carga + rota) |
| `PUT` | `/api/cargas/{id}/status` | Atualizar status da carga |

### 🛣️ Rotas
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/api/rotas` | Listar todas as rotas |
| `POST` | `/api/rotas` | Criar nova rota |
| `PUT` | `/api/rotas/{id}/status` | Atualizar status da rota |

### 📮 Entregas
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/api/entregas` | Listar todas as entregas |
| `POST` | `/api/entregas` | Criar nova entrega |
| `PUT` | `/api/entregas/{id}/status` | Atualizar status da entrega |
| `PUT` | `/api/motorista/{id}/entregas/{id}/status` | Motorista atualiza status |

### 📊 Dashboard
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/api/dashboard` | Dados completos do dashboard |
| `GET` | `/api/dashboard/alertas` | Alertas ativos |
| `GET` | `/api/dashboard/entregas` | Estatísticas de entregas |
| `GET` | `/api/dashboard/metricas-rapidas` | Métricas rápidas |

### Exemplos de Uso da API

**Listar usuários:**
```bash
curl -X GET http://localhost:5000/api/usuarios
```

**Criar veículo:**
```bash
curl -X POST http://localhost:5000/api/veiculos \
  -H "Content-Type: application/json" \
  -d '{
    "placa": "ABC1234",
    "capacidade": "2000kg",
    "status": "DISPONIVEL"
  }'
```

**Registrar carga completa:**
```bash
curl -X POST http://localhost:5000/api/logistica/registrar-carga \
  -H "Content-Type: application/json" \
  -d '{
    "volume": "2m³",
    "peso": "500kg",
    "dataprevista": "2024-12-20",
    "origem": "Armazém Centro",
    "destino": "Cliente ABC",
    "u_veiculo": 1,
    "u_motorista": 1
  }'
```

## 🏗️ Estrutura do Projeto

```
supplytrack-python/
├── 📄 app.py                 # Aplicação principal Flask
├── 📄 config.py             # Configurações da aplicação
├── 📄 requirements.txt      # Dependências do Python
├── 📄 README.md            # Este arquivo de documentação
├── 📄 .env.example         # Modelo de variáveis de ambiente
├── 📁 database/
│   ├── __init__.py
│   ├── connection.py       # Conexão com MySQL
│   └── schema.sql          # Script de criação do banco
├── 📁 models/              # Modelos de dados (MVC)
│   ├── __init__.py
│   ├── usuario_model.py
│   ├── veiculo_model.py
│   ├── motorista_model.py
│   ├── carga_model.py
│   ├── rota_model.py
│   ├── entrega_model.py
│   ├── alerta_model.py
│   └── dashboard_model.py
├── 📁 controllers/         # Lógica de negócio (MVC)
│   ├── __init__.py
│   ├── usuario_controller.py
│   ├── veiculo_controller.py
│   ├── motorista_controller.py
│   ├── logistica_controller.py
│   └── dashboard_controller.py
├── 📁 routes/             # Rotas da API (MVC)
│   ├── __init__.py
│   ├── usuario.py
│   ├── veiculo.py
│   ├── motorista.py
│   ├── carga.py
│   ├── rota.py
│   ├── entrega.py
│   ├── logistica.py
│   └── dashboard.py
└── 📁 frontend/           # Interface web
    ├── dashboard.html     # Dashboard principal
    └── api-tester.html   # Interface de teste de APIs
```

## 💻 Desenvolvimento

### Padrão Arquitetural
O projeto segue o padrão **MVC (Model-View-Controller)**:
- **Models:** Lógica de dados e acesso ao banco
- **Views:** Interface web (HTML/JavaScript)
- **Controllers:** Lógica de negócio e orquestração

### Convenção de Commits
- `feat:` Nova funcionalidade
- `fix:` Correção de bug
- `docs:` Documentação
- `style:` Formatação de código
- `refactor:` Refatoração de código
- `test:` Adição de testes

### Execução em Desenvolvimento
```bash
# Modo desenvolvimento com auto-reload
python app.py

# Ou usando Flask CLI
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

## ✅ Funcionalidades Implementadas

### Módulo de Gestão de Usuários
- [x] Cadastro de usuários com diferentes perfis
- [x] Autenticação e controle de acesso
- [x] Validação de dados de entrada
- [x] Criptografia de senhas

### Módulo de Frota e Veículos
- [x] Cadastro completo de veículos
- [x] Controle de status (Disponível, Em uso, Manutenção)
- [x] Gestão de capacidade e características
- [x] Associação com motoristas

### Módulo de Motoristas
- [x] Cadastro com dados da CNH
- [x] Controle de status (Ativo, Férias, Licença)
- [x] Histórico de entregas
- [x] Interface específica para motoristas

### Módulo de Cargas e Estoque
- [x] Registro de cargas com volume e peso
- [x] Controle de status (No armazém, Em trânsito, Entregue)
- [x] Rastreamento de localização
- [x] Gestão de múltiplos armazéns

### Módulo de Rotas e Entregas
- [x] Planejamento de rotas com origem e destino
- [x] Cálculo de distância e tempo estimado
- [x] Associação de cargas a rotas
- [x] Controle completo do ciclo de entrega

### Módulo de Dashboard e Analytics
- [x] Métricas em tempo real
- [x] Gráficos de status de entregas
- [x] Alertas e notificações
- [x] KPIs operacionais

### Sistema de Alertas
- [x] Alertas automáticos por atrasos
- [x] Notificações de problemas em rotas
- [x] Alertas de status de veículos
- [x] Sistema de prioridades

### API REST
- [x] Endpoints completos para todas as entidades
- [x] Documentação interativa via API Tester
- [x] Tratamento de erros e validações
- [x] Respostas padronizadas em JSON

## 👥 Desenvolvido por
  
📧 [GitHub](https://github.com/GabiCaproni)  
🎓 Projeto acadêmico - Disciplina de Desenvolvimento de Software

