from models.motorista import MotoristaModel
from models.usuario import UsuarioModel

class MotoristaController:
    @staticmethod
    def criar_motorista(id_usuario, cnh, status='LIVRE'):
        """Cria um novo motorista a partir de usuário existente"""
        try:
            # Validações básicas
            if not id_usuario or not cnh:
                return False, "ID do usuário e CNH são obrigatórios"
            
            # Verificar se usuário existe
            usuario = UsuarioModel.buscar_por_id(id_usuario)
            if not usuario:
                return False, "Usuário não encontrado"
            
            # Verificar se o usuário tem perfil de motorista
            if usuario.get('tipo_perfil') != 'MOTORISTA':
                return False, "O usuário deve ter perfil de MOTORISTA"
            
            # Chamar o modelo para cadastrar
            motorista_id, mensagem = MotoristaModel.cadastrar(id_usuario, cnh, status)
            
            if motorista_id:
                return True, {
                    'id_motorista': motorista_id,
                    'message': mensagem
                }
            else:
                return False, mensagem
                
        except Exception as e:
            print(f"Erro no MotoristaController: {e}")
            return False, f"Erro interno: {str(e)}"

    @staticmethod
    def criar_motorista_completo(nome, email, senha, cnh, status='LIVRE'):
        """Cria um usuário e motorista em uma única operação"""
        try:
            # Primeiro criar o usuário com perfil MOTORISTA
            usuario_id, mensagem = UsuarioModel.cadastrar(nome, email, senha, 'MOTORISTA')
            
            if not usuario_id:
                return False, mensagem
            
            # Depois criar o motorista
            motorista_id, mensagem_motorista = MotoristaModel.cadastrar(usuario_id, cnh, status)
            
            if motorista_id:
                return True, {
                    'id_usuario': usuario_id,
                    'id_motorista': motorista_id,
                    'message': 'Motorista criado com sucesso'
                }
            else:
                # Se falhar ao criar motorista, deletar o usuário criado
                UsuarioModel.deletar(usuario_id)
                return False, mensagem_motorista
                
        except Exception as e:
            print(f"Erro ao criar motorista completo: {e}")
            return False, f"Erro ao criar motorista: {str(e)}"

    @staticmethod
    def listar_motoristas():
        """Lista todos os motoristas"""
        try:
            motoristas = MotoristaModel.listar_motoristas()
            return True, motoristas
        except Exception as e:
            print(f"Erro ao listar motoristas: {e}")
            return False, f"Erro ao listar motoristas: {str(e)}"