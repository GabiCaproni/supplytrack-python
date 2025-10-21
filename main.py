import os
from models.usuario import UsuarioModel
from models.veiculo import VeiculoModel
from models.carga import CargaModel
from models.rota import RotaModel
from models.alerta import AlertaModel
from models.motorista import MotoristaModel
from views.dashboard import Dashboard

class SupplyTrackSystem:
    def __init__(self):
        self.usuario_logado = None
    
    def limpar_tela(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def mostrar_menu_principal(self):
        while True:
            self.limpar_tela()
            print("🚚 SUPPLYTRACK - SISTEMA DE LOGÍSTICA")
            print("=" * 40)
            
            if self.usuario_logado:
                print(f"👤 Usuário: {self.usuario_logado['nome']} ({self.usuario_logado['tipo_perfil']})")
                print("=" * 40)
            
            print("1. 📋 Dashboard")
            print("2. 👥 Cadastro de Usuário")
            print("3. 🚛 Cadastro de Veículo")
            print("4. 📦 Cadastro de Carga")
            print("5. 🗺️ Roteirização")
            print("6. 📊 Listar Dados")
            print("7. ⚠️ Gerenciar Alertas")
            
            if self.usuario_logado and self.usuario_logado['tipo_perfil'] == 'MOTORISTA':
                print("8. 🚗 Área do Motorista")
            
            # CORREÇÃO: Opção única para Sair/Login
            if self.usuario_logado:
                print("0. 🚪 Sair do programa")
            else:
                print("0. 🔐 Login")
            
            opcao = input("\nEscolha uma opção: ")
            
            if opcao == '1':
                self.mostrar_dashboard()
            elif opcao == '2':
                self.cadastrar_usuario()
            elif opcao == '3':
                self.cadastrar_veiculo()
            elif opcao == '4':
                self.cadastrar_carga()
            elif opcao == '5':
                self.criar_rota()
            elif opcao == '6':
                self.listar_dados()
            elif opcao == '7':
                self.gerenciar_alertas()
            elif opcao == '8' and self.usuario_logado and self.usuario_logado['tipo_perfil'] == 'MOTORISTA':
                self.area_motorista()
            elif opcao == '0':
                if self.usuario_logado:
                    print("👋 Até logo!")
                    break
                else:
                    self.fazer_login()
            else:
                input("❌ Opção inválida! Pressione Enter para continuar...")
    
    def fazer_login(self):
        self.limpar_tela()
        print("🔐 LOGIN")
        print("=" * 20)
        email = input("Email: ").strip()
        senha = input("Senha: ").strip()
        
        # Validação básica
        if not email or not senha:
            input("❌ Email e senha são obrigatórios! Pressione Enter para continuar...")
            return
        
        usuario = UsuarioModel.verificar_login(email, senha)
        if usuario:
            self.usuario_logado = usuario
            input(f"✅ Login realizado com sucesso! Bem-vindo(a), {usuario['nome']}! Pressione Enter para continuar...")
        else:
            input("❌ Email ou senha incorretos! Pressione Enter para continuar...")
    
    def mostrar_dashboard(self):
        self.limpar_tela()
        print("📊 DASHBOARD")
        print("=" * 30)
        
        # Verifica se usuário está logado
        if not self.usuario_logado:
            input("❌ Você precisa estar logado para acessar o dashboard. Pressione Enter para continuar...")
            return
        
        stats = Dashboard.obter_estatisticas()
        
        print(f"👥 Total de Usuários: {stats['total_usuarios']}")
        print(f"🚛 Veículos Disponíveis: {stats['veiculos_disponiveis']}")
        print(f"📦 Cargas Pendentes: {stats['cargas_pendentes']}")
        print(f"🛣️ Rotas em Andamento: {stats['rotas_andamento']}")
        print(f"⚠️ Alertas Abertos: {stats['alertas_abertos']}")
        
        print("\n📋 ENTREGAS RECENTES:")
        print("-" * 40)
        entregas = Dashboard.obter_entregas_recentes()
        for entrega in entregas:
            status_emoji = {
                'PENDENTE': '⏳',
                'SAIU_PARA_ENTREGA': '🚚',
                'ENTREGUE': '✅',
                'NAO_ENTREGUE': '❌'
            }
            print(f"{status_emoji.get(entrega['status'], '📦')} Rota {entrega['idRota']} - {entrega['status']} - Motorista: {entrega.get('motorista_nome', 'N/A')}")
        
        input("\nPressione Enter para voltar...")
    
    def cadastrar_usuario(self):
        self.limpar_tela()
        print("👥 CADASTRO DE USUÁRIO")
        print("=" * 30)
        
        nome = input("Nome: ").strip()
        email = input("Email: ").strip()
        senha = input("Senha: ").strip()
        
        # Validação básica
        if not nome or not email or not senha:
            input("❌ Todos os campos são obrigatórios! Pressione Enter para continuar...")
            return
        
        print("Tipo de Perfil (ADMIN, MOTORISTA, OPERADOR): ")
        tipo_perfil = input().upper()
        
        if tipo_perfil not in ['ADMIN', 'MOTORISTA', 'OPERADOR']:
            input("❌ Tipo de perfil inválido! Pressione Enter para continuar...")
            return
        
        usuario_id, mensagem = UsuarioModel.cadastrar(nome, email, senha, tipo_perfil)
        input(f"{mensagem} Pressione Enter para continuar...")
    
    def cadastrar_veiculo(self):
        self.limpar_tela()
        print("🚛 CADASTRO DE VEÍCULO")
        print("=" * 30)
        
        placa = input("Placa: ").strip()
        capacidade = input("Capacidade (ex: 2000 kg): ").strip()
        
        if not placa or not capacidade:
            input("❌ Placa e capacidade são obrigatórios! Pressione Enter para continuar...")
            return
        
        print("Deseja vincular a um motorista? (s/n): ")
        opcao_motorista = input().lower()
        
        id_motorista = None
        if opcao_motorista == 's':
            motoristas = MotoristaModel.listar_motoristas()
            if motoristas:
                print("\nMotoristas disponíveis:")
                for motorista in motoristas:
                    print(f"{motorista['id_motorista']}. {motorista['nome']} - {motorista['cnh']}")
                
                try:
                    id_motorista = int(input("\nID do motorista: "))
                except ValueError:
                    input("❌ ID inválido! Pressione Enter para continuar...")
                    return
            else:
                input("❌ Nenhum motorista disponível. Pressione Enter para continuar...")
                return
        
        veiculo_id, mensagem = VeiculoModel.cadastrar(placa, capacidade, id_motorista)
        input(f"{mensagem} Pressione Enter para continuar...")
    
    def cadastrar_carga(self):
        self.limpar_tela()
        print("📦 CADASTRO DE CARGA")
        print("=" * 30)
        
        volume = input("Volume (ex: 15 m³): ").strip()
        peso = input("Peso (ex: 800 kg): ").strip()
        
        if not volume or not peso:
            input("❌ Volume e peso são obrigatórios! Pressione Enter para continuar...")
            return
        
        print("\nArmazéns disponíveis:")
        print("1. Armazém Centro")
        print("2. Armazém Zona Norte")
        print("3. Armazém Zona Sul")
        
        try:
            id_armazem = int(input("\nID do armazém (1-3): "))
            if id_armazem not in [1, 2, 3]:
                input("❌ ID do armazém inválido! Pressione Enter para continuar...")
                return
        except ValueError:
            input("❌ ID inválido! Pressione Enter para continuar...")
            return
        
        carga_id, mensagem = CargaModel.cadastrar(volume, peso, id_armazem)
        input(f"{mensagem} Pressione Enter para continuar...")
    
    def criar_rota(self):
        self.limpar_tela()
        print("🗺️ CRIAR ROTA")
        print("=" * 30)
        
        data_saida = input("Data de saída (YYYY-MM-DD): ").strip()
        distancia = input("Distância (ex: 350 km): ").strip()
        
        if not data_saida or not distancia:
            input("❌ Data e distância são obrigatórios! Pressione Enter para continuar...")
            return
        
        # Listar veículos disponíveis
        veiculos = VeiculoModel.listar_veiculos()
        veiculos_disponiveis = [v for v in veiculos if v['status'] == 'DISPONIVEL']
        
        if not veiculos_disponiveis:
            input("❌ Nenhum veículo disponível! Pressione Enter para continuar...")
            return
        
        print("\nVeículos disponíveis:")
        for veiculo in veiculos_disponiveis:
            print(f"{veiculo['id_veiculo']}. {veiculo['placa']} - {veiculo['capacidade']}")
        
        try:
            id_veiculo = int(input("\nID do veículo: "))
        except ValueError:
            input("❌ ID inválido! Pressione Enter para continuar...")
            return
        
        # Listar motoristas disponíveis
        motoristas = MotoristaModel.listar_motoristas()
        motoristas_disponiveis = [m for m in motoristas if m['status'] == 'LIVRE']
        
        if not motoristas_disponiveis:
            input("❌ Nenhum motorista disponível! Pressione Enter para continuar...")
            return
        
        print("\nMotoristas disponíveis:")
        for motorista in motoristas_disponiveis:
            print(f"{motorista['id_motorista']}. {motorista['nome']} - {motorista['cnh']}")
        
        try:
            id_motorista = int(input("\nID do motorista: "))
        except ValueError:
            input("❌ ID inválido! Pressione Enter para continuar...")
            return
        
        rota_id, mensagem = RotaModel.criar_rota(data_saida, distancia, id_veiculo, id_motorista)
        
        if rota_id:
            # Atualizar status do veículo e motorista
            VeiculoModel.atualizar_status(id_veiculo, 'EM_USO')
            MotoristaModel.atualizar_status(id_motorista, 'EM_VIAGEM')
            
            # Criar alerta de nova rota
            AlertaModel.criar_alerta('OUTRO', f'Nova rota criada: {distancia}', rota_id, id_veiculo, id_motorista)
        
        input(f"{mensagem} Pressione Enter para continuar...")
    
    def listar_dados(self):
        self.limpar_tela()
        print("📊 LISTAR DADOS")
        print("=" * 30)
        print("1. 👥 Usuários")
        print("2. 🚛 Veículos")
        print("3. 📦 Cargas")
        print("4. 🛣️ Rotas")
        print("5. ⚠️ Alertas")
        print("6. ↩️ Voltar")
        
        opcao = input("\nEscolha uma opção: ")
        
        if opcao == '1':
            dados = UsuarioModel.listar_usuarios()
            titulo = "USUÁRIOS"
        elif opcao == '2':
            dados = VeiculoModel.listar_veiculos()
            titulo = "VEÍCULOS"
        elif opcao == '3':
            dados = CargaModel.listar_cargas()
            titulo = "CARGAS"
        elif opcao == '4':
            dados = RotaModel.listar_rotas()
            titulo = "ROTAS"
        elif opcao == '5':
            dados = AlertaModel.listar_alertas()
            titulo = "ALERTAS"
        elif opcao == '6':
            return
        else:
            input("❌ Opção inválida! Pressione Enter para continuar...")
            return
        
        self.limpar_tela()
        print(f"📋 {titulo}")
        print("=" * 50)
        
        if not dados:
            print("Nenhum dado encontrado.")
        else:
            for item in dados:
                print(item)
        
        input("\nPressione Enter para voltar...")
    
    def gerenciar_alertas(self):
        self.limpar_tela()
        print("⚠️ GERENCIAR ALERTAS")
        print("=" * 30)
        
        alertas = AlertaModel.listar_alertas()
        
        if not alertas:
            print("Nenhum alerta encontrado.")
        else:
            for alerta in alertas:
                status_emoji = '🔴' if alerta['status'] == 'ABERTO' else '🟢'
                print(f"{status_emoji} {alerta['tipo']} - {alerta['horario']} - {alerta['status']}")
        
        print("\n1. Criar novo alerta")
        print("2. Fechar alerta")
        print("3. Voltar")
        
        opcao = input("\nEscolha uma opção: ")
        
        if opcao == '1':
            self.criar_alerta()
        elif opcao == '2':
            self.fechar_alerta()
    
    def criar_alerta(self):
        self.limpar_tela()
        print("⚠️ CRIAR ALERTA")
        print("=" * 20)
        
        print("Tipos: ATRASO, PERIGO, ROTA_INVALIDA, OUTRO")
        tipo = input("Tipo do alerta: ").upper()
        
        if tipo not in ['ATRASO', 'PERIGO', 'ROTA_INVALIDA', 'OUTRO']:
            input("❌ Tipo de alerta inválido! Pressione Enter para continuar...")
            return
        
        descricao = input("Descrição do alerta: ").strip()
        if not descricao:
            descricao = "Alerta criado manualmente"
        
        alerta_id, mensagem = AlertaModel.criar_alerta(tipo, descricao)
        input(f"{mensagem} Pressione Enter para continuar...")
    
    def fechar_alerta(self):
        self.limpar_tela()
        print("✅ FECHAR ALERTA")
        print("=" * 20)
        
        alertas = AlertaModel.listar_alertas_abertos()
        if not alertas:
            input("❌ Nenhum alerta aberto encontrado! Pressione Enter para continuar...")
            return
        
        print("Alertas abertos:")
        for alerta in alertas:
            print(f"{alerta['id_alerta']}. {alerta['tipo']} - {alerta['descricao']}")
        
        try:
            id_alerta = int(input("\nID do alerta a fechar: "))
            sucesso, mensagem = AlertaModel.fechar_alerta(id_alerta)
            input(f"{mensagem} Pressione Enter para continuar...")
        except ValueError:
            input("❌ ID inválido! Pressione Enter para continuar...")
    
    def area_motorista(self):
        self.limpar_tela()
        print("🚗 ÁREA DO MOTORISTA")
        print("=" * 30)
        print(f"Bem-vindo, {self.usuario_logado['nome']}!")
        
        # Buscar rotas do motorista atual
        motorista = MotoristaModel.buscar_por_usuario_id(self.usuario_logado['id_usuario'])
        if not motorista:
            input("❌ Perfil de motorista não encontrado! Pressione Enter para continuar...")
            return
        
        rotas = RotaModel.listar_rotas_por_motorista(motorista['id_motorista'])
        
        print("\n1. 📋 Minhas rotas")
        print("2. ✅ Atualizar status de entrega")
        print("3. ↩️ Voltar")
        
        opcao = input("\nEscolha uma opção: ")
        
        if opcao == '1':
            self.minhas_rotas(motorista['id_motorista'])
        elif opcao == '2':
            self.atualizar_status_entrega(motorista['id_motorista'])
    
    def minhas_rotas(self, id_motorista):
        self.limpar_tela()
        print("📋 MINHAS ROTAS")
        print("=" * 25)
        
        rotas = RotaModel.listar_rotas_por_motorista(id_motorista)
        
        if not rotas:
            print("Nenhuma rota atribuída.")
        else:
            for rota in rotas:
                status_emoji = {
                    'PLANEJADA': '📅',
                    'EM_ANDAMENTO': '🚚',
                    'CONCLUIDA': '✅',
                    'CANCELADA': '❌'
                }
                print(f"{status_emoji.get(rota['status'], '📦')} Rota {rota['id_rota']} - {rota['distancia']} - Status: {rota['status']}")
        
        input("\nPressione Enter para voltar...")
    
    def atualizar_status_entrega(self, id_motorista):
        self.limpar_tela()
        print("✅ ATUALIZAR STATUS DE ENTREGA")
        print("=" * 35)
        
        rotas = RotaModel.listar_rotas_por_motorista(id_motorista)
        rotas_ativas = [r for r in rotas if r['status'] in ['PLANEJADA', 'EM_ANDAMENTO']]
        
        if not rotas_ativas:
            input("❌ Nenhuma rota ativa para atualizar! Pressione Enter para continuar...")
            return
        
        print("Rotas ativas:")
        for rota in rotas_ativas:
            print(f"{rota['id_rota']}. {rota['distancia']} - Status atual: {rota['status']}")
        
        try:
            id_rota = int(input("\nID da rota: "))
            print("\nNovo status:")
            print("1. 🚚 EM_ANDAMENTO")
            print("2. ✅ CONCLUIDA")
            print("3. ❌ CANCELADA")
            
            opcao_status = input("\nEscolha o novo status: ")
            
            status_map = {
                '1': 'EM_ANDAMENTO',
                '2': 'CONCLUIDA',
                '3': 'CANCELADA'
            }
            
            novo_status = status_map.get(opcao_status)
            if novo_status:
                sucesso, mensagem = RotaModel.atualizar_status(id_rota, novo_status)
                input(f"{mensagem} Pressione Enter para continuar...")
            else:
                input("❌ Opção inválida! Pressione Enter para continuar...")
                
        except ValueError:
            input("❌ ID inválido! Pressione Enter para continuar...")

if __name__ == "__main__":
    system = SupplyTrackSystem()
    system.mostrar_menu_principal()