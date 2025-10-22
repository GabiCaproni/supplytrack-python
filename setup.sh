#!/bin/bash

# ===============================================
# SCRIPT DE SETUP AUTOMÁTICO DO SUPPLYTRACK
# ===============================================

echo "🚚 Iniciando a configuração automática do SupplyTrack..."
echo ""

# --- 1. CONFIGURAÇÃO DE CREDENCIAIS ---

# Pede a senha do usuário root do MySQL (necessária para criar o banco de dados)
read -sp "Digite a senha do usuário 'root' do MySQL: " MYSQL_ROOT_PASSWORD
echo ""

# Parâmetros do banco de dados (extraídos dos arquivos de configuração)
DB_HOST="localhost"
DB_USER="root"
DB_NAME="supplytrack"
DB_PORT="3306"
DB_PASSWORD="1234" # Senha padrão configurada no connection.py

# --- 2. CONFIGURAÇÃO DO AMBIENTE PYTHON ---

echo "🛠️ Criando e ativando o ambiente virtual Python..."

# Cria o ambiente virtual se não existir
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# Ativa o ambiente virtual (adaptado para sistemas operacionais comuns)
if [ -f "venv/Scripts/activate" ]; then
    source venv/Scripts/activate
elif [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
else
    echo "❌ Erro ao ativar o ambiente virtual. Por favor, ative manualmente."
    exit 1
fi

echo "✅ Ambiente virtual ativado."
echo "📦 Instalando dependências (Flask, PyMySQL, etc.) conforme requirements.txt..."
pip install -r requirements.txt

# --- 3. CONFIGURAÇÃO DO BANCO DE DADOS (MySQL) ---

echo "---"
echo "🌐 Configurando o banco de dados MySQL: ${DB_NAME}"

# Comando MySQL para criar o banco e carregar o schema
SQL_COMMAND="
CREATE SCHEMA IF NOT EXISTS ${DB_NAME} DEFAULT CHARACTER SET utf8;
USE ${DB_NAME};
SOURCE database/schema.sql;
"

# Executa os comandos no MySQL usando a senha do root fornecida
# ESTE É O COMANDO QUE ESTÁ CAUSANDO O ERRO 'mysql' NÃO É RECONHECIDO NO SEU PC
mysql -h ${DB_HOST} -u ${DB_USER} -P ${DB_PORT} -p"${MYSQL_ROOT_PASSWORD}" -e "${SQL_COMMAND}"

# Verifica o código de saída do MySQL
if [ $? -eq 0 ]; then
    echo "✅ Banco de dados e tabelas configurados com sucesso."
else
    # Se falhar, avisa sobre a falha e sugere a execução manual
    echo "❌ ERRO: Falha ao configurar o banco de dados. O comando 'mysql' não funcionou."
    echo "👉 Por favor, execute as seguintes etapas manualmente:"
    echo "   1. Abra o MySQL Workbench ou o cliente de linha de comando."
    echo "   2. Conecte-se como 'root' com sua senha."
    echo "   3. Execute o script 'database/schema.sql' no seu servidor."
    # O script DEVE continuar para configurar o .env e rodar o app
fi

# --- 4. CRIAÇÃO DO ARQUIVO .ENV (CONFIGURAÇÃO DA APLICAÇÃO) ---

echo "---"
echo "⚙️ Criando o arquivo de configuração .env..."

# Cria o arquivo .env com as credenciais padrão usadas pelo connection.py
cat > .env << EOL
# Configurações do Banco de Dados MySQL (Usando credenciais do arquivo connection.py)
DB_HOST=${DB_HOST}
DB_USER=${DB_USER}
DB_PASSWORD=${DB_PASSWORD}
DB_NAME=${DB_NAME}
DB_PORT=${DB_PORT}

# Configurações da Aplicação
DEBUG=True
SECRET_KEY=supplytrack-super-secret-key-2024
EOL

echo "✅ Arquivo .env criado (DB_PASSWORD=1234)."
echo ""

# --- 5. EXECUÇÃO DO PROJETO ---

echo "---"
echo "🚀 Configuração concluída!"
echo "Para iniciar a aplicação Flask, execute o comando:"
echo "python app.py"

read -p "Deseja iniciar a aplicação agora? (s/N): " RUN_APP

if [[ "$RUN_APP" == "s" || "$RUN_APP" == "S" ]]; then
    echo ""
    python app.py
fi