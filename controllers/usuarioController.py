from models.usuario import UsuarioModel
from models.motorista import MotoristaModel

class UsuarioController:
    @staticmethod
    def cadastrar_usuario_completo(dados):
        """
        Cadastra usuário e motorista se necessário
        """
        try:
            nome = dados.get('nome')
            email = dados.get('email')
            senha = dados.get('senha')
            tipo_perfil = dados.get('tipo_perfil')
            cnh = dados.get('cnh')  # Apenas para motoristas
            
            # Cadastrar motorista primeiro se for do tipo MOTORISTA
            u_motorista = None
            if tipo_perfil == 'MOTORISTA' and cnh:
                motorista_id, mensagem = MotoristaModel.cadastrar(cnh)
                if not motorista_id:
                    return False, f"Erro ao cadastrar motorista: {mensagem}"
                u_motorista = motorista_id
            
            # Cadastrar usuário
            usuario_id, mensagem = UsuarioModel.cadastrar(
                nome, email, senha, tipo_perfil, u_motorista
            )
            
            if usuario_id:
                return True, "Usuário cadastrado com sucesso"
            else:
                # Se falhar, remover motorista cadastrado (rollback)
                if u_motorista:
                    MotoristaModel.excluir(u_motorista)
                return False, mensagem
                
        except Exception as e:
            return False, f"Erro no cadastro: {str(e)}"

    @staticmethod
    def login(email, senha):
        """Realiza login do usuário"""
        usuario = UsuarioModel.verificar_senha(email, senha)
        if usuario:
            return True, {
                'id': usuario['u_usuario'],
                'nome': usuario['nome'],
                'email': usuario['email'],
                'tipo_perfil': usuario['tipo_perfil']
            }
        else:
            return False, "Credenciais inválidas"

    @staticmethod
    def listar_usuarios():
        """Lista todos os usuários"""
        return UsuarioModel.listar_usuarios()